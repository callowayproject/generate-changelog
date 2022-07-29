# Generate Changelog

<!-- start badges -->
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/coordt/generate-changelog/master.svg)](https://results.pre-commit.ci/latest/github/coordt/generate-changelog/master)
[![Coverage Status](https://coveralls.io/repos/github/coordt/generate-changelog/badge.svg?branch=master)](https://coveralls.io/github/coordt/generate-changelog?branch=master)
Use your commit log to make a beautiful changelog file.
<!-- end badges -->

- [Documentation](https://coordt.github.io/generate-changelog/)
- [GitHub](https://github.com/coordt/generate-changelog)

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

Python 3.7 or higher.

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
