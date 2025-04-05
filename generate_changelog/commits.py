"""Filter and process commits into contexts."""

import collections
import re
from typing import Callable, List, Optional

from git import Actor, Commit, Repo

from generate_changelog import git_ops
from generate_changelog.actions.metadata import MetadataCollector
from generate_changelog.configuration import Configuration
from generate_changelog.context import CommitContext, GroupingContext, VersionContext
from generate_changelog.git_ops import GitTag
from generate_changelog.pipeline import Action, pipeline_factory
from generate_changelog.utilities import resolve_name


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
    output: List[VersionContext] = []

    for tag in tags:
        version_context = create_version_context(config, tag)

        if output:
            output[-1].previous_tag = version_context.tag

        output.append(version_context)

    if starting_tag and output and output[-1].previous_tag is None:
        output[-1].previous_tag = starting_tag

    return output


def create_version_context(config: Configuration, tag: GitTag) -> VersionContext:
    """
    Generate a [`VersionContext`][generate_changelog.context.VersionContext] from a tag dictionary.

    Args:
        config: The current configuration object.
        tag: A GitTag used as the basis for a VersionContext

    Returns:
        The finished version context.
    """
    version_metadata_func = MetadataCollector()
    version_commit_groups = collections.defaultdict(list)

    for commit in tag.commits:
        if any(re.search(ignore_pat, commit.summary) is not None for ignore_pat in config.ignore_patterns):
            continue

        commit_ctx = generate_commit_context(commit, config, version_metadata_func)
        version_commit_groups[commit_ctx.grouping].append(commit_ctx)

    tag_label = tag.tag_name if tag.tag_name != "HEAD" else config.unreleased_label

    if tag.tag_info:
        tag_name = tag.tag_info.name
        tag_datetime = tag.tag_info.tagged_datetime
        if isinstance(tag.tag_info.tagger, Actor):
            tagger = f"{tag.tag_info.tagger.name} <{tag.tag_info.tagger.email}>"
        else:
            tagger = str(tag.tag_info.tagger)
    else:
        tag_name = None
        tag_datetime = None
        tagger = None

    version_commits = sort_group_commits(version_commit_groups)

    return VersionContext(
        label=tag_label,
        date_time=tag_datetime,
        tag=tag_name,
        tagger=tagger,
        grouped_commits=version_commits,
        metadata=version_metadata_func.metadata,
    )


def generate_commit_context(
    commit: Commit, config: Configuration, version_metadata_func: Optional[Callable]
) -> CommitContext:
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
        action_list=config.summary_pipeline,
        commit_metadata_func=commit_metadata_func,
        version_metadata_func=version_metadata_func,
    )
    summary = summary_pipeline.run(commit.summary)
    body_pipeline = pipeline_factory(
        action_list=config.body_pipeline,
        commit_metadata_func=commit_metadata_func,
        version_metadata_func=version_metadata_func,
    )
    body_text = "\n".join(commit.message.splitlines()[1:])
    body = body_pipeline.run(body_text)

    commit_ctx = CommitContext(
        sha=commit.hexsha,
        commit_datetime=commit.committed_datetime,
        committer=f"{commit.committer.name} <{commit.committer.email}>",
        summary=summary,
        body=body,
        grouping=(),
        metadata=commit_metadata_func.metadata.copy(),
        files=set(commit.stats.files.keys()),
    )
    category = first_matching(config.commit_classifiers, commit_ctx)
    commit_ctx.metadata["category"] = category

    # The grouping is a tuple of the appropriate values according to the group_by configuration
    # We can sort commits later and grouped by this.
    grouping = tuple(resolve_name(commit_ctx, group) for group in config.group_by)
    commit_ctx.grouping = grouping
    return commit_ctx


def sort_group_commits(commit_groups: dict) -> list[GroupingContext]:
    """
    Sort the commit groups and convert the `dict` into a list of `GroupingContext` objects.

    Args:
        commit_groups: A dict where the keys are grouping values.

    Returns:
        A list of `GroupingContext` objects.
    """
    # Props to this sorting method goes to:
    # https://scipython.com/book2/chapter-4-the-core-python-language-ii/questions/sorting-a-list-containing-none/

    def key_func(input_value: tuple) -> tuple:
        """Generate the sortable key for tuples that may contain None."""
        return tuple((i is not None, i) for i in input_value[0])

    sorted_groups = sorted(commit_groups.items(), key=key_func)
    return [GroupingContext(*item) for item in sorted_groups]


def first_matching(actions: list, commit: CommitContext) -> Optional[str]:
    """
    Return the first section that matches the given commit summary.

    Args:
        actions: A mapping of section names to a list of regular expressions for matching.
        commit: The commit context to evaluate

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
    return None
