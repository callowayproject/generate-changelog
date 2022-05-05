"""Test the metadata collectors."""
import pytest
from pytest import param

from generate_changelog.actions import metadata

sample_msg_1 = """
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


def test_parse_trailers():
    """Parse trailers should parse all trailers out of the message and store the data."""
    metadata_collector = metadata.MetadataCollector()
    parse_trailers = metadata.ParseTrailers(commit_metadata=metadata_collector)
    msg = parse_trailers(sample_msg_1)
    assert msg == sample_msg_1[:63]

    md = metadata_collector.metadata
    assert "trailers" in md
    assert len(md["trailers"]) == 5
    trailers = md["trailers"]
    assert trailers["bug"] == ["#42"]
    assert trailers["change-id"] == ["Ic8aaa0728a43936cd4c6e1ed590e01ba8f0fbf5b"]
    assert trailers["signed-off-by"] == ["A. U. Thor <committer@example.com>"]
    assert trailers["cc"] == ["R. E. Viewer <reviewer@example.com>"]
    assert trailers["subject"] == ["This is a fake subject spanning to several lines\nas you can see"]


def test_metadata_collector():
    """Metadata collector should collect metadata."""
    mdc = metadata.MetadataCollector()
    mdc(foo="bar")
    assert mdc.metadata == {"foo": "bar"}

    mdc = metadata.MetadataCollector({"foo": ["bar"]})
    assert mdc.metadata == {"foo": ["bar"]}

    mdc(foo=["bar"])
    assert mdc.metadata == {"foo": ["bar"]}

    mdc(foo=["baz"])
    assert set(mdc.metadata["foo"]) == {"baz", "bar"}


def test_parse_issue():
    """Parsing a pattern puts the match in the commit metadata issue key."""

    mdc = metadata.MetadataCollector()
    action = metadata.ParseIssue(mdc, r"issue#(\d+)")
    action("This messsage references issue#123 and issue#234")
    assert mdc.metadata == {"issue": ["123", "234"]}


def test_parse_issue_no_issue():
    """Parsing a pattern without an issue reference does nothing."""

    mdc = metadata.MetadataCollector()
    action = metadata.ParseIssue(mdc, r"issue#(\d+)")
    action("This messsage references contains no references")
    assert "issue" not in mdc.metadata


def test_parse_github_issue():
    """Github issue references are parsed into commit metadata."""

    mdc = metadata.MetadataCollector()
    action = metadata.ParseGitHubIssue(mdc)
    action("This messsage references #123 and #234")
    assert mdc.metadata == {"issue": ["123", "234"]}


def test_parse_jira_issue():
    """Jira issue references are parsed into commit metadata."""

    mdc = metadata.MetadataCollector()
    action = metadata.ParseJiraIssue(mdc)
    action("This messsage references FOO-123 and BAR-234")
    assert mdc.metadata == {"issue": ["FOO-123", "BAR-234"]}


def test_parse_azure_board_issue():
    """Azure board issue references are parsed into commit metadata."""

    mdc = metadata.MetadataCollector()
    action = metadata.ParseAzureBoardIssue(mdc)
    action("This messsage references AB#123 and AB#234")
    assert mdc.metadata == {"issue": ["123", "234"]}


brk_chg_msg_with_other_footers = """
This is a message body.

Bug: #42
Change-Id: Ic8aaa0728a43936cd4c6e1ed590e01ba8f0fbf5b
Signed-off-by: A. U. Thor <committer@example.com>
BREAKING_CHANGE: This is a breaking change.
CC: R. E. Viewer <reviewer@example.com>
Subject: This is a fake subject spanning to several lines
  as you can see
"""

brk_chg_msg_with_other_footers_expected = """
This is a message body.

Bug: #42
Change-Id: Ic8aaa0728a43936cd4c6e1ed590e01ba8f0fbf5b
Signed-off-by: A. U. Thor <committer@example.com>
CC: R. E. Viewer <reviewer@example.com>
Subject: This is a fake subject spanning to several lines
  as you can see
"""


def test_parse_breaking_change_footer_with_other_footers():
    """Test parsing out the breaking change footer."""
    mdc = metadata.MetadataCollector()
    action = metadata.ParseBreakingChangeFooter(mdc)
    msg = action(brk_chg_msg_with_other_footers)
    assert mdc.metadata == {"has_breaking_change": True, "breaking_changes": "This is a breaking change."}
    assert msg == brk_chg_msg_with_other_footers_expected


multiple_brk_chg_msg_with_other_footers = """
This is a message body.

Bug: #42
Change-Id: Ic8aaa0728a43936cd4c6e1ed590e01ba8f0fbf5b
Signed-off-by: A. U. Thor <committer@example.com>
BREAKING_CHANGE: This is a breaking change.
CC: R. E. Viewer <reviewer@example.com>
BREAKING_CHANGE: This is another breaking change.
Subject: This is a fake subject spanning to several lines
  as you can see
"""


def test_parse_breaking_change_footer_with_multiple():
    """Test parsing out the breaking change footer."""
    mdc = metadata.MetadataCollector()
    action = metadata.ParseBreakingChangeFooter(mdc)
    msg = action(multiple_brk_chg_msg_with_other_footers)
    assert mdc.metadata == {
        "has_breaking_change": True,
        "breaking_changes": "This is a breaking change. This is another breaking change.",
    }
    assert msg == brk_chg_msg_with_other_footers_expected


@pytest.mark.parametrize(
    ["message", "expected_metadata", "desc"],
    [
        param(
            "feat: Message with only commit type",
            {"commit_type": "feat", "scope": []},
            "Message with only commit type",
        ),
        param(
            "feat!: Message with commit type and a breaking change",
            {"commit_type": "feat", "scope": [], "has_breaking_change": True},
            "Message with commit type and a breaking change",
        ),
        param(
            "deploy(ingress): Message with commit type and scope",
            {"commit_type": "deploy", "scope": ["ingress"]},
            "Message with commit type and scope",
        ),
        param(
            "fix(rule,api): Message with commit type and multiple scopes",
            {"commit_type": "fix", "scope": ["rule", "api"]},
            "Message with commit type and multiple scopes",
        ),
        param(
            "fix(rule/api)!: Message with commit type, multiple scopes and breaking change",
            {"commit_type": "fix", "scope": ["rule", "api"], "has_breaking_change": True},
            "Message with commit type, multiple scopes and breaking change",
        ),
        param(
            "Message that doesn't match",
            {},
            "Message that doesn't match",
        ),
    ],
)
def test_parse_conventional_commit(message, expected_metadata, desc):
    """Parse subject lines and correctly parse it."""
    mdc = metadata.MetadataCollector()
    action = metadata.ParseConventionalCommit(mdc)
    msg = action(message)
    assert mdc.metadata == expected_metadata
    assert msg == desc
