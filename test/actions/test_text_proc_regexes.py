"""Regular Expression command testing."""
import re

import pytest
from pytest import param

from generate_changelog.actions import text_processing


def test_regex_flags():
    """The flags properety should properly OR the RegexFlags."""
    # No flags
    re_cmd = text_processing.RegExCommand("")
    assert re_cmd.flags == 0

    # Two flags
    re_cmd1 = text_processing.RegExCommand("", ignorecase_flag=True, multiline_flag=True)
    assert re_cmd1.flags == re.IGNORECASE | re.MULTILINE


gfrm_text_1 = """Heading

1.0 1234-23-44
0.4.5
"""


@pytest.mark.parametrize(
    ["text", "pattern", "named_subgroup", "default", "expected"],
    (
        param(gfrm_text_1, r"(?P<rev>\d+\.\d+(?:\.\d+)?)", "rev", "", "1.0", id="simple-version"),
        param(gfrm_text_1, r"(?P<rev>\d+\.\d+\.\d+)", "rev", "", "0.4.5", id="full-version"),
        param(gfrm_text_1, r"(?P<rev>\d+\.\d+(?:\.\d+)?)", "foo", "", "1.0", id="missing-named-subgroup"),
        param(gfrm_text_1, r"(?P<rev>idontexist)", "rev", "default", "default", id="no-match-yields-default"),
    ),
)
def test_get_first_regex_match(text, pattern, named_subgroup, default, expected):
    """Should find the first item in the string."""
    regex_cmd = text_processing.FirstRegExMatch(pattern=pattern, named_subgroup=named_subgroup, default_value=default)
    assert regex_cmd(text) == expected


@pytest.mark.parametrize(
    ["text", "pattern", "replacement", "expected"],
    (
        param("Baked Beans And Spam", r"(?i)\sAND\s", " & ", "Baked Beans & Spam", id="replacement"),
        param("Baked Beans And Spam", r"\sAND\s", " & ", "Baked Beans And Spam", id="no-match"),
        param("Spam And Spam", r"(Spam) And \1", r"\1 & \1", "Spam & Spam", id="backreferences"),
    ),
)
def test_regex_sub(text, pattern, replacement, expected):
    """The replacement is substituted for the matched pattern."""
    regex_cmd = text_processing.RegexSub(pattern=pattern, replacement=replacement)
    assert regex_cmd(text) == expected
