"""Test basic git ops."""

import pytest
from pytest import param

from generate_changelog import git_ops
from generate_changelog.configuration import get_config


@pytest.mark.parametrize(
    ["start", "end", "length"],
    (
        param(None, None, 6, id="no-start-end"),
        param("0.0.3", None, 1, id="start-no-end"),
        param("0.0.1", "0.0.2", 1, id="start-and-end"),
        param(None, "0.0.2", 2, id="end-no-start"),
    ),
)
def test_parse_commits_no_start_end(default_repo, start, end, length):
    """Parse commits from a repo without a start or end."""
    commits = git_ops.parse_commits(default_repo, start, end)
    assert len(commits) == length


def test_get_tags(default_repo):
    """get_tags should return all the tags."""
    tags = git_ops.get_tags(default_repo)
    assert len(tags) == 3
    assert tags[0].name == "0.0.3"
    assert tags[0].tagger.name == "Bob"
    assert tags[0].date_string == "2022-01-05"
    assert tags[1].name == "0.0.2"
    assert tags[1].tagger.name == "Alice"
    assert tags[2].name == "0.0.1"
    assert tags[2].tagger.name == "Bob"


def test_get_commits_by_all_tags(default_repo):
    """Commits should be grouped by tags and filtered."""
    grouping = git_ops.get_commits_by_tags(default_repo, get_config().tag_pattern)

    assert len(grouping) == 4

    expected = [("HEAD", 1), ("0.0.3", 3), ("0.0.2", 1), ("0.0.1", 1)]
    for group, expect in zip(grouping, expected):
        assert group["tag_name"] == expect[0]
        assert len(group["commits"]) == expect[1]


def test_get_commits_since_tag(default_repo):
    """Commits should be grouped by tags and filtered since tag."""
    grouping = git_ops.get_commits_by_tags(default_repo, get_config().tag_pattern, "0.0.2")

    assert len(grouping) == 2

    expected = [
        ("HEAD", 1),
        ("0.0.3", 3),
    ]
    for group, expect in zip(grouping, expected):
        assert group["tag_name"] == expect[0]
        assert len(group["commits"]) == expect[1]
