from werkzeug.exceptions import HTTPException
from werkzeug.wrappers import Request
from werkzeug.routing import Rule, Map
from http import HTTPMethod

from . import routes


class App:
    def __init__(self, root):
        self.root = root

        self.urlmap = Map(
            [
                Rule(
                    "/_static/<path:local_path>",
                    endpoint="static",
                    methods=[HTTPMethod.GET],
                ),
                Rule(
                    "/_assets/<path:local_path>",
                    endpoint="assets",
                    methods=[HTTPMethod.GET],
                ),
                Rule(
                    "/_components/<path:local_path>",
                    endpoint="components",
                ),
                Rule(
                    "/<path:local_path>",
                    endpoint="default",
                    methods=[HTTPMethod.GET],
                ),
            ]
        )

    def __call__(self, environ, start_response):
        request = Request(environ)
        adapter = self.urlmap.bind_to_environ(environ)

        try:
            endpoint, values = adapter.match()
            handler = getattr(routes, endpoint)
            response = handler(self, request, **values)
            return response(environ, start_response)

        except HTTPException as err:
            return err(environ, start_response)
