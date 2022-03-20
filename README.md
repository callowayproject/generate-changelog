# Generate Changelog

Use your commit log to make a beautiful changelog file.

## Features

- Configurable to adapt to your changelog preferences.
- Filter out commits and tags based on regular expression matching.
- Classify commit messages into sections such as "New", "Fixes", and "Changes".
- Templated using [Jinja](https://jinja.palletsprojects.com/en/3.0.x/) templates.
- Rewrite commit summary or commit body using pipelines of actions.
- Supports your merge or rebase workflows and complicated git histories.
- Supports full or incremental changelog generation.
- Parses [trailers key values](https://zerokspot.com/weblog/2020/10/24/git-commit-messages-with-attributes/)
- Supports of multi-authors for one commit through configurable [trailers key values](https://git.wiki.kernel.org/index.php/CommitMessageConventions)

## Requirements

Python 3.8 or higher.

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
