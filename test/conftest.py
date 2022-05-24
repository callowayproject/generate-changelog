"""Testing fixtures."""
from typing import Optional

import collections
import datetime
import textwrap
from collections import OrderedDict
from dataclasses import dataclass

import pytest
from faker import Faker
from git import Actor, Repo

fake = Faker()

# https://www.reddit.com/r/git/comments/nl36wl/the_top_1_commit_trailers_of_gitgit/
trailer_weighting = OrderedDict(
    {
        "acked-by ": 0.255,
        "reviewed-by": 0.227,
        "helped-by": 0.175,
        "reported-by": 0.126,
        "mentored-by": 0.05,
        "suggested-by ": 0.037,
        "cc ": 0.029,
        "noticed-by ": 0.022,
        "tested-by": 0.02,
        "improved-by": 0.012,
        "thanks-to": 0.009,
        "based-on-patch-by": 0.007,
        "contributions-by ": 0.006,
        "co-authored-by ": 0.005,
        "requested-by ": 0.004,
        "original-patch-by": 0.004,
        "inspired-by": 0.003,
        "explained-by ": 0.001,
        "found-by ": 0.001,
        "trivially-acked-by ": 0.001,
        "commit-message-by": 0.001,
        "fixes": 0.001,
        "initial-patch-by ": 0.001,
        "reported-and-tested-by ": 0.001,
        "diagnosed-by ": 0.001,
        "based-on-a-patch-by": 0.001,
    }
)


@dataclass
class FakeCommitter:
    """A fake commiter."""

    name: str
    email: str


@dataclass
class FakeCommit:
    """A fake commit object for testing."""

    hexsha: str
    committed_datetime: datetime.datetime
    committer: FakeCommitter
    summary: str
    message: str
    trailers: Optional[dict] = None


def commit_factory(
    committer_name: Optional[str] = None,
    committer_email: Optional[str] = None,
    summary: Optional[str] = None,
    body: Optional[str] = None,
    trailers: Optional[dict] = None,
):
    """Generate commits."""
    committer = FakeCommitter(name=committer_name or fake.name(), email=committer_email or fake.ascii_email())
    summary = summary or fake.sentence(nb_words=8, variable_nb_words=True)
    body = body or "\n".join(
        [summary, fake.text(max_nb_chars=160), ""]
        + [f"* {line}" for line in fake.sentences(nb=fake.random_int(max=5))]
        + [
            "",
        ]
    )
    body_list = [body]
    trailer_tokens = fake.random_elements(elements=trailer_weighting, length=fake.random_int(max=3))
    if trailers is None:
        trailers = collections.defaultdict(list)
        for token in trailer_tokens:
            trailers[token].append((fake.name(), fake.ascii_email()))

    for token, items in trailers.items():
        body_list.extend(f"{token}: {name} <{email}>" for name, email in items)

    return FakeCommit(
        hexsha=fake.sha1(),
        committed_datetime=fake.past_datetime(tzinfo=fake.pytimezone()),
        committer=committer,
        summary=summary,
        message="\n".join(body_list),
        trailers=trailers,
    )


@pytest.fixture
def bare_git_repo(tmp_path):
    """Create a temporary bare git repository."""
    return Repo.init(tmp_path / "bare-repo", bare=True)


@pytest.fixture
def default_repo(bare_git_repo):
    """Make a bunch of default commits to a temporary bare git repo."""
    idx = bare_git_repo.index
    idx.commit(
        message="new: first commit", committer=Actor("Bob", "bob@example.com"), commit_date="2022-01-01 10:00:00"
    )
    bare_git_repo.create_tag("0.0.1")
    idx.commit(
        message=textwrap.dedent(
            """
            add ``b`` with non-ascii chars éèàâ§µ and HTML chars ``&<``

            Change-Id: Ic8aaa0728a43936cd4c6e1ed590e01ba8f0fbf5b"""
        ).strip(),
        committer=Actor("Alice", "alice@example.com"),
        commit_date="2022-01-02 11:00:00",
    )
    bare_git_repo.create_tag("0.0.2")
    idx.commit(
        message="new: add file ``c``",
        committer=Actor("Charly", "charly@example.com"),
        commit_date="2022-01-03 12:00:00",
    )
    idx.commit(
        message=textwrap.dedent(
            """
            new: add file ``e``, modified ``b``

            This is a message body.

            With multi-line content:
            - one
            - two

            Bug: #42
            Change-Id: Ic8aaa0728a43936cd4c6e1ed590e01ba8f0fbf5b
            Signed-off-by: A. U. Thor <committer@example.com>
            CC: R. E. Viewer <reviewer@example.com>
            Subject: This is a fake subject spanning to several lines
              as you can see
            """
        ).strip(),
        committer=Actor("Bob", "bob@example.com"),
        commit_date="2022-01-04 13:00:00",
    )
    idx.commit(
        message="chg: modified ``b`` !minor",
        committer=Actor("Bob", "bob@example.com"),
        commit_date="2022-01-05 13:00:00",
    )
    bare_git_repo.create_tag("0.0.3")
    idx.commit(
        message=textwrap.dedent(
            """
            chg: modified ``b`` XXX

            Co-committed-By: Juliet <juliet@example.com>
            Co-committed-By: Charly <charly@example.com>
            """
        ).strip(),
        committer=Actor("Alice", "alice@example.com"),
        commit_date="2022-01-06 11:00:00",
    )

    return bare_git_repo
