# Conventional Commits

- https://www.conventionalcommits.org
- How to group breaking changes?

Commit classifiers:
- list of actions that set the commit type
- first one that matches, sets the commit type


Change the organization of the commits to be version

Have a version-commit sorting configuration



Add metadata to each commit
    - type
    - scope (optional)
    - has_breaking_change (optional)
    - breaking_changes (optional)

- subject_pipeline

type
opt scope (multi-delimiter: "/", "\", ",")
description

- body_pipeline

parse BREAKING CHANGE: to metadata as a trailer
