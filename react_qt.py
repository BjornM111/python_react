from PySide2.QtCore import SignalInstance
from PySide2.QtWidgets import QWidget, QLayout, QLineEdit, QTextEdit

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
        root_ = self.get_element(root)
        if root_.item:
            root_.item.show()

    def _create_instance(self, element):
        element.item = element.Class()

    def _move_instance(self, from_element, to_element):
        to_element.item = from_element and from_element.item

    def _pop(self, element, i):
        element.item.takeAt(i)

    def _insert(self, parent, i, element):
        if isinstance(element.item, QWidget):
            parent.item.insertWidget(i, element.item)
        elif isinstance(element.item, QLayout):
            parent.item.insertLayout(i, element.item)
        else:
            raise NotImplementedError(
                "type for {} is not supported yet".format(element.item)
            )

    def _clear(self, element):
        while element.item.takeAt(0):
            pass

    def _add(self, parent, element):
        if isinstance(element.item, QWidget):
            parent.item.addWidget(element.item)
        elif isinstance(element.item, QLayout):
            parent.item.addLayout(element.item)
        else:
            raise NotImplementedError(
                "type for {} is not supported yet".format(element.item)
            )

    def _setprops(self, element, props, old=None):
        meta = element.item.metaObject()
        element.item.blockSignals(True)
        for key, value in props.items():
            # we need to take care of text cursors as they are normally cleared
            # when the text us updated
            if  key == "text" and isinstance(element.item, QLineEdit):
                cursor = element.item.cursorPosition()
                element.item.setText(value)
                if cursor:
                    element.item.setCursorPosition(
                        min(cursor, len(value)),
                    )
                continue

            if  meta.indexOfProperty(key) != -1:
                element.item.setProperty(key, value)
                continue

            signal = getattr(element.item, key)
            if old and old.props.get(key):
                signal.disconnect(old.props[key])
            signal.connect(value)
        element.item.blockSignals(False)

    def _setlayout(self, element, layout):
        element.item.setLayout(layout.item)

    def _remove(self, element):
        element.item.deleteLater()


def style(**kwargs):
    return "".join(
        "{}: {};".format(key.replace("_", "-"), value)
        for key, value
        in kwargs.items()
        if value
    )
