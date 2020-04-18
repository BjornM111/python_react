from itertools import zip_longest
from functools import partial
import enum
from types import FunctionType
from inspect import signature


class Status(enum.Enum):
    REPLACED = 0
    UPDATED = 1
    NEW = 2
    REMOVED = 3
    NOTHING = 4
    SAME = 5


def split_props(props):
    props = props.copy()
    layout = props.pop('layout', None)
    widgets = props.pop('widgets', None)
    return props, layout, widgets


class Element(object):
    def __init__(self, Class, **props):
        self.Class = Class
        self.props = props or {}
        self.result = None
        self.state = []
        self.state_index = -1
        self.parent_layout = None
        self.parent_widget = None


class State(list):
    def __init__(self, renderer):
        self.element = None
        self.current_index = -1
        self.renderer = renderer

    def use_state(self, default):
        self.current_index += 1
        if self.current_index == len(self):
            self.append([
                default,
                partial(self.set_state, self.current_index),
            ])
        return self[self.current_index]

    def set_state(self, index, value):
        self[index][0] = value
        self.renderer.state_changed(self.element)



class Renderer(object):

    def __init__(self):
        self.root = None

    def render(self, root):
        raise NotImplementedError('this should be overridden')

    def _render(self, new, old):

        if not new:
            if not old:
                return Status.NOTHING
            self.remove(old)
            return Status.REMOVED

        if isinstance(new.Class, FunctionType):
            removed = False
            if old and old.Class != new.Class:
                self.remove(old)
                old = None
                removed = True
            status = self.render_component(new, old)
            return Status.REPLACED if status == Status.NEW else status

        if new is old:
            return Status.SAME

        if not old:
            self.add(new)
            return Status.NEW

        if new.Class != old.Class:
            self.remove(old)
            self.add(new)
            return Status.REPLACED

        self.update(new, old)
        return Status.UPDATED

    def state_changed(self, element):
        if element.parent_layout:
            raise NotImplementedError()
        if element.parent_widget:
            raise NotImplementedError()
        self.render(element)

    def render_component(self, element, old=None):

        element.state = old.state if old else State(self)
        element.state.element = element

        props = element.props.copy()
        sig = signature(element.Class)
        if 'use_state' in sig.parameters:
            props['use_state'] = element.state.use_state

        result = element.Class(**props)
        status = self._render(result, old and old.result)
        self._move_instance(result, element)
        element.result = result
        element.state.current_index = -1
        return status

    def add(self, element):

        props, layout, widgets = split_props(element.props)

        self._create_instance(element)
        if props:
            self._setprops(element, props)

        if layout:
            self.add(layout)
            layout.parent_widget = element
            self._setlayout(element, layout)

        if widgets:
            i = 0
            for widget in widgets:
                if not widget:
                    continue
                self.add(widget)
                element.parent_layout = widget
                self._insert(element, i, widget)
                i += 1

    def update(self, new, old):

        props = {}

        for key, value in new.props.items():
            if old.props.get(key) != value:
                props[key] = value

        for key in old.props:
            if key not in new.props:
                props[key] = None

        props, layout, widgets = split_props(props)

        self._move_instance(old, new)
        if props:
            self._setprops(new, props, old)

        if layout:
            self._render(layout, old.props.get('layout'))
            layout.parent_widget = new
            self._setlayout(new, layout)

        if widgets:
            self.update_widgets(new, widgets, old.props['widgets'])

    def update_widgets(self, element, new, old):
        i = 0
        for new_widget, old_widget in zip_longest(new, old):
            status = self._render(new_widget, old_widget)
            if status == Status.NOTHING:
                continue
            if status == Status.NEW:
                self._insert(element, i, new_widget)
                new_widget.parent_layout = element
                i += 1
                continue
            if status == Status.REPLACED:
                self._pop(new, i)
                self._insert(element, i, new_widget)
                new_widget.parent_layout = element
                i += 1
                continue
            if status == Status.REMOVED:
                self._pop(element, i)
                continue
            if status == Status.UPDATED:
                i += 1
                continue
            if status == Status.SAME:
                i += 1
                continue
            raise RuntimeError("shit should not happen")

    def remove(self, element):
        props, layout, widgets = split_props(element.props)

        self._remove(element)

        if layout:
            self.remove(layout)

        if widgets:
            for widget in widgets:
                if widget:
                    self.remove(widget)

