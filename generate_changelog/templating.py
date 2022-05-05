"""Templating functions."""
from typing import List, Optional

import collections
import re

from git import Actor, Commit, Repo
from jinja2 import ChoiceLoader, Environment, FileSystemLoader, PackageLoader, select_autoescape
from utilities import diff_index, resolve_name

from generate_changelog import git_ops
from generate_changelog.actions.metadata import MetadataCollector
from generate_changelog.configuration import Configuration, get_config
from generate_changelog.context import CommitContext, GroupedCommit, VersionContext
from generate_changelog.lazy import LazyObject
from generate_changelog.pipeline import Action, pipeline_factory

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
    output = []
    version_metadata_func = MetadataCollector()

    for tag in tags:
        version_commit_groups = collections.defaultdict(list)
        for commit in tag["commits"]:
            if any(re.search(pattern, commit.summary) is not None for pattern in config.ignore_patterns):
                continue

            commit_ctx = generate_commit_context(commit, config, version_metadata_func)
            version_commit_groups[commit_ctx.grouping].append(commit_ctx)

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

        version_commits = sort_group_commits(version_commit_groups)

        if output:
            output[-1].previous_tag = tag_name

        output.append(
            VersionContext(
                label=tag_label,
                date_time=tag_datetime,
                tag=tag_name,
                tagger=tagger,
                grouped_commits=version_commits,
                metadata=version_metadata_func.metadata,
            )
        )
    return output


def generate_commit_context(commit, config, version_metadata_func) -> CommitContext:
    """
    Create the renderable context for this commit.

    The summary and body are processed through their pipelines, and a category is assigned.

    Args:
        commit: The original commit data
        config: The configuration to use
        version_metadata_func: An optional callable to set version metadata while processing

    Returns:
        The render-able commit context
    """
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
    category = first_matching(config.commit_classifiers, commit)
    commit_metadata_func(category=category)

    commit_ctx = CommitContext(
        sha=commit.hexsha,
        commit_datetime=commit.committed_datetime,
        committer=f"{commit.committer.name} <{commit.committer.email}>",
        summary=summary,
        body=body,
        grouping=(),
        metadata=commit_metadata_func.metadata.copy(),
    )

    # The grouping is a tuple of the appropriate values according to the group_by configuration
    # We can sort commits later and grouped by this.
    grouping = tuple(resolve_name(commit_ctx, group) for group in config.group_by)
    commit_ctx.grouping = grouping
    return commit_ctx


def sort_group_commits(commit_groups: dict) -> list:
    """
    Sort the commit groups and convert the `dict` into a list of `GroupedCommit` objects.

    Args:
        commit_groups: A dict where the keys are grouping values.

    Returns:
        A list
    """
    # Props to this sorting method goes to:
    # https://scipython.com/book2/chapter-4-the-core-python-language-ii/questions/sorting-a-list-containing-none/
    sorted_groups = sorted(commit_groups.items(), key=lambda x: tuple((i is None, i) for i in x))
    return [GroupedCommit(*item) for item in sorted_groups]


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
    context["diff_index"] = diff_index
    context["group_depth"] = len(config.group_by)

    if starting_tag:
        heading_str = default_env.get_template("heading.md.jinja").render()
        versions_str = default_env.get_template("versions.md.jinja").render(context)
        return "\n".join([heading_str, versions_str])

    return default_env.get_template("base.md.jinja").render(context)


def first_matching(actions: list, commit: Commit) -> str:
    """
    Return the first section that matches the given commit summary.

    Args:
        actions: A mapping of section names to a list of regular expressions for matching.
        commit: The commit summary to match to a section.

    Returns:
        The name of the section.
    """
    for action in actions:
        if action.get("action", None) is None:
            return action.get("category", None)

        act = Action(
            action=action["action"],
            id_=action.get("id"),
            args=action.get("args"),
            kwargs=action.get("kwargs"),
        )
        if act.run(context={}, input_value=commit):
            return action.get("category", None)
