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
    def __init__(self, Class, key=None, **props):
        self.Class = Class
        self.key = key
        self.props = props or {}
        self.result = None
        self.state = []
        self.state_index = -1
        self.parent_layout = None
        self.parent_widget = None
        self.dirty = False

    def __repr__(self):
        return "Element({}{}, {})".format(
            self.Class.__name__,
            ", key="+str(self.key) if self.key is not None else "",
            self.props,
        )


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
        self.element.dirty = True
        self.renderer.state_changed(self.element)


class Effects(list):
    def __init__(self):
        self.current_index = -1
        self.schedule = []

    def run_schedule(self):
        for index, func in self.schedule:
            self[index][0] = result = func()
            try:
                next(result)
            except (TypeError, StopIteration):
                pass
        self.schedule = []

    def use_effect(self, func, *args):
        self.current_index += 1
        if self.current_index == len(self):
            self.append([None])
        cleanup, *prev_args = self[self.current_index]
        if args != tuple(prev_args):
            if cleanup:
                try:
                    next(cleanup)
                except TypeError:
                    cleanup()
                except StopIteration:
                    pass

            self.schedule.append([
                self.current_index,
                partial(func, *args),
            ])
            self[self.current_index] = [None, *args]


class Renderer(object):

    def __init__(self):
        self.root = None

    def render(self, root):
        raise NotImplementedError('this should be overridden')

    def _create_instance(self, element):
        raise NotImplementedError('this should be overridden')

    def _move_instance(self, from_element, to_element):
        raise NotImplementedError('this should be overridden')

    def _pop(self, element, i):
        raise NotImplementedError('this should be overridden')

    def _insert(self, parent, i, element):
        raise NotImplementedError('this should be overridden')

    def _setprops(self, element, props, old=None):
        raise NotImplementedError('this should be overridden')

    def _setlayout(self, element, layout):
        raise NotImplementedError('this should be overridden')

    def _remove(self, element):
        raise NotImplementedError('this should be overridden')

    def _add_task(self, func):
        raise NotImplementedError('this should be overridden')

    def _render(self, new, old):

        if not new:
            if not old:
                return Status.NOTHING
            self.remove(old)
            return Status.REMOVED

        if not new.dirty and new is old:
            return Status.SAME

        if isinstance(new.Class, FunctionType):
            removed = False
            if old and old.Class != new.Class:
                self.remove(old)
                old = None
                removed = True
            status = self.render_component(new, old)
            return Status.REPLACED if removed and status == Status.NEW else status

        if not old:
            self.update(new)
            return Status.NEW

        if new.Class != old.Class:
            self.remove(old)
            self.update(new)
            return Status.REPLACED

        self.update(new, old)
        return Status.UPDATED

    def state_changed(self, element):
        if element.parent_layout:
            self.update_widgets(
                element.parent_layout,
                element.parent_layout.props['widgets'],
                element.parent_layout.props['widgets'],
            )
            return
        if element.parent_widget:
            raise NotImplementedError()
        self.render(element)

    def render_component(self, element, old=None):

        element.state = old.state if old else State(self)
        element.state.element = element
        element.dirty = False

        element.effects = old.effects if old else Effects()

        props = element.props.copy()
        sig = signature(element.Class)
        if 'use_state' in sig.parameters:
            props['use_state'] = element.state.use_state
        if 'use_effect' in sig.parameters:
            props['use_effect'] = element.effects.use_effect

        result = element.Class(**props)
        status = self._render(result, old and old.result)
        element.result = result
        element.state.current_index = -1
        element.effects.current_index = -1
        if element.effects.schedule:
            self._add_task(element.effects.run_schedule)

        return status

    def update(self, new, old=None):

        if old:
            props = {}

            for key, value in new.props.items():
                if old.props.get(key) != value:
                    props[key] = value

            for key in old.props:
                if key not in new.props:
                    props[key] = None

            self._move_instance(old, new)
        else:
            self._create_instance(new)
            props = new.props

        props, layout, widgets = split_props(props)

        if props:
            self._setprops(new, props, old)

        if layout:
            self._render(layout, old and old.props.get('layout'))
            layout.parent_widget = new
            self._setlayout(new, layout)

        if widgets:
            self.update_widgets(
                new,
                widgets,
                old.props['widgets'] if old else [],
            )

    def get_element(self, element):
        """
        Helper function for getting the actual element
        if element is a component-element the result is returned
        """
        if not element:
            return None
        if isinstance(element.Class, FunctionType):
            return element.result
        return element

    def update_widgets(self, element, new, old, skip_clear=None):
        if not skip_clear:
            self._clear(element)

        for new_widget, old_widget in zip_longest(new, old):

            if isinstance(new_widget, list):
                if isinstance(old_widget, list):
                    key_map = {widget.key: widget for widget in old_widget}
                    old_widget = [key_map.pop(widget.key, None) for widget in new_widget]
                    for widget in key_map.values():
                        self.remove(widget)
                else:
                    if old_widget:
                        self.remove(old_widget)
                    old_widget = []

                self.update_widgets(element, new_widget, old_widget, True)
                continue

            if isinstance(old_widget, list):
                for widget in old_widget:
                    self.remove(widget)

            self._render(new_widget, old_widget)

            if new_widget:
                new_widget.parent_layout = element

                new_widget_ = self.get_element(new_widget)
                if new_widget_:
                    self._add(element, new_widget_)

    def remove(self, element):
        _, layout, widgets = split_props(element.props)

        self._remove(element)

        if layout:
            self.remove(layout)

        if widgets:
            for widget in widgets:
                if widget:
                    self.remove(widget)

