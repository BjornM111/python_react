"""
import sys

from PySide2 import QtWidgets


def main():
    app = QtWidgets.QApplication(sys.argv)
    label = QtWidgets.QLabel("Majs")
    label.show()
    app.exec_()

if __name__ == "__main__":
    main()

"""
import sys

from PySide2 import QtWidgets

from wrapper import wrap
from react import Element
from react_qt import QtRenderer, style

wrap('QtWidgets', QtWidgets, Element)
from wrapper.QtWidgets import (
    QApplication,
    QDialog,
    QVBoxLayout,
    QPushButton,
    QLabel,
)


def master(use_state):
    a, set_a = use_state(True)
    b, set_b = use_state(True)
    c, set_c = use_state(True)

    return QDialog(
        layout=QVBoxLayout(
            widgets=[
                QPushButton(
                    text=str(a),
                    styleSheet=style(color="green" if a else None),
                    pressed=lambda: set_a(not a),
                ) if c else None,
                QPushButton(
                    text="remove me",
                    pressed=lambda: set_b(not b),
                ) if b and c else None,
                QPushButton(
                    text="remove all",
                    pressed=lambda: set_c(not c),
                ) if c else None,
                QPushButton(
                    text="reset",
                    styleSheet=style(font_weight="bold"),
                    pressed=lambda: (set_a(True), set_b(True), set_c(True)),
                    visible=not a or not b or not c,
                ),
            ]
        )
    )


def main():
    app = QtWidgets.QApplication(sys.argv)
    renderer = QtRenderer()

    renderer.render(Element(master))
    app.exec_()

if __name__ == "__main__":
    main()