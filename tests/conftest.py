import pytest

from react import Renderer


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
        self.item = root and root.item

    def _pop(self, element, i):
        element.item.widgets.pop(i)

    def _insert(self, parent, i, element):
        parent.item.widgets.insert(i, element.item)


@pytest.fixture
def renderer():
    yield TestRenderer()
