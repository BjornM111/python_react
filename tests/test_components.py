from react import Element


class Label(object):
    def __init__(self):
        self.text = None


class Button(object):
    def __init__(self):
        self.pressed = None


class Layout(object):
    def __init__(self):
        self.widgets = None


class Widget(object):
    def __init__(self):
        self.layout = None


def simple(text=None):
    return Element(
        Label,
        text="Very nice "+text,
    )


def test_create(renderer):
    renderer.render(
        Element(
            simple,
            text="hej",
        )
    )
    assert renderer.steps == [
        ("add", Label),
        ("update", {"text": "Very nice hej"}),
    ]
    assert isinstance(renderer.item, Label)
    assert renderer.item.text == "Very nice hej"


def test_update(renderer):
    renderer.render(
        Element(
            simple,
            text="hej",
        )
    )
    renderer.render(
        Element(
            simple,
            text="hej2",
        )
    )
    assert renderer.steps == [
        ("add", Label),
        ("update", {"text": "Very nice hej"}),
        ("update", {"text": "Very nice hej2"}),
    ]
    assert isinstance(renderer.item, Label)
    assert renderer.item.text == "Very nice hej2"


def test_none(renderer):
    def none():
        return None

    renderer.render(
        Element(none)
    )
    assert renderer.steps == []
    assert renderer.item is None


def test_state_root(renderer):

    def component(use_state):
        visible, set_visible = use_state(True)
        if not visible:
            return None
        return Element(
            Button,
            pressed=lambda: set_visible(False),
        )

    renderer.render(
        Element(component)
    )
    assert isinstance(renderer.item, Button)
    renderer.root.state[0][0] = True
    renderer.item.pressed()
    renderer.root.state[0][0] = False
    assert renderer.item is None


def stest_state_layout(renderer):

    def component(use_state):
        visible, set_visible = use_state(True)
        if not visible:
            return None
        return Element(
            Button,
            pressed=lambda: set_visible(False),
        )

    renderer.render(
        Element(
            Layout,
            widgets=[Element(component)],
        )
    )
    assert isinstance(renderer.item, Button)
    renderer.root.widgets[0].state[0][0] = True
    renderer.item.pressed()
    renderer.root.widgets[0].state[0][0] = False
    assert renderer.item is None

