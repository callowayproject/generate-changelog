"""Command line interface for clgen."""
from typing import List, Optional

from pathlib import Path

import typer

import clgen
from clgen.configuration import DEFAULT_CONFIG_FILE_NAMES, load_config_file
from clgen.gitchangelog import changelog, get_log_encoding, get_revision, rest_py
from clgen.processors.file_processing import stdout
from clgen.processors.text_processing import noop
from clgen.utilities import eval_if_callable

app = typer.Typer()


def version_callback(value: bool):
    if value:
        typer.echo(clgen.__version__)
        raise typer.Exit()


@app.command()
def main(
    revlist: Optional[List[str]] = typer.Argument(None, help="Optional git-rev-list style arguments"),
    version: Optional[bool] = typer.Option(
        None, help="show program's version number and exit", callback=version_callback, is_eager=True
    ),
    debug: bool = typer.Option(False, "--debug", "-d", help="Enable debug mode (show full tracebacks)."),
    config_file: Optional[Path] = typer.Option(
        None, "--config", "-c", help="Path to the config file.", envvar="CLGEN_CONFIG_FILE"
    ),
):

    description_msg = """\
    Run this command in a git repository to output a formatted changelog.
    """

    epilog_msg = """\
    %(exname)s uses a config file to filter meaningful commits or do some
    formatting in commit messages.

    Config file location will be resolved in this order:
      - in shell environment variable GITCHANGELOG_CONFIG_FILENAME
      - in git configuration: ``git config gitchangelog.rc-path``
      - as '.%(exname)s.rc' in the root of the current git repository

    """

    # Load default configuration
    default_config = load_config_file(Path(__file__).parent / "default_config.yaml")

    # Load user configuration
    if config_file:  # was it passed in?
        user_config = load_config_file(config_file)
    else:  # Is there a configuration file?
        user_config = next(
            (load_config_file(Path(name)) for name in DEFAULT_CONFIG_FILE_NAMES if Path(name).exists()),
            {},
        )

    default_config.update(user_config)

    # get git repo
    repository = ...

    log_encoding = get_log_encoding(repository, config)
    revlist = get_revision(repository, config, opts)
    config["unreleased_version_label"] = eval_if_callable(config["unreleased_version_label"])

    content = changelog(
        repository=repository,
        revlist=revlist,
        ignore_regexps=config["ignore_regexps"],
        section_regexps=config["section_regexps"],
        unreleased_version_label=config["unreleased_version_label"],
        tag_filter_regexp=config["tag_filter_regexp"],
        output_engine=config.get("output_engine", rest_py),
        include_merge=config.get("include_merge", True),
        body_process=config.get("body_process", noop),
        subject_process=config.get("subject_process", noop),
        log_encoding=log_encoding,
    )

    if isinstance(content, str):
        content = content.splitlines(True)

    config.get("publish", stdout)(content)


if __name__ == "__main__":
    app()
