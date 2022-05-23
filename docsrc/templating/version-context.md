# Version Context

| Name            | Type                                 | Description                                                                               |
|-----------------|--------------------------------------|-------------------------------------------------------------------------------------------|
| label           | `string`                             | The version label.                                                                        |
| date_time       | `datetime`                           | The date and time with timezone offset the version was tagged.                            |
| tag             | `string`                             | The tag.                                                                                  |
| previous_tag    | `string`                             | The previous tag.                                                                         |
| tagger          | `string`                             | The name and email of the person who tagged this version in `name <email@ex.com>` format. |
| grouped_commits | `list` of {class}`~.GroupingContext` | The sections that group the commits in this version.                                      |
| metadata        | `dict`                               | Metadata for this version parsed from commits.                                            |

## Grouping Context

| Name     | Type                               | Description                                                                                      |
|----------|------------------------------------|--------------------------------------------------------------------------------------------------|
| grouping | `list` of `string`                 | The values that group these commits based on the {class}`~.Configuration.group_by` configuration |
| commits  | `list` of {class}`~.CommitContext` | The commits with this grouping                                                                   |
