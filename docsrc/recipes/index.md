# Configuration Recipes

## Specifying regular expression flags

All regular expression actions have the following boolean parameters:

- [ascii_flag](https://docs.python.org/3/library/re.html#re.ASCII)
- [ignorecase_flag](https://docs.python.org/3/library/re.html#re.IGNORECASE)
- [locale_flag](https://docs.python.org/3/library/re.html#re.LOCALE)
- [multiline_flag](https://docs.python.org/3/library/re.html#re.MULTILINE)
- [dotall_flag](https://docs.python.org/3/library/re.html#re.DOTALL)
- [verbose_flag](https://docs.python.org/3/library/re.html#re.VERBOSE)

For example, this sets the multi-line flag and the ignore case flag:

```yaml
- action: FirstRegExMatch
  kwargs:
    pattern: ^## (?P<rev>\d+\.\d+(?:\.\d+)?)\s+\(\d+-\d{2}-\d{2}\)$
    named_subgroup: rev
    ignorecase_flag: true
    multiline_flag: true
```

You can also use inline notation `(?<flags>)` where `<flags>` is one or more of `a` (ASCII), `i` (ignore case), `l` (locale), `m` (multi-line), `s` (dot matches all), or `x` (verbose). 

This is equivalent to the above example, with `(?im)` setting the multi-line and ignore case flags:

```yaml
- action: FirstRegExMatch
  kwargs:
    pattern: (?im)^## (?P<rev>\d+\.\d+(?:\.\d+)?)\s+\(\d+-\d{2}-\d{2}\)$
    named_subgroup: rev
```

## Incremental change logs

This will generate a change log for everything since the last version in the change log. This example assumes your version headings are formatted like `## 1.0.2 (2022-01-01)`.

All content above the matched `last_heading_pattern` is replaced with the newly generated content.

```yaml
starting_tag_pipeline:
- action: ReadFile
  comment: Read the existing change log file
  kwargs:
    filename: CHANGELOG.md
- action: FirstRegExMatch
  comment: Find the name of the latest version using the headings
  kwargs:
    pattern: (?im)^## (?P<rev>\d+\.\d+(?:\.\d+)?)\s+\(\d+-\d{2}-\d{2}\)$
    named_subgroup: rev

output_pipeline:
- action: IncrementalFileInsert
  kwargs:
    filename: CHANGELOG.md
    last_heading_pattern: (?im)^## \d+\.\d+(?:\.\d+)?\s+\([0-9]+-[0-9]{2}-[0-9]{2}\)$
```

## Parsing commit trailers

```yaml
body_pipeline:
- action: ParseTrailers
  comment: Parse the trailers into metadata.
  kwargs:
    commit_metadata: save_commit_metadata

template_dirs:
  - ".github/changelog_templates/"
```

Then create a directory in `.github` called `changelog_templates`. Create a file named `commit.md.jinja` with contents similar to:

```jinja
- {{ commit.summary }}
  {{ commit.body|indent(2, first=True) }}
  {% for key, val in commit.metadata["trailers"].items() %}
  {% if key not in VALID_AUTHOR_TOKENS %}
  **{{ key }}:** {{ val|join(", ") }}

  {% endif %}
{% endfor %}
```

This will render a commit similar to:

```markdown
- This is the summary line.
    
  This is a message body.

  **bug:** #42

  **change-id:** Ic8aaa0728a43936cd4c6e1ed590e01ba8f0fbf5b

  **signed-off-by:** A. U. Thor <committer@example.com>

  **cc:** R. E. Viewer <reviewer@example.com>

  **subject:** This is a fake subject spanning to several lines
as you can see
```

## Showing authors

You can use this in the template like:

```jinja
<ul>{% for author in commit.authors %}
  <li>{{ author.name }} [{{ author.email }}]</li>
{% endfor %}</ul>
```

or:

```jinja
Author{% if commit.author_names|length > 1 %}s{% endif %}: {{ commit.author_names|join(", ") }}
```

## Using variables
