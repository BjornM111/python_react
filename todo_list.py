import sys
from dataclasses import dataclass

from PySide2 import QtWidgets

from wrapper import wrap
from react import Element
from react_qt import QtRenderer, style

wrap('QtWidgets', QtWidgets, Element)
from wrapper.QtWidgets import (
    QCheckBox,
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QRadioButton,
    QSpacerItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


@dataclass
class Todo:
    description: str
    done: bool = False


def master(use_state):
    todos, set_todos = use_state([])
    description, set_description = use_state("")
    filter_, set_filter = use_state(0)

    return QDialog(
        windowTitle="Todos: {} / {}".format(
            sum(not todo.done for todo in todos),
            len(todos),
        ),
        layout=QVBoxLayout(
            widgets=[
                [
                    QHBoxLayout(key=i, widgets=[
                        QLabel(text=todo.description),
                        QCheckBox(
                            checked=todo.done,
                            stateChanged=lambda checked, i=i, todo=todo: set_todos([
                                *todos[:i],
                                Todo(todo.description, bool(checked)),
                                *todos[i+1:],
                            ]),
                        ),
                    ])
                    for i, todo in enumerate(todos)
                    if (filter_ == 0) or (filter_ == 1 and not todo.done) or (filter_ == 2 and todo.done)
                ],
                QHBoxLayout(
                    widgets=[
                        QLineEdit(
                            text=description,
                            textEdited=lambda x: set_description(x),
                        ),
                        QPushButton(
                            text="Add Todo",
                            enabled=bool(description),
                            styleSheet=style(font_weight="bold"),
                            pressed=lambda: (
                                set_todos([*todos, Todo(description)]),
                                set_description(""),
                            ),
                        ),
                    ]
                ),
                QHBoxLayout(widgets=[
                    QRadioButton(
                        text="all",
                        checked=filter_==0,
                        toggled=lambda x: set_filter(0),
                        autoExclusive=False,
                    ),
                    QRadioButton(
                        text="in progress",
                        checked=filter_==1,
                        toggled=lambda x: set_filter(1),
                        autoExclusive=False,
                    ),
                    QRadioButton(
                        text="done",
                        checked=filter_==2,
                        toggled=lambda x: set_filter(2),
                        autoExclusive=False,
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
