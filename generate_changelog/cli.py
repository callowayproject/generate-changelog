"""Command line interface for generate_changelog."""

import functools
import json
from pathlib import Path
from typing import Callable, Optional

import rich_click as click
from click.core import Context, Parameter
from git import Repo

from generate_changelog import __version__
from generate_changelog.commits import get_context_from_tags
from generate_changelog.configuration import DEFAULT_CONFIG_FILE_NAMES, Configuration, write_default_config
from generate_changelog.indented_logger import get_indented_logger, setup_logging
from generate_changelog.release_hint import suggest_release_type


def generate_config_callback(ctx: Context, param: Parameter, value: bool) -> None:
    """Generate a default configuration file."""
    if not value:  # pragma: no cover
        return
    f = Path.cwd() / Path(DEFAULT_CONFIG_FILE_NAMES[0])
    file_path = f.expanduser().resolve()
    if file_path.exists():
        overwrite = click.confirm(f"{file_path} already exists. Overwrite it?")
        if not overwrite:
            click.echo("Aborting configuration file generation.")
            click.Abort()
    write_default_config(f)
    click.echo(f"The configuration file was written to {f}.")
    ctx.exit()


@click.command(
    context_settings={
        "help_option_names": ["-h", "--help"],
    },
    add_help_option=True,
)
@click.option(
    "--generate-config",
    is_flag=True,
    help="Generate a default configuration file",
    callback=generate_config_callback,
    is_eager=True,
    expose_value=False,
)
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, path_type=Path),
    help="Path to the config file.",
    envvar="CHANGELOG_CONFIG_FILE",
)
@click.option("--repo-path", "-r", help="Path to the repository, if not within the current directory")
@click.option("--starting-tag", "-t", help="Tag to generate a changelog from.")
@click.option("--output", "-o", type=click.Choice(["release-hint", "notes", "all"]), help="What output to generate.")
@click.option("--skip-output-pipeline", is_flag=True, help="Do not execute the output pipeline in the configuration.")
@click.option("--branch-override", "-b", help="Override the current branch for release hint decisions.")
@click.option(
    "--debug-report",
    "-d",
    type=click.Path(file_okay=True, dir_okay=False, path_type=Path),
    required=False,
    help="Output a debug report to a file.",
    envvar="CHANGELOG_REPORT_FILE",
)
@click.option("--verbose", "-v", count=True, help="Increase verbosity.")
@click.version_option(version=__version__)
def cli(
    config: Optional[Path],
    repo_path: Optional[Path],
    starting_tag: Optional[str],
    output: Optional[str],
    skip_output_pipeline: bool,
    branch_override: Optional[str],
    debug_report: Optional[Path],
    verbose: int,
) -> None:
    """Generate a change log from git commits."""
    from generate_changelog import templating
    from generate_changelog.pipeline import pipeline_factory

    echo_func = functools.partial(echo, quiet=bool(output))
    configuration = get_user_config(config, echo_func)
    if verbose:
        configuration.verbosity = verbose
    if debug_report:
        configuration.report_path = debug_report

    setup_logging(configuration.verbosity)
    logger = get_indented_logger(__name__)

    repository = Repo(repo_path) if repo_path else Repo(search_parent_directories=True)

    current_branch = repository.head if repository.head.is_detached else repository.active_branch

    # get starting tag based on configuration if not passed in
    if not starting_tag and configuration.starting_tag_pipeline:
        start_tag_pipeline = pipeline_factory(configuration.starting_tag_pipeline, **configuration.variables)
        starting_tag = start_tag_pipeline.run()

    if not starting_tag:
        logger.info("No starting tag found. Generating entire change log.")
    else:
        logger.info(f"Generating change log from tag: '{starting_tag}'.")

    version_contexts = get_context_from_tags(repository, configuration, starting_tag)

    branch_name = branch_override or current_branch.name
    release_hint = suggest_release_type(branch_name, version_contexts, configuration)

    # use the output pipeline to deal with the rendered change log.
    has_starting_tag = bool(starting_tag)
    rendered_chglog = templating.render_changelog(version_contexts, configuration, has_starting_tag)

    if not skip_output_pipeline:
        echo_func("Executing output pipeline.")
        output_pipeline = pipeline_factory(configuration.output_pipeline, **configuration.variables)
        output_pipeline.run(rendered_chglog.full)

    if output == "release-hint":
        click.echo(release_hint)
    elif output == "notes":
        if rendered_chglog.notes:
            click.echo(rendered_chglog.notes)
        else:
            click.echo(rendered_chglog.full)
    elif output == "all":
        notes = rendered_chglog.notes or rendered_chglog.full
        out = {"release_hint": release_hint, "notes": notes}
        click.echo(json.dumps(out))
    else:
        click.echo("Done.")


def get_user_config(config_file: Optional[Path], echo_func: Callable) -> Configuration:
    """
    Get the default configuration and update it with the user's config file.

    Args:
        config_file: The path to the user's configuration file
        echo_func: The function to call to echo output

    Returns:
        The configuration object
    """
    from generate_changelog.configuration import get_config

    config = get_config()
    if user_config := config_file or next(
        (Path.cwd() / Path(name) for name in DEFAULT_CONFIG_FILE_NAMES if (Path.cwd() / Path(name)).exists()),
        None,
    ):
        echo_func(f"Using configuration file: {user_config}")
        config.update_from_file(user_config)
    else:
        echo_func("No configuration file found. Using default configuration.")
    return config


def echo(message: str, quiet: bool = False) -> None:
    """
    Display a message to the user.

    Args:
        message: The message to send to the user
        quiet: Do it quietly
    """
    if not quiet:
        click.echo(message)
