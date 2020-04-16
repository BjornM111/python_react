from itertools import zip_longest
import enum
from types import FunctionType


class Status(enum.Enum):
    REPLACED = 0
    UPDATED = 1
    NEW = 2
    REMOVED = 3
    NOTHING = 4


def split_props(props):
    props = props.copy()
    layout = props.pop('layout', None)
    widgets = props.pop('widgets', None)
    return props, layout, widgets


class Element(object):
    def __init__(self, Class, **props):
        self.Class = Class
        self.props = props or {}


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

        if not old:
            self.add(new)
            return Status.NEW

        if new.Class != old.Class:
            self.remove(old)
            self.add(new)
            return Status.REPLACED

        self.update(new, old)
        return Status.UPDATED

    def add(self, element):
        props, layout, widgets = split_props(element.props)

        self._create_instance(element)
        self._setprops(element, props)

        if layout:
            self.add(layout)
            self._setlayout(element, layout)

        if widgets:
            for i, widget in enumerate(widgets):
                self.add(widget)
                self._insert(element, i, widget)

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
            self._setlayout(new, layout)

        if widgets:
            i = 0
            for new_widget, old_widget in zip_longest(widgets, old.props.get('widgets')):
                status = self._render(new_widget, old_widget)
                if status == Status.NOTHING:
                    continue
                if status == Status.NEW:
                    self._insert(new, i, new_widget)
                    self += 1
                    continue
                if status == Status.REPLACED:
                    self._pop(new, i)
                    self._insert(new, i, new_widget)
                    i += 1
                    continue
                if status == Status.REMOVED:
                    self._pop(new, i)
                    continue
                if status == Status.UPDATED:
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

