"""Command line interface for generate_changelog."""
from typing import Optional

from pathlib import Path

import typer
from git import Repo

from generate_changelog.configuration import DEFAULT_CONFIG_FILE_NAMES, write_default_config

app = typer.Typer()


def version_callback(value: bool):
    """Display the version and exit."""
    import generate_changelog

    if value:
        typer.echo(generate_changelog.__version__)
        raise typer.Exit()


def generate_config_callback(value: bool):
    """Generate a default configuration file."""
    if not value:  # pragma: no cover
        return
    f = Path.cwd() / Path(DEFAULT_CONFIG_FILE_NAMES[0])
    file_path = f.expanduser().resolve()
    if file_path.exists():
        overwrite = typer.confirm(f"{file_path} already exists. Overwrite it?")
        if not overwrite:
            typer.echo("Aborting configuration file generation.")
            typer.Abort()
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
    repository_path: Optional[Path] = typer.Option(
        None, "--repo-path", "-r", help="Path to the repository, if not within the current directory"
    ),
):
    """Generate a change  log from git commits."""
    from generate_changelog import templating
    from generate_changelog.configuration import get_config
    from generate_changelog.pipeline import pipeline_factory

    # Load default configuration
    config = get_config()
    user_config = config_file or next(
        (Path.cwd() / Path(name) for name in DEFAULT_CONFIG_FILE_NAMES if (Path.cwd() / Path(name)).exists()), None
    )
    if user_config:
        typer.echo(f"Using configuration file: {user_config}")
        config.update_from_file(user_config)
    else:
        typer.echo("No configuration file found. Using default configuration.")

    if repository_path:  # pragma: no cover
        repository = Repo(repository_path)
    else:
        repository = Repo(search_parent_directories=True)

    # get starting tag based on configuration
    if config.starting_tag_pipeline:
        start_tag_pipeline = pipeline_factory(config.starting_tag_pipeline, **config.variables)
        starting_tag = start_tag_pipeline.run()
    else:
        starting_tag = None

    if not starting_tag:
        typer.echo("No starting tag found. Generating entire change log.")
    else:
        typer.echo(f"Generating change log from tag: '{starting_tag}'.")

    # use the output pipeline to deal with the rendered change log.
    output_pipeline = pipeline_factory(config.output_pipeline, **config.variables)
    output_pipeline.run(templating.render(repository, config, starting_tag))
    typer.echo("Done.")
    raise typer.Exit()


if __name__ == "__main__":
    app()
