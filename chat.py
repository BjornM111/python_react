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
    QHBoxLayout,
    QPushButton,
    QLabel,
    QTextEdit,
    QLineEdit,
    QWidget,
)


def master(use_state):
    messages, set_messages = use_state([])
    message, set_message = use_state("")

    return QDialog(
        windowTitle=message,
        layout=QVBoxLayout(
            widgets=[
                QTextEdit(
                    plainText="\n".join(messages),
                ),
                QHBoxLayout(
                    widgets=[
                        QLineEdit(
                            text=message,
                            textEdited=lambda x: set_message(x),
                        ),
                        QPushButton(
                            text=">",
                            styleSheet=style(font_weight="bold"),
                            pressed=lambda: (
                                (
                                    set_messages([*messages, message]),
                                    set_message(""),
                                ) if message else None
                            ),
                        ),
                    ]
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
