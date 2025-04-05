"""Templating functions."""

from dataclasses import dataclass
from typing import List, Optional

from jinja2 import ChoiceLoader, Environment, FileSystemLoader, PackageLoader, select_autoescape

from generate_changelog.configuration import Configuration, get_config
from generate_changelog.context import ChangelogContext, VersionContext


@dataclass
class RenderedChangelog:
    r"""
    The output of rendering a changelog.

    If it is an incremental changelog, `full` contains `{heading}\n{notes}`

    If it is a full changelog, `heading` and `notes` are empty.
    """

    heading: Optional[str] = None
    notes: Optional[str] = None
    full: Optional[str] = None


def get_default_env(config: Optional[Configuration] = None) -> Environment:
    """The default Jinja environment for rendering a changelog."""
    if config is None:
        config = get_config()
    return Environment(
        loader=ChoiceLoader([FileSystemLoader(config.template_dirs), PackageLoader("generate_changelog")]),
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
        autoescape=select_autoescape(),
    )


def get_pipeline_env(config: Optional[Configuration] = None) -> Environment:
    """The Jinja environment for rendering actions and pipelines."""
    if config is None:
        config = get_config()
    return Environment(
        loader=ChoiceLoader([FileSystemLoader(config.template_dirs), PackageLoader("generate_changelog")]),
        autoescape=select_autoescape(),
    )


def render_changelog(
    version_context: List[VersionContext], config: Configuration, incremental: bool = False
) -> RenderedChangelog:
    """
    Render the full or incremental changelog for the repository to a string.

    Args:
        version_context: The processed commits
        config: The current configuration object.
        incremental: `True` to generate an incremental changelog. `False` to render the entire thing.

    Returns:
        The full or partial changelog
    """
    context = ChangelogContext(config=config, versions=version_context)
    if incremental:
        heading_str = get_default_env(config).get_template("heading.md.jinja").render()
        versions_str = get_default_env(config).get_template("versions.md.jinja").render(context.as_dict())
        return RenderedChangelog(heading=heading_str, notes=versions_str, full=f"{heading_str}\n{versions_str}")

    chglog = get_default_env(config).get_template("base.md.jinja").render(context.as_dict())
    return RenderedChangelog(full=chglog)
