# Conventional Commits

## Configuration

Add the [`ParseConventionalCommit`][generate_changelog.actions.metadata.ParseConventionalCommit] action to the `summary_pipeline` configuration.

```{literalinclude} ../../test/fixtures/conventional-commit.yaml
:language: yaml
:lines: 1-20
:emphasize-lines: 9-12
```

Add the [`ParseBreakingChangeFooter`][generate_changelog.actions.metadata.ParseBreakingChangeFooter] action to the `body_pipeline` configuration.

```{literalinclude} ../../test/fixtures/conventional-commit.yaml
:language: yaml
:lines: 21-29
:emphasize-lines: 2-5
```

Update the `group_by` configuration. This example orders it by the category (set by the [`commit_classifiers`][generate_changelog.configuration.Configuration.commit_classifiers) and then by the first scope, if it exists.

```{literalinclude} ../../test/fixtures/conventional-commit.yaml
:language: yaml
:lines: 30-32
:emphasize-lines: 2-3
```

Set the [`commit_classifiers`](configuration-commit_classifiers) configuration.

```{literalinclude} ../../test/fixtures/conventional-commit.yaml
:language: yaml
:lines: 33-53
:emphasize-lines: 2-21
```

The commit is classsified by the first rule that matches. So the rules in this example are:

1. "Breaking Changes" if the commit's metadata includes `has_breaking_change` and it is `True`
2. "New Features" if the commit's metadata includes `commit_type` and it is `feat`
3. "Updates" if the commit's metadata includes `commit_type` and it is `fix`, `refactor`, or `update`
4. "Other" if there are no other matches

To filter out some commit types, use `ignore_patterns`:

```yaml
ignore_patterns:
  - (?i)^(?:build|chore|ci|docs|style|perf|test):
```
