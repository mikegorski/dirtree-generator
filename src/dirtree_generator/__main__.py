from pathlib import Path

import click
import typer
from typing_extensions import Annotated

from dirtree_generator.docstrings import HELP_APP, HELP_GEN, HELP_HIDDEN, HELP_ROOT, HELP_STYLE, HELP_VERBOSE
from dirtree_generator.generators import GEN_MAPPING, STYLES
from dirtree_generator.presenter import TreePresenter

app = typer.Typer(help=HELP_APP, rich_markup_mode="rich")


@app.callback(invoke_without_command=True)
def main(
    root: Annotated[Path, typer.Argument(help=HELP_ROOT, rich_help_panel="Arguments")] = Path.cwd(),
    generator_type: Annotated[
        str,
        typer.Option(
            "--generator", "-g", click_type=click.Choice(GEN_MAPPING.keys()), help=HELP_GEN, rich_help_panel="Style"
        ),
    ] = "plain",
    style: Annotated[
        str,
        typer.Option("--style", "-s", click_type=click.Choice(STYLES.keys()), help=HELP_STYLE, rich_help_panel="Style"),
    ] = "simple",
    verbose: Annotated[
        bool, typer.Option("--verbose", "-v", help=HELP_VERBOSE, rich_help_panel="Additional Controls")
    ] = False,
    show_hidden: Annotated[
        bool, typer.Option("--show-hidden", "-h", help=HELP_HIDDEN, rich_help_panel="Additional Controls")
    ] = False,
):
    gen_class = GEN_MAPPING[generator_type]
    generator = gen_class(root=root, style=style, verbose=verbose, show_hidden=show_hidden)
    generator.build_tree()
    presenter = TreePresenter(generator=generator)
    presenter.display()


if __name__ == "__main__":
    app()
