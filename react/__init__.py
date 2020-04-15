from typing import Optional
from itertools import zip_longest


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
    
    def _update(self, new, old):
        if not new:
            if old:
                self.remove(old)
            return

        if old and new.Class != old.Class:
            self.remove(old)
            old = None

        if not old:
            item = self.add(new)
            return

        props = {}

        for key, value in new.props.items():
            if old.props.get(key) != value:
                props[key] = value

        for key in old.props:
            if key not in new.props:
                props[key] = None

        self.update(props, new, old)
    
    def add(self, element):
        props, layout, widgets = split_props(element.props)

        item = element.Class()
        for key, value in props.items():
            setattr(item, key, value)

        self.steps.append(
            ("add", element.Class, props),
        )

        if layout:
            self.add(layout)
            item.layout = layout.item

        element.item = item

        if widgets:
            for i, widget in enumerate(widgets):
                self.add(widget)
                self._insert(element, i, widget)

    def update(self, props, new, old):
        props, layout, widgets = split_props(props)

        if props:
            for key, value in props.items():
                setattr(old.item, key, value)

            self.steps.append(
                ("update", props),
            )

        if layout:
            self._update(layout, old.props.get('layout'))
            old.item.layout = layout.item

        if widgets:
            i = 0
            for new_widget, old_widget in zip_longest(widgets, old.props.get('widgets')):
                if not old_widget and not new_widget:
                    continue
                self._update(new_widget, old_widget)
                if not old_widget:
                    self._pop(old, i)
                    self._insert(old, i, new_widget)
                    i += 1
                    continue
                if not new_widget:
                    self._pop(old, i)
                    continue
                if new_widget.item is old_widget.item:
                    i += 1
                    continue

        new.item = old.item

    def remove(self, element):
        props, layout, widgets = split_props(element.props)

        self.steps.append(
            ("remove", element.Class),
        )

        if layout:
            self.remove(layout)

        if widgets:
            for widget in widgets:
                if widget:
                    self.remove(widget)

