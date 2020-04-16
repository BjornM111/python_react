from PySide2.QtCore import SignalInstance

from react import Renderer


class QtRenderer(Renderer):
    def __init__(self, *args, **kwargs):
        super(QtRenderer, self).__init__(*args, **kwargs)

    def render(self, root):
        self._render(
            root,
            self.root,
        )
        self.root = root
        if root.item:
            root.item.show()

    def _create_instance(self, element):
        element.item = element.Class()

    def _move_instance(self, from_element, to_element):
        to_element.item = from_element.item

    def _pop(self, element, i):
        element.item.takeAt(i)

    def _insert(self, parent, i, element):
        parent.item.insertWidget(i, element.item)

    def _setprops(self, element, props, old=None):
        for key, value in props.items():
            if  key != "visible" and isinstance(getattr(element.item, key), SignalInstance):
                signal = getattr(element.item, key)
                if old and key in old.props:
                    signal.disconnect(old.props[key])
                signal.connect(value)
                continue
            setter = getattr(element.item, 'set'+key.capitalize())
            setter(value)

    def _setlayout(self, element, layout):
        element.item.setLayout(layout.item)

    def _remove(self, element):
        element.item.deleteLater()
