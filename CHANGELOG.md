# Changelog

## 0.9.0 (2022-08-27)

[Compare the full difference.](https://github.com/coordt/generate-changelog/compare/0.8.0...0.9.0)

### Fixes

- Fixed a typing error that impacted tests. [4de2cf7](https://github.com/coordt/generate-changelog/commit/4de2cf78b94461ba4a53b6ea220a601f7fd38dc4)
    
- Fixed typing issues raised by mypy. [7479bb0](https://github.com/coordt/generate-changelog/commit/7479bb05a3082fb50a551ceca207ccbe292f6308)
    
### New

- Added ability to use the current branch in release hint rules. [0965dec](https://github.com/coordt/generate-changelog/commit/0965dec12a93f0fa45ef75a1890e92db4d932b0b)
    
### Other

- [pre-commit.ci] pre-commit autoupdate. [076d1a1](https://github.com/coordt/generate-changelog/commit/076d1a1c16ab2e50fc0f3d190d12407ca5e8691b)
    
  **updates:** - [github.com/PyCQA/flake8: 5.0.2 → 5.0.4](https://github.com/PyCQA/flake8/compare/5.0.2...5.0.4)

- [pre-commit.ci] pre-commit autoupdate. [eb7e105](https://github.com/coordt/generate-changelog/commit/eb7e105876c70be083cc34dc312e58798ba8d6c1)
    
  **updates:** - [github.com/PyCQA/flake8: 4.0.1 → 5.0.2](https://github.com/PyCQA/flake8/compare/4.0.1...5.0.2)



## 0.8.0 (2022-07-29)

[Compare the full difference.](https://github.com/coordt/generate-changelog/compare/0.7.6...0.8.0)

### Fixes

- Fixed the return values of several actions. [f679d62](https://github.com/coordt/generate-changelog/commit/f679d6203ffed04015e438e64422d958d239d038)
    
  - stdout now returns the input string
  - IncrementalFileInsert now returns the input string
### New

- Added release hinting functionality to CLI. [49eccc7](https://github.com/coordt/generate-changelog/commit/49eccc7159a8d046ec38503bb94fc9d56afcb09e)
    
- Added release hinting for commits. [ae4ade8](https://github.com/coordt/generate-changelog/commit/ae4ade88627ded694f515823c331d7c81aa9911c)
    
- Added ability to specify starting tag on the CLI. [ca4928e](https://github.com/coordt/generate-changelog/commit/ca4928ec588ff7956b62770dfbff82058b43a1d2)
    
- Added file processing action docs. [17123a4](https://github.com/coordt/generate-changelog/commit/17123a464a376e0149ca8e8c8ba5dfb6dbce4f43)
    
- Added diff linking and bump2version docs. [6178d2d](https://github.com/coordt/generate-changelog/commit/6178d2dda93fedabdca47f150bbfc3b50847cfa2)
    
- Added group_by configuration docs. [637a91e](https://github.com/coordt/generate-changelog/commit/637a91e55f3b7684879fe58ce8d1dd37a9d22326)
    
- Added typing_extensions requirement. [8abd74a](https://github.com/coordt/generate-changelog/commit/8abd74aa015e1e8082f4ec429531d6d8b10e0ca0)
    
- Added action to publish documentation on tagging. [30c8deb](https://github.com/coordt/generate-changelog/commit/30c8debdc3ca4a0e771c28707baf2f40eed4e03b)
    
### Other

- [pre-commit.ci] pre-commit autoupdate. [9b6c246](https://github.com/coordt/generate-changelog/commit/9b6c246854a3db1ca2eff534399f30c3965278ee)
    
  **updates:** - [github.com/psf/black: 22.3.0 → 22.6.0](https://github.com/psf/black/compare/22.3.0...22.6.0)

- [pre-commit.ci] pre-commit autoupdate. [d77419c](https://github.com/coordt/generate-changelog/commit/d77419c323a91fda00dc804f5c8ae6ca56e52da6)
    
  **updates:** - [github.com/pre-commit/pre-commit-hooks: v4.2.0 → v4.3.0](https://github.com/pre-commit/pre-commit-hooks/compare/v4.2.0...v4.3.0)

- Moved documentation requirements into requirements/docs.txt. [29382e5](https://github.com/coordt/generate-changelog/commit/29382e52648c13304905e5e2a7e4120900c3d71c)
    
- Create codeql-analysis workflow. [0982149](https://github.com/coordt/generate-changelog/commit/09821491f70f7f34fbfb489eae0fc9cec2543643)
    
### Updates

- Updated the readme. [9739ffb](https://github.com/coordt/generate-changelog/commit/9739ffb71b243602b4b19efc6c7dfd06cbb1e170)
    
- Updated the documentation for release hinting. [2302a26](https://github.com/coordt/generate-changelog/commit/2302a269338562c939f75a4dcc78f56278788eb0)
    
- Refactored how the user config and output. [84b54f9](https://github.com/coordt/generate-changelog/commit/84b54f92ed253e57200e0c2625be3d848f5af50b)
    
  - Added new method for getting the user config
  - Added generic output method that is aware of if output should be generated based on the -o flag
- Updated docs. [1bd0f12](https://github.com/coordt/generate-changelog/commit/1bd0f1234492545603f638b72e577cf2fede9e80)
    
- Removed unused configuration setting. [70a6d27](https://github.com/coordt/generate-changelog/commit/70a6d2711df0fbbbcffa50102d82806107515bd5)
    
  - release_hint_default ended up not being used
- Refactored templating to accept a version context. [094fa94](https://github.com/coordt/generate-changelog/commit/094fa94dd4d1aa4d3a8ef73fbf81a013199c673e)
    
- Refactored commit tests into new file. [d21c035](https://github.com/coordt/generate-changelog/commit/d21c03577999b5c5015fc684dd1b150924421ac4)
    
- Renamed render to render_changelog for clarity. [357ba9a](https://github.com/coordt/generate-changelog/commit/357ba9a28fee6d8bb001fa60e567c7fadb4477d9)
    
- Refactored commit processing to its own module. [e285ea5](https://github.com/coordt/generate-changelog/commit/e285ea590ae430881d591c2f4c3e77ecd2317c81)
    
  - All commit processing moved from the templating module to the commits module.
- Refactored a dict into a dataclass. [81c54de](https://github.com/coordt/generate-changelog/commit/81c54ded6268dc0610e216670074bcf462153b6b)
    
  - `get_commits_by_tag` now returns a list of `GitTag` objects
- Updated conventional commit docs. [af237cd](https://github.com/coordt/generate-changelog/commit/af237cd089ecdf1bf42faa81078fa4d47d97af59)
    
- Updated template docs. [ece7da5](https://github.com/coordt/generate-changelog/commit/ece7da5f8e5c4e7a60d7bcd5c45b83125a87979a)
    
- Renamed publish-docs workflow. [549703b](https://github.com/coordt/generate-changelog/commit/549703bdf81fa18762c8cf80af1637da48a63f6a)
    


## 0.7.6 (2022-05-25)

[Compare the full difference.](https://github.com/coordt/generate-changelog/compare/0.7.5...0.7.6)

### Fixes

- Fixes packaging. Now includes the templates!. [e298c03](https://github.com/coordt/generate-changelog/commit/e298c03d685a48266c7562efb912244295fec168)
    

## 0.7.5 (2022-05-24)

[Compare the full difference.](https://github.com/coordt/generate-changelog/compare/0.7.4...0.7.5)

### Updates

- Updated setup.cfg. [0a13c61](https://github.com/coordt/generate-changelog/commit/0a13c614d37d37ffee5b3da01baa8a9e92b2f4b5)
    

## 0.7.4 (2022-05-24)

[Compare the full difference.](https://github.com/coordt/generate-changelog/compare/0.7.3...0.7.4)

### Fixes

- Fixed manifest file. [7a2c8a5](https://github.com/coordt/generate-changelog/commit/7a2c8a582586b23664db76480e609e457dc5e11d)
    
### Updates

- Updated setup.cfg. [fca1d10](https://github.com/coordt/generate-changelog/commit/fca1d101392991e11b9dff851d45369083a990fc)
    
  - Replaces `...HEAD` with appropriate version
  - Sets the minimum required version of Python to 3.7
  - Improved package discovery

## 0.7.3 (2022-05-24)

[Compare the full difference.](https://github.com/coordt/generate-changelog/compare/0.7.2...0.7.3)

### Fixes

- Fixes a bug when generating an incremental changelog. [7cc3c16](https://github.com/coordt/generate-changelog/commit/7cc3c16d46ba64520d4d693c6866d984e588d272)
    

## 0.7.2 (2022-05-24)

[Compare the full difference.](https://github.com/coordt/generate-changelog/compare/0.7.1...0.7.2)

### Updates

- Updates the publish package workflow again. [4434571](https://github.com/coordt/generate-changelog/commit/44345711fca328760f2afcae5bcf702185656b91)
    
## 0.7.1 (2022-05-24)

[Compare the full difference.](https://github.com/coordt/generate-changelog/compare/0.7.0...0.7.1)

### Fixes

- Fixes the publish package workflow. [26743f0](https://github.com/coordt/generate-changelog/commit/26743f0bac632c581e90f4e1186d276298002234)
    
## 0.7.0 (2022-05-24)

[Compare the full difference.](https://github.com/coordt/generate-changelog/compare/0.6.1...0.7.0)

### New

- Added Python 3.7 compatibility. [263c3d6](https://github.com/coordt/generate-changelog/commit/263c3d656653ca834b224c9e109cc6cff091abbe)
    
- Added existence check for configuration file during generation. [9e00e1c](https://github.com/coordt/generate-changelog/commit/9e00e1c67390b2ed414dca2fa28ac87cb6b3d765)
    
  - Asks if you want to overwrite existing configuration
- Added tests for command line interface. [12837b6](https://github.com/coordt/generate-changelog/commit/12837b6e0ed4c5f1815bf25c667cd0a86351886e)
    
- Added tests for conventional commits. [6bac10b](https://github.com/coordt/generate-changelog/commit/6bac10b31c925eb9b40e5f228d19a92d0b32c8de)
    
- Added tests for matching and metadata. [7dac045](https://github.com/coordt/generate-changelog/commit/7dac04502081302fdd7893feab9d55dc627340ef)
    
- Added conventional commit actions. [34615cd](https://github.com/coordt/generate-changelog/commit/34615cd974ab0175acf09496490a00a447a4718e)
    
  - ParseConventionalCommit
  - ParseBreakingChangeFooter
### Other

- Reformatted the changelog output. [b7d0f61](https://github.com/coordt/generate-changelog/commit/b7d0f61a211c687e53c72e6f9f6b8c3db21b989e)
    
- - Updated tests to use new contexts. [b222e96](https://github.com/coordt/generate-changelog/commit/b222e96b70145a3f0485d7d21bb92d5b2edec7cf)
    
### Updates

- Updated documentation. [ec5dc40](https://github.com/coordt/generate-changelog/commit/ec5dc40839c11f853b5550c187d0f9ead33cc06d)
    
- Refactored the template contexts. [c5fbf68](https://github.com/coordt/generate-changelog/commit/c5fbf682752703d510be4442d80dd9cb800d3923)
    
  - Changed `GroupedCommit` to `GroupingContext`
  - Added `ChangelogContext` as a root context for templates.
- Removed the lazy objects. [abd0c96](https://github.com/coordt/generate-changelog/commit/abd0c96586105e210a954267e5901e5730462b2b)
    
- Removed the lazy objects. [75b2d35](https://github.com/coordt/generate-changelog/commit/75b2d3552fd976bf633d7797e2f62fd6ff9eb47f)
    
- Updated write_default_config to write comments. [60e66cd](https://github.com/coordt/generate-changelog/commit/60e66cdb45c4185636ca369868ae3f4b3011b13d)
    
- Updated configuration. [3c288d2](https://github.com/coordt/generate-changelog/commit/3c288d29cb4f1d55172578f25ce3946fef61c32c)
    
  - added `rendered_variables` property
  - added a default variable
  - updated docstrings
  - added default template directory
- Updated changelog configuration. [92d0a43](https://github.com/coordt/generate-changelog/commit/92d0a432a4d560b9588c825720af0f6cd8031b5a)
    
- Updated the rendering for new grouping method. [16dd292](https://github.com/coordt/generate-changelog/commit/16dd292d9a042842f6bcbcb0b0623b49ad1b1b1b)
    
  - Added `resolve_name` and `diff_index` utility methods
  - refactored the `get_context_from_tags` function
  - added `diff_index` function to template context
  - added `group_depth` variable to template context
  - refactored `first_matching` to use the commit_classifiers
  - Updated the `versions.md.jinja`, `section_heading.md.jinja`, and `commit.md.jinja` templates
- Changed the template contexts. [71d4e01](https://github.com/coordt/generate-changelog/commit/71d4e01cb8c0caed81bef91eead948f57c9f04f1)
    
  - `CommitContext` now has a `grouping` tuple
  - Replaced `SectionContext` with `GroupedCommmit`
  - Replaced `VersionContext.sections` with `VersionContext.grouped_commits`
- Changed method of grouping commits within versions. [78d9813](https://github.com/coordt/generate-changelog/commit/78d98136dfb791c420309d239faadcb7b73f803c)
    
  - added `group_by` to configuration
  - added `commit_classifiers` to configuration
  - added `SummaryRegexMatch` as a commit classifier to emulate previous functionality
  - added `MetadataMatch` to use commit metadata to assign to groups

## 0.6.1 (2022-05-02)

[Compare the full difference.](https://github.com/coordt/generate-changelog/compare/0.6.0...0.6.1)

### Fixes

- Fixed Makefile. [7f4384d](https://github.com/coordt/generate-changelog/commit/7f4384d4a38657ed84ffa7470ea95440c17cb322)
    
## 0.6.0 (2022-05-02)

[Compare the full difference.](https://github.com/coordt/generate-changelog/compare/0.5.0...0.6.0)

### Fixes

- Fixed Makefile. [1fa22f9](https://github.com/coordt/generate-changelog/commit/1fa22f9eb37ddf978c9edb71e08c8ae431638155)
    
- Fixed configuraation import. [23d437b](https://github.com/coordt/generate-changelog/commit/23d437bb22c6269d6b9ac3905a2b1dc35fcebf13)
    
- Fixed Python 3.10 spec in workflows. [cacd9e2](https://github.com/coordt/generate-changelog/commit/cacd9e2393c8efe45aecd4a0d1b6fa84b5a32764)
    
- Fixed primary branch name in workflows. [94e4203](https://github.com/coordt/generate-changelog/commit/94e4203f09c33071868b6b8d64f6e7b31c3d4c43)
    
### New

- Added Github Action CI configs. [4737ce8](https://github.com/coordt/generate-changelog/commit/4737ce800378113848edeef46a600d42850773b1)
    
- Added a test for cross-branch tags. [b5a523c](https://github.com/coordt/generate-changelog/commit/b5a523c8b58424b1a7bd0ad1339f30e71e9d6c8a)
    
### Other

- [pre-commit.ci] pre-commit autoupdate. [1e856c7](https://github.com/coordt/generate-changelog/commit/1e856c7ed2be8d1932d80a6b86c4e88ada0022aa)
    
  **updates:** - https://github.com/timothycrosley/isort → https://github.com/PyCQA/isort

- [pre-commit.ci] pre-commit autoupdate. [373c1dd](https://github.com/coordt/generate-changelog/commit/373c1dd87134a0381ccd19f0cf50ff324248b0b0)
    
  **updates:** - https://github.com/timothycrosley/isort → https://github.com/PyCQA/isort

### Updates

- Updated release script. [44d1b93](https://github.com/coordt/generate-changelog/commit/44d1b937ad41a1c964ef5fa57531a3967ff25814)
    
- Updated documentation. [9b56b4a](https://github.com/coordt/generate-changelog/commit/9b56b4a0bfe90bfd46eae58aa233abf1db18bc1f)
    
- Changed pre-commit to exclude tests. [0f9e56d](https://github.com/coordt/generate-changelog/commit/0f9e56dd09bde764583ff832c35b5ff49bada6cf)
    
- Changed and standardized to term 'summary'. [2bd7634](https://github.com/coordt/generate-changelog/commit/2bd7634b9202407fe55c6e65f67331d6e41602b4)
    
- Refactored context into new module. [5b1e921](https://github.com/coordt/generate-changelog/commit/5b1e92160c5878a02edf5ae0993ad866322f3e9d)
    
- Removed variable start string difference from pipeline env. [5dc5903](https://github.com/coordt/generate-changelog/commit/5dc59039da3a8c10fdfd84874da969d7c3f1f188)
    
  - Didn't make sense to have a different method of specifying variables in the pipeline from the default.
## 0.5.0 (2022-03-15)

[Compare the full difference.](https://github.com/coordt/generate-changelog/compare/0.4.0...0.5.0)

### New

- Added a minimal readme. [8ba2ec1](https://github.com/coordt/generate-changelog/commit/8ba2ec1133be3515720dbd6a20d2689ef4c96bba)
    
- Added issue parsing actions. [95e0e35](https://github.com/coordt/generate-changelog/commit/95e0e35dd49ba85b1f5befc327b92c7ac2493ecc)
    
  - ParseIssue: base class and generic issue parser
  - ParseGitHubIssue: parse GitHub issue patterns
  - ParseJiraIssue: parse Jira issue patterns
  - ParseAzureBoardIssue: parse Azure board issue patterns
- Added initial documentation for actions. [14ba3be](https://github.com/coordt/generate-changelog/commit/14ba3be844bb2af41c8e14d6d5d90bcfe730da6a)
    
### Updates

- Renamed processors module to actions. [99284e3](https://github.com/coordt/generate-changelog/commit/99284e3d42a35f91d17d417bae948c35364de49f)
    
## 0.4.0 (2022-03-13)

[Compare the full difference.](https://github.com/coordt/generate-changelog/compare/0.3.0...0.4.0)

### Fixes

- Fixed missing variables in render context. [0bed08e](https://github.com/coordt/generate-changelog/commit/0bed08eab48fd24a55b63b010c7cc8e665447cac)
    
### New

- Added support for `__contains__` in registry. [848421d](https://github.com/coordt/generate-changelog/commit/848421d8123738f7c876875301c114f4c8bc1087)
    
- Added action registry. [a363c25](https://github.com/coordt/generate-changelog/commit/a363c25588f2dff507150776d58fc4d876b1220c)
    
  - Accessing the registry ensures the built-in actions are loaded.
- Added changelog configuration and templates. [32f4f23](https://github.com/coordt/generate-changelog/commit/32f4f23635b06839c19b3f811a1e2058dc81764e)
    
- Added a `previous_tag` attribute to the version context. [5760576](https://github.com/coordt/generate-changelog/commit/576057668dfc90eba19070d6f94d14d60ca9ada6)
    
- Added lazy evaluation of Jinja environments. [f57d007](https://github.com/coordt/generate-changelog/commit/f57d007f71105f4f4d6e6d1a005f39e71f816dfe)
    
  - This allows for proper setup of the configuration.
- Added accessor for current configuration. [83a728f](https://github.com/coordt/generate-changelog/commit/83a728f6c09bf7c618f031820e35267504f5f866)
    
  - `get_config()` will instantiate a new configuration or return the existing configuration.
### Updates

- Updated processors doc strings. [9102ec7](https://github.com/coordt/generate-changelog/commit/9102ec757788f3210d381e57d41e64cd57d24718)
    
- Updated configuration doc strings. [ff818af](https://github.com/coordt/generate-changelog/commit/ff818aff84744fdea955e26f539ad9c8a3a953d2)
    
- Updated data_merge doc strings. [2840242](https://github.com/coordt/generate-changelog/commit/28402420496a0fb6403e7bed58eb0d74ee237457)
    
- Updated git_ops and lazy doc strings. [26ecd54](https://github.com/coordt/generate-changelog/commit/26ecd54bb3f2f38c1c2198afde0cedf296a18120)
    
- Updated pipeline doc strings. [2a2c052](https://github.com/coordt/generate-changelog/commit/2a2c05296541c71373b4f8d59ced3fd0d2fc4f35)
    
- Updated templating doc strings. [b942302](https://github.com/coordt/generate-changelog/commit/b942302c879f5dabfc0553f103d80864bd7ebadf)
    
- Updated utility doc strings. [a7ae93f](https://github.com/coordt/generate-changelog/commit/a7ae93f757792ebf4cabf5c51fc353f65d593fef)
    
- Removed ActionSpec. [29942ac](https://github.com/coordt/generate-changelog/commit/29942acbde3b7e4b9b9a68e2b840b38417643174)
    
  - It was unnecessary. Now Action classes are instantiated directly.
- Removed author rendering from commits. [e44de67](https://github.com/coordt/generate-changelog/commit/e44de6784a7e26422679a5597b4e21322ac49f08)
    
## 0.3.0 (2022-03-05)

[Compare the full difference.](https://github.com/coordt/generate-changelog/compare/0.2.0...0.3.0)

### Updates

- Changed the package name to `generate_changelog`. [1e4945a](https://github.com/coordt/generate-changelog/commit/1e4945adc762c20b9c450cd7234d9791897459e2)
    
- Change the configuration file base name to `.changelog-config`. [ac3fc2e](https://github.com/coordt/generate-changelog/commit/ac3fc2e2fb4fd609b9f0a995a7ef95f7b77d53dd)
    
## 0.2.0 (2022-03-05)

[Compare the full difference.](https://github.com/coordt/generate-changelog/compare/0.1.0...0.2.0)

### Fixes

- Fixed the merge handling in git_ops. [e9666f5](https://github.com/coordt/generate-changelog/commit/e9666f519fd2edea9c2b8e3fa97b4b9ee1d10042)
    
- Fixed the `include_merges` setting. [cf6c4f2](https://github.com/coordt/generate-changelog/commit/cf6c4f2bba26f3e50010fbf424ad4326d1fe45bc)
    
  Wasn't hooked up with the git_ops module.
- Fixed a bug in the capitalize action. [8fee744](https://github.com/coordt/generate-changelog/commit/8fee744bfedfea5850f7fa61d36f202815514210)
    
  Used to capitalize the first letter but also convert all other characters to lowercase.
### New

- Added release tooling in a Makefile. [8064d3d](https://github.com/coordt/generate-changelog/commit/8064d3de42435b65a61b9686231973240f80f558)
    
- Added `Slice` and `FirstRegExMatchPosition` actions. [19cf66e](https://github.com/coordt/generate-changelog/commit/19cf66ebacc275c4b15fb1b5371ca9190a4b85f7)
    
  - `Slice` will slice the input text when called
  - `FirstRegExMatchPosition` will return the position of the first match of the regular expression.
- Added `IncrementalFileInsert` action. [d40ba36](https://github.com/coordt/generate-changelog/commit/d40ba3624ae01350b63ec15613838c8d81825dd0)
    
  Simplifies incremental change log generation for the output action.
- Added `create_if_missing` option to `ReadFile`. [8d1eaef](https://github.com/coordt/generate-changelog/commit/8d1eaefaa3868d3322453ceeafa2a416a95e3a7a)
    
  Allows for the creation of an empty file when trying to read from a non-existent file.
- Added MIT license and entry point config for CLI. [579134b](https://github.com/coordt/generate-changelog/commit/579134bd497362c88e82593eb7fd2fe83a04718c)
    
### Other

- Moved `VALID_AUTHOR_TOKENS` from templating to configuration. [dc93fc3](https://github.com/coordt/generate-changelog/commit/dc93fc324a02cfda0aed53d2648726c6be130074)
    
### Updates

- Updated command line interface. [d8abd8d](https://github.com/coordt/generate-changelog/commit/d8abd8d3a8b1ab6d112423ee4ea2408f36a8b802)
    
- Updated configuration. [a8ded3f](https://github.com/coordt/generate-changelog/commit/a8ded3f3c8c20f5117f95ca3d0020f326d112db9)
    
  - Fixed `DEFAULT_IGNORE_PATTERNS` with commas
  - Updated `DEFAULT_STARTING_TAG_PIPELINE` with better pattern
  - Added `chg` to ``DEFAULT_SECTION_PATTERNS`
  - Added `DEFAULT_OUTPUT_PIPELINE` for incremental changes
  - Added `valid_author_tokens` to configuration
- Updated tests for pipelines. [e280fb8](https://github.com/coordt/generate-changelog/commit/e280fb863d98450f48c35d7f2382770813271210)
    
- Updates the commit template and rendering. [e76fd3a](https://github.com/coordt/generate-changelog/commit/e76fd3ace753fc3244c38af89adcf589354e5b0f)
    
- Updated `eval_if_callable`. [ebab2cf](https://github.com/coordt/generate-changelog/commit/ebab2cf34f98cb06bfb485a8eb2c44717aa4f0be)
    
  - Will now instantiate actions or pipelines and run them.
- Renamed `GetFirstRegExMatch` to `FirstRegExMatch`. [82b907f](https://github.com/coordt/generate-changelog/commit/82b907faf481f1c7218cc29c82d7072a0014314f)
    
## 0.1.0 (2022-03-01)

[Compare the full difference.](https://github.com/coordt/generate-changelog/compare/None...0.1.0)

### Other

- Initial commit. [41ab840](https://github.com/coordt/generate-changelog/commit/41ab8402b7cd59f4d48da528f92664e4482b962d)
