from werkzeug.wrappers import Response
from http import HTTPStatus

from lxml.html.builder import E as e
from lxml import html

import requests


def get(request):
    r = requests.get("https://httpbin.org/anything")
    body = e.pre(e.code(r.text))

    return Response(
        html.tostring(body),
        status=HTTPStatus.OK,
        content_type="text/html; charset=utf-8",
    )
