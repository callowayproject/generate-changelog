"""Tests for the text processing module."""
import re

import pytest
from pytest import param

from generate_changelog.actions import text_processing


@pytest.mark.parametrize(
    ["text", "default", "expected"],
    (
        param("This has text", "default", "This has text", id="text-exists"),
        param("", "default", "default", id="empty-text"),
        param(None, "default", "default", id="None"),
        param("", lambda: "default", "default", id="callable-default"),
        param(lambda: "This has text", "default", "This has text", id="callable-text"),
    ),
)
def test_set_default(text, default, expected):
    """SetDefault should return a default value when missing a value."""
    set_default = text_processing.SetDefault(default)
    assert set_default(text) == expected


@pytest.mark.parametrize(
    ["text", "prefix", "expected"],
    (
        param("This has text", "prefix", "prefixThis has text", id="normal"),
        param("", "prefix", "prefix", id="empty-text"),
        param(None, "prefix", "prefix", id="None"),
        param("This has text", lambda: "prefix", "prefixThis has text", id="callable-prefix"),
        param(lambda: "This has text", "prefix", "prefixThis has text", id="callable-text"),
    ),
)
def test_prefix_string(text, prefix, expected):
    """PrefixString should return the value with the prefix in front."""
    prefix_string = text_processing.PrefixString(prefix)
    assert prefix_string(text) == expected


@pytest.mark.parametrize(
    ["text", "append", "expected"],
    (
        param("This has text", "append", "This has textappend", id="normal"),
        param("", "append", "append", id="empty-text"),
        param(None, "append", "append", id="None"),
        param("This has text", lambda: "append", "This has textappend", id="callable-append"),
        param(lambda: "This has text", "append", "This has textappend", id="callable-text"),
    ),
)
def test_append_string(text, append, expected):
    """AppendString should return the value with the postfix behind."""
    append_string = text_processing.AppendString(append)
    assert append_string(text) == expected


@pytest.mark.parametrize(
    ["text", "chars", "expected"],
    (
        param("   This has text   ", " ", "This has text", id="normal"),
        param("", " ", "", id="empty-text"),
        param(None, " ", "", id="None"),
        param("   This has text   ", lambda: " ", "This has text", id="callable-chars"),
        param(lambda: "    This has text   ", " ", "This has text", id="callable-text"),
    ),
)
def test_strip(text, chars, expected):
    """Strip should return the value leading and trailing chars removed."""
    strip = text_processing.Strip(chars)
    assert strip(text) == expected


prefix_lines = "This is first line.\nThis is second line\n"
prefix_lines2 = "This is first line.\n\nThis is second line\n"
prefix_lines3 = "This is first line.\nThis is second line"


@pytest.mark.parametrize(
    ["text", "prefix", "first_line", "expected"],
    (
        param("This has text", "prefix", None, "prefixThis has text\n", id="one-line-no-first"),
        param("This has text", "prefix", "first", "firstThis has text\n", id="one-line-w-first"),
        param("", "prefix", None, "", id="empty-text-no-first"),
        param("", "prefix", "first", "", id="empty-text-w-first"),
        param(None, "prefix", None, "", id="None-no-first"),
        param(None, "prefix", "first", "", id="None-w-first"),
        param("This has text", lambda: "prefix", None, "prefixThis has text\n", id="callable-prefix-no-first"),
        param("This has text", lambda: "prefix", "first", "firstThis has text\n", id="callable-prefix-w-first"),
        param(lambda: "This has text", "prefix", None, "prefixThis has text\n", id="callable-text-no-first"),
        param("line1\nline2", "  ", None, "  line1\n  line2\n", id="multiline-no-first"),
        param("line1\nline2", "  ", "- ", "- line1\n  line2\n", id="multiline-w-first"),
        param(prefix_lines, "| ", None, "| This is first line.\n| This is second line\n", id="pipe-space"),
        param(prefix_lines, "  ", "- ", "- This is first line.\n  This is second line\n", id="first-line"),
        param(prefix_lines2, "  ", "- ", "- This is first line.\n\n  This is second line\n", id="blank-line"),
        param(prefix_lines, "| ", None, "| This is first line.\n| This is second line\n", id="no-trailing-newline"),
    ),
)
def test_prefix_lines(text, prefix, first_line, expected):
    """PrefixLines should return the lines with the prefix in front."""
    prefix_string = text_processing.PrefixLines(prefix, first_line)
    assert prefix_string(text) == expected


def test_paragraph_wrap():
    """Paragraphs should wrap at a specific line length."""
    p = (
        "Nulla esse veniam deserunt magna sed veniam ea excepteur dolore eu mollit dolore est proident sed fugiat "
        "velit. Duis consequat fugiat dolore quis fugiat deserunt sit consequat quis culpa in nisi enim reprehenderit "
        "dolor. Enim do anim est do ut veniam aliquip pariatur dolore proident laboris mollit ea. Non deserunt magna "
        "aute sed commodo anim eu reprehenderit consequat irure officia in minim laborum proident voluptate laboris "
        "velit fugiat. Culpa deserunt sint dolore reprehenderit labore dolore velit sint velit sed quis sed qui "
        "labore. Irure tempor aliquip sed enim est nulla deserunt officia consectetur consequat.\n\n"
        "Anim quis tempor est sint dolor qui reprehenderit eiusmod tempor consectetur consequat. Nulla proident culpa "
        "officia laborum excepteur est eu exercitation officia in sunt sint proident sed adipiscing occaecat nostrud "
        "officia. Excepteur dolor deserunt pariatur velit aute lorem eu minim elit lorem sunt qui. Esse proident "
        "tempor est nostrud elit deserunt deserunt consequat amet fugiat cupidatat id cupidatat do in culpa cillum "
        "irure.\n\n\n"
        "Do occaecat proident sint qui sunt in consequat enim non deserunt aute aliqua nulla exercitation cupidatat "
        "id. Nostrud ea non sint adipiscing culpa tempor commodo proident ullamco laborum occaecat consequat velitad. "
        "Dolore labore ullamco consequat ea officia commodo excepteur duis nostrud commodo eiusmod et incididunt sit "
        "duis sit."
        ""
    )
    paragraph_wrap = text_processing.WrapParagraphs(r"\n\n+", "\n", 90)
    result = paragraph_wrap(p)
    assert max(len(x) for x in result.splitlines()) <= 90
    assert re.search(r"\n\n+", result) is None

    paragraph_wrap = text_processing.WrapParagraphs(r"\n\n+", "\n\n", 45)
    result = paragraph_wrap(p)
    assert max(len(x) for x in result.splitlines()) <= 45
    assert re.search(r"\n\n\n", result) is None


def test_capitalize():
    """The first character of a string should be capitalized."""
    assert text_processing.capitalize("i am a test") == "I am a test"
    assert text_processing.capitalize("[i] am a test") == "[i] am a test"
    assert text_processing.capitalize("i AM a Test") == "I AM a Test"
