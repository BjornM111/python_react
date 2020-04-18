from itertools import zip_longest
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


class Renderer(object):

    def __init__(self):
        self.root = None

    def render(self, root):
        raise NotImplementedError('this should be overridden')

    def _render(self, new, old):
        if new is old:
            return Status.SAME

        if not new:
            if not old:
                return Status.NOTHING
            self.remove(old)
            return Status.REMOVED

        if not old:
            self.add(new)
            return Status.NEW

        if new.Class != old.Class:
            self.remove(old)
            self.add(new)
            return Status.REPLACED

        self.update(new, old)
        return Status.UPDATED

    def render_component(self, element, props, old=None):
        if old:
            self._move_instance(old, element)

        if not props and old:
            return

        if old:
            element.state = old.state

        result = element.Class(**props)
        self._render(result, old and old.result)
        self._move_instance(result, element)
        element.result = result

    def add(self, element):

        if isinstance(element.Class, FunctionType):
            self.render_component(element, element.props)
            return

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

        if isinstance(new.Class, FunctionType):
            self.render_component(new, props, old)
            return

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

