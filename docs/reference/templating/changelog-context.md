# Changelog Context

| Name                | Type                                                                    | Description                                                                             |
|---------------------|-------------------------------------------------------------------------|-----------------------------------------------------------------------------------------|
| config              | [`Configuration`][generate_changelog.configuration.Configuration]       | The changelog generation configuration.                                                 |
| versions            | `list` of [`VersionContext`][generate_changelog.context.VersionContext] | The version contexts to render in the changelog.                                        |
| unreleased_label    | `string`                                                                | The configured label used as the version title of the changes since the last valid tag. |
| valid_author_tokens | `list` of `string`                                                      | The configured tokens in git commit trailers that indicate authorship.                  |
| group_by            | `list` of `string`                                                      | The configured grouping aspects for commits within a version.                           |
| group_depth         | `int`                                                                   | The number of levels version commits are grouped by.                                    |
| diff_index          | `function`                                                              | The index of the first difference between two lists                                     |
