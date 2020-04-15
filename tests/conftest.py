import pytest

from react import Renderer


def split_props(props):
    props = props.copy()
    layout = props.pop('layout', None)
    widgets = props.pop('widgets', None)
    return props, layout, widgets


class TestRenderer(Renderer):
    def __init__(self, *args, **kwargs):
        super(TestRenderer, self).__init__(*args, **kwargs)
        self.steps = []

    def render(self, root):
        self._update(
            root,
            self.root,
        )
        self.root = root
        self.item = root.item

    def add(self, element):
        props, layout, widgets = split_props(element.props)

        item = element.Class()
        for key, value in props.items():
            setattr(item, key, value)

        self.steps.append(
            ("add", element.Class, props),
        )

        if layout:
            self.add(layout)
            item.layout = layout.item
        
        if widgets:
            for widget in widgets:
                self.add(widget)
                item.widgets.append(widget.item)

        element.item = item
        return

    def update(self, props, new, old):
        props, layout, widgets = split_props(props)

        for key, value in props.items():
            setattr(old.item, key, value)

        self.steps.append(
            ("update", props),
        )

        if layout:
            self._update(layout, old.props['layout'])
            old.item.layout = layout.item

        new.item = old.item

    def remove(self, item):
        raise NotImplemented('remove not implemented')


@pytest.fixture
def renderer():
    yield TestRenderer()
