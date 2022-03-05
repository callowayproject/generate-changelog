"""Templating functions."""
from typing import List, Optional

import collections
import datetime
import re
from dataclasses import dataclass, field

from git import Actor, Repo
from jinja2 import ChoiceLoader, Environment, FileSystemLoader, PackageLoader, select_autoescape

from generate_changelog import git_ops
from generate_changelog.configuration import CONFIG, VALID_AUTHOR_TOKENS, Configuration
from generate_changelog.pipeline import pipeline_factory
from generate_changelog.processors import load_builtins
from generate_changelog.processors.metadata import MetadataCollector

load_builtins()

default_env = Environment(
    loader=ChoiceLoader([FileSystemLoader(CONFIG.template_dirs), PackageLoader("generate_changelog")]),
    trim_blocks=True,
    lstrip_blocks=True,
    keep_trailing_newline=True,
    autoescape=select_autoescape(),
)
pipeline_env = Environment(
    loader=ChoiceLoader([FileSystemLoader(CONFIG.template_dirs), PackageLoader("generate_changelog")]),
    autoescape=select_autoescape(),
    variable_start_string="${{",
)


@dataclass
class CommitContext:
    """A commit for the template context."""

    sha: str
    commit_datetime: datetime.datetime
    subject: str
    body: str
    committer: str
    _authors: Optional[list] = field(init=False)  # list of dicts with name and email keys
    _author_names: Optional[list] = field(init=False)  # list of just the names
    metadata: dict = field(default_factory=dict)

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
        """Return a list of dicts name and emails."""
        if self._authors is not None:
            return self._authors

        raw_authors = [self.committer]
        trailers = self.metadata.get("trailers", collections.defaultdict(list))
        for token in VALID_AUTHOR_TOKENS:
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
        """Return a list of the author names."""
        if self._author_names is not None:
            return self._author_names

        self._author_names = [x["name"] for x in self.authors]

        return self._author_names


@dataclass
class SectionContext:
    """A section for the template context."""

    label: str
    commits: List[CommitContext] = field(default_factory=list)


@dataclass
class VersionContext:
    """A tagged version for the template context."""

    label: str
    date_time: Optional[datetime.datetime] = None
    tag: Optional[str] = None
    tagger: Optional[str] = None
    sections: List[SectionContext] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)


def get_context_from_tags(repository: Repo, config: Configuration, starting_tag: Optional[str] = None):
    """Get the template context from tags."""
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
                action_list=CONFIG.subject_pipeline,
                commit_metadata_func=commit_metadata_func,
                version_metadata_func=version_metadata_func,
            )
            subject = subject_pipeline.run(commit.summary)
            body_pipeline = pipeline_factory(
                action_list=CONFIG.body_pipeline,
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
    """Render the changelog for the repository to a string."""
    context = get_context_from_tags(repository, config, starting_tag)
    if starting_tag:
        heading_str = default_env.get_template("heading.md.jinja").render()
        versions_str = default_env.get_template("versions.md.jinja").render(
            {"versions": context, "VALID_AUTHOR_TOKENS": VALID_AUTHOR_TOKENS}
        )
        return "\n".join([heading_str, versions_str])

    return default_env.get_template("base.md.jinja").render(
        {"versions": context, "VALID_AUTHOR_TOKENS": VALID_AUTHOR_TOKENS}
    )


def first_matching(section_patterns: dict, string: str) -> str:
    """Return the section that either matches the given string."""
    for section, patterns in section_patterns.items():
        if patterns is None:
            return section
        for pattern in patterns:
            if re.search(pattern, string) is not None:
                return section
