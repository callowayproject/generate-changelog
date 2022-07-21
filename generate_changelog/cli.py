"""Command line interface for generate_changelog."""
from typing import Optional

import json
from enum import Enum
from pathlib import Path

import typer
from git import Repo

from generate_changelog.commits import get_context_from_tags
from generate_changelog.configuration import DEFAULT_CONFIG_FILE_NAMES, write_default_config
from generate_changelog.release_hint import suggest_release_type

app = typer.Typer()


class OutputOption(str, Enum):
    """Types of output available."""

    release_hint = "release-hint"
    notes = "notes"
    all = "all"


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
    starting_tag: Optional[str] = typer.Option(None, "--starting-tag", "-t", help="Tag to generate a changelog from."),
    output: Optional[OutputOption] = typer.Option(None, "--output", "-o", help="What output to generate."),
    skip_output_pipeline: bool = typer.Option(
        False, "--skip-output-pipeline", help="Do not execute the output pipeline in the configuration."
    ),
):
    """Generate a change log from git commits."""
    from generate_changelog import templating
    from generate_changelog.configuration import get_config
    from generate_changelog.pipeline import pipeline_factory

    # Load default configuration
    config = get_config()
    user_config = config_file or next(
        (Path.cwd() / Path(name) for name in DEFAULT_CONFIG_FILE_NAMES if (Path.cwd() / Path(name)).exists()), None
    )
    if user_config:
        if not output:
            typer.echo(f"Using configuration file: {user_config}")
        config.update_from_file(user_config)
    elif not output:
        typer.echo("No configuration file found. Using default configuration.")

    if repository_path:  # pragma: no cover
        repository = Repo(repository_path)
    else:
        repository = Repo(search_parent_directories=True)

    # get starting tag based configuration if not passed in
    if not starting_tag and config.starting_tag_pipeline:
        start_tag_pipeline = pipeline_factory(config.starting_tag_pipeline, **config.variables)
        starting_tag = start_tag_pipeline.run()

    if not output:
        if not starting_tag:
            typer.echo("No starting tag found. Generating entire change log.")
        else:
            typer.echo(f"Generating change log from tag: '{starting_tag}'.")

    version_contexts = get_context_from_tags(repository, config, starting_tag)

    release_hint = suggest_release_type(version_contexts, config)

    # use the output pipeline to deal with the rendered change log.
    notes = templating.render_changelog(version_contexts, config, not starting_tag)

    if not skip_output_pipeline:
        if not output:
            typer.echo("Executing output pipeline.")
        output_pipeline = pipeline_factory(config.output_pipeline, **config.variables)
        output_pipeline.run(notes)

    if output == OutputOption.release_hint:
        typer.echo(release_hint)
    elif output == OutputOption.notes:
        typer.echo(notes)
    elif output == OutputOption.all:
        out = {"release_hint": release_hint, "notes": notes}
        typer.echo(json.dumps(out))
    else:
        typer.echo("Done.")

    raise typer.Exit()


if __name__ == "__main__":
    app()
