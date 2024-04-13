from uuid import uuid4

from werkzeug.wrappers import Response
from http import HTTPStatus

from lxml.html.builder import E as e
from lxml import html


def get(request):
    base_id = str(uuid4())

    form = e.div(
        e.form(
            e.div(
                e.label("Name", **{"class": "label"}),
                e.div(
                    e.input(
                        **{
                            "type": "text",
                            "name": "name",
                            "required": "true",
                            "class": "input is-radiusless",
                        }
                    ),
                    **{"class": "control"},
                ),
                **{"class": "field"},
            ),
            e.div(
                e.div(
                    e.button(
                        "Submit",
                        **{
                            "class": "button is-link is-radiusless",
                            "type": "submit",
                        },
                    ),
                    **{"class": "control"},
                ),
                **{"class": "field"},
            ),
            **{
                "hx-post": request.path,
                "hx-trigger": "submit",
                "hx-target": f"#form-{base_id}-result",
                "hx-indicator": f"#form-{base_id}-indicator",
            },
        ),
        e.div(
            e.div(
                **{
                    "id": f"form-{base_id}-indicator",
                    "class": "htmx-indicator",
                },
            ),
            **{"id": f"form-{base_id}-result"},
        ),
    )

    return Response(
        html.tostring(form),
        status=HTTPStatus.OK,
        content_type="text/html; charset=utf-8",
    )


def post(app, request):
    name = request.form.get("name", "Anonymous")
    body = e.p(f"Hello, {name}!")
    return Response(
        html.tostring(body),
        status=HTTPStatus.OK,
        content_type="text/html; charset=utf-8",
    )
