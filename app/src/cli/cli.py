import typer

from src.transformations.cli import app as transformations_app
from src.sources.cli import app as sources_app
from src.governance.cli import app as governance_app

app = typer.Typer()
app.add_typer(transformations_app, name="transform")
app.add_typer(sources_app, name="source")
app.add_typer(governance_app, name="govern")


# @app.command()
# def run_parallel():
#     run_in_parallel(4, func1)


@app.callback()
def default_app_args():
    """
    A simple CLI application with greeting commands.
    """
    pass


# if __name__ == "__main__":
#     print("Starting the CLI application...")
#     app()  # This will invoke the Typer app
