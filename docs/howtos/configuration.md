# Configuring Your Changelog Generation

## The configuration file

`generate-changelog` uses its default configuration as a base, and then updates it with your configuration file. This allows you to keep your configuration file small and only override what you need.

You simply put a `.changelog-config.yaml` file in the root directory of your repository for the configuration file. You can dump the defaults with:

```console
$ generate-changelog --generate-config
```

Since your configuration only needs to contain the differences from the default values, you can delete the default configurations you like and keep your changes.

All configuration string values are treated as Jinja templates, except for the `variables` section. 

Some values accept pipelines, which are a chain of actions that transform an input.

## General Configuration Options

(configuration-variables)=
### variables

:YAML type: [`mapping`](https://yaml.org/spec/1.2.2/#21-collections)

:Description:
  Variables are key-value pairs for use in other parts of the configuration and in template rendering. Variable values can include references to previous variables.

  Each configuration string value is treated as a Jinja template. You can reference your variables using `{{ my_variable }}` markup.

:Default: `{}`

:Example:

  Referencing variables within variables:

  ```yaml
  variables:
    root_url: https://www.example.com/
    sub_url: {{ root_url }}sub_path/2
  ```

  You can use variables in the rendering of your changelog templates. If the configuration file contains:

  ```yaml
  variables:
    repo_url: https://github.com/callowayproject/generate-changelog
  ```

  You can reference it in your `commit.md.jinja` template like:

  ```jinja
  [{{ commit.short_sha }}]({{ repo_url }}/commit/{{ commit.sha }})
  ```

  You can also use variables in `args` and `kwargs` values in your configuration:

  ```yaml
  variables:
    changelog_file: CHANGELOG.md
  
  starting_tag_pipeline:
    - action: ReadFile
      kwargs:
        filename: {{ changelog_file }} 
  ```

(configuration-starting_tag_pipeline)=
### starting_tag_pipeline

:YAML type: [`sequence` of `mapping`](https://yaml.org/spec/1.2.2/#21-collections)

:Description:
  Generate the changelog from the tag returned by this pipeline.

  The default value reads your `CHANGELOG.md` file and looks for the first level 2 heading like `## 1.1.1 (2022-01-01)` and returns the `1.1.1` part. This configuration will generate a full changelog if either `CHANGELOG.md` doesn't exist or the pattern is not found. 

  These defaults are also the basis for generating an incremental changelog. Setting `starting_tag_pipeline` to nothing will cause it to generate a full changelog each time.

:Default:
  ```yaml
  starting_tag_pipeline:
    - action: ReadFile
      kwargs:
        filename: CHANGELOG.md
    - action: FirstRegExMatch
      kwargs:
        pattern: (?im)^## (?P<rev>\d+\.\d+(?:\.\d+)?)\s+\(\d+-\d{2}-\d{2}\)$
        named_subgroup: rev
  ```

## Output Configuration Options

(configuration-unreleased_label)=
### unreleased_label

:YAML type: `str`

:Description:
    This value is used as the section title of the changes since the last valid tag, instead of the version number.

:Default: `Unreleased`

(configuration-tag_pattern)=
### tag_pattern

:YAML type: `str`

:Description:
  Only tags matching this regular expression are used as "versions" for the changelog.

  The default pattern matches [SemVer](https://semver.org) versions like `1.1.1` and `1.1`.

  This allows you to have other tags, such as beta or development versions that do not show up in the changelog.

:Default: `^[0-9]+\.[0-9]+(?:\.[0-9]+)?$`

(configuration-output_pipeline)=
### output_pipeline

:YAML type: [`sequence` of `mapping`](https://yaml.org/spec/1.2.2/#21-collections)

:Description:
  Pipeline to do something with the full or partial changelog.

  The default value reads your `CHANGELOG.md` file and looks for the first level 2 heading like `## 1.1.1 (2022-01-01)`. If found, all content above that point in the file is replaced with the generated content. If the pattern is not found, all content in the file is replaced. 

:Default:
  ```yaml
  output_pipeline:
    - action: IncrementalFileInsert
      kwargs:
        filename: CHANGELOG.md
        last_heading_pattern: (?im)^## \d+\.\d+(?:\.\d+)?\s+\([0-9]+-[0-9]{2}-[0-9]{2}\)$
  ```

(configuration-template_dirs)=
### template_dirs

:YAML type: [`sequence` of `str`](https://yaml.org/spec/1.2.2/#21-collections)

:Description:
  Paths to look for output generation templates.

:Default:

  ```yaml
  template_dirs:
    - .github/changelog_templates/
  ```

(configuration-group_by)=
### group_by

:YAML type: [`sequence` of `str`](https://yaml.org/spec/1.2.2/#21-collections)

:Description:
  Group the commits within a version by these commit attributes. Valid values are any attributes of a [Commit Context](../reference/templating/commit-context.md). Use dot notation to specify dictionary keys, object attributes or sequence indexes. For example, `authors.0.name` references the first author's `name` key in the `authors` list.

:Default:

  ```yaml
  group_by:
    - metadata.category
  ```

## Commit Parsing Options

(configuration-summary_pipeline)=

### summary_pipeline

:YAML type: [`sequence` of `mapping`](https://yaml.org/spec/1.2.2/#21-collections)

:Description:
  Process the commit's subject for use in the changelog. The pipeline will get the subject line of the commit as its input. The output of the pipeline is rendered into the changelog.

  The default pipeline normalizes the string by:

  1. Stripping leading and trailing spaces
  2. Stripping trailing periods
  3. Setting the value to `no commit message` if there isn't one
  4. Capitalizing the first letter
  5. Adding a period to the end

:Default:
  ```yaml
  summary_pipeline:
    - action: strip_spaces
    - action: Strip
      comment: Get rid of any periods so we don't get double periods
      kwargs:
        chars: .
    - action: SetDefault
      args:
      - no commit message
    - action: capitalize
    - action: append_dot
  ```

(configuration-body_pipeline)=

### body_pipeline

:YAML type: [`sequence` of `mapping`](https://yaml.org/spec/1.2.2/#21-collections)

:Description:
  Process the commit's body for use in the changelog.

  The default value will strip the trailers from the commit message and put them into the commit's `metadata["trailers"]` attribute.

:Default:
  ```yaml
  body_pipeline:
    - action: ParseTrailers
      comment: Parse the trailers into metadata.
      kwargs:
        commit_metadata: save_commit_metadata
  ```

(configuration-include_merges)=

### include_merges
:YAML type: bool = False

:Description:
  Tells git-log whether to include merge commits in the log.

:Default: `false`


(configuration-ignore_patterns)=

### ignore_patterns
:YAML type: [`sequence` of `str`](https://yaml.org/spec/1.2.2/#21-collections)

:Description:
  Ignore commits that match any of these regular expression patterns.

:Default:
  ```yaml
  ignore_patterns:
    - '[@!]minor'
    - '[@!]cosmetic'
    - '[@!]refactor'
    - '[@!]wip'
    - ^$
    - ^Merge branch
    - ^Merge pull
  ```

(configuration-commit_classifiers)=

### commit_classifiers

:YAML type: [`sequence` of `mapping`](https://yaml.org/spec/1.2.2/#21-collections)

:Description:
  Group commits into categories if they match any of these regular expressions.

  The default uses categories of `New` for commits that add new things; `Updates` for commits that change things; `Fixes` for commits that fix things; and `Other` for commits that aren't matched by other sections.

:Default:

  ```yaml
  section_patterns:
    New:
    - (?i)^(?:new|add)[^\n]*$
    Updates:
    - (?i)^(?:update|change|rename|remove|delete|improve|refactor|chg)[^\n]*$
    Fixes:
    - (?i)^(?:fix)[^\n]*$
    Other: null
  ```

(configuration-valid_author_tokens)=

### valid_author_tokens
:YAML type: [`sequence` of `str`](https://yaml.org/spec/1.2.2/#21-collections)

:Description:
  Tokens in git commit trailers that indicate authorship.

  If `ParseTrailers` is in the `body_pipeline` configuration, the values are parsed and available in the commit's `authors` and `author_names` attributes.

:Default:
  ```yaml
  valid_author_tokens:
  - author
  - based-on-a-patch-by
  - based-on-patch-by
  - co-authored-by
  - co-committed-by
  - contributions-by
  - from
  - helped-by
  - improved-by
  - original-patch-by
  ```

## Release Hinting Options

(configuration-release_hint_rules)=

### release_hint_rules
:YAML type: [`sequence` of `mapping`](https://yaml.org/spec/1.2.2/#21-collections)

:Description: Rules applied to unreleased commits to determine the type of release to suggest.

:Default:
  ```YAML
  release_hint_rules:
    - match_result: "patch"
      no_match_result: "no-release"
      grouping: "Other"
    - match_result: "patch"
      no_match_result: "no-release"
      grouping: "Fixes"
    - match_result: "minor"
      no_match_result: "no-release"
      grouping: "Updates"
    - match_result: "minor"
      no_match_result: "no-release"
      grouping: "New"
    - match_result: "major"
      no_match_result: "no-release"
      grouping: "Breaking Changes"
  ```
