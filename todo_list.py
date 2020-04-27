import sys
from dataclasses import dataclass

from PySide2 import QtWidgets
from PySide2.QtWidgets import QApplication, QSizePolicy
import requests

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


def fetch_todos(set_todos, i):
    result = requests.get('https://jsonplaceholder.typicode.com/todos')
    set_todos([Todo(todo['title'], todo['completed']) for todo in result.json()[i:i+7]])


def master(use_state, use_effect):
    todos, set_todos = use_state([])
    description, set_description = use_state("")
    filter_, set_filter = use_state(0)
    reload_index, set_reload_index = use_state(0)

    use_effect(fetch_todos, set_todos, reload_index)

    return QDialog(
        windowTitle="Todos: {} / {}".format(
            sum(not todo.done for todo in todos),
            len(todos),
        ),
        layout=QVBoxLayout(
            widgets=[
                [
                    QHBoxLayout(key=i, widgets=[
                        QLabel(
                            text=todo.description,
                            sizePolicy=QSizePolicy(
                                QSizePolicy.Expanding,
                                QSizePolicy.Preferred,
                            ),
                        ),
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
                QWidget(
                    sizePolicy=QSizePolicy(
                        QSizePolicy.Expanding,
                        QSizePolicy.Preferred,
                    ),
                ),
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
                    QPushButton(
                        pressed=lambda: set_reload_index(reload_index+1),
                    )
                ]
                ),
            ]
        )
    )


def main():
    app = QApplication(sys.argv)
    renderer = QtRenderer()

    renderer.render(Element(master))
    app.exec_()

if __name__ == "__main__":
    main()
