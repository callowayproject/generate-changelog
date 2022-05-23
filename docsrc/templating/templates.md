# Templates

The changelog is generated with over-ridable [Jinja templates](https://jinja.palletsprojects.com/en/3.1.x/). You don't have to override all the templates, simply the ones you want to.

You can configure where `generate-changelog` looks for [custom templates](generate_changelog.configuration.Configuration.template_dirs).

The core of the changelog is the commit. The rest is just a grouping of the commits in a desired method.

## base.md.jinja

The base template is used when generating the changelog from scratch. Incremental generations will only use the [heading](#headingmdjinja) and [versions](#versionsmdjinja) templates.

```{literalinclude} ../../generate_changelog/templates/base.md.jinja
```

## heading.md.jinja

The heading template is used for the title of the changelog.

```{literalinclude} ../../generate_changelog/templates/heading.md.jinja
```

## versions.md.jinja

```{literalinclude} ../../generate_changelog/templates/versions.md.jinja
```

## version_heading.md.jinja

The version heading template is used for the title for each tagged version.

```{literalinclude} ../../generate_changelog/templates/version_heading.md.jinja
```

## section_heading.md.jinja

```{literalinclude} ../../generate_changelog/templates/section_heading.md.jinja
```

## commit.md.jinja

```{literalinclude} ../../generate_changelog/templates/commit.md.jinja
```

## footer.md.jinja

```{literalinclude} ../../generate_changelog/templates/footer.md.jinja
```
