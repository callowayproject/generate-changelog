"""Templating functions."""
from typing import Optional

from git import Repo
from jinja2 import ChoiceLoader, Environment, FileSystemLoader, PackageLoader, select_autoescape

from generate_changelog.configuration import Configuration, get_config
from generate_changelog.context import ChangelogContext

from .commits import get_context_from_tags


def get_default_env(config: Optional[Configuration] = None):
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


def get_pipeline_env(config: Optional[Configuration] = None):
    """The Jinja environment for rendering actions and pipelines."""
    if config is None:
        config = get_config()
    return Environment(
        loader=ChoiceLoader([FileSystemLoader(config.template_dirs), PackageLoader("generate_changelog")]),
        autoescape=select_autoescape(),
    )


def render_changelog(repository: Repo, config: Configuration, starting_tag: Optional[str] = None) -> str:
    """
    Render the full or incremental changelog for the repository to a string.

    Args:
        repository: The git repository to evaluate.
        config: The current configuration object.
        starting_tag: Optional starting tag for generating incremental changelogs.

    Returns:
        The full or partial changelog
    """
    version_context = get_context_from_tags(repository, config, starting_tag)
    context = ChangelogContext(config=config, versions=version_context)
    if starting_tag:
        heading_str = get_default_env(config).get_template("heading.md.jinja").render()
        versions_str = get_default_env(config).get_template("versions.md.jinja").render(context.as_dict())
        return "\n".join([heading_str, versions_str])

    return get_default_env(config).get_template("base.md.jinja").render(context.as_dict())
