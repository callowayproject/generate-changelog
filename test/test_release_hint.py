"""Tests of the release_hint module."""
from typing import Optional, Union

import pytest
from faker import Faker
from pytest import param

from generate_changelog import configuration, release_hint
from generate_changelog.context import CommitContext, GroupingContext, VersionContext
from generate_changelog.release_hint import InvalidRuleError

fake = Faker()

TEST_RULES = [
    {
        "match_result": "dev",
        "no_match_result": "no-release",
        "branch": "^((?!master|main).)*$",
    },
    {
        "match_result": "patch",
        "no_match_result": None,
        "grouping": "Other",
        "path": "src/*",
        "branch": "master|main",
    },
    {
        "match_result": "patch",
        "no_match_result": "no-release",
        "grouping": "Fixes",
        "path": "src/*",
        "branch": "master|main",
    },
    {
        "match_result": "minor",
        "no_match_result": None,
        "grouping": "Updates",
        "path": "src/*",
        "branch": "master|main",
    },
    {
        "match_result": "minor",
        "no_match_result": None,
        "grouping": "New",
        "path": "src/*",
        "branch": "master|main",
    },
    {
        "match_result": "unknown",
        "no_match_result": None,
        "grouping": "New",
        "path": "unknown/*",
        "branch": "master|main",
    },
]


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
    grouping = (grouping,) if isinstance(grouping, str) else grouping
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
    assert rule(commit_ctx, "master") == "success"


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
    assert rule(commit_ctx, "master") == "fail"


@pytest.mark.parametrize(
    ["commit_paths", "rule_path"],
    [
        param({"foo/bar.txt"}, "foo/*", id="star matches subdirectory"),
        param({"foo/bar/baz.txt"}, "foo/*", id="star matches nested subdirectory"),
        param({"foo/bar/baz/huh.txt"}, "foo/*", id="star matches really nested subdirectory"),
        param({"foo/bar/baz/huh.txt"}, "foo/**/*.txt", id="recursive match really nested file"),
    ],
)
def test_releaserule_match_path(commit_paths: set, rule_path: str):
    """ReleaseRule should return the match_result if the commit matches."""
    rule = release_hint.ReleaseRule(match_result="success", path=rule_path)
    commit_ctx = commit_context_factory(files=commit_paths)
    assert rule(commit_ctx, "master") == "success"


@pytest.mark.parametrize(
    ["commit_paths", "rule_path"],
    [
        param({"foo/bar.txt"}, "foo/*.xml", id="mismatched file extensions"),
        param({"foo/bar/baz.txt"}, "bar/*", id="mismatched directories"),
    ],
)
def test_releaserule_match_path_failures(commit_paths: set, rule_path: str):
    """ReleaseRule should return the match_result if the commit matches."""
    rule = release_hint.ReleaseRule(match_result="success", no_match_result="failure", path=rule_path)
    commit_ctx = commit_context_factory(files=commit_paths)
    assert rule(commit_ctx, "master") == "failure"


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
def test_releaserule_match_path_and_grouping(commit_paths: set, rule_path: str, commit_grouping, rule_grouping):
    """ReleaseRule should return the match_result if the commit matches."""
    rule = release_hint.ReleaseRule(match_result="success", path=rule_path, grouping=rule_grouping)
    commit_ctx = commit_context_factory(grouping=commit_grouping, files=commit_paths)
    assert rule(commit_ctx, "master") == "success"


def test_releaserule_match_path_grouping_and_branch():
    """The branch should affect the release hint."""
    commit_paths = {"foo/bar.txt"}
    rule_path = "foo/*"
    commit_grouping = ("new",)
    rule_grouping = "new"
    master_rule = release_hint.ReleaseRule(
        match_result="success", path=rule_path, grouping=rule_grouping, branch="master"
    )
    dev_rule = release_hint.ReleaseRule(match_result="success", path=rule_path, grouping=rule_grouping, branch="dev")
    commit_ctx = commit_context_factory(grouping=commit_grouping, files=commit_paths)
    assert master_rule(commit_ctx, "master") == "success"
    assert master_rule(commit_ctx, "dev") == "no-release"
    assert dev_rule(commit_ctx, "master") == "no-release"
    assert dev_rule(commit_ctx, "dev") == "success"


def test_releaserule_match_invalid():
    """Trying to match an invalid rule raises an error."""
    commit_ctx = commit_context_factory()
    rule = release_hint.ReleaseRule(match_result="success", no_match_result="failure")

    with pytest.raises(InvalidRuleError):
        rule(commit_ctx, "master")


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
def test_ruleprocessor(commit_grouping: tuple, commit_path: set, expected: str):
    """RuleProcessor should return the best match."""
    rule_processor = release_hint.RuleProcessor(rule_list=TEST_RULES)
    commit = commit_context_factory(commit_grouping, commit_path)
    assert rule_processor(commit, "master") == expected


def test_suggest_release_type_no_commits():
    """No commits in an unreleased version should suggest no-release."""
    config = configuration.get_default_config()
    config.release_hint_rules = TEST_RULES

    version_contexts = [
        VersionContext(
            label=config.unreleased_label, grouped_commits=[GroupingContext(grouping=("ignored",), commits=[])]
        )
    ]

    assert release_hint.suggest_release_type("master", version_contexts, config) == "no-release"


def test_suggest_release_type_no_unrelease():
    """No unreleased version should suggest no-release."""
    config = configuration.get_default_config()
    config.release_hint_rules = TEST_RULES

    version_contexts = [
        VersionContext(label="1.0.0", grouped_commits=[GroupingContext(grouping=("ignored",), commits=[])])
    ]

    assert release_hint.suggest_release_type("master", version_contexts, config) == "no-release"


def test_suggest_release_type_minor():
    """Minor release should win out over other types."""
    config = configuration.get_default_config()
    config.release_hint_rules = TEST_RULES

    version_contexts = [
        VersionContext(
            label=config.unreleased_label,
            grouped_commits=[
                GroupingContext(
                    grouping=("ignored",),
                    commits=[
                        commit_context_factory(("Fixes",), {"docs/file.py"}),  # "no-release"
                        commit_context_factory(("Fixes",), {"src/file.py"}),  # "patch"
                        commit_context_factory(("New",), {"src/file.py"}),  # "minor"
                    ],
                ),
            ],
        )
    ]

    assert release_hint.suggest_release_type("master", version_contexts, config) == "minor"


def test_suggest_release_type_multi_groups():
    """Multiple groupings should suggest a release."""
    config = configuration.get_default_config()
    config.release_hint_rules = TEST_RULES

    version_contexts = [
        VersionContext(
            label=config.unreleased_label,
            grouped_commits=[
                GroupingContext(
                    grouping=("ignored",), commits=[commit_context_factory(("Fixes",), {"src/file.py"})]  # "patch"
                ),
                GroupingContext(
                    grouping=("ignored", "forsure"),
                    commits=[commit_context_factory(("Fixes",), {"src/file.py"})],  # "patch"
                ),
            ],
        )
    ]

    assert release_hint.suggest_release_type("master", version_contexts, config) == "patch"


def test_suggest_release_type_all_nones():
    """If all the release types are None, return no-release."""
    config = configuration.get_default_config()
    config.release_hint_rules = TEST_RULES

    version_contexts = [
        VersionContext(
            label=config.unreleased_label,
            grouped_commits=[
                GroupingContext(
                    grouping=("ignored",),
                    commits=[
                        commit_context_factory(("Fixes",), {"docs/file.py"}),  # "no-release"
                        commit_context_factory(("Fixes",), {"foo/file.py"}),  # "no-release"
                        commit_context_factory(("New",), {"bar/file.py"}),  # "no-release"
                    ],
                ),
            ],
        )
    ]

    assert release_hint.suggest_release_type("master", version_contexts, config) == "no-release"
