"""Templating functions."""
from typing import Dict, List, Optional

import collections
import re

from git import Actor, Repo
from jinja2 import ChoiceLoader, Environment, FileSystemLoader, PackageLoader, select_autoescape

from generate_changelog import git_ops
from generate_changelog.actions.metadata import MetadataCollector
from generate_changelog.configuration import Configuration, get_config
from generate_changelog.context import CommitContext, SectionContext, VersionContext
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
            summary_pipeline = pipeline_factory(
                action_list=get_config().summary_pipeline,
                commit_metadata_func=commit_metadata_func,
                version_metadata_func=version_metadata_func,
            )
            summary = summary_pipeline.run(commit.summary)
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
                    summary=summary,
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
    context = config.variables.copy()
    context["versions"] = version_context
    context["VALID_AUTHOR_TOKENS"] = config.valid_author_tokens

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
