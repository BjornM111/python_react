import pytest

from react import Renderer


class TestRenderer(Renderer):
    def __init__(self, *args, **kwargs):
        super(TestRenderer, self).__init__(*args, **kwargs)
        self.steps = []

    def render(self, root):
        self._render(
            root,
            self.root,
        )
        self.root = root
        root_ = self.get_element(root)
        self.item = root_ and root_.item

    def _create_instance(self, element):
        element.item = element.Class()

        self.steps.append(
            ("add", element.Class),
        )

    def _move_instance(self, from_element, to_element):
        to_element.item = from_element and from_element.item

    def _pop(self, element, i):
        element.item.widgets.pop(i)

    def _insert(self, parent, i, element):
        parent.item.widgets.insert(i, element.item)

    def _setprops(self, element, props, old_element=None):
        self.steps.append(
            ("update", props),
        )
        for key, value in props.items():
            setattr(element.item, key, value)

    def _setlayout(self, element, layout):
        element.item.layout = layout.item

    def _remove(self, element):
        self.steps.append(
            ("remove", element.Class),
        )


@pytest.fixture
def renderer():
    yield TestRenderer()
