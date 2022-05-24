"""Configuration management for generate_changelog."""
from typing import Callable, Optional, Union

try:
    from functools import cached_property
except ImportError:
    from backports.cached_property import cached_property  # NOQA

try:
    from typing import TypeAlias
except ImportError:
    from typing_extensions import TypeAlias

from dataclasses import asdict, dataclass, field
from pathlib import Path

import typer
from ruamel.yaml import YAML

yaml = YAML()
yaml.indent(mapping=2, sequence=4, offset=2)

StrOrCallable: TypeAlias = Union[str, Callable[[], str]]
"""The type should be either a string or a callable that returns a string."""

IntOrCallable: TypeAlias = Union[int, Callable[[], int]]
"""The type should be either an int or a callable that returns an int."""

DEFAULT_CONFIG_FILE_NAME = ".changelog-config"
"""Base default configuration file name"""

DEFAULT_CONFIG_FILE_NAMES = [
    f"{DEFAULT_CONFIG_FILE_NAME}.yaml",
    f"{DEFAULT_CONFIG_FILE_NAME}.yml",
    DEFAULT_CONFIG_FILE_NAME,
]
"""Valid permutations of the default configuration file name."""

DEFAULT_VARIABLES = {
    "changelog_filename": "CHANGELOG.md",
}

DEFAULT_VALID_AUTHOR_TOKENS = [
    "author",
    "based-on-a-patch-by",
    "based-on-patch-by",
    "co-authored-by",
    "co-committed-by",
    "contributions-by",
    "from",
    "helped-by",
    "improved-by",
    "original-patch-by",
]

DEFAULT_IGNORE_PATTERNS = [
    "[@!]minor",
    "[@!]cosmetic",
    "[@!]refactor",
    "[@!]wip",
    "^$",  # ignore commits with empty messages
    "^Merge branch",
    "^Merge pull",
]

DEFAULT_COMMIT_CLASSIFIERS = [
    {"action": "SummaryRegexMatch", "category": "New", "kwargs": {"pattern": r"(?i)^(?:new|add)[^\n]*$"}},
    {
        "action": "SummaryRegexMatch",
        "category": "Updates",
        "kwargs": {"pattern": r"(?i)^(?:update|change|rename|remove|delete|improve|refactor|chg|modif)[^\n]*$"},
    },
    {"action": "SummaryRegexMatch", "category": "Fixes", "kwargs": {"pattern": r"(?i)^(?:fix)[^\n]*$"}},
    {"action": None, "category": "Other"},  # Match all lines
]

DEFAULT_STARTING_TAG_PIPELINE = [
    {"action": "ReadFile", "kwargs": {"filename": "{{ changelog_filename }}"}},
    {
        "action": "FirstRegExMatch",
        "kwargs": {
            "pattern": r"(?im)^## (?P<rev>\d+\.\d+(?:\.\d+)?)\s+\(\d+-\d{2}-\d{2}\)$",
            "named_subgroup": "rev",
        },
    },
]

DEFAULT_SUMMARY_PIPELINE = [
    {"action": "strip_spaces"},
    {
        "action": "Strip",
        "comment": "Get rid of any periods so we don't get double periods",
        "kwargs": {"chars": "."},
    },
    {"action": "SetDefault", "args": ["no commit message"]},
    {"action": "capitalize"},
    {"action": "append_dot"},
]

DEFAULT_BODY_PIPELINE = [
    {
        "action": "ParseTrailers",
        "comment": "Parse the trailers into metadata.",
        "kwargs": {"commit_metadata": "save_commit_metadata"},
    }
]

DEFAULT_OUTPUT_PIPELINE = [
    {
        "action": "IncrementalFileInsert",
        "kwargs": {
            "filename": "{{ changelog_filename }}",
            "last_heading_pattern": r"(?im)^## \d+\.\d+(?:\.\d+)?\s+\([0-9]+-[0-9]{2}-[0-9]{2}\)$",
        },
    },
]

DEFAULT_GROUP_BY = [
    "metadata.category",
]

DEFAULT_TEMPLATE_DIRS = [".github/changelog_templates/"]


@dataclass
class Configuration:
    """Configuration options for generate-changelog."""

    variables: dict = field(default_factory=dict)
    """User variables for reference in other parts of the configuration."""

    starting_tag_pipeline: Optional[list] = field(default_factory=list)
    """Pipeline to find the most recent tag for incremental changelog generation.
    Leave empty to always start at first commit."""

    #
    # Output
    #
    unreleased_label: str = "Unreleased"
    """Used as the version title of the changes since the last valid tag."""

    summary_pipeline: list = field(default_factory=list)
    """Process the commit's first line for use in the changelog."""

    body_pipeline: list = field(default_factory=list)
    """Process the commit's body for use in the changelog."""

    output_pipeline: list = field(default_factory=list)
    """Process and store the full or partial changelog."""

    template_dirs: list = field(default_factory=list)
    """Full or relative paths to look for output generation templates."""

    group_by: list = field(default_factory=list)
    """Group the commits within a version by these commit attributes."""

    #
    # Commit filtering
    #
    tag_pattern: str = r"^[0-9]+\.[0-9]+(?:\.[0-9]+)?$"
    """Only tags matching this regular expression are used for the changelog."""

    include_merges: bool = False
    """Tells ``git-log`` whether to include merge commits in the log."""

    ignore_patterns: list = field(default_factory=list)
    """Ignore commits whose summary line matches any of these regular expression patterns."""

    commit_classifiers: list = field(default_factory=list)
    """Set the commit's category metadata to the first classifier that returns ``True``."""

    valid_author_tokens: list = field(default_factory=list)
    """Tokens in git commit trailers that indicate authorship."""

    @cached_property
    def rendered_variables(self) -> dict:
        """Render each variable value using the previous variables as the context."""
        from .templating import get_pipeline_env

        context = {}
        for key, value in self.variables.items():
            context[key] = get_pipeline_env(self).from_string(value, globals=context).render()

        return context

    def update_from_file(self, filename: Path):
        """
        Updates this configuration instance in place from a YAML file.

        Args:
            filename: Path to the YAML file

        Raises:
            Exit: if the path does not exist or is a directory
        """
        file_path = filename.expanduser().resolve()

        if not file_path.exists():
            typer.echo(f"'{filename}' does not exist.", err=True)
            raise typer.Exit(1)

        if not file_path.is_file():
            typer.echo(f"'{filename}' is not a file.", err=True)
            raise typer.Exit(1)

        content = file_path.read_text()
        values = yaml.load(content)

        for key, val in values.items():
            if key == "variables" and isinstance(val, dict):
                self.variables.update(val)
            elif hasattr(self, key):
                setattr(self, key, val)


def get_default_config() -> Configuration:
    """
    Create a new :py:class:`Configuration` object with default values.

    Returns:
        A new Configuration object
    """
    return Configuration(
        variables=DEFAULT_VARIABLES,
        ignore_patterns=DEFAULT_IGNORE_PATTERNS,
        commit_classifiers=DEFAULT_COMMIT_CLASSIFIERS,
        body_pipeline=DEFAULT_BODY_PIPELINE,
        summary_pipeline=DEFAULT_SUMMARY_PIPELINE,
        starting_tag_pipeline=DEFAULT_STARTING_TAG_PIPELINE,
        output_pipeline=DEFAULT_OUTPUT_PIPELINE,
        valid_author_tokens=DEFAULT_VALID_AUTHOR_TOKENS,
        group_by=DEFAULT_GROUP_BY,
        template_dirs=DEFAULT_TEMPLATE_DIRS,
    )


def write_default_config(filename: Path):
    """
    Write a default configuration file to the specified path.

    Args:
        filename: Path to write to
    """
    from ruamel.yaml.comments import CommentedMap

    from ._attr_docs import attribute_docstrings

    file_path = filename.expanduser().resolve()
    default_config = get_default_config()

    config_docstrings = attribute_docstrings(Configuration)

    yaml_config = CommentedMap(**asdict(default_config))
    yaml_config.yaml_set_start_comment(
        "For more configuration information, please see https://coordt.github.io/generate-changelog/"
    )
    for attr, doc in config_docstrings.items():
        yaml_config.yaml_set_comment_before_after_key(key=attr, before="")
        yaml_config.yaml_set_comment_before_after_key(key=attr, before=doc)
    yaml.dump(yaml_config, file_path)


_CONFIG = None
"""The global running configuration."""


def set_config(key, value):
    """Set a configuration key to a value."""
    global _CONFIG

    if _CONFIG is None:
        _CONFIG = get_default_config()
    setattr(_CONFIG, key, value)
    return _CONFIG


def get_config() -> Configuration:
    """
    Return the current configuration.

    If the configuration has never been initialized, it is instantiated with the defaults.

    Returns:
        The global configuration object.
    """
    global _CONFIG

    if _CONFIG is None:
        _CONFIG = get_default_config()
    return _CONFIG
