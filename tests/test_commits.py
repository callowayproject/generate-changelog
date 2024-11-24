import datetime
from tests.conftest import commit_factory

import pytest
from faker import Faker
from pytest import param

import generate_changelog.commits
from generate_changelog.configuration import DEFAULT_COMMIT_CLASSIFIERS, get_default_config
from generate_changelog.context import CommitContext

fake = Faker()


@pytest.mark.parametrize(
    ["string", "expected"],
    (
        param(commit_factory(summary="Newly added something"), "New"),
        param(commit_factory(summary="added something new"), "New"),
        param(commit_factory(summary="changed something new"), "Updates"),
        param(commit_factory(summary="Updates something old"), "Updates"),
        param(commit_factory(summary="renamed something I didn't like."), "Updates"),
        param(commit_factory(summary="Removed something old"), "Updates"),
        param(commit_factory(summary="deletes something old"), "Updates"),
        param(commit_factory(summary="improved something old"), "Updates"),
        param(commit_factory(summary="refactored something old"), "Updates"),
        param(commit_factory(summary="fixed an error or something"), "Fixes"),
        param(commit_factory(summary="I don't know what this does"), "Other"),
    ),
)
def test_first_matching(string, expected):
    """The first matching function should properly categorize a string."""
    assert generate_changelog.commits.first_matching(DEFAULT_COMMIT_CLASSIFIERS, string) == expected


def test_commit_context():
    """CommitContexts should properly parse things."""
    commit = commit_factory()
    context = CommitContext(
        sha=commit.hexsha,
        commit_datetime=commit.committed_datetime,
        committer=f"{commit.committer.name} <{commit.committer.email}>",
        summary=commit.summary,
        grouping=("a", "b"),
        body="\n".join(commit.message.splitlines()[1:]),
    )
    assert commit.hexsha[:7] == context.short_sha
    assert commit.committer.name in context.author_names
    # Calling it again should trigger the caching lines
    assert commit.committer.name in context.author_names


def test_commit_with_no_email():
    """A trailer without an email should still get parsed."""
    commit = commit_factory()
    name_only = fake.name()
    context = CommitContext(
        sha=commit.hexsha,
        commit_datetime=commit.committed_datetime,
        committer=f"{commit.committer.name} <{commit.committer.email}>",
        summary=commit.summary,
        grouping=(None,),
        body="\n".join(commit.message.splitlines()[1:]),
        metadata={"trailers": {"co-authored-by": [name_only]}},
    )
    assert name_only in context.author_names
    assert {"name": name_only, "email": ""} in context.authors


def test_get_context_from_tags(default_repo):
    """Get context from tags should return commits correctly filtered."""
    config = get_default_config()
    context = generate_changelog.commits.get_context_from_tags(default_repo, config)
    assert len(context) == 4
    v = context[0]
    assert v.label == config.unreleased_label
    assert v.date_time.date() == datetime.date(2022, 1, 6)
    assert len(v.grouped_commits) == 1
    assert v.grouped_commits[0].grouping == ("Updates",)
    assert len(v.grouped_commits[0].commits) == 1
    assert v.grouped_commits[0].commits[0].metadata["trailers"]["co-committed-by"] == [
        "Juliet <juliet@example.com>",
        "Charly <charly@example.com>",
    ]

    v = context[1]
    assert v.label == "0.0.3"
    assert v.previous_tag == "0.0.2"
    assert v.date_time.date() == datetime.date(2022, 1, 5)
    assert len(v.grouped_commits) == 1
    assert v.grouped_commits[0].grouping == ("New",)
    assert len(v.grouped_commits[0].commits) == 2
    assert len(v.grouped_commits[0].commits[0].metadata["trailers"]) == 5
    assert len(v.grouped_commits[0].commits[1].metadata["trailers"]) == 0
