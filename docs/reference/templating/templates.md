# Templates

The changelog is generated with over-ridable [Jinja templates](https://jinja.palletsprojects.com/en/3.1.x/). You don't have to override all the templates, simply the ones you want to.

You can configure where `generate-changelog` looks for [`custom templates`][generate_changelog.configuration.Configuration.template_dirs].

The core of the changelog is the commit. The rest is just a grouping of the commits in a desired method.

## base.md.jinja

The base template is rendered when generating the changelog from scratch. Incremental generations will only use the [heading](#headingmdjinja) and [versions](#versionsmdjinja) templates.

```jinja title="base.md.jinja"
--8<-- "generate_changelog/templates/base.md.jinja"
```

## heading.md.jinja

The heading template is rendered for the title of the changelog.

```jinja title="heading.md.jinja"
--8<-- "generate_changelog/templates/heading.md.jinja"
```

## versions.md.jinja

```jinja title="versions.md.jinja"
--8<-- "generate_changelog/templates/versions.md.jinja"
```

To understand how this template works, understanding how the commits are processed and grouped will help.

The commits are enriched with metadata and sorted by the version and grouping values. In this table you can see the commit version and the values of the [`group_by`][generate_changelog.configuration.Configuration.group_by] configuration, sorted. 

| version | committer, metadata.category | Commit   |
|:--------|:-----------------------------|:---------|
| 1.0.1   | Alice, Changes               | commit8  |
| 1.0.1   | Alice, New                   | commit2  |
| 1.0.1   | Alice, New                   | commit5  |
| 1.0.1   | Bob, Changes                 | commit7  |
| 1.0.1   | Bob, Fixes                   | commit10 |
| 1.0.1   | Bob, New                     | commit1  |
| 1.0.1   | Bob, New                     | commit4  |
| 1.0.1   | Charly, Changes              | commit6  |
| 1.0.1   | Charly, Fixes                | commit9  |
| 1.0.1   | Charly, New                  | commit3  |

This is consolidated into the context that looks something like this (See the [VersionContext](version-context.md) for better information):

```python
simplified_version_context = {
    "label": "1.0.1",
    "grouped_commits": {
        ("Alice", "Changes"): ["commit8"],
        ("Alice", "New"): ["commit2", "commit5"],
        ("Bob", "Changes"): ["commit7"],
        ("Bob", "Fixes"): ["commit10"],
        ("Bob", "New"): ["commit1", "commit4"],
        ("Charly", "Changes"): ["commit6"],
        ("Charly", "Fixes"): ["commit9"],
        ("Charly", "New"): ["commit3"],
    }
}
```

The template looks for changes in the grouping values and renders [section headings](#section_headingmdjinja) for the new value. The result is something like:

```markdown
## 1.0.1 (2022-01-01)

### Alice

#### Changes

- commit8

#### New

- commit2

- commit5

...
```

## version_heading.md.jinja

The version heading template is rendered for the title of each tagged version.

```jinja title="version_heading.md.jinja"
--8<-- "generate_changelog/templates/version_heading.md.jinja"
```

## section_heading.md.jinja

The section heading template is rendered for the value changes in the grouping. The heading level is adjusted based on the `level` parameter set in the `version_heading.md.jinja` template.

```jinja title="section_heading.md.jinja"
--8<-- "generate_changelog/templates/section_heading.md.jinja"
```

## commit.md.jinja

This template is rendered for each commit.

```jinja title="commit.md.jinja"
--8<-- "generate_changelog/templates/commit.md.jinja"
```

## footer.md.jinja

The default footer templaate is blank. You can override this to add your own information.

```jinja title="footer.md.jinja"
--8<-- "generate_changelog/templates/footer.md.jinja"
```
