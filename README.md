# Generate Changelog

<!-- start badges -->
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/callowayproject/generate-changelog/master.svg)](https://results.pre-commit.ci/latest/github/callowayproject/generate-changelog/master)
[![codecov](https://codecov.io/gh/callowayproject/generate-changelog/branch/master/graph/badge.svg?token=IPRMV15D17)](https://codecov.io/gh/callowayproject/generate-changelog)

Use your commit log to make a beautiful changelog file.
<!-- end badges -->

- [Documentation](https://callowayproject.github.io/generate-changelog/)
- [GitHub](https://github.com/callowayproject/generate-changelog)

<!--start-->

`generate-changelog` does what it says: it generates a full changelog, or updates an existing one. Git tags and commits are the inputs by which `generate-changelog` performs its task.

The primary goal of this tool was to provide the benefits of [conventional commits](https://www.conventionalcommits.org/) without requiring a strict syntax. `generate-changelog` accomplishes this using configurable regular expressions or commit metadata matching. The thought is natural language is easier for developers to remember and requires less tooling to enforce.

## Features

### Commit and tag processing

- Filter out commits and tags based on regular expression matching.
- Classify commit messages into sections such as "New", "Fixes", and "Changes" using configurable regular expressions, metadata, or custom criteria.
- Rewrite commit summary or commit body using pipelines of actions.
- Extract parts of the commit summary or body into metadata available for templates and filters.
- Built-in issue parsers for Jira, GitHub, Azure DevOps Board.
- Built-in conventional commit parser

### Changelog rendering

- Templated using [Jinja](https://jinja.palletsprojects.com/en/3.0.x/) templates.
- Each template has a large amount of metadata that allows linking to a commit, a version diff, and issue trackers.
- Easily customize just the template you want.
- Supports full or incremental changelog generation.

### Release hints

- Can use user-defined rules to suggest a release type for use in another part of your CI pipeline.

### Git support

- Supports your merge or rebase workflows and complicated git histories.
- Supports of multi-authors for one commit through configurable [trailers key values](https://git.wiki.kernel.org/index.php/CommitMessageConventions).
- Built-in parser for turning [trailers key values](https://zerokspot.com/weblog/2020/10/24/git-commit-messages-with-attributes/) into metadata.

## Requirements

Python 3.9 or higher.

## Installation

```bash
$ pip install generate-changelog
```

## Usage

Create a default configuration file.

```bash
$ generate-changelog --generate-config
```

This creates a file named `.changelog-config.yaml`. You can make changes to the default configuration.

Generate your changelog via:

```bash
$ generate-changelog
```

## GitHub Action

### Inputs

- `config_file` Path to the config file if it is not one of the defaults.
- `starting_tag` Starting tag to generate a changelog from. Default is to start from the last tag in the current change log.
- `skip_output_pipeline` Do not generate or update the CHANGELOG, but still return the release hint.
- `branch_override` Override the current branch for release hint decisions.

### Outputs

- `release_hint` The suggested release type for the current or `branch_override` branch.

### Generated files

The changelog file is written based on the configuration and value of the `branch_override` input.
This file is not added to your Git repo. 
You must add and commit it if you want to keep it.

### Example usage

```yaml
on: [push]

jobs:
  sample_job:
    runs-on: ubuntu-latest
    name: Just an example
    steps:
      - name: Generate changelog and release hint
        id: changelog
        uses: callowayproject/generate-changelog@v0
        with:
          config_file: .changelog-config.yaml
      - name: Use the release hint
        run: echo "The release hint was ${{ steps.changelog.outputs.release_hint }}"
```


<!--end-->
