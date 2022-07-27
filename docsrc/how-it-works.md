# How it works

Assumes versions, or releases, are tags in the git repository.

1. **Get last release:** Obtain the version number corresponding to the last release.
   1. Uses `--starting-tag` command line option or `starting_tag_pipeline` configuration to determine starting tag
   2. If no starting tag is found, it starts at the beginning
2. **Process commits:** Filter and process commits since a starting point, setting metadata and normalizing information.
   1. Uses `tag_pattern` configuration to filter tags since starting commit
   2. Groups commits according to their tag or the next tag in the timeline in 
   3. Commits since the last tag are grouped under a tag placeholder named `HEAD`
   4. Each tag is converted to a `VersionContext`. The `HEAD` placeholder is renamed to the `unreleased_label` configuration
   5. Each commit within the tag are processed
      1. Filtered using `ignore_patterns` configuration
      2. The commit's `summary` line is run through the `summary_pipeline` configuration
      3. The commit's `body` is run through the `body_pipeline` configuration
      4. The commit is assigned a `category` based on the first matching item in the `commit_classifiers` configuration
      5. The commit is assigned a `grouping` based on the `group_by` configuration
      6. Each commit is converted to a `CommitContext`
   6. The processed commits are sorted by their `grouping` attribute
3. **Suggest release hint:** Applies rules to every `CommitContext` in the `unreleased_label` `VersionContext`. If there is not an `unreleased_label` version, or if its commits are empty, a hint of `no-release` is returned
   1. Each rule in the `release_hint_rules` configuration is applied to each `CommitContext` in the unreleased `VersionContext` and collected in a unique set of possible release types
   2. The commit's possible release types are sorted according to `major` > `minor` > `patch` > `no-release`.
   3. The highest possible release type for each commit is assigned to a unique set for the unreleased version
   4. The release hint is the maximum release type in the unique set of possible release types
4. **Render changelog and release notes:** Render the `VersionContext`(s) into a document.
   1. Create a `ChangelogContext` from the configuration and `VersionContext`(s)
   2. For incremental change logs (those with a starting tag), only the `heading.md.jinja` and `versions.md.jinja` are rendered and returned
   3. For full change logs, the `base.md.jinja` is rendered and returned
