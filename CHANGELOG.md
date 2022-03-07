# Changelog

## Unreleased (2022-03-07)

[Compare the full difference.](https://github.com/coordt/generate-changelog/compare/0.3.0...HEAD)

### New

- Added a `previous_tag` attribute to the version context. [5760576](https://github.com/coordt/generate-changelog/commit/576057668dfc90eba19070d6f94d14d60ca9ada6)
    

- Added lazy evaluation of Jinja environments. [f57d007](https://github.com/coordt/generate-changelog/commit/f57d007f71105f4f4d6e6d1a005f39e71f816dfe)
    
  - This allows for proper setup of the configuration.

- Added accessor for current configuration. [83a728f](https://github.com/coordt/generate-changelog/commit/83a728f6c09bf7c618f031820e35267504f5f866)
    
  - `get_config()` will instantiate a new configuration or return the existing configuration.

### Updates

- Removed author rendering from commits. [e44de67](https://github.com/coordt/generate-changelog/commit/e44de6784a7e26422679a5597b4e21322ac49f08)
    

## 0.3.0 (2022-03-05)

[Compare the full difference.](https://github.com/coordt/generate-changelog/compare/0.2.0...0.3.0)

### Updates

- Changed the package name to `generate_changelog`. [1e4945a](https://github.com/coordt/generate-changelog/commit/1e4945adc762c20b9c450cd7234d9791897459e2)
    

- Change the configuration file base name to `.changelog-config`. [ac3fc2e](https://github.com/coordt/generate-changelog/commit/ac3fc2e2fb4fd609b9f0a995a7ef95f7b77d53dd)
    

## 0.2.0 (2022-03-05)

[Compare the full difference.](https://github.com/coordt/generate-changelog/compare/0.1.0...0.2.0)

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
    

### Fixes

- Fixed the merge handling in git_ops. [e9666f5](https://github.com/coordt/generate-changelog/commit/e9666f519fd2edea9c2b8e3fa97b4b9ee1d10042)
    

- Fixed the `include_merges` setting. [cf6c4f2](https://github.com/coordt/generate-changelog/commit/cf6c4f2bba26f3e50010fbf424ad4326d1fe45bc)
    
  Wasn't hooked up with the git_ops module.

- Fixed a bug in the capitalize action. [8fee744](https://github.com/coordt/generate-changelog/commit/8fee744bfedfea5850f7fa61d36f202815514210)
    
  Used to capitalize the first letter but also convert all other characters to lowercase.

### Other

- Moved `VALID_AUTHOR_TOKENS` from templating to configuration. [dc93fc3](https://github.com/coordt/generate-changelog/commit/dc93fc324a02cfda0aed53d2648726c6be130074)
    

## 0.1.0 (2022-03-01)

[Compare the full difference.](https://github.com/coordt/generate-changelog/compare/None...0.1.0)

### Other

- Initial commit. [41ab840](https://github.com/coordt/generate-changelog/commit/41ab8402b7cd59f4d48da528f92664e4482b962d)
    
