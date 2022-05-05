"""Metadata callback and processing functions."""
from typing import Callable, Optional

import re
import textwrap
from collections import defaultdict
from dataclasses import dataclass, field

from generate_changelog.actions import register_builtin
from generate_changelog.data_merge import comprehensive_merge

RFC822_KEY_VALUE_PATTERN = r"(?:^|\n)(?P<key>[-\w]*)\s*:\s*(?P<value>[^\n]*(?:\n\s+[^\n]*)*)"
BREAKING_CHANGE_PATTERN = r"(?:^|\n)BREAKING[-_ ]CHANGE\s*:\s*(?P<description>[^\n]*(?:\n\s+[^\n]*)*)"
CONV_COMMIT_PATTERN = r"(?i)^(?P<type>[\w]+)(\((?P<scope>[\\,/\w\-]+)\))?(?P<breaking>!)?: (?P<description>.*)"


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
        for match in re.finditer(RFC822_KEY_VALUE_PATTERN, message, re.MULTILINE | re.IGNORECASE):
            pos = min(pos, match.start())
            dct = match.groupdict()
            key = dct["key"].lower()
            value = dct["value"]

            # Convert a multiline description to a single line.
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
        matches = self.issue_pattern.findall(message)
        if matches:
            self.commit_metadata(issue=matches)
        return message


@register_builtin
class ParseGitHubIssue(ParseIssue):
    """Parse GitHub issue references from commits.

    Link these GitHub issues to their source using a URL pattern like:

    https://github.com/<owner>/<repository>/issues/<issue number>

    References:
        - https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/autolinked-references-and-urls.  # NOQA
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


@register_builtin
class ParseBreakingChangeFooter:
    """Parse a breaking change footer."""

    def __init__(self, commit_metadata: Callable):
        self.commit_metadata = commit_metadata

    def __call__(self, message: str) -> str:
        """
        Parse a BREAKING CHANGE footer.

        Args:
            message: The commit message

        Returns:
            The commit message for later processing.
        """
        from more_itertools import chunked

        msg_length = len(message)
        breaking_changes = []
        message_cut_points = [0]  # a list of start and stop positions

        for match in re.finditer(BREAKING_CHANGE_PATTERN, message, re.MULTILINE | re.IGNORECASE):
            start_pos = min(msg_length, match.start())
            end_pos = min(msg_length, match.end())
            message_cut_points.extend([start_pos, end_pos])

            value = match.groupdict()["description"]

            # Convert a multiline description to a single line.
            if "\n" in value:
                first_line, remaining = value.split("\n", 1)
                value = f"{first_line}\n{textwrap.dedent(remaining)}"

            breaking_changes.append(value)

        message_cut_points.append(msg_length)

        message_spans = [
            message[start_pos:end_pos] for start_pos, end_pos in chunked(message_cut_points, 2, strict=True)
        ]
        if breaking_changes:
            self.commit_metadata(has_breaking_change=True, breaking_changes=" ".join(breaking_changes))

        return "".join(message_spans)


@register_builtin
class ParseConventionalCommit:
    """
    Parse a line of text using the conventional commit syntax.

    The metadata will contain ``commit_type``, a string and ``scopes``, an empty list or a list of strings.

    If a breaking change is indicated (with the ``!``), metadata will also contain ``has_breaking_change`` set
    to ``True``.

    The description is returned for further processing.

    If the summary does not match a conventional commit, the whole line is returned.
    """

    def __init__(self, commit_metadata: Callable):
        self.commit_metadata = commit_metadata

    def __call__(self, message: str) -> str:
        """
        Parse a line of text using the conventional commit syntax.

        Args:
            message: The commit message

        Returns:
            The description for later processing.
        """
        match = re.match(CONV_COMMIT_PATTERN, message)
        if not match:
            return message

        grp_dict = match.groupdict()
        metadata = {
            "commit_type": grp_dict["type"],
            "scope": [],
        }

        if grp_dict["breaking"]:
            metadata["has_breaking_change"] = True
        if grp_dict["scope"]:
            scopes = re.split(r"[\\,/]\s*", grp_dict["scope"])
            metadata["scope"] = scopes
        self.commit_metadata(**metadata)
        return grp_dict["description"]
