"""Test the retrieval of release notes from the changelog."""

from pathlib import Path

import pytest

from generate_changelog import configuration, notes
from generate_changelog.notes import MissingConfigurationError

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def test_pairs():
    """The pairs function should return a list of pairs."""
    assert list(notes.pairs([1, 2, 3])) == [(1, 2), (3, None)]
    assert list(notes.pairs([1, 2, 3, 4])) == [(1, 2), (3, 4)]


def test_split_changelog():
    """The split_changelog function should split the changelog into a list of tuples."""
    configuration._CONFIG = configuration.get_default_config()
    contents = FIXTURES_DIR.joinpath("rendered_conv_commit_repo.md").read_text()
    parsed_notes = notes.split_changelog(contents, r"(?im)^## (?P<rev>\d+\.\d+(?:\.\d+)?)\s+\(\d+-\d{2}-\d{2}\)$")
    assert len(parsed_notes) == 4


def test_get_section_pattern():
    """The get_section_pattern function should return a regex pattern."""
    configuration._CONFIG = configuration.get_default_config()
    assert notes.get_section_pattern() == r"(?im)^## (?P<rev>\d+\.\d+(?:\.\d+)?)\s+\(\d+-\d{2}-\d{2}\)$"

    configuration._CONFIG.starting_tag_pipeline = []
    with pytest.raises(MissingConfigurationError):
        notes.get_section_pattern()

    configuration._CONFIG.starting_tag_pipeline = [
        {"action": "ReadFile", "kwargs": {"filename": "{{ changelog_filename }}"}},
    ]
    with pytest.raises(MissingConfigurationError):
        notes.get_section_pattern()


def test_get_changelog_path():
    """The get_changelog_path function should return the path to the changelog."""
    configuration._CONFIG = configuration.get_default_config()
    assert notes.get_changelog_path() == Path("{{ changelog_filename }}")

    configuration._CONFIG.starting_tag_pipeline = []
    with pytest.raises(MissingConfigurationError):
        notes.get_changelog_path()

    configuration._CONFIG.starting_tag_pipeline = [
        {"action": "NoAction", "kwargs": {"filename": "{{ changelog_filename }}"}},
    ]
    with pytest.raises(MissingConfigurationError):
        notes.get_changelog_path()


def test_get_version_notes():
    """The get_version_notes function should return the notes for the given version."""
    configuration._CONFIG = configuration.get_default_config()
    configuration._CONFIG.starting_tag_pipeline[0]["kwargs"] = {
        "filename": str(FIXTURES_DIR.joinpath("rendered_conv_commit_repo.md"))
    }
    assert notes.get_version_notes("1.1.0") == (
        "### New Features\n"
        "#### Other\n\n"
        "- Readme.\n    \n"
        "- Docker.\n    \n"
        "### Other\n"
        "#### release\n\n"
        "- 1.1.0.\n    \n"
        "### Updates\n"
        "#### Other\n\n"
        "- Crash on connection reset."
    )
