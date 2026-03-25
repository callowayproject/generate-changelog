"""Tests for generate_changelog.actions.text_processing."""

import pytest
from pytest import param

from generate_changelog.actions.text_processing import capitalize


@pytest.mark.parametrize(
    ["msg", "expected"],
    (
        param("", "", id="empty-string"),
        param("hello", "Hello", id="lowercase"),
        param("Hello", "Hello", id="already-capitalized"),
        param(" hello", " hello", id="leading-space"),
        param("hELLO", "HELLO", id="mixed-case"),
    ),
)
def test_capitalize(msg, expected):
    """capitalize should uppercase the first character without crashing on empty strings."""
    assert capitalize(msg) == expected
