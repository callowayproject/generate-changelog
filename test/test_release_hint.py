"""Tests of the release_hint module."""
from typing import Optional, Union

import pytest
from faker import Faker
from pytest import param

from generate_changelog import release_hint
from generate_changelog.context import CommitContext
from generate_changelog.release_hint import InvalidRuleError

fake = Faker()


def commit_context_factory(grouping: Union[str, tuple, None] = None, files: Optional[set] = None):
    """Return a commit context with sample data."""
    summary = fake.sentence(nb_words=8, variable_nb_words=True)
    body = "\n".join(
        [summary, fake.text(max_nb_chars=160), ""]
        + [f"* {line}" for line in fake.sentences(nb=fake.random_int(max=5))]
        + [
            "",
        ]
    )
    committer = f"{fake.name()} <{fake.ascii_email()}>"
    return CommitContext(
        sha=fake.sha1(),
        commit_datetime=fake.past_datetime(tzinfo=fake.pytimezone()),
        summary=summary,
        body=body,
        committer=committer,
        grouping=grouping,
        files=files,
    )


@pytest.mark.parametrize(
    ["commit_grouping", "rule_grouping"],
    [
        param(("foo",), "foo", id="string matches simple tuple"),
        param(
            (
                "bar",
                "foo",
            ),
            "foo",
            id="string matches in a tuple",
        ),
        param(
            (
                "foo",
                "bar",
            ),
            ("foo", "bar"),
            id="tuple matches tuple exactly",
        ),
        param(
            (
                "foo",
                "bar",
            ),
            ("foo", "bar", "*"),
            id="tuple with star matches tuple 1",
        ),
        param(
            (
                "foo",
                "bar",
            ),
            ("foo", "*"),
            id="tuple with star matches tuple 2",
        ),
    ],
)
def test_releaserule_match_grouping(commit_grouping, rule_grouping):
    """ReleaseRule should return the match_result if the commit matches."""
    rule = release_hint.ReleaseRule(match_result="success", grouping=rule_grouping)
    commit_ctx = commit_context_factory(grouping=commit_grouping)
    assert rule(commit_ctx) == "success"


@pytest.mark.parametrize(
    ["commit_grouping", "rule_grouping"],
    [
        param(("foo",), "bar", id="string not in tuple"),
        param(("foo",), ("bar",), id="tuples don't match"),
        param(
            (
                "foo",
                "bar",
            ),
            ("bar", "*"),
            id="tuple with star doesn't match tuple",
        ),
        param(("foo",), 1, id="non-string or iterable in rule fails"),
    ],
)
def test_releaserule_match_grouping_failures(commit_grouping, rule_grouping):
    """Test expected failures."""
    rule = release_hint.ReleaseRule(match_result="success", no_match_result="fail", grouping=rule_grouping)
    commit_ctx = commit_context_factory(grouping=commit_grouping)
    assert rule(commit_ctx) == "fail"


@pytest.mark.parametrize(
    ["commit_paths", "rule_path"],
    [
        param({"foo/bar.txt"}, "foo/*", id="star matches subdirectory"),
        param({"foo/bar/baz.txt"}, "foo/*", id="star matches nested subdirectory"),
        param({"foo/bar/baz/huh.txt"}, "foo/*", id="star matches really nested subdirectory"),
        param({"foo/bar/baz/huh.txt"}, "foo/**/*.txt", id="recursive match really nested file"),
    ],
)
def test_releaserule_match_path(commit_paths, rule_path):
    """ReleaseRule should return the match_result if the commit matches."""
    rule = release_hint.ReleaseRule(match_result="success", path=rule_path)
    commit_ctx = commit_context_factory(files=commit_paths)
    assert rule(commit_ctx) == "success"


@pytest.mark.parametrize(
    ["commit_paths", "rule_path"],
    [
        param({"foo/bar.txt"}, "foo/*.xml", id="mismatched file extensions"),
        param({"foo/bar/baz.txt"}, "bar/*", id="mismatched directories"),
    ],
)
def test_releaserule_match_path_failures(commit_paths, rule_path):
    """ReleaseRule should return the match_result if the commit matches."""
    rule = release_hint.ReleaseRule(match_result="success", no_match_result="failure", path=rule_path)
    commit_ctx = commit_context_factory(files=commit_paths)
    assert rule(commit_ctx) == "failure"


@pytest.mark.parametrize(
    ["commit_paths", "rule_path", "commit_grouping", "rule_grouping"],
    [
        param({"foo/bar.txt"}, "foo/*", ("new",), "new", id="star matches subdirectory"),
        param({"foo/bar/baz.txt"}, "foo/*", ("foo",), ("foo",), id="star matches nested subdirectory"),
        param(
            {"foo/bar/baz/huh.txt"},
            "foo/*",
            (
                "foo",
                "bar",
            ),
            ("foo", "bar", "*"),
            id="star matches really nested subdirectory",
        ),
        param({"foo/bar/baz/huh.txt"}, "foo/**/*.txt", ("new",), "new", id="recursive match really nested file"),
    ],
)
def test_releaserule_match_path_and_grouping(commit_paths, rule_path, commit_grouping, rule_grouping):
    """ReleaseRule should return the match_result if the commit matches."""
    rule = release_hint.ReleaseRule(match_result="success", path=rule_path)
    commit_ctx = commit_context_factory(files=commit_paths)
    assert rule(commit_ctx) == "success"


def test_releaserule_match_invalid():
    """Trying to match an invalid rule raises an error."""
    commit_ctx = commit_context_factory()
    rule = release_hint.ReleaseRule(match_result="success", no_match_result="failure")

    with pytest.raises(InvalidRuleError):
        rule(commit_ctx)


@pytest.mark.parametrize(
    ["commit_grouping", "commit_path", "expected"],
    [
        param(("New",), {"src/file.py"}, "minor", id="minor release-new"),
        param(("Updates",), {"src/file.py"}, "minor", id="minor release-updates"),
        param(("Fixes",), {"src/file.py"}, "patch", id="patch release-fixes"),
        param(("Other",), {"src/file.py"}, "patch", id="patch release-other"),
        param(("New",), {"unknown/file.py"}, "unknown", id="unknown release type"),
    ],
)
def test_ruleprocessor(commit_grouping, commit_path, expected):
    """RuleProcessor should return the best match."""
    rules = [
        {
            "match_result": "patch",
            "no_match_result": None,
            "grouping": "Other",
            "path": "src/*",
        },
        {
            "match_result": "patch",
            "no_match_result": None,
            "grouping": "Fixes",
            "path": "src/*",
        },
        {
            "match_result": "minor",
            "no_match_result": None,
            "grouping": "Updates",
            "path": "src/*",
        },
        {
            "match_result": "minor",
            "no_match_result": None,
            "grouping": "New",
            "path": "src/*",
        },
        {
            "match_result": "unknown",
            "no_match_result": None,
            "grouping": "New",
            "path": "unknown/*",
        },
    ]
    rule_processor = release_hint.RuleProcessor(rule_list=rules)
    commit = commit_context_factory(commit_grouping, commit_path)
    assert rule_processor(commit) == expected
