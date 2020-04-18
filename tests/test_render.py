from react import Element
from .widgets import Label, Text, VLayout, HLayout, Widget


def test_create(renderer):
    renderer.render(
        Element(
            Label,
            text='hello',
        )
    )
    assert renderer.steps == [
        ("add", Label),
        ("update", {"text": "hello"}),
    ]
    assert renderer.item == Label(text="hello")


def test_change_prop(renderer):
    renderer.render(
        Element(
            Label,
            text='hello',
        )
    )
    assert renderer.item == Label(text="hello")
    label = renderer.item
    renderer.render(
        Element(
            Label,
            text='hello2',
        )
    )
    assert renderer.steps == [
        ("add", Label),
        ("update", {"text": "hello"}),
        ("update", {"text": "hello2"}),
    ]
    assert renderer.item == Label(text="hello2")
    assert renderer.item is label


def test_remove(renderer):
    renderer.render(
        Element(
            Label,
            text='hello',
        )
    )
    renderer.render(
        None
    )
    assert renderer.steps == [
        ("add", Label),
        ("update", {"text": "hello"}),
        ("remove", Label),
    ]
    assert renderer.item is None


def test_change_class(renderer):
    renderer.render(
        Element(
            Label,
            text='hello',
        )
    )
    assert renderer.item == Label(text="hello")
    renderer.render(
        Element(
            Text,
            text='hello2',
        )
    )
    assert renderer.steps == [
        ("add", Label),
        ("update", {"text": "hello"}),
        ("remove", Label),
        ("add", Text),
        ("update", {"text": "hello2"}),
    ]
    assert renderer.item == Text(text="hello2")


def test_layout(renderer):
    renderer.render(
        Element(
            Widget,
            layout=Element(
                VLayout,
                widgets=[
                    Element(
                        Label,
                        text="hello"
                    ),
                    Element(
                        Label,
                        text="hello2"
                    ),
                ]
            )
        )
    )

    assert renderer.steps == [
        ("add", Widget),
        ("add", VLayout),
        ("add", Label),
        ("update", {"text": "hello"}),
        ("add", Label),
        ("update", {"text": "hello2"}),
    ]
    assert renderer.item == Widget(
        layout=VLayout(
            widgets=[
                Label(text="hello"),
                Label(text="hello2"),
            ]
        )
    )

    widgets = renderer.item.layout.widgets[:]

    renderer.render(
        Element(
            Widget,
            layout=Element(
                VLayout,
                widgets=[
                    Element(
                        Label,
                        text="hello2"
                    ),
                    Element(
                        Label,
                        text="hello3"
                    ),
                ]
            )
        )
    )

    assert renderer.steps[6:] == [
        ("update", {"text": "hello2"}),
        ("update", {"text": "hello3"}),
    ]
    assert renderer.item == Widget(
        layout=VLayout(
            widgets=[
                Label(text="hello2"),
                Label(text="hello3"),
            ]
        )
    )
    assert renderer.item.layout.widgets == widgets

    renderer.render(
        Element(
            Widget,
            layout=Element(
                VLayout,
                widgets=[
                    None,
                    Element(
                        Label,
                        text="hello3"
                    ),
                ]
            )
        )
    )
    assert renderer.steps[8:] == [
        ("remove", Label),
    ]
    assert renderer.item == Widget(
        layout=VLayout(
            widgets=[
                Label(text="hello3"),
            ]
        )
    )
    assert renderer.item.layout.widgets == [widgets[1]]
