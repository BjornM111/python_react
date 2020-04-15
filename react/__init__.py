from typing import Optional


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
            self.remove(old)
            return

        if old and new.Class != old.Class:
            self.remove(item)
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
        return
    
    def add(self, element):
        raise NotImplementedError('this should be overridden')

    def update(self, props, new, old):
        raise NotImplementedError('this should be overridden')

    def remove(self, element):
        raise NotImplementedError('this should be overridden')
