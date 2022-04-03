"""Templating functions."""
from typing import Dict, List, Optional

import collections
import datetime
import re
from dataclasses import dataclass, field

from git import Actor, Repo
from jinja2 import ChoiceLoader, Environment, FileSystemLoader, PackageLoader, select_autoescape

from generate_changelog import git_ops
from generate_changelog.actions.metadata import MetadataCollector
from generate_changelog.configuration import Configuration, get_config
from generate_changelog.lazy import LazyObject
from generate_changelog.pipeline import pipeline_factory

default_env = LazyObject(
    lambda: Environment(
        loader=ChoiceLoader([FileSystemLoader(get_config().template_dirs), PackageLoader("generate_changelog")]),
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
        autoescape=select_autoescape(),
    )
)
"""The default Jinja environment for rendering a changelog."""

pipeline_env = LazyObject(
    lambda: Environment(
        loader=ChoiceLoader([FileSystemLoader(get_config().template_dirs), PackageLoader("generate_changelog")]),
        autoescape=select_autoescape(),
    )
)
"""The Jinja environment for rendering actions and pipelines."""


@dataclass
class CommitContext:
    """Commit information for the template context."""

    sha: str
    """The full hex SHA of the commit."""

    commit_datetime: datetime.datetime
    """The date and time of the commit with timezone offset."""

    subject: str
    """The first line of the commit message."""

    body: str
    """The commit message sans the first line."""

    committer: str
    """The name and email of the committer as `name <email@ex.com>`."""

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
            if match := author_regex.match(author):
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
class SectionContext:
    """Section information for the template context."""

    label: str
    """The section label."""

    commits: List[CommitContext] = field(default_factory=list)
    """The commits that belong in this section."""


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

    sections: List[SectionContext] = field(default_factory=list)
    """The sections that group the commits in this version."""

    metadata: dict = field(default_factory=dict)
    """Metadata for this version parsed from commits."""


def get_context_from_tags(
    repository: Repo, config: Configuration, starting_tag: Optional[str] = None
) -> List[VersionContext]:
    """
    Generate the template context from git tags.

    Args:
        repository: The git repository to evaluate.
        config: The current configuration object.
        starting_tag: Optional starting tag for generating incremental changelogs.

    Returns:
        A list of VersionContext objects.
    """
    tags = git_ops.get_commits_by_tags(repository, config.tag_pattern, starting_tag)
    section_order = config.section_patterns.keys()
    output = []
    version_metadata_func = MetadataCollector()

    for tag in tags:
        sections = collections.defaultdict(list)
        for commit in tag["commits"]:
            if any(re.search(pattern, commit.summary) is not None for pattern in config.ignore_patterns):
                continue

            commit_metadata_func = MetadataCollector()
            subject_pipeline = pipeline_factory(
                action_list=get_config().subject_pipeline,
                commit_metadata_func=commit_metadata_func,
                version_metadata_func=version_metadata_func,
            )
            subject = subject_pipeline.run(commit.summary)
            body_pipeline = pipeline_factory(
                action_list=get_config().body_pipeline,
                commit_metadata_func=commit_metadata_func,
                version_metadata_func=version_metadata_func,
            )
            body_text = "\n".join(commit.message.splitlines()[1:])
            body = body_pipeline.run(body_text)

            matched_section = first_matching(config.section_patterns, commit.summary)
            sections[matched_section].append(
                CommitContext(
                    sha=commit.hexsha,
                    commit_datetime=commit.committed_datetime,
                    committer=f"{commit.committer.name} <{commit.committer.email}>",
                    subject=subject,
                    body=body,
                    metadata=commit_metadata_func.metadata.copy(),
                )
            )
        tag_label = tag["tag_name"] if tag["tag_name"] != "HEAD" else config.unreleased_label
        if tag["tag_info"]:
            tag_name = tag["tag_info"].name
            tag_datetime = tag["tag_info"].tagged_datetime
            if isinstance(tag["tag_info"].tagger, Actor):
                tagger = f'{tag["tag_info"].tagger.name} <{tag["tag_info"].tagger.email}>'
            else:
                tagger = str(tag["tag_info"].tagger)
        else:
            tag_name = None
            tag_datetime = None
            tagger = None

        version_sections = [SectionContext(label=k, commits=sections[k]) for k in section_order if k in sections]
        if output:
            output[-1].previous_tag = tag_name

        output.append(
            VersionContext(
                label=tag_label,
                date_time=tag_datetime,
                tag=tag_name,
                tagger=tagger,
                sections=version_sections,
                metadata=version_metadata_func.metadata,
            )
        )
    return output


def render(repository: Repo, config: Configuration, starting_tag: Optional[str] = None) -> str:
    """
    Render the full or incremental changelog for the repository to a string.

    Args:
        repository: The git repository to evaluate.
        config: The current configuration object.
        starting_tag: Optional starting tag for generating incremental changelogs.

    Returns:
        The full or partial changelog
    """
    version_context = get_context_from_tags(repository, config, starting_tag)
    context = get_config().variables.copy()
    context["versions"] = version_context
    context["VALID_AUTHOR_TOKENS"] = get_config().valid_author_tokens

    if starting_tag:
        heading_str = default_env.get_template("heading.md.jinja").render()
        versions_str = default_env.get_template("versions.md.jinja").render(context)
        return "\n".join([heading_str, versions_str])

    return default_env.get_template("base.md.jinja").render(context)


def first_matching(section_patterns: Dict[str, Optional[list]], commit_summary: str) -> str:
    """
    Return the first section that matches the given commit summary.

    Args:
        section_patterns: A mapping of section names to a list of regular expressions for matching.
        commit_summary: The commit summary to match to a section.

    Returns:
        The name of the section.
    """
    for section, patterns in section_patterns.items():
        if patterns is None:
            return section
        for pattern in patterns:
            if re.search(pattern, commit_summary) is not None:
                return section
