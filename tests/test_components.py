from react import Element


class Label(object):
    def __init__(self):
        self.text = None


def simple(text=None):
    return Element(
        Label,
        text="Very nice "+text,
    )


def none():
    return None


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
    renderer.render(
        Element(none)
    )
    assert renderer.steps == []
