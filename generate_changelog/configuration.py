"""Configuration management for generate_changelog."""

from typing import Callable, Optional, Union

try:
    from typing import TypeAlias
except ImportError:
    from typing_extensions import TypeAlias

from dataclasses import asdict, dataclass, field
from pathlib import Path

import typer
import yaml

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

DEFAULT_SECTION_PATTERNS = {
    "New": [r"(?i)^(?:new|add)[^\n]*$"],
    "Updates": [r"(?i)^(?:update|change|rename|remove|delete|improve|refactor|chg)[^\n]*$"],
    "Fixes": [r"(?i)^(?:fix)[^\n]*$"],
    "Other": None,  # Match all lines
}

DEFAULT_STARTING_TAG_PIPELINE = [
    {"action": "ReadFile", "kwargs": {"filename": "CHANGELOG.md"}},
    {
        "action": "FirstRegExMatch",
        "kwargs": {
            "pattern": r"(?im)^## (?P<rev>\d+\.\d+(?:\.\d+)?)\s+\(\d+-\d{2}-\d{2}\)$",
            "named_subgroup": "rev",
        },
    },
]

DEFAULT_SUBJECT_PIPELINE = [
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
            "filename": "CHANGELOG.md",
            "last_heading_pattern": r"(?im)^## \d+\.\d+(?:\.\d+)?\s+\([0-9]+-[0-9]{2}-[0-9]{2}\)$",
        },
    },
]


@dataclass
class Configuration:
    """Configuration options for generate_changelog."""

    variables: dict = field(default_factory=dict)
    """User variables for reference in other parts of the configuration."""

    starting_tag_pipeline: Optional[list] = field(default_factory=list)
    """Generate the changelog from this tag. ``None`` means start at first commit."""

    #
    # Output
    #
    unreleased_label: str = "Unreleased"
    """Used as the section title of the changes since the last valid tag."""

    subject_pipeline: list = field(default_factory=list)
    """Process the commit's subject for use in the changelog."""

    body_pipeline: list = field(default_factory=list)
    """Process the commit's body for use in the changelog."""

    output_pipeline: list = field(default_factory=list)
    """Pipeline to do something with the full or partial changelog."""

    template_dirs: list = field(default_factory=list)
    """Paths to look for output generation templates."""

    #
    # Commit filtering
    #
    tag_pattern: str = r"^[0-9]+\.[0-9]+(?:\.[0-9]+)?$"
    """Only tags matching this regular expression are used for the changelog."""

    include_merges: bool = False
    """Tells git-log whether to include merge commits in the log."""

    ignore_patterns: list = field(default_factory=list)
    """Ignore commits that match any of these regular expression patterns."""

    section_patterns: dict = field(default_factory=dict)
    """Group commits into groups if they match any of these regular expressions."""

    valid_author_tokens: list = field(default_factory=list)
    """Tokens in git commit trailers that indicate authorship."""

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
        values = yaml.safe_load(content)

        for key, val in values.items():
            if hasattr(self, key):
                setattr(self, key, val)


def get_default_config() -> Configuration:
    """
    Create a new :py:class:`Configuration` object with default values.

    Returns:
        A new Configuration object
    """
    return Configuration(
        ignore_patterns=DEFAULT_IGNORE_PATTERNS,
        section_patterns=DEFAULT_SECTION_PATTERNS,
        body_pipeline=DEFAULT_BODY_PIPELINE,
        subject_pipeline=DEFAULT_SUBJECT_PIPELINE,
        starting_tag_pipeline=DEFAULT_STARTING_TAG_PIPELINE,
        output_pipeline=DEFAULT_OUTPUT_PIPELINE,
        valid_author_tokens=DEFAULT_VALID_AUTHOR_TOKENS,
    )


def write_default_config(filename: Path):
    """
    Write a default configuration file to the specified path.

    Args:
        filename: Path to write to
    """
    file_path = filename.expanduser().resolve()
    config = asdict(get_default_config())
    with file_path.open("w") as f:
        yaml.safe_dump(config, f, sort_keys=False)


_CONFIG = None
"""The global running configuration."""


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
