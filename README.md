# DocEaser

Dynamic Interactive documentation made easier.

## Introduction

DocEaser is a very simple framework used to render Markdown documents. The twist
is that those documents can embed HTMX components written in Python, to add
interactivity to your documentation.

## Installation

```shell
$ pip install git+https://github.com/linkdd/doceaser
```

## Usage

### Run the server

Create a folder for your content:

```shell
$ mkdir content/
$ mkdir content/_static
$ python -m doceaser.cli --root content/
Listening on http://localhost:8080/
```

The server is based on the production-ready WSGI server
[waitress](https://docs.pylonsproject.org/projects/waitress/en/latest/).

### Organizing your content

Static files go in the `content/_static/` directory and will be served at
`/_static/...` URLs:

| Content path | URL |
| --- | --- |
| `content/_static/screenshot.png` | `/_static/screenshot.png` |

HTMX components go in the `content/` directory as Python files, and will be
served at `/_components/...` URLs:

| Content path | URL |
| --- | --- |
| `content/form.py` | `/_components/form` |
| `content/hello/world.py` | `/_components/hello/world` |

Markdown files go in the `content/` directory, and will be served at `/...`
URLs. The special file `_index.md` can be used as an index section:

| Content path | URL |
| --- | --- |
| `content/about.md` | `/about` |
| `content/_index.md` | `/` |
| `content/about/_index.md` | `/about` |
| `content/about/legal.md` | `/about/legal` |

### Writing Markdown files

Markdown files may have a *frontmatter* header (using YAML, TOML or JSON):

```markdown
---
title: Hello world
---

# Hello World
```

The `title` property will be used for the `<title/>` HTML tag.

To embed an HTMX component, you can use this special syntax (an extension of
the [CommonMark](https://spec.commonmark.org/0.30/) specification):

```markdown
{< htmx:form >}

{< htmx:hello/world >}
```

This will render to the following HTML (with some extra irrelevant details):

```html
<div hx-get="/_components/form" hx-trigger="load"></div>

<div hx-get="/_components/hello/world" hx-trigger="load"></div>
```

### Writing HTMX components

An HTMX component is a Python file in the `content/` directory.
This file may implement a function per HTTP method to handle the request. That
function accepts a [werkzeug](https://werkzeug.palletsprojects.com/) Request and
returns a *werkzeug* Response:

```python
from werkzeug.wrappers import Request, Response
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
```

**NB:**

 - You can use any method you like to render the HTML. Internally, DocEaser uses
   `lxml`, so you might as well use it. But it is not mandatory.
 - Any extra Python dependencies you might want shall be installed by you (like
   `requests` in the example above).

## Documentation

None at the moment except this README and a few examples in the `examples/`
directory.

## Roadmap

This project is mostly a Proof of Concept. Nothing has been planned ahead (yet).
I will probably not actively develop it, but I can at least guarantee that bugs
will be addressed, and feature requests will be discussed (and maybe
implemented?).

Here are a few ideas that might be nice, from the top of my head:

 - **Make the website layout customizable:** At the moment, I simply generate a
   single page with [Bulma](https://bulma.io) as the CSS framework, everything
   is tightly coupled to it (fine for a PoC, not ideal for a finished product)
 - **Cache the Markdown rendering:** Everything is rerendered from scratch on
   every call. This might not be the best for performance.

Any other ideas, and Pull Requests are more than welcome! Give a look to the
[CONTRIBUTING](./CONTRIBUTING.md) file.

## License

This software is released under the terms of the [MIT License](./LICENSE.txt).
