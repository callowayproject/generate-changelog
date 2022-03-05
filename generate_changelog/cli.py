"""Command line interface for generate_changelog."""
from typing import Optional

from pathlib import Path

import typer
from git import Repo

from generate_changelog.configuration import DEFAULT_CONFIG_FILE_NAMES, get_default_config, write_default_config

app = typer.Typer()


def version_callback(value: bool):
    """Display the version and exit."""
    import generate_changelog

    if value:
        typer.echo(generate_changelog.__version__)
        raise typer.Exit()


def generate_config_callback(value: bool):
    """Generate a default configuration file."""
    if value:
        f = Path.cwd() / Path(DEFAULT_CONFIG_FILE_NAMES[0])
        write_default_config(f)
        typer.echo(f"The configuration file was written to {f}.")
        raise typer.Exit()


@app.command()
def main(
    version: Optional[bool] = typer.Option(
        None, "--version", help="Show program's version number and exit", callback=version_callback, is_eager=True
    ),
    generate_config: Optional[bool] = typer.Option(
        None,
        "--generate-config",
        help="Generate a default configuration file",
        callback=generate_config_callback,
    ),
    config_file: Optional[Path] = typer.Option(
        None, "--config", "-c", help="Path to the config file.", envvar="CLGEN_CONFIG_FILE"
    ),
):
    """Generate a change  log from git commits."""
    from generate_changelog import templating
    from generate_changelog.pipeline import pipeline_factory

    # Load default configuration
    config = get_default_config()

    if user_config := config_file or next(
        (Path.cwd() / Path(name) for name in DEFAULT_CONFIG_FILE_NAMES if (Path.cwd() / Path(name)).exists()), None
    ):
        typer.echo(f"Using configuration file: {user_config}")
        config.update_from_file(user_config)
    else:
        typer.echo("No configuration file found. Using default configuration.")

    repository = Repo(search_parent_directories=True)

    # get starting tag based on configuration
    start_tag_pipeline = pipeline_factory(config.starting_tag_pipeline)
    starting_tag = start_tag_pipeline.run()
    if not starting_tag:
        typer.echo("No starting tag found. Generating entire change log.")
    else:
        typer.echo(f"Generating change log from tag: '{starting_tag}'.")

    # use the output pipeline to deal with the rendered change log.
    output_pipeline = pipeline_factory(config.output_pipeline)
    output_pipeline.run(templating.render(repository, config, starting_tag))


if __name__ == "__main__":
    app()
