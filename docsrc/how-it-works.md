# How Generate Changelog works

Generate Changelog requires a git tag to indicate each version, or release, in the git repository.

The two foundational functions are getting the starting tag and processing the commits from that starting point. From the result of the foundational functions we can suggest a release hint and render a change log and release notes.

## Getting the starting tag

This step uses the {option}`--starting-tag` command line option or the {ref}`configuration-starting_tag_pipeline` configuration to determine the starting point for processing. If no starting tag is found, it starts at the first commit.

## Processing commits

This step filters and processes each commit since a starting point. 

For each commit since the starting point:

1. Discard the commit if it matches the {ref}`configuration-ignore_patterns` configuration.
2. Run the `summary` line through the {ref}`configuration-summary_pipeline` configuration.
3. Run the `body` through the {ref}`configuration-body_pipeline` configuration.
4. Assign the commit a `category` based on the first matching item in the {ref}`configuration-commit_classifiers` configuration.
5. Assign the commit a `grouping` based on the {ref}`configuration-group_by` configuration.
6. Create a {class}`~.context.CommitContext` from the commit's processed attributes.

Then we must process the tags and create {class}`~.context.VersionContext`s. This involves gathering the list of tags since the starting point and using the {ref}`configuration-tag_pattern` configuration to filter out unwanted tags. Tags are converted to {class}`~.context.VersionContext`s.

Each {class}`~.context.CommitContext` is assigned a version according to the next valid tag in the timeline (or their own tag, if the underlying commit itself is tagged). {class}`~.context.CommitContext`s since the last tag assigned a version named {ref}`configuration-unreleased_label`.

Each {class}`~.context.VersionContext` sorts its assigned {class}`~.context.CommitContext`s by its `grouping` attribute.

## Suggesting a release type

This optional step applies rules to every {class}`~.context.CommitContext` in the {class}`~.context.VersionContext` labeled {ref}`configuration-unreleased_label` to determine what type of release (e.g. `patch`, `minor`, or `major`) to suggest. A `no-release` suggestion means that no release is warranted. This can happen if there is not an {ref}`configuration-unreleased_label` version, if {ref}`configuration-unreleased_label` version has no commit, or all the rules returned `no-release`.

Essentially this is a map-reduce function where each rule in the {ref}`configuration-release_hint_rules` configuration maps a release hint to each {class}`~.context.CommitContext` in the unreleased {class}`~.context.VersionContext`. The resulting values are reduced to the maximum value according to:

1. no-release
2. alpha
3. beta
4. dev
5. pre-release
6. release-candidate
7. patch
8. minor
9. major


## Rendering the changelog

This involves rendering a complete or partial changelog using [Jinja templates](https://jinja.palletsprojects.com). For incremental change logs (those with a starting tag), only the `heading.md.jinja` and `versions.md.jinja` templates are rendered and returned. For full change logs, the `base.md.jinja` template is rendered and returned.
