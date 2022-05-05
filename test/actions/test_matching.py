"""Testing the matching actions."""
import datetime

import pytest
from pytest import param

from generate_changelog.actions import matching
from generate_changelog.context import CommitContext


@pytest.mark.parametrize(
    ["pattern", "message", "expected"],
    [
        param(r"(?i)^(?:new|add)[^\n]*$", "Newly added something", True, id="Positive Test"),
        param(r"(?i)^(?:new|add)[^\n]*$", "Changed something", False, id="Negative Test"),
        param(None, "Changed something", True, id="None matches all"),
    ],
)
def test_match_summary_regex_match(pattern, message, expected):
    matcher = matching.SummaryRegexMatch(pattern=pattern)
    context = CommitContext(
        sha="1234567890", commit_datetime=datetime.datetime.now(), summary=message, body="", committer="foo"
    )
    assert matcher(context) is expected
