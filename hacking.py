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

from wrapper import wrap
from PySide2 import QtWidgets

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


a = True
b = True
c = True


def main():
    app = QtWidgets.QApplication(sys.argv)
    renderer = QtRenderer()

    def a_pressed():
        global a
        a = not a
        render()

    def b_pressed():
        global b
        b = not b
        render()

    def c_pressed():
        global c
        c = not c
        render()

    def reset():
        global a
        global b
        global c
        a = True
        b = True
        c = True
        render()

    def render():
        print("rendering", a, b, c)
        renderer.render(
            QDialog(
                layout=QVBoxLayout(
                    widgets=[
                        QPushButton(
                            text=str(a),
                            styleSheet=style(color="green" if a else None),
                            pressed=a_pressed,
                        ) if c else None,
                        QPushButton(
                            text="remove me",
                            pressed=b_pressed,
                        ) if b and c else None,
                        QPushButton(
                            text="remove all",
                            pressed=c_pressed,
                        ) if c else None,
                        QPushButton(
                            text="reset",
                            styleSheet=style(font_weight="bold"),
                            pressed=reset,
                            visible=not a or not b or not c,
                        ),
                    ]
                )
            )
        )

    render()
    app.exec_()

if __name__ == "__main__":
    main()