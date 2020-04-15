from react import Element


class Widget(object):
    def __init__(self):
        self.layout = None


class Label(object):
    def __init__(self):
        super().__init__()
        self.text = None


class Text(object):
    def __init__(self):
        super().__init__()
        self.text = None


class VLayout(object):
    def __init__(self):
        self.widgets = []


class HLayout(object):
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


def test_change_prop(renderer):
    renderer.render(
        Element(
            Label,
            text='hello',
        )
    )
    label = renderer.item
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
        ("add", Label, {"text": "hello"}),
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
    renderer.render(
        Element(
            Text,
            text='hello2',
        )
    )
    assert renderer.steps == [
        ("add", Label, {"text": "hello"}),
        ("remove", Label),
        ("add", Text, {"text": "hello2"}),
    ]
    assert renderer.item.text == "hello2"
    assert isinstance(renderer.item, Text)


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
        ("add", Widget, {}),
        ("add", VLayout, {}),
        ("add", Label, {"text": "hello"}),
        ("add", Label, {"text": "hello2"}),
    ]
    assert renderer.item.layout.widgets[0].text == "hello"
    assert renderer.item.layout.widgets[1].text == "hello2"

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

    assert renderer.steps[4:] == [
        ("update", {"text": "hello2"}),
        ("update", {"text": "hello3"}),
    ]
    assert renderer.item.layout.widgets[0].text == "hello2"
    assert renderer.item.layout.widgets[1].text == "hello3"
    assert isinstance(renderer.item.layout, VLayout)
    assert renderer.item.layout.widgets == widgets
