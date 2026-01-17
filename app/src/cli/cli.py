"""This is the Entry point for the application CLI, this CLI exposes all the submodules CLIs."""

__all__ = ["app"]

import typer

from src.transformations.cli import app as transformations_app
from src.sources.cli import app as sources_app
from src.governance.cli import app as governance_app

app = typer.Typer()
app.add_typer(transformations_app, name="transform")
app.add_typer(sources_app, name="source")
app.add_typer(governance_app, name="govern")


@app.callback()
def default_app_args():
    """A simple CLI application with greeting commands."""
    pass
