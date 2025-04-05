"""Parse the changelog and return the release notes."""

import re
from itertools import islice, tee, zip_longest
from pathlib import Path
from typing import Any, Iterable, Iterator, List, Optional, Tuple

from generate_changelog.configuration import get_config


class MissingConfigurationError(Exception):
    """An optional part of the configuration is missing for this operation."""

    pass


def pairs(iterable: Iterable) -> Iterator[Tuple[Any, Any]]:
    """
    Return successive non-overlapping pairs taken from the input iterable.

    Examples:
        >>> list(pairs('ABCDEFG'))
        [('A', 'B'), ('C', 'D'), ('E', 'F'), ('G', None)]

    Args:
        iterable: The iterable to split into pairs

    Returns:
        An iterator of 2-tuples.
    """
    a, b = tee(iterable)
    return zip_longest(islice(a, 0, None, 2), islice(b, 1, None, 2))


def split_changelog(contents: str, section_pattern: Optional[str] = None) -> List[Tuple[str, str]]:
    """
    Read the changelog and split it into version and note sections.

    Args:
        contents: The contents of the changelog.
        section_pattern: A regex pattern to split the changelog into sections.
            If `None`, the pattern is derived from the [`starting_tag_pipeline`]
            [generate_changelog.configuration.Configuration.starting_tag_pipeline] configuration option.

    Returns:
        A list of version and note sections.
    """
    from generate_changelog.templating import get_default_env

    config = get_config()
    section_pattern = section_pattern or get_section_pattern()
    header_text = get_default_env(config).get_template("heading.md.jinja").render()

    parts = re.split(section_pattern, contents)
    if parts[0].startswith(header_text):
        parts = parts[1:]

    return list(pairs(parts))


def get_section_pattern() -> str:
    """
    Get the version section pattern for the changelog.

    Raises:
        MissingConfigurationError: If the ``starting_tag_pipeline`` configuration is missing or incorrect.

    Returns:
        The version section pattern.
    """
    config = get_config()

    if not config.starting_tag_pipeline:
        raise MissingConfigurationError(
            "The 'starting_tag_pipeline' configuration is is required for parsing the changelog."
        )

    regex = next(
        (
            action["kwargs"]["pattern"]
            for action in config.starting_tag_pipeline
            if action["action"] == "FirstRegExMatch"
        ),
        None,
    )
    if not regex:
        raise MissingConfigurationError(
            "The 'starting_tag_pipeline' configuration is missing a 'FirstRegExMatch' "
            "action to indicate the version sections."
        )

    return regex


def get_changelog_path() -> Path:
    """
    Return the path to the changelog.

    Raises:
        MissingConfigurationError: If the ``starting_tag_pipeline`` configuration is missing or incorrect.

    Returns:
        The path to the changelog.
    """
    config = get_config()

    if not config.starting_tag_pipeline:
        raise MissingConfigurationError(
            "The 'starting_tag_pipeline' configuration is is required for parsing the changelog."
        )

    changelog_path = next(
        (
            Path(action["kwargs"]["filename"])
            for action in config.starting_tag_pipeline
            if action["action"] == "ReadFile"
        ),
        None,
    )

    if not changelog_path:
        raise MissingConfigurationError(
            "The 'starting_tag_pipeline' configuration is missing a 'ReadFile' action to indicate the changelog file."
        )

    return changelog_path


def get_version_notes(version: str) -> str:
    """Parse the changelog.md file and return the notes for the given version."""
    changelog_path = get_changelog_path()
    changelog_contents = changelog_path.read_text()

    return next(
        (notes.strip() for vrsn, notes in split_changelog(changelog_contents) if vrsn.startswith(version)),
        "",
    )
