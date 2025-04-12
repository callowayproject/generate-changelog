"""Methods for generating a release hint."""

import copy
import fnmatch
import re
from collections import defaultdict
from dataclasses import dataclass
from itertools import groupby
from operator import attrgetter
from pathlib import Path
from typing import Iterable, List, Optional, Sequence, Set, Union

from rich.box import SIMPLE
from rich.console import Console, Group, RenderableType, group
from rich.padding import Padding
from rich.table import Table
from rich.text import Text

from generate_changelog.configuration import RELEASE_TYPE_ORDER, Configuration
from generate_changelog.context import CommitContext, VersionContext
from generate_changelog.indented_logger import get_indented_logger

logger = get_indented_logger(__name__)


class InvalidRuleError(Exception):
    """The evaluated rule is invalid."""

    pass


@dataclass
class ReleaseRuleResult:
    """The result of evaluating a release rule."""

    rule_id: int
    commit: str
    matches_grouping: bool
    matches_path: bool
    matches_branch: bool
    result: str

    @property
    def matches_all(self) -> bool:
        """All the commit criteria were met."""
        return all([self.matches_grouping, self.matches_path, self.matches_branch])

    def __str__(self) -> str:
        return self.result or ""


class ReleaseRule:
    """
    A commit evaluation rule for hinting at the level of change.

    Args:
        id_: The id of this rule. Used for debugging.
        match_result: Release type if a commit context matches the rule.
        no_match_result: Release type if a commit context doesn't match the rule.
        grouping: The partial or exact grouping of the commit context
        path: A globbing pattern that matches against files included in the commit
        branch: A regular expression pattern to match against the branch
    """

    def __init__(
        self,
        id_: int,
        match_result: Optional[str],
        no_match_result: Optional[str] = "no-release",
        grouping: Union[str, tuple, list, None] = None,
        path: Optional[Union[str, Sequence[str]]] = None,
        branch: Optional[str] = None,
    ):
        self.id = id_
        self.match_result = match_result
        self.no_match_result = no_match_result or "no-release"
        self.grouping = grouping if grouping != "*" else None
        normalized_path = path if path != "*" else None
        if isinstance(normalized_path, str):
            self.path: Union[str, Sequence[str]] = [normalized_path]
        else:
            self.path = normalized_path or []
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
            commit: The commit context whose files should match

        Returns:
            `True` if any file in the commit context matches the pattern or if ``self.path`` is ``None``
        """
        if not self.path:
            return True

        results = []
        for path in self.path:
            re_pattern = fnmatch.translate(path)
            results.append(any(re.match(re_pattern, p) for p in commit.files))
        return any(results)

    def matches_branch(self, current_branch: str) -> bool:
        """
        Does the current branch match the rule?

        Args:
            current_branch: The name of the current branch

        Returns:
            ``True`` if the current branch matches or if ``self.branch`` is ``None``
        """
        return bool(re.match(self.branch, current_branch)) if self.branch else True

    def __call__(self, commit: CommitContext, current_branch: str) -> ReleaseRuleResult:
        """Evaluate the commit using this rule."""
        if not self.is_valid:
            raise InvalidRuleError()

        matches_grouping = self.matches_grouping(commit)
        matches_path = self.matches_path(commit)
        matches_branch = self.matches_branch(current_branch)
        matches_all = all([matches_grouping, matches_path, matches_branch])
        result = self.match_result if matches_all else self.no_match_result
        return ReleaseRuleResult(
            rule_id=self.id,
            commit=commit.sha[:7],
            matches_grouping=matches_grouping,
            matches_path=matches_path,
            matches_branch=matches_branch,
            result=result,
        )


class RuleProcessor:
    """
    Process a commit through all the rules and return the suggestion.

    Args:
        rule_list: The list of dictionaries representing release rules
    """

    def __init__(self, rule_list: List[dict]):
        self.rules = [ReleaseRule(id_=idx, **kwargs) for idx, kwargs in enumerate(rule_list)]
        self.results: List[ReleaseRuleResult] = []

    def __call__(self, commit: CommitContext, current_branch: str) -> Optional[str]:
        """
        Return the result of applying all the rules to a commit.

        Args:
            commit: The commit context to apply rules to
            current_branch: The name of the current branch

        Returns:
            The release hint
        """
        self.results = [rule(commit, current_branch) for rule in self.rules]
        suggestions: Set[str] = {str(result.result) for result in self.results}
        if unknown_suggestions := suggestions - set(RELEASE_TYPE_ORDER):
            return unknown_suggestions.pop()  # Return a random value from the unknowns

        sorted_suggestions = sorted(suggestions, key=lambda s: RELEASE_TYPE_ORDER.index(s))
        return sorted_suggestions[-1]

    def rule_string(self) -> str:
        """Return a string representation of the rules."""
        output: List[str] = []
        for rule in self.rules:
            output.extend(
                (
                    f"Rule: {rule.id}",
                    f"  Grouping: {rule.grouping}",
                    f"  Path: {rule.path}",
                    f"  Branch: {rule.branch}",
                    f"  Match (no-match) Result: {rule.match_result} ({rule.no_match_result})",
                )
            )
        return "\n".join(output)


def suggest_release_type(current_branch: str, version_contexts: List[VersionContext], config: Configuration) -> str:
    """
    Suggest the type of release based on the unreleased commits.

    Args:
        current_branch: The name of the current branch
        version_contexts: The processed commits to process
        config: The current configuration

    Returns:
        The type of release based on the rules, or `no-release`
    """
    logger.info("Processing commits to suggest release type...")
    logger.indent()

    rule_processor = RuleProcessor(rule_list=config.release_hint_rules)
    report_parts = [
        Text(f"Current branch: {current_branch}"),
        rule_processor.rule_string(),
    ]

    # If the latest release is not "unreleased", there is no need for a release
    if version_contexts[0].label != config.unreleased_label:
        logger.info(f"The latest release is {version_contexts[0].label}. No release is suggested.")
        logger.dedent()
        return "no-release"

    suggestions = set()
    results = defaultdict(list)
    commit_results = {}
    for commit_group in version_contexts[0].grouped_commits:
        for commit in commit_group.commits:
            new_suggestions = rule_processor(commit, current_branch)
            suggestions.add(new_suggestions)
            grouping_str = "Grouping: " + " ".join(commit_group.grouping)
            commit_results[commit.sha] = new_suggestions
            results[grouping_str].extend(copy.deepcopy(rule_processor.results))

    report_parts.append(print_table(results, commit_results))

    if not suggestions:
        logger.info("No suggestions found. No release is suggested.")
        logger.dedent()
        return "no-release"

    sorted_suggestions = sorted(suggestions, key=lambda s: RELEASE_TYPE_ORDER.index(s))
    result = sorted_suggestions[-1] or "no-release"

    report_parts.append(Text(f"Suggested release type: {result}"))
    output_report(report_parts, config.report_path)
    logger.info("Suggested release type: %s", result)
    logger.dedent()
    return result


def format_bool(bool_var: bool) -> Text:
    """Format a boolean value as a string."""
    return Text("X", style="bold green") if bool_var else Text("-", style="bold red")


def print_table(results: dict, commit_results: dict) -> RenderableType:
    """Print the test results as a table."""
    group = []
    for group_name, result_list in results.items():
        group.append(Text(group_name))

        group.extend(
            Padding(get_commit_results(list(commit_results)), (0, 0, 0, 2))
            for commit_sha, commit_results in groupby(result_list, attrgetter("commit"))
        )
    return Group(*group)


@group()
def get_commit_results(results: List[ReleaseRuleResult]) -> Iterable[RenderableType]:
    """Return the contents of the commit results table."""
    yield Text(f"Commit {results[0].commit}")
    table = Table(box=SIMPLE)
    table.add_column("Rule", justify="center")
    table.add_column("Group", justify="center")
    table.add_column("Path", justify="center")
    table.add_column("Branch", justify="center")
    table.add_column("Result")
    for result in results:
        style = "default" if result.result == "no-release" else "default on cornsilk1"
        table.add_row(
            str(result.rule_id),
            format_bool(result.matches_grouping),
            format_bool(result.matches_path),
            format_bool(result.matches_branch),
            result.result,
            style=style,
        )
    yield Padding(table, (0, 0, 0, 2))


def output_report(renderables: List[RenderableType], path: Optional[Path] = None) -> None:
    """Output the release hint report."""
    if path is None:
        return

    logger.info(f"Writing release hint report to {path}")
    console = Console(force_terminal=True)
    with console.capture() as capture:
        for renderable in renderables:
            console.print(renderable)
    output = capture.get()
    path.write_text(output)
