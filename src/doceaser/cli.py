from pathlib import Path

from waitress import serve
import click

from .wsgi import App


@click.command()
@click.option(
    "--root",
    type=click.Path(
        exists=True,
        readable=True,
        file_okay=False,
        resolve_path=True,
        path_type=Path,
    ),
    default=".",
    help="Root directory to serve",
)
@click.option(
    "--host",
    default="localhost",
    help="Host to bind to",
)
@click.option(
    "--port",
    default=8080,
    type=int,
    help="Port to bind to",
)
def main(root, host, port) -> None:
    print(f"Listening on http://{host}:{port}")
    serve(App(root), host=host, port=port)


if __name__ == "__main__":
    main()
