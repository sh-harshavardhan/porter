"""A CLI application using Typer for source related commands."""

__all__ = ["app"]

import typer

app = typer.Typer()


@app.callback()
def main():
    """A simple CLI application with greeting commands."""
    pass
