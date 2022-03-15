"""Metadata callback and processing functions."""
from typing import Callable, Optional

import re
import textwrap
from collections import defaultdict
from dataclasses import dataclass, field

from generate_changelog.actions import register_builtin
from generate_changelog.data_merge import comprehensive_merge

REGEX_RFC822_KEY_VALUE = r"(?:^|\n)(?P<key>[-\w]*)\s*:\s*(?P<value>[^\n]*(?:\n\s+[^\n]*)*)"


@dataclass
class MetadataCollector:
    """Creates a callable to collect key-value metadata."""

    metadata: dict = field(default_factory=dict)

    def __call__(self, **kwargs):
        """
        Put keyword arguments into metadata storage.

        Args:
            **kwargs: keyword arguments to update metadata
        """
        self.metadata = comprehensive_merge(self.metadata, kwargs)


@register_builtin
class ParseTrailers:
    """Parse and extract trailers from a commit message."""

    def __init__(self, commit_metadata: Callable):
        self.commit_metadata = commit_metadata

    def __call__(self, message: str) -> str:
        """Parse and extract trailers from a commit message."""
        pos = len(message)
        trailers = defaultdict(list)
        for match in re.finditer(REGEX_RFC822_KEY_VALUE, message, re.MULTILINE | re.IGNORECASE):
            pos = min(pos, match.start())
            dct = match.groupdict()
            key = dct["key"].lower()
            value = dct["value"]
            if "\n" in value:
                first_line, remaining = value.split("\n", 1)
                value = f"{first_line}\n{textwrap.dedent(remaining)}"

            trailers[key].append(value)
        self.commit_metadata(trailers=trailers)
        return message[:pos]


@register_builtin
class ParseIssue:
    """Base class to parse an issue reference and put it into the commit metadata."""

    issue_pattern: re.Pattern

    def __init__(self, commit_metadata: Callable, issue_pattern: Optional[str] = None):
        self.commit_metadata = commit_metadata

        if issue_pattern:
            self.issue_pattern = re.compile(issue_pattern)

    def __call__(self, message: str) -> str:
        """
        Put the issue(s) reference into the commit metadata using the keyword ``issue`` .

        Args:
            message: The commit message

        Returns:
            The commit message for later processing.
        """
        if matches := self.issue_pattern.findall(message):
            self.commit_metadata(issue=matches)
        return message


@register_builtin
class ParseGitHubIssue(ParseIssue):
    """Parse GitHub issue references from commits.

    Link these GitHub issues to their source using a URL pattern like:

    https://github.com/<owner>/<repository>/issues/<issue number>

    References:
        - https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/autolinked-references-and-urls.
    """

    issue_pattern = re.compile(r"(?im)(?:#|GH-)(\d+)")


@register_builtin
class ParseJiraIssue(ParseIssue):
    """
    Parse Jira issues from commits.

    https://support.atlassian.com/jira-software-cloud/docs/process-issues-with-smart-commits/
    """

    issue_pattern = re.compile(r"(?im)([a-z]{3}-\d+)")


@register_builtin
class ParseAzureBoardIssue(ParseIssue):
    """
    Parse Azure board issues from commits.

    Link these Azure board issues to their source using a URL pattern like:

    https://dev.azure.com/<organization>/<project>/_workitems/edit/<issue number>

    References:
        - https://docs.microsoft.com/en-us/azure/devops/boards/github/link-to-from-github
    """

    issue_pattern = re.compile(r"(?im)AB#(\d+)")
