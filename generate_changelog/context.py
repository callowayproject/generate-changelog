"""Context definitions."""
from typing import List, Optional, Tuple

import collections
import datetime
import re
from dataclasses import dataclass, field

from generate_changelog.configuration import get_config


@dataclass
class CommitContext:
    """Commit information for the template context."""

    sha: str
    """The full hex SHA of the commit."""

    commit_datetime: datetime.datetime
    """The date and time of the commit with timezone offset."""

    summary: str
    """The first line of the commit message."""

    body: str
    """The commit message sans the first line."""

    committer: str
    """The name and email of the committer as `name <email@ex.com>`."""

    grouping: tuple = field(default_factory=tuple)
    """The values to group this commit based on the ``group_by`` configuration."""

    metadata: dict = field(default_factory=dict)
    """Metadata for this commit parsed from the commit message."""

    _authors: Optional[list] = field(init=False)  # list of dicts with name and email keys
    _author_names: Optional[list] = field(init=False)  # list of just the names

    def __post_init__(self):
        """Set the cached author information to None."""
        self._authors = None
        self._author_names = None

    @property
    def short_sha(self) -> str:
        """The first seven characters of the hex sha."""
        return self.sha[:7]

    @property
    def authors(self) -> list:
        """
        A list of authors' names and emails.

        Returns:
            A list of dictionaries with name and email keys.
        """
        if self._authors is not None:
            return self._authors

        raw_authors = [self.committer]
        trailers = self.metadata.get("trailers", collections.defaultdict(list))
        for token in get_config().valid_author_tokens:
            raw_authors.extend(trailers.get(token, []))
        author_regex = re.compile(r"^(?P<name>[^<]+)\s+(?:<(?P<email>[^>]+)>)?$")

        self._authors = []
        for author in raw_authors:
            match = author_regex.match(author)
            if match:
                self._authors.append(match.groupdict())
            else:
                self._authors.append({"name": author, "email": ""})

        self._authors.sort(key=lambda x: x["name"])
        return self._authors

    @property
    def author_names(self) -> list:
        """A list of the authors' names."""
        if self._author_names is not None:
            return self._author_names

        self._author_names = [x["name"] for x in self.authors]

        return self._author_names


@dataclass
class GroupedCommit:
    """A combination of a tuple of the sorted values and a list of the CommitContexts in that group."""

    grouping: Tuple[str]
    commits: List[CommitContext]


@dataclass
class VersionContext:
    """Version information for the template context."""

    label: str
    """The version label."""

    date_time: Optional[datetime.datetime] = None
    """The date and time with timezone offset the version was tagged."""

    tag: Optional[str] = None
    """The tag."""

    previous_tag: Optional[str] = None
    """The previous tag."""

    tagger: Optional[str] = None
    """The name and email of the person who tagged this version in `name <email@ex.com>` format."""

    grouped_commits: List[GroupedCommit] = field(default_factory=list)
    """The sections that group the commits in this version."""

    metadata: dict = field(default_factory=dict)
    """Metadata for this version parsed from commits."""
