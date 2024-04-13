from typing import TYPE_CHECKING
import textwrap

from importlib.machinery import SourceFileLoader
from importlib import resources
from pathlib import Path
import mimetypes

from werkzeug.wrappers import Response, Request
from wsgiref.util import FileWrapper
from http import HTTPStatus

from lxml.html.builder import E as e
from lxml import html

import frontmatter
import marko

from .htmx import HtmxComponentExtension

if TYPE_CHECKING:
    from .wsgi import App


def static(app, request, local_path):
    static_path = app.root / "_static" / local_path

    if not static_path.is_file():
        return Response(
            "File Not found",
            status=HTTPStatus.NOT_FOUND,
            content_type="text/plain",
        )

    content_type, _ = mimetypes.guess_type(static_path)
    if content_type is None:
        content_type = "application/octet-stream"

    data = FileWrapper(static_path.open("rb"))
    return Response(data, status=HTTPStatus.OK, content_type=content_type)


def assets(app, request, local_path):
    asset_path = resources.files() / "assets" / local_path

    if not asset_path.is_file():
        return Response(
            "File Not found",
            status=HTTPStatus.NOT_FOUND,
            content_type="text/plain",
        )

    content_type, _ = mimetypes.guess_type(asset_path)
    if content_type is None:
        content_type = "application/octet-stream"

    data = FileWrapper(asset_path.open("rb"))
    return Response(data, status=HTTPStatus.OK, content_type=content_type)


def components(app, request, local_path):
    component_path = (app.root / local_path).with_suffix(".py")

    if not component_path.is_file():
        return Response(
            "Component Not found",
            status=HTTPStatus.NOT_FOUND,
            content_type="text/plain",
        )

    module_name = component_path.stem
    module_loader = SourceFileLoader(module_name, str(component_path))
    module = module_loader.load_module()

    handler = getattr(module, request.method.lower(), None)
    if handler is None:
        return Response(
            "Method not allowed",
            status=HTTPStatus.METHOD_NOT_ALLOWED,
            content_type="text/plain",
        )

    return handler(request)


def default(app, request, local_path):
    document_path = app.root / local_path / "_index.md"
    if not document_path.is_file():
        document_path = (app.root / local_path).with_suffix(".md")

    if not document_path.is_file():
        return Response(
            "Document Not found",
            status=HTTPStatus.NOT_FOUND,
            content_type="text/plain",
        )

    meta, content = frontmatter.parse(document_path.read_text())
    md = marko.Markdown(extensions=[HtmxComponentExtension])
    article = md.convert(content)

    page = e.html(
        e.head(
            e.title(meta.get("title", f"{document_path}")),
            e.meta(charset="utf-8"),
            e.meta(
                name="viewport",
                content="width=device-width, initial-scale=1",
            ),
            e.link(
                rel="stylesheet",
                href="/_assets/bulma.css",
            ),
            e.link(
                rel="stylesheet",
                href="/_assets/animate.css",
            ),
            e.script(
                type="application/javascript",
                src="/_assets/htmx.js",
            ),
            e.script(
                type="application/javascript",
                src="/_assets/hyperscript.js",
            ),
            e.script(
                type="application/javascript",
                src="/_assets/bulma-toast.js",
            ),
        ),
        e.body(
            e.main(
                e.article(
                    e.div(
                        *html.fragments_fromstring(article),
                        **{"class": "content"},
                    ),
                    **{"class": "box is-radiusless has-background-white"},
                ),
                **{"class": "container py-3"},
            ),
            e.footer(
                e.p(
                    "Powered by ",
                    e.b("idocbook"),
                    **{"class": "has-text-right p-3"},
                ),
            ),
        ),
        **{
            "data-theme": "light",
            "class": "has-background-primary-95",
            "style": "overflow-y: auto;",
            "_": textwrap.dedent(
                """
                on htmx:responseError
                    call bulmaToast.toast({
                        message: "An error occured: " + detail.xhr.responseText,
                        type: "is-danger is-radiusless has-text-white is-clickable",
                        position: "bottom-right",
                        animate: { in: "fadeIn", out: "fadeOut" }
                    })
                """
            ).strip(),
        },
    )

    return Response(
        html.tostring(page),
        status=HTTPStatus.OK,
        content_type="text/html; charset=utf-8",
    )
