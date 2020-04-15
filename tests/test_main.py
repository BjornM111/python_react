from react import Element


class Widget(object):
    def __init__(self):
        self.layout = None


class Label(object):
    def __init__(self):
        super().__init__()
        self.text = None

class ColumnLayout(object):
    def __init__(self):
        self.widgets = []


def test_create(renderer):
    renderer.render(
        Element(
            Label,
            text='hello',
        )
    )
    assert renderer.steps == [
        ("add", Label, {"text": "hello"}),
    ]
    assert renderer.item.text == "hello"


def test_change(renderer):
    renderer.render(
        Element(
            Label,
            text='hello',
        )
    )
    renderer.render(
        Element(
            Label,
            text='hello2',
        )
    )
    assert renderer.steps == [
        ("add", Label, {"text": "hello"}),
        ("update", {"text": "hello2"}),
    ]
    assert renderer.item.text == "hello2"


def test_layout(renderer):
    renderer.render(
        Element(
            Widget,
            layout=Element(
                ColumnLayout,
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
        ("add", Widget, {}),
        ("add", ColumnLayout, {}),
        ("add", Label, {"text": "hello"}),
        ("add", Label, {"text": "hello2"}),
    ]
