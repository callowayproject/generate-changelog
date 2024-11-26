# How *Generate Changelog* Works

Generate Changelog requires a git tag to indicate each version, or release, in the git repository.

The two foundational functions are getting the starting tag and processing the commits from that starting point. Based on the results of these functions, we can suggest a release hint and render a change log and release notes.

## Get the starting tag

This step determines the processing starting point using the `--starting-tag` command line option or the `starting_tag_pipeline` configuration. If no starting tag is found, it starts at the first commit.

## Process commits

This step filters and processes each commit from a starting point and converts it to a [`CommitContext`][generate_changelog.context.CommitContext].

For each commit since the starting point:

1. Discard the commit if it matches the [`ignore_patterns`][generate_changelog.configuration.Configuration.ignore_patterns] configuration.
2. Run the `summary` line through the [`summary_pipeline`][generate_changelog.configuration.Configuration.summary_pipeline] configuration.
3. Run the `body` through the [`body_pipeline`][generate_changelog.configuration.Configuration.body_pipeline] configuration.
4. Assign the commit a `category` based on the first matching item in the [`commit_classifiers`][generate_changelog.configuration.Configuration.commit_classifiers] configuration.
5. Assign the commit a `grouping` based on the [`group_by`][generate_changelog.configuration.Configuration.group_by] configuration.
6. Create a [`CommitContext`][generate_changelog.context.CommitContext] from the commit's processed attributes.

## Process tags

This step gathers and filters all tags from a starting point and converts them to a [`VersionContext`][generate_changelog.context.VersionContext].

For each tag since the starting point:

1. Discard the tag if it does not match the [`tag_pattern`][generate_changelog.configuration.Configuration.tag_pattern] configuration.
2. Convert the tag to a [`VersionContext`][generate_changelog.context.VersionContext].
3. Assign each [`CommitContext`][generate_changelog.context.CommitContext] to a [`VersionContext`][generate_changelog.context.VersionContext] according to its tag if the underlying commit is tagged or the next valid tag in the timeline. 
4. Assign [`CommitContext`][generate_changelog.context.CommitContext]s since the last tag assigned a [`VersionContext`][generate_changelog.context.VersionContext] named [`unreleased_label`][generate_changelog.configuration.Configuration.unreleased_label].

5. Each [`VersionContext`][generate_changelog.context.VersionContext] sorts its assigned [`CommitContext`][generate_changelog.context.CommitContext]s by its `grouping` attribute.

## Optional: suggest a release type

This is a map-reduce function where each rule in the [`release_hint_rules`][generate_changelog.configuration.Configuration.release_hint_rules] configuration is applied to each [`CommitContext`][generate_changelog.context.CommitContext] in the unreleased [`VersionContext`][generate_changelog.context.VersionContext] and returns a [`release_type`][generate_changelog.configuration.RELEASE_TYPE_ORDER]. The resulting values are reduced to the maximum value according to this listing:

1. no-release
2. alpha
3. beta
4. dev
5. pre-release
6. release-candidate
7. patch
8. minor
9. major


## Render the changelog

This involves rendering a complete or partial changelog using [Jinja templates](https://jinja.palletsprojects.com). For incremental change logs (those with a starting tag), only the `heading.md.jinja` and `versions.md.jinja` templates are rendered and returned. For full change logs, the `base.md.jinja` template is rendered and returned.
