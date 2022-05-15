"""Commit matching functions."""
from typing import Any, Optional

import operator as op
import re

from generate_changelog.actions import register_builtin
from generate_changelog.context import CommitContext


@register_builtin
class SummaryRegexMatch:
    r"""
    Matches the commit summary using a regular expression.

    If ``pattern`` is ``None`` all commits will match.

    Example:
        In ``.changelog-config.yaml`` ::

            commit_classifiers:
            - action: SummaryRegexMatch
              category: New
              kwargs:
                pattern: (?i)^(?:new|add)[^\n]*$
    """

    def __init__(self, pattern: Optional[str] = None):
        self.pattern = re.compile(pattern) if pattern else None

    def __call__(self, commit: CommitContext) -> bool:
        """Does the commit summary match the pattern?"""
        if self.pattern is None:
            return True
        return re.search(self.pattern, commit.summary) is not None


@register_builtin
class MetadataMatch:
    """
    Evaluates an attribute in the metadata against a value using an operator.

    Examples:
        To group breaking changes::

            - action: MetadataMatch
              category: Breaking Changes
              kwargs:
                attribute: has_breaking_change
                operator: is
                value: True

        To match a specific value::

            - action: MetadataMatch
              category: Feature
              kwargs:
                attribute: commit_type
                operator: ==
                value: feat

        To match multiple values::

            - action: MetadataMatch
              category: Updates
              kwargs:
                attribute: commit_type
                operator: in
                value: ["fix", "refactor", "update"]
    """

    operator_map: dict = {
        "==": op.eq,
        "!=": op.ne,
        "<": op.lt,
        ">": op.gt,
        ">=": op.ge,
        "<=": op.le,
        "is": op.is_,
        "is not": op.is_not,
        "in": op.contains,
        "not in": lambda x, y: x not in y,
    }
    """Mapping of operator strings to functions for evaluation."""

    def __init__(self, attribute: str, operator: str, value: Any):
        """
        Set up the matcher.

        Valid operators: ``==``,  ``!=``, ``<``, ``>``, ``>=``, ``<=``, ``is``, ``is not``, ``in``, ``not in``

        Args:
            attribute: The name of the metadata key whose value will be evaluated
            operator: One of the valid operators described above
            value: The value to evaluate the against the metadata

        Raises:
            ValueError: If the operator value is not recognized
        """
        self.attribute = attribute
        if operator not in self.operator_map:
            raise ValueError(
                f"'{operator}' is not a valid operator. Must be one of {', '.join(self.operator_map.keys())}."
            )
        self.operator = self.operator_map[operator]
        self.value = value
        self.swap_operands = operator in {"in", "not in"}

    def __call__(self, commit: CommitContext) -> bool:
        """Does the commit metadata attribute meet the conditional?"""
        if self.attribute not in commit.metadata:
            return False

        attr_value = commit.metadata[self.attribute]
        if self.swap_operands:
            return self.operator(self.value, attr_value)
        return self.operator(attr_value, self.value)
