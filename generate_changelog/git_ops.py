"""git information access."""

from typing import List, Optional, Union

import datetime
import os
import re
from dataclasses import dataclass

from git import Actor, Repo

from generate_changelog.configuration import get_config

GIT_FORMAT_KEYS = {
    "sha1": "%H",
    "sha1_short": "%h",
    "author_name": "%an",
    "author_email": "%ae",
    "author_date_timestamp": "%at",
    "committer_name": "%cn",
    "committer_date_timestamp": "%ct",
    "summary": "%s",
    "body": "%b",
}
GIT_FULL_FORMAT_STRING = "%x00".join(GIT_FORMAT_KEYS.values()) + "%x1F"


@dataclass(frozen=True)
class TagInfo:
    """Simple storage of tag information."""

    name: str
    commit: str
    tagger: Union[str, Actor]
    tagged_datetime: datetime.datetime

    @property
    def date_string(self) -> str:
        """Convenience method to return an ISO8601 date string."""
        return self.tagged_datetime.strftime("%Y-%m-%d")


def get_repo(repo_path: Optional[str] = None) -> Repo:
    """
    Get the git repo from a specific path or the current working directory.

    Args:
        repo_path: The path to the directory with git repository. If None, the current working directory is used.

    Returns:
        Repository object
    """
    return Repo(repo_path or os.getcwd())


def parse_commits(repository: Repo, starting_rev: Optional[str] = None, ending_rev: Optional[str] = None) -> list:
    """
    Parse the commits for later processing.

    Args:
        repository: The repository object.
        starting_rev: Include all commits after this revision.
        ending_rev: include all commmits before and including this revision.

    Returns:
        A list of CommitInfo objects.
    """
    if starting_rev and ending_rev:
        revs = f"{starting_rev}..{ending_rev}"
    elif starting_rev:
        revs = f"{starting_rev}..HEAD"
    elif ending_rev:
        revs = ending_rev
    else:
        revs = "HEAD"

    log_opts = ["-z", "--topo-order", "--pretty=tformat:%H"]

    if get_config().include_merges:
        log_opts.append("--no-merges")

    log_opts.append(revs)
    out: str = repository.git.log(*log_opts)
    commits = out.split("\x00")
    return [repository.commit(commit) for commit in commits if commit]


def get_tags(repository: Repo) -> List[TagInfo]:
    """
    Get all the tags in a repository.

    Args:
        repository: The repository object containing the tags

    Returns:
        A list of TagInfo objects with the most recent first
    """
    tags = repository.tags
    tags_list = []

    for tag in tags:
        commit = tag.commit
        if tag.tag:
            tzoffset = datetime.timedelta(seconds=-tag.tag.tagger_tz_offset)
            tzone = datetime.timezone(tzoffset)
            tag_datetime = datetime.datetime.utcfromtimestamp(tag.tag.tagged_date).astimezone(tzone)
            tagger = tag.tag.tagger
        else:
            tag_datetime = tag.commit.committed_datetime
            tagger = tag.commit.committer

        tag_info = TagInfo(
            name=tag.name,
            commit=commit.hexsha,
            tagger=tagger,
            tagged_datetime=tag_datetime,
        )
        tags_list.append(tag_info)

    tags_list.sort(key=lambda t: t.tagged_datetime, reverse=True)

    return tags_list


def get_commits_by_tags(repository: Repo, tag_filter_pattern: str, starting_tag: Optional[str] = None) -> List[dict]:
    """
    Group commits by the tags they belong to.

    Args:
        repository: The git repository object
        tag_filter_pattern: A regular expression pattern that matches valid tags as versions
        starting_tag: Only include tags after this one

    Returns:
        A list of dictionaries with tag information with most recent first
    """
    from generate_changelog.utilities import pairs

    tags = [tag for tag in get_tags(repository) if re.match(tag_filter_pattern, tag.name)]
    head_commit = repository.commit("HEAD")
    head_tagger = head_commit.committer.name
    if head_commit.committer.email:
        head_tagger += f" <{head_commit.committer.email}>"

    head = TagInfo(
        name="HEAD",
        commit=head_commit.hexsha,
        tagger=head_tagger,
        tagged_datetime=head_commit.committed_datetime,
    )
    tags.insert(0, head)
    groups = []
    for end_tag, start_tag in pairs(tags):
        start_tag_name = getattr(start_tag, "name", None)
        groups.append(
            {
                "tag_name": end_tag.name,
                "tag_info": end_tag,
                "commits": parse_commits(repository, start_tag_name, end_tag.name),
            }
        )
        if starting_tag and start_tag_name == starting_tag:
            break

    return groups
