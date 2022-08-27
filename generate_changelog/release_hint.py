"""Methods for generating a release hint."""
from typing import List, Optional, Union

import fnmatch
import re

from generate_changelog.configuration import RELEASE_TYPE_ORDER, Configuration
from generate_changelog.context import CommitContext, VersionContext


class InvalidRuleError(Exception):
    """The evaluated rule is invalid."""

    pass


class ReleaseRule:
    """A commit evaluation rule for hinting at the level of change."""

    def __init__(
        self,
        match_result: Optional[str],
        no_match_result: Optional[str] = "no-release",
        grouping: Union[str, tuple, list, None] = None,
        path: Optional[str] = None,
        branch: Optional[str] = None,
    ):
        """
        Initialize the callable rule.

        Args:
            match_result: Release type if a commit context matches the rule.
            no_match_result: Release type if a commit context doesn't match the rule.
            grouping: The partial or exact grouping of the commit context
            path: A globbing pattern that matches against files included in the commit
            branch: A regular expression pattern to match against the branch
        """
        self.match_result = match_result
        self.no_match_result = no_match_result
        self.grouping = grouping if grouping != "*" else None
        self.path = path if path != "*" else None
        self.branch = branch or None
        self.is_valid = any([self.path, self.grouping, self.branch])

    def matches_grouping(self, commit: CommitContext) -> bool:
        """
        Does the commit grouping match the rule?

        - If ``self.grouping`` is a string, it checks if the string is in the commit's ``grouping``.

        - If ``self.grouping`` is a list or tuple of strings, it must match the commit's ``grouping``.

        - If ``self.grouping`` is a list or tuple of strings and the last item in the list is a "*",
          it must match the beginning of the commit's ``grouping``.

        - If ``self.grouping`` is None, it will return a match

        Args:
            commit: The commit context whose grouping should match

        Returns:
            ``True`` if the grouping matches
        """
        if self.grouping is None:
            return True
        elif isinstance(self.grouping, str):
            return self.grouping in commit.grouping
        elif not isinstance(self.grouping, (list, tuple)):
            return False

        if "*" not in self.grouping:
            return tuple(self.grouping) == commit.grouping

        split_index = self.grouping.index("*")
        prefix = self.grouping[:split_index]
        return prefix == commit.grouping[: len(prefix)]

    def matches_path(self, commit: CommitContext) -> bool:
        """
        Do any of the paths in the commit match the rule?

        Args:
            commit:  The commit context whose files should match

        Returns:
            ``True`` if any file in the commit context matches the pattern or if ``self.path`` is ``None``
        """
        if not self.path:
            return True

        re_pattern = fnmatch.translate(self.path)
        return any(re.match(re_pattern, p) for p in commit.files)

    def matches_branch(self, current_branch: str) -> bool:
        """
        Does the current branch match the rule?

        Args:
            current_branch: The name of the current branch

        Returns:
            ``True`` if the current branch matches or if ``self.branch`` is ``None``
        """
        return bool(re.match(self.branch, current_branch)) if self.branch else True

    def __call__(self, commit: CommitContext, current_branch: str) -> Optional[str]:
        """Evaluate the commit using this rule."""
        if not self.is_valid:
            raise InvalidRuleError()

        matches_grouping = self.matches_grouping(commit)
        matches_path = self.matches_path(commit)
        matches_branch = self.matches_branch(current_branch)
        return self.match_result if all([matches_grouping, matches_path, matches_branch]) else self.no_match_result


class RuleProcessor:
    """Process a commit through all the rules and return the suggestion."""

    def __init__(self, rule_list: List[dict]):
        """
        Set up the :class:`RuleProcessor`.

        Args:
            rule_list: The list of dictionaries representing release rules
        """
        self.rules = [ReleaseRule(**kwargs) for kwargs in rule_list]

    def __call__(self, commit: CommitContext, current_branch: str) -> Optional[str]:
        """
        Return the result of applying all the rules to a commit.

        Args:
            commit: The commit context to apply rules to
            current_branch: The name of the current branch

        Returns:
            The release hint
        """
        suggestions = {rule(commit, current_branch) for rule in self.rules}
        unknown_suggestions = suggestions - set(RELEASE_TYPE_ORDER)
        if unknown_suggestions:
            return unknown_suggestions.pop()  # Return a random value from the unknowns

        sorted_suggestions = sorted(suggestions, key=lambda s: RELEASE_TYPE_ORDER.index(s))
        return sorted_suggestions[-1]


def suggest_release_type(current_branch: str, version_contexts: List[VersionContext], config: Configuration) -> str:
    """
    Suggest the type of release based on the unreleased commits.

    Args:
        current_branch: The name of the current branch
        version_contexts: The processed commits to process
        config: The current configuration

    Returns:
        The type of release based on the rules, or ``no-release``
    """
    rule_processor = RuleProcessor(rule_list=config.release_hint_rules)

    # If the latest release is not "unreleased", there is no need for a release
    if version_contexts[0].label != config.unreleased_label:
        return "no-release"

    suggestions = set()
    for commit_group in version_contexts[0].grouped_commits:
        suggestions |= {rule_processor(commit, current_branch) for commit in commit_group.commits}

    if not suggestions:
        return "no-release"

    sorted_suggestions = sorted(suggestions, key=lambda s: RELEASE_TYPE_ORDER.index(s))
    return sorted_suggestions[-1] or "no-release"
