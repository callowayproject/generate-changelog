"""Tests of temmplating functions."""
import datetime
import textwrap
from pathlib import Path
from test import conftest

import pytest
from faker import Faker
from pytest import param

from generate_changelog import configuration, templating
from generate_changelog.configuration import DEFAULT_SECTION_PATTERNS, get_config

FIXTURES_DIR = Path(__file__).parent / "fixtures"
fake = Faker()


@pytest.mark.parametrize(
    ["string", "expected"],
    (
        param("Newly added something", "New"),
        param("added something new", "New"),
        param("changed something new", "Updates"),
        param("Updates something old", "Updates"),
        param("renamed something I didn't like.", "Updates"),
        param("Removed something old", "Updates"),
        param("deletes something old", "Updates"),
        param("improved something old", "Updates"),
        param("refactored something old", "Updates"),
        param("fixed an error or something", "Fixes"),
        param("I don't know what this does", "Other"),
    ),
)
def test_first_matching(string, expected):
    """The first matching function should properly categorize a string."""
    assert templating.first_matching(DEFAULT_SECTION_PATTERNS, string) == expected


def test_commit_context():
    """CommitContexts should properly parse things."""
    commit = conftest.commit_factory()
    context = templating.CommitContext(
        sha=commit.hexsha,
        commit_datetime=commit.committed_datetime,
        committer=f"{commit.committer.name} <{commit.committer.email}>",
        subject=commit.summary,
        body="\n".join(commit.message.splitlines()[1:]),
    )
    assert commit.hexsha[:7] == context.short_sha
    assert commit.committer.name in context.author_names
    # Calling it again should trigger the caching lines
    assert commit.committer.name in context.author_names


def test_commit_with_no_email():
    """A trailer without an email should still get parsed."""
    commit = conftest.commit_factory()
    name_only = fake.name()
    context = templating.CommitContext(
        sha=commit.hexsha,
        commit_datetime=commit.committed_datetime,
        committer=f"{commit.committer.name} <{commit.committer.email}>",
        subject=commit.summary,
        body="\n".join(commit.message.splitlines()[1:]),
        metadata={"trailers": {"co-authored-by": [name_only]}},
    )
    assert name_only in context.author_names
    assert {"name": name_only, "email": ""} in context.authors


def test_get_context_from_tags(default_repo):
    """Get context from tags should return gits correctly filtered."""
    context = templating.get_context_from_tags(default_repo, get_config())
    assert len(context) == 4

    v = context[0]
    assert v.label == get_config().unreleased_label
    assert v.date_time.date() == datetime.date(2022, 1, 6)
    assert len(v.sections) == 1
    assert v.sections[0].label == "Updates"
    assert len(v.sections[0].commits) == 1
    assert v.sections[0].commits[0].metadata["trailers"]["co-committed-by"] == [
        "Juliet <juliet@example.com>",
        "Charly <charly@example.com>",
    ]

    v = context[1]
    assert v.label == "0.0.3"
    assert v.date_time.date() == datetime.date(2022, 1, 5)
    assert len(v.sections) == 1
    assert v.sections[0].label == "New"
    assert len(v.sections[0].commits) == 2
    assert len(v.sections[0].commits[0].metadata["trailers"]) == 5
    assert len(v.sections[0].commits[1].metadata["trailers"]) == 0


def test_render(default_repo, capsys):
    """Render should render the changelog."""
    config = configuration.get_default_config()
    output = templating.render(default_repo, config, None)
    expected = (FIXTURES_DIR / "rendered_default_repo.md").read_text()
    assert output.strip() == expected.strip()


def test_render_from_tag(default_repo, capsys):
    """Render should render the changelog."""
    config = configuration.get_default_config()
    output = templating.render(default_repo, config, "0.0.3")
    expected = textwrap.dedent(
        """
        # Changelog
        
        ## Unreleased (2022-01-06)
        
        ### Updates
        
        - Chg: modified ``b`` XXX. [Alice](alice@example.com), [Charly](charly@example.com), [Juliet](juliet@example.com)    

    """
    )
    assert output.strip() == expected.strip()
