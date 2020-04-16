from PySide2 import QtWidgets

from react import Element
from wrapper import wrap


def test_wrapper():
    wrap("QtWidgets", QtWidgets, Element)
    from wrapper.QtWidgets import QLabel

    element = QLabel(text="hej")
    assert isinstance(element, Element)
    assert element.Class == QtWidgets.QLabel
    assert element.props == {"text": "hej"}
