# File Processing Actions

These actions read and write to file-like objects. 

## ReadFile

Read a file's contents and return them. You can optionally have the file created if it's missing. If the file is missing or empty, it returns an empty string.

This action is unusual in that it doesn't do anything with input passed to it. This makes it most useful at the beginning of a pipeline.

### Arguments

- `filename`: The full path or path relative to the current working directory.

- `create_if_missing`: Defaults to `true`. When `true`, missing files are created.

### Examples

```yaml
starting_tag_pipeline:
  - action: ReadFile
    kwargs:
      filename: CHANGELOG.md
```

## WriteFile

Write the input string to a file and return the input string.

```{warning}
The file must exist and be writable.
```

### Arguments

- `filename`: The full path or path relative to the current working directory.

### Examples

```yaml
output_pipeline:
  - action: WriteFile
    kwargs:
      filename: CHANGELOG.md
```

## stdout

Write the input string to `stdout` and return the input string.

### Examples

```yaml
output_pipeline:
  - action: stdout
```

```yaml
output_pipeline:
  - action: WriteFile
    kwargs:
      filename: CHANGELOG.md
  - action: stdout
```


## IncrementalFileInsert

Replace the start of a file with the input text.

The `filename` is read and the `last_heading_pattern` regular expression is used to find the offset of the valid text. All content from the start of the file to that point is replaced with the input text. If the `last_heading_pattern` is not found, _the entire file is replaced._

The input text is returned.

### Arguments

- `filename`: The full path or path relative to the current working directory.

- `last_heading_pattern`: A regular expression to find valid content. The beginning of the match is used as the offset point.

### Examples

```yaml
output_pipeline:
  - action: IncrementalFileInsert
    kwargs:
      filename: CHANGELOG.md
      last_heading_pattern: (?im)^## \d+\.\d+(?:\.\d+)?\s+\([0-9]+-[0-9]{2}-[0-9]{2}\)$
```
