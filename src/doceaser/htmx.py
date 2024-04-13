from pathlib import Path

from lxml.html.builder import E as e
from lxml import html

from marko.helpers import MarkoExtension
from marko.inline import InlineElement


class HtmxComponent(InlineElement):
    pattern = r"\{\< *htmx *\: *(.+?) *\>\}"
    parse_children = False


class HtmxComponentRender:
    def render_htmx_component(self, element):
        component = e.div(
            **{
                "hx-get": str(Path("/_components/") / element.children),
                "hx-trigger": "load",
                "hx-swap": "outerHTML",
                "class": "skeleton-block is-radiusless",
            },
        )
        return html.tostring(component, encoding=str)


HtmxComponentExtension = MarkoExtension(
    elements=[HtmxComponent],
    renderer_mixins=[HtmxComponentRender],
)
