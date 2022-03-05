# Changelog

## 0.3.0 (2022-03-05)

### Updates

- Changed the package name to `generate_changelog`. [Corey Oordt](coreyoordt@gmail.com)    

- Change the configuration file base name to `.changelog-config`. [Corey Oordt](coreyoordt@gmail.com)    


## 0.2.0 (2022-03-05)

### New

- Added release tooling in a Makefile. [Corey Oordt](coreyoordt@gmail.com)    

- Added `Slice` and `FirstRegExMatchPosition` actions. [Corey Oordt](coreyoordt@gmail.com)    
  - `Slice` will slice the input text when called
  - `FirstRegExMatchPosition` will return the position of the first match of the regular expression.

- Added `IncrementalFileInsert` action. [Corey Oordt](coreyoordt@gmail.com)    
  Simplifies incremental change log generation for the output action.

- Added `create_if_missing` option to `ReadFile`. [Corey Oordt](coreyoordt@gmail.com)    
  Allows for the creation of an empty file when trying to read from a non-existent file.

- Added MIT license and entry point config for CLI. [Corey Oordt](coreyoordt@gmail.com)    

### Updates

- Updated command line interface. [Corey Oordt](coreyoordt@gmail.com)    

- Updated configuration. [Corey Oordt](coreyoordt@gmail.com)    
  - Fixed `DEFAULT_IGNORE_PATTERNS` with commas
  - Updated `DEFAULT_STARTING_TAG_PIPELINE` with better pattern
  - Added `chg` to ``DEFAULT_SECTION_PATTERNS`
  - Added `DEFAULT_OUTPUT_PIPELINE` for incremental changes
  - Added `valid_author_tokens` to configuration

- Updated tests for pipelines. [Corey Oordt](coreyoordt@gmail.com)    

- Updates the commit template and rendering. [Corey Oordt](coreyoordt@gmail.com)    

- Updated `eval_if_callable`. [Corey Oordt](coreyoordt@gmail.com)    
  - Will now instantiate actions or pipelines and run them.

- Renamed `GetFirstRegExMatch` to `FirstRegExMatch`. [Corey Oordt](coreyoordt@gmail.com)    

### Fixes

- Fixed the merge handling in git_ops. [Corey Oordt](coreyoordt@gmail.com)    

- Fixed the `include_merges` setting. [Corey Oordt](coreyoordt@gmail.com)    
  Wasn't hooked up with the git_ops module.

- Fixed a bug in the capitalize action. [Corey Oordt](coreyoordt@gmail.com)    
  Used to capitalize the first letter but also convert all other characters to lowercase.

### Other

- Moved `VALID_AUTHOR_TOKENS` from templating to configuration. [Corey Oordt](coreyoordt@gmail.com)    


## 0.1.0 (2022-03-01)

### Other

- Initial commit. [Corey Oordt](coreyoordt@gmail.com)    
