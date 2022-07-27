# Generating a release hint

## What is a "release hint?"

A release hint provides guidance on if and what type of software release is warranted. The guidance is based on user-defined rules applied to the commit messages included in the release and the files modified.

You can use this release hint as input to your release tooling. 

## How it works

Each release rule is matched against each commit based on how the commit is categorized in the change log and the files the commit effects. There is a hint for if there is a match and if there isn't a match. The highest value of the combination of all the hints is returned based on this order:

1. None
2. alpha
3. beta
4. dev
5. pre-release
6. release-candidate
7. patch
8. minor
9. major

Your rules do not have to support all the values.

## Release Rules

There are four parts to a release rule: `match_result`, `no_match_result`, `grouping` and `path`. Only `match_result` is required, but without a `grouping` or `path` the rule will never work.

### Grouping

The value of the release rule's `grouping` is matched against the commit's value set by the `group_by` configuration. It can match in several ways:

- **string value:** 

a release hint leverages the commit grouping capability to decide whether the changes warrant a new release, and what kind.

- release rules
    - based on `group_by` values (from configuration)
    - group_by values can be set with `commit_classifiers` (from configuration)
    - Also allows for file globbing to determine release type

# If no hint rule matches, this is the result
release_hint_default: "patch" # major, minor, patch or None for no release

# If a rule does not have at least one of grouping or path, and release, the rule is ignored
# If a rule has both grouping and path, both must match
release_hint_rules:
    - grouping: # if grouping is a string, it checks if the string is in the tuple
                # If grouping is a list of strings, it must match the tuple
                # If the last item in the list is a "*" it will match the beginning of the list with the beginning of the tuple
                # If the grouping is None, "*" or missing, it is not used.
    
      path: # A globbing pattern that matches against files included in the commit
            # If path is None, "*" or missing, it is not used
    
      release: # major, minor, patch or None for no release


Generic workflow for releasing software
(Inspired and modified from [Semantic Release](https://semantic-release.gitbook.io/semantic-release/#release-steps))

1. Setup: Create or verify all the conditions to proceed with the release.
   1. Sets up the environment
   2. Raises errors if it can not proceed
   3. Raises warnings if it can proceed, but something is up
   4. Inputs: 
      1. Configuration based on tooling
   5. Outputs: 
      1. None
2. Get last release: Obtain the version number corresponding to the last release.
   1. Inputs:
      1. Configuration depending on tooling
   2. Outputs: 
      1. `last_release_version`: Version number as string
3. Process commits: Filter and process commits since last release, setting metadata and normalizing information.
   1. Inputs:
      1. Path to git repository
      2. Starting git reference (like SHA)
      3. Ending git reference (like HEAD)
      4. Other config depending on tooling
   2. Outputs:
      1. `commits`: Processed commit information as an array of JSON objects
4. Suggest release type: Determine the type of release based on the commits added since the last release.
   1. Inputs:
      1. `commits`: Processed commits since last release as an array of JSON objects
      2. default release type
      3. list of release rules
      4. Other config depending on tooling
   2. Outputs:
      1. `release_hint`: A string
   3. Raises `no-release-required` error if the tool determined no release is necessary. If `commits` is empty, it will raise `no-release-required` error regardless of the default release type.
5. Generate notes: Generate release notes for the commits added since the last release.
   1. Inputs:
      1. `commits`: Processed commits since last release as an array of JSON objects
      2. Other config depending on tooling
   2. Outputs:
      1. `release_notes`: Text of the changes. **Note:** This output is used for other parts of the workflow, but doesn't prohibit updating a CHANGELOG file as part of its execution.
6. Update version: Update the version in one or more files
   1. Inputs:
      1. `last_release_version`: Version number of the last release as a string
      2. update type as string. This could be either a release type such as `patch` or a specific version.
      3. Other config depending on tooling
   2. Outputs:
      1. None
7. Verify release: Verify the release conformity.
   1. Inputs:
      1. Config depending on tooling
   2. Outputs:
      1. None
   3. Raises errors if it can not proceed
   4. Raises warnings if it can proceed, but something is up
8. Create Git tag: Commit (if necessary) and create a Git tag corresponding to the new release version.
   1. Inputs:
      1. Path to git repository
      2. New release version as string
      3. Other config depending on tooling
   2. Outputs:
      1. None
9. Prepare: Prepare and package the release.
   1. Inputs:
      1. Config depending on tooling
   2. Outputs:
      1. None
   3. Raises errors if it can not proceed
   4. Raises warnings if it can proceed, but something is up
10. Publish: Publish the release.
   1. Inputs:
      1. Config depending on tooling
   2. Outputs:
      1. None
   3. Raises errors if it can not proceed
   4. Raises warnings if it can proceed, but something is up
11. Notify: Notify of new releases or errors.

You don't need to implement the workflow in one tool. You may use several tools and methods of triggering steps. Some steps may do nothing in your workflow. Some steps may be manual and others automated. 
