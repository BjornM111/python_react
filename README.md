# pact &middot; ![run tests](https://github.com/BjornM111/python_react/workflows/run%20tests/badge.svg)
**pact** is a declarative gui framework which is heavily inspired by [react](https://reactjs.org)

## Running the tests
```sh
pip install -r requirements.txt
pytest
```

## Examples
### hacking.py
The hacking example is a simple application that tests many features at the same time (wrapper, state, react_qt and rendering).
```sh
python hacking.py
```
### chat.py
A simple one-person chat program, write in the text box and press ">" or the enter key to send your message to yourself
```sh
python chat.py
```
### todo_list.py
A run-of-the-mill todo app, add a todo by writing in the line-edit and press "Add Todo". Check the checkboxes to mark a todo as "done" and apply filters with the radio-buttons at the buttons at the bottom
```sh
python todo_list.py
```