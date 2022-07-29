# Generating a release hint

## What is a "release hint?"

A release hint provides guidance on if and what type of software release is warranted. The guidance is based on user-defined rules applied to every {class}`~.context.CommitContext` in the unreleased {class}`~.VersionContext`. Each rule may use how the commit is grouped in the release, the files modified, or both.

You can use this release hint as input to your release tooling. 

## Methods of generating the hint

Adding the {option}`--output` option to the command allows you to specify `hint` or `all`. `hint` will return the release hint after updating the change log. `all` will return a JSON object with a `release_hint` key after updating the change log.

If you only want the hint, add the {option}`--skip-output-pipeline` option to `--output hint`.

```console
$ generate-changelog --output hint --skip-output-pipeline
patch
```

## Release rules

There are four parts to a release rule: `match_result`, `no_match_result`, `grouping` and `path`. Only `match_result` is required, but without a `grouping` or `path` value, the rule is ignored. `no_match_result` defaults to `no-release`.

### Match result

This is the hint returned if both the `grouping` and `path` values match. This is required.

### No match result

This is the hint returned if either the `grouping` or `path` values do not match. By default, this is `no-release`.

### Grouping

The {attr}`.CommitContext.grouping` attribute is always a `tuple` with one or more string values.

The value of {attr}`.ReleaseHint.grouping` will match the {attr}`.CommitContext.grouping` differently depending on its value:

:string value: 
  The value is in the {attr}`.CommitContext.grouping`. For example: `"New"` would match both `("Features", "New", )` and `("New", )`.

:sequence of string values:
  The value must match the {attr}`.CommitContext.grouping` exactly. For example `("New", )` would match `("New", )` but not `("Features", "New", )` or `("New", "Features", )`

:sequence of string values ending with a "*":
  The value must match the beginning of the {attr}`.CommitContext.grouping`. For example `("New", "*", )` would match `("New", )` and `("New", "Features", )` but not `("Features", "New", )`. 

:None:
  It will return a match and rely on the {attr}`.ReleaseHint.path` to match or not. This is saying "I don't care about the grouping I only care about the path."

### Path

The {attr}`.CommitContext.files` attribute is a `set` of paths relative to the repository root. The {attr}`.ReleaseHint.path` uses [globbing patterns](https://www.malikbrowne.com/blog/a-beginners-guide-glob-patterns) to match against {attr}`.CommitContext.files`.

## Examples

This will provide a "patch" hint if the grouping contains "Other", but only when a modified file is within the `src` directory. Otherwise it will provide a "no-release" hint.

```yaml
- match_result: "patch"
  no_match_result: "no-release"
  grouping: "Other"
  path: src/*
```
