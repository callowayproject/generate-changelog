# Changelog

## 0.16.0 (2025-05-30)

[Compare the full difference.](https://github.com/callowayproject/generate-changelog/compare/0.15.0...0.16.0)

### Fixes

- Fix output variable name in bump-version workflow. [afd6d62](https://github.com/callowayproject/generate-changelog/commit/afd6d62ffdf44c37582ec8616162f9de91cc820b)

  Replaced incorrect occurrences of `$GITHUB_OUTPUTS` with `$GITHUB_OUTPUT` to properly set outputs in the workflow. This fixes potential issues with downstream steps relying on these outputs.

### New

- Add Python version check in `IndentedLoggerAdapter` for type handling. [0fc89d5](https://github.com/callowayproject/generate-changelog/commit/0fc89d527a3cfe59a3d3e941947c76f9037b7b44)

- Add `MDFormat` action for changelog markdown formatting. [cd66f37](https://github.com/callowayproject/generate-changelog/commit/cd66f37c6151d3b5752e387fca29ef9058bee8b0)

- Add `MDFormat` action for formatting markdown files. [d9c7a01](https://github.com/callowayproject/generate-changelog/commit/d9c7a0192ff9f99c43eedd5c1d5c5141f4bb41e7)

  - Introduced a new `MDFormat` dataclass to enable markdown file formatting using `mdformat`.
  - Updates include reading, formatting, and saving content back to the file.

- Add `mdformat` dependency and update `uv.lock`. [45525cf](https://github.com/callowayproject/generate-changelog/commit/45525cf63d80205bd087efa0bfb788ebf8c97dab)

  - Included `mdformat>=0.7.22` in `pyproject.toml`.
  - Updated `uv.lock` to reflect dependency changes and updated metadata.

### Other

- [pre-commit.ci] auto fixes from pre-commit.com hooks. [74a2cc2](https://github.com/callowayproject/generate-changelog/commit/74a2cc2cb68b0d861497aeb4bc4868c54b41bf09)

  for more information, see https://pre-commit.ci

- Bump astral-sh/setup-uv from 5 to 6. [4d08932](https://github.com/callowayproject/generate-changelog/commit/4d089325060250e74f8cb27d8a1af0e40f19b70a)

  Bumps [astral-sh/setup-uv](https://github.com/astral-sh/setup-uv) from 5 to 6.

  - [Release notes](https://github.com/astral-sh/setup-uv/releases)
  - [Commits](https://github.com/astral-sh/setup-uv/compare/v5...v6)

  ______________________________________________________________________

  **updated-dependencies:** - dependency-name: astral-sh/setup-uv
  dependency-version: '6'
  dependency-type: direct:production
  update-type: version-update:semver-major

  **signed-off-by:** dependabot[bot] <support@github.com>

- [pre-commit.ci] pre-commit autoupdate. [3c020a4](https://github.com/callowayproject/generate-changelog/commit/3c020a46d041a5db393dc9e7a87983ea72165f37)

  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.11.6 → v0.11.11](https://github.com/astral-sh/ruff-pre-commit/compare/v0.11.6...v0.11.11)

- [pre-commit.ci] pre-commit autoupdate. [2fb4d43](https://github.com/callowayproject/generate-changelog/commit/2fb4d43918ecbfe37509d60b6d652165bff8c584)

  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.11.4 → v0.11.6](https://github.com/astral-sh/ruff-pre-commit/compare/v0.11.4...v0.11.6)

### Updates

- Improve error handling and test coverage for pipeline actions. [07a1780](https://github.com/callowayproject/generate-changelog/commit/07a17807bbe7566d17b9ec5a266d0a66741a169f)

  - Added logging for missing action imports; default to `noop_func` with a warning.
  - Updated `noop_func` to accept both positional and keyword arguments.
  - Improved `Action` class error handling when setting `action_function`.
  - Enhanced CLI tests by organizing them in a class for better structure and readability.
  - Added new unit tests for missing action function fallback.

- Update workflows to adjust docs preview and publishing steps. [04efac2](https://github.com/callowayproject/generate-changelog/commit/04efac213ed00a32d911541b3e8b84bb6ae93be9)

  - Added `Build and publish docs preview` step to `publish-docs-preview.yaml`.
  - Removed redundant `Build and publish docs preview` step from `publish-docs.yaml`.

- Update README and bumpversion config for changelog versioning. [c50bc90](https://github.com/callowayproject/generate-changelog/commit/c50bc90fbec5bdc8a7b6f398a6461dc708f46c58)

  Added README.md to bumpversion configuration to ensure version updates. Also corrected the changelog action version in README from v1 to v0.

## 0.15.0 (2025-04-13)

[Compare the full difference.](https://github.com/callowayproject/generate-changelog/compare/0.14.0...0.15.0)

### Fixes

- Fixed workflows. [e314026](https://github.com/callowayproject/generate-changelog/commit/e314026e460854c14b041e70a6511fe21cb07dae)

  - Replaced custom setup-git action with published action
  - fixed docker source in action

- Fix bug in bump-version-preview.yaml. [b3d5106](https://github.com/callowayproject/generate-changelog/commit/b3d5106b3c67d3a1beadb8aa3f97358aba82d151)

  The dry-run of bump-my-version requires the CHANGELOG.md to have an 0.15.0 header

- Fix: bump-version-preview and debugging. [a684bcc](https://github.com/callowayproject/generate-changelog/commit/a684bcc7224bf3384a8d999aaa46e2d73570a040)

- Fixed docstring rendering. [cc9f7eb](https://github.com/callowayproject/generate-changelog/commit/cc9f7eb77b765316357e55814fb7eb00087bb732)

- Fixed bump-version.yaml workflow. [8bdbf11](https://github.com/callowayproject/generate-changelog/commit/8bdbf110431516e64736e57c24776d1719f034d1)

  - Added contents: write permission for committing and pushing
  - Added missing `uv` step

### New

- Added release hint debuging report to GitHub action output. [4da1360](https://github.com/callowayproject/generate-changelog/commit/4da1360273a59bfd68a73097b8f5af3d0c7fcf30)

- Add support for generating debug reports in release hints. [f045d37](https://github.com/callowayproject/generate-changelog/commit/f045d3747767eeb0788c254b67d3a6e6286d67ec)

  Introduced a `report_path` configuration option to write detailed release hint reports to a file. Enhanced logging and report generation, modularized outputs with `output_report`, and added a CLI option `--debug-report` to configure the report file path. Adjusted test cases and imports to accommodate changes.

- Added workflow_call to build_python workflow. [6a83ef0](https://github.com/callowayproject/generate-changelog/commit/6a83ef090aaadad05bd1f6a3dded3875068c2a6d)

- Add concurrency control to GitHub Actions workflows. [e29fcee](https://github.com/callowayproject/generate-changelog/commit/e29fcee0de0f4dd9dea51611a7318d5b98a40d1a)

  Added concurrency groups to "bump-version-preview" and "publish-docs" workflows to prevent overlapping runs. This ensures cleaner and more reliable workflow executions by canceling redundant jobs.

### Other

- [pre-commit.ci] pre-commit autoupdate. [97a227d](https://github.com/callowayproject/generate-changelog/commit/97a227d6351f31d3d0938ff1cda30234a8a3b542)

  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.11.3 → v0.11.4](https://github.com/astral-sh/ruff-pre-commit/compare/v0.11.3...v0.11.4)

- Enable manual workflow triggering and add build provenance. [bfee4b3](https://github.com/callowayproject/generate-changelog/commit/bfee4b39dbfffc887f8942966e7f0d72b3ce0799)

  Added `workflow_dispatch` to allow manual triggering of the workflow. Included additional permissions and steps to support build provenance attestation via GitHub Actions. This improves the security and flexibility of the build process.

### Updates

- Refactored verbose release hint logging. [c5b3001](https://github.com/callowayproject/generate-changelog/commit/c5b3001f9424819c6b0922d08f998065a5f20d93)

- Refactor release hint logic and add indented logger. [529ae78](https://github.com/callowayproject/generate-changelog/commit/529ae78b38ed65bf3ba3f8e4768ea8405bc98271)

  Refactored `ReleaseRule` to return structured results and updated related tests. Introduced `IndentedLoggerAdapter` for structured, indented logging and integrated it into the change log generation process. Enhanced CLI with verbosity options and improved logging outputs for better traceability.

- Update release workflows. [692705d](https://github.com/callowayproject/generate-changelog/commit/692705d933491f4ee17999780ce022a84b103a22)

  Now they are callable from the build-python workflow

- Update build workflow with release jobs and input support. [a823f51](https://github.com/callowayproject/generate-changelog/commit/a823f51a9ceb2b2e229434c5cb25a8a0988a9864)

  Added optional `ref` input for workflow_dispatch to support flexible checkouts. Introduced additional jobs for container, GitHub, and PyPI releases, enhancing the release process automation. Adjusted triggers to exclude tag pushes prefixed with 'v'.

## 0.14.0 (2025-04-03)

[Compare the full difference.](https://github.com/callowayproject/generate-changelog/compare/0.13.0...0.14.0)

### Fixes

- Fixed typo in test workflow. [d451948](https://github.com/callowayproject/generate-changelog/commit/d451948a5979bbc9cce62cc981683e0a9db56c15)

- Fix dependabot config. [70d91cf](https://github.com/callowayproject/generate-changelog/commit/70d91cfd72f0f00ad006143c916239cb8f04a679)

### New

- Add non-root user and update Dockerfile metadata. [a38b154](https://github.com/callowayproject/generate-changelog/commit/a38b154996e7c151cddb65f1cd36af129877485f)

  Introduced a non-root user with configurable UID and GID for better security and flexibility. Updated Dockerfile metadata to include authors, creation date, license, and improved labeling for compliance with OCI standards.

- Add ref container tag when triggered by workflow dispatch. [31d24c7](https://github.com/callowayproject/generate-changelog/commit/31d24c77c5034da83dd389168bf44daf4e754cde)

- Add dependabot config. [670c42b](https://github.com/callowayproject/generate-changelog/commit/670c42b3f1acc9c9213041a2475ae052efaf5c9b)

- Added workflow_dispatch as a trigger for building containers. [cc4c027](https://github.com/callowayproject/generate-changelog/commit/cc4c0275cc003636453143bfe71a19a7c268008d)

- Added name to build container workflow. [428788f](https://github.com/callowayproject/generate-changelog/commit/428788f124617a831970b0b225b55a0e0da7c58d)

- Adds docker building. [4c47587](https://github.com/callowayproject/generate-changelog/commit/4c47587aef298c70cfc3759c987d47ba68dd471c)

- Added moveable version tags for github actions. [ee676a9](https://github.com/callowayproject/generate-changelog/commit/ee676a96f7aed141b90a7779a54a799c48c6161c)

### Other

- Upgrade GitHub Actions to latest stable versions. [165f157](https://github.com/callowayproject/generate-changelog/commit/165f1573d18835d36bada5dfd444ecb9378d6fe9)

  Updated actions in workflows to use newer versions, including CodeQL actions (v3), Codecov action (v5), and GitHub release action (v2). This ensures compatibility, access to new features, and improved performance.

- [pre-commit.ci] pre-commit autoupdate. [410317c](https://github.com/callowayproject/generate-changelog/commit/410317ce61fd42347a76d74e13edd6c69bc703d1)

  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.9.6 → v0.11.2](https://github.com/astral-sh/ruff-pre-commit/compare/v0.9.6...v0.11.2)

- Modularize GitHub workflows and streamline release process. [61bedea](https://github.com/callowayproject/generate-changelog/commit/61bedeae62e310d88c490da242452d4aed6f8702)

  Reorganized and consolidated workflows for clarity and efficiency. Deprecated unnecessary workflows like `bumpversion.yaml` and `release.yaml`, introduced modular workflows (e.g., `build-python.yaml`, `release-pypi.yaml`), and ensured consistent dependency and Python setup across jobs. Enhanced documentation and test workflows for better alignment with project needs.

- Switch to Hatch for build system and update project configuration. [f32d026](https://github.com/callowayproject/generate-changelog/commit/f32d02623fb5cdd39ad2ce72d717947544a4e5a3)

  - Replaced setuptools with Hatch as the build system, updating related configurations in `pyproject.toml`.
  - Adjusted license declaration, versioning setup, and package management to align with Hatch's conventions.
  - Included changes to `bumpversion` workflow for consistency.

- Fies container tag on workflow_dispatch. [7edaef4](https://github.com/callowayproject/generate-changelog/commit/7edaef4929ea33dd2936fded2b0b418efadc2e0e)

- [pre-commit.ci] pre-commit autoupdate. [736ddfa](https://github.com/callowayproject/generate-changelog/commit/736ddfad57860264b57cc486adc89bcbac2ae5d4)

  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.8.6 → v0.9.6](https://github.com/astral-sh/ruff-pre-commit/compare/v0.8.6...v0.9.6)

### Updates

- Rename and simplify action to setup-git. [fc64f9b](https://github.com/callowayproject/generate-changelog/commit/fc64f9b970d725c3103f6b16a0a2d0591ce32766)

  Removed Python setup steps to focus solely on Git configuration. Updated Git user email and name setup to dynamically use GitHub actor details for improved accuracy.

- Rename setup python and git action. [237f460](https://github.com/callowayproject/generate-changelog/commit/237f460a959eb39b7b034a8be09952fdeaf38ef2)

- Changes the ocker image used for the action. [5b76d03](https://github.com/callowayproject/generate-changelog/commit/5b76d03bfa12a443f34859e1b2a763f3face07a0)

- Modify release hint workflow. [63fca08](https://github.com/callowayproject/generate-changelog/commit/63fca085c29d4ab896fddd2040509dc9f44f2770)

- Refactored the PR workflow. [5c9cc84](https://github.com/callowayproject/generate-changelog/commit/5c9cc84081dc7b401c252ad5fe7f6661942d1d6a)

- Update workflows. [01e24e4](https://github.com/callowayproject/generate-changelog/commit/01e24e44447834c8dfa027b0d754a709e6745c9f)

  Enhanced the GitTag class docstring for clarity and detailed explanation of attributes. Updated GitHub workflows to remove unnecessary PAT tokens, upgrade dependencies, and streamline configurations for package building and artifact downloading.

## 0.13.0 (2025-02-16)

[Compare the full difference.](https://github.com/callowayproject/generate-changelog/compare/0.12.1...0.13.0)

### New

- Add GitHub Action details and Python dependency lockfile. [bf32a74](https://github.com/callowayproject/generate-changelog/commit/bf32a74d036e3ccbc4f59e3dd9bdbed573b71c7c)

  Updated the README to include configuration and usage instructions for the new GitHub Action. Added the `uv.lock` file to track Python dependencies for reproducible builds. These changes improve documentation and enhance dependency management.

- Add GitHub Action to generate and update changelog. [93fc1bc](https://github.com/callowayproject/generate-changelog/commit/93fc1bc1cdfef7af267e2293666379f87fd844c7)

  This commit introduces a new GitHub Action using `generate-changelog` to automate changelog creation or updates. It includes an `action.yml` for configuration, an `entrypoint.sh` script for handling inputs and execution, and a `Dockerfile` to set up the required environment.

### Updates

- Update github action to use uv. [c93a125](https://github.com/callowayproject/generate-changelog/commit/c93a12570ee5c0aeb1ff40bb3ddc47379b43fb61)

- Refactor release rule matching for paths and grouping. [291b925](https://github.com/callowayproject/generate-changelog/commit/291b9253cbc700808aee646f6b7e82bbc9dfc4f7)

  Normalize paths as sequences in the release rule logic, enabling support for multiple path patterns. Refactor tests to improve modularity and readability, ensuring consistency with the updated path handling mechanism. Extend functionality to handle more flexible path and grouping validations.

- Updated the PR workflow. [738cdb0](https://github.com/callowayproject/generate-changelog/commit/738cdb0689429760cbc58a798c8dd78541178f70)

- Refactor dependency groups and update bumpversion config. [dbaa2c8](https://github.com/callowayproject/generate-changelog/commit/dbaa2c8a6cf53f7302339d2a17dac795cfaafebf)

  Renamed `[project.optional-dependencies]` to `[dependency-groups]` for clarity and alignment with updated conventions. Added `Dockerfile` to the bumpversion configuration to ensure version consistency across all relevant files.

## 0.12.1 (2025-01-11)

[Compare the full difference.](https://github.com/callowayproject/generate-changelog/compare/0.12.0...0.12.1)

### Fixes

- Fix: add encoding="utf-8" in file_processing.py. [4b0eda7](https://github.com/callowayproject/generate-changelog/commit/4b0eda7140c406af645895a4ad2d30264c49644d)

### Other

- [pre-commit.ci] pre-commit autoupdate. [8c5c6d1](https://github.com/callowayproject/generate-changelog/commit/8c5c6d1365e8d41b754005ed510a6889f56b7c3a)

  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.8.0 → v0.8.6](https://github.com/astral-sh/ruff-pre-commit/compare/v0.8.0...v0.8.6)

## 0.12.0 (2024-11-26)

[Compare the full difference.](https://github.com/callowayproject/generate-changelog/compare/0.11.0...0.12.0)

### New

- Added additional files to documentation. [6836603](https://github.com/callowayproject/generate-changelog/commit/68366035abff38e98d79f501bc9aeab233da890e)

### Updates

- Changed the documentation generator from Sphinx to MkDocs. [770c70d](https://github.com/callowayproject/generate-changelog/commit/770c70dd5587c032a434b1cceb49e3ae6a5bf727)

## 0.11.0 (2024-11-24)

[Compare the full difference.](https://github.com/callowayproject/generate-changelog/compare/0.10.2...0.11.0)

### Fixes

- Fixed typo in release hint option. [31ad577](https://github.com/callowayproject/generate-changelog/commit/31ad577b5d9d3db0117dad830870e608721a30f7)

### Other

- [pre-commit.ci] pre-commit autoupdate. [5fb1154](https://github.com/callowayproject/generate-changelog/commit/5fb1154a49ce4918f43b58d3e11bb8dcb74e643c)

  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.5.4 → v0.7.4](https://github.com/astral-sh/ruff-pre-commit/compare/v0.5.4...v0.7.4)

- Bump actions/download-artifact from 3 to 4.1.7 in /.github/workflows. [83fc29a](https://github.com/callowayproject/generate-changelog/commit/83fc29aecef68c52f23b8e56ac12f7ea29e41aa7)

  Bumps [actions/download-artifact](https://github.com/actions/download-artifact) from 3 to 4.1.7.

  - [Release notes](https://github.com/actions/download-artifact/releases)
  - [Commits](https://github.com/actions/download-artifact/compare/v3...v4.1.7)

  ______________________________________________________________________

  **updated-dependencies:** - dependency-name: actions/download-artifact
  dependency-type: direct:production

  **signed-off-by:** dependabot[bot] <support@github.com>

### Updates

- Update Python versions in CI workflow. [4b32198](https://github.com/callowayproject/generate-changelog/commit/4b321983463a8e1ee8449e02ebac7c6b41a9c29a)

  Removed support for Python 3.8 and added support for Python 3.13 in the test workflow. This ensures compatibility with the latest Python releases and drops an older version that is now less commonly used.

- Changed framework from Typer to Click. [f08d922](https://github.com/callowayproject/generate-changelog/commit/f08d922c83e17d9c0b6ec4bfb164f3c7d1179238)

- Refactored test locations. [06d7a45](https://github.com/callowayproject/generate-changelog/commit/06d7a458fd14416835563d3fe64974e3fc3bab92)

## 0.10.2 (2024-07-23)

[Compare the full difference.](https://github.com/callowayproject/generate-changelog/compare/0.10.1...0.10.2)

### Other

- [pre-commit.ci] auto fixes from pre-commit.com hooks. [11bf6de](https://github.com/callowayproject/generate-changelog/commit/11bf6de5bd70c47e9a1fa7efc2ae383031bdb281)

  for more information, see https://pre-commit.ci

- [pre-commit.ci] pre-commit autoupdate. [b37195b](https://github.com/callowayproject/generate-changelog/commit/b37195bf1259e7438035aa855480398e051160d4)

  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.3.5 → v0.5.4](https://github.com/astral-sh/ruff-pre-commit/compare/v0.3.5...v0.5.4)

## 0.10.1 (2024-04-06)

[Compare the full difference.](https://github.com/callowayproject/generate-changelog/compare/0.10.0...0.10.1)

### Fixes

- Fixed version hint display triggers. [d013300](https://github.com/callowayproject/generate-changelog/commit/d0133007d82741512af0d644c98f58aa508cd05e)

### Other

- [pre-commit.ci] auto fixes from pre-commit.com hooks. [4a41aa9](https://github.com/callowayproject/generate-changelog/commit/4a41aa92c7539fdb10fdcc4a76b3aa031d02e49b)

  for more information, see https://pre-commit.ci

- [pre-commit.ci] pre-commit autoupdate. [b964e83](https://github.com/callowayproject/generate-changelog/commit/b964e83dd04c9aa0415d96a4670510f61d544ef3)

  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.1.6 → v0.3.5](https://github.com/astral-sh/ruff-pre-commit/compare/v0.1.6...v0.3.5)

- [pre-commit.ci] pre-commit autoupdate. [59030cd](https://github.com/callowayproject/generate-changelog/commit/59030cdcede27f8b0ebc96925b90c187c8f39918)

  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.1.5 → v0.1.6](https://github.com/astral-sh/ruff-pre-commit/compare/v0.1.5...v0.1.6)

- Updating the automation. [ee3299e](https://github.com/callowayproject/generate-changelog/commit/ee3299e3c6ba1088d0807361fcdfaa4b8bcaea31)

- Only run tests if it is a change to Python code. [a665442](https://github.com/callowayproject/generate-changelog/commit/a6654425e9284f1885f17d8ed34819cc80f8202d)

### Updates

- Updated the makefile and the doc automation. [b6da42e](https://github.com/callowayproject/generate-changelog/commit/b6da42e9647024123171d33e1379658950110577)

## 0.10.0 (2023-12-04)

[Compare the full difference.](https://github.com/callowayproject/generate-changelog/compare/0.9.2...0.10.0)

### Fixes

- Fixed bug when in a detatched head state. [1d47e41](https://github.com/callowayproject/generate-changelog/commit/1d47e4198a6f197c9f7287076f62eadbc7a1e7c5)

- Fixed the release automation. [2207ed3](https://github.com/callowayproject/generate-changelog/commit/2207ed33f85d832ced98d06b8bf4cef826a10d8f)

- Fixed test automation. [be6e77d](https://github.com/callowayproject/generate-changelog/commit/be6e77d3d4f5a4e7f42c4a82252acceec05d8878)

- Fixed incorrect URLs. [7e87375](https://github.com/callowayproject/generate-changelog/commit/7e8737523e0379201387c7846fb0ef81e2d23846)

### New

- Added `--branch-override` option. [1f1d68b](https://github.com/callowayproject/generate-changelog/commit/1f1d68b5278031ceff29cca7847b60663ad3bbf4)

  This allows the release hint to use the overridden branch name instead of the current branch

- Added codecov to Workflows. [afd33fd](https://github.com/callowayproject/generate-changelog/commit/afd33fd3990a2286e981303840097033f317475f)

- Added changelog parsing for retrieving notes for a specific version. [75bc35d](https://github.com/callowayproject/generate-changelog/commit/75bc35d76386e305305565f11e3f552cfebe6b9b)

### Other

- [pre-commit.ci] pre-commit autoupdate. [ba75e09](https://github.com/callowayproject/generate-changelog/commit/ba75e090da9ed93053dfff5720fc120fb243e1e0)

  **updates:** - [github.com/psf/black: 23.3.0 → 23.7.0](https://github.com/psf/black/compare/23.3.0...23.7.0)

- [pre-commit.ci] pre-commit autoupdate. [248544a](https://github.com/callowayproject/generate-changelog/commit/248544a7368b59f59a9748bd2604ff66cb825cf7)

  **updates:** - [github.com/pre-commit/mirrors-mypy: v1.2.0 → v1.3.0](https://github.com/pre-commit/mirrors-mypy/compare/v1.2.0...v1.3.0)

- [pre-commit.ci] pre-commit autoupdate. [ce00736](https://github.com/callowayproject/generate-changelog/commit/ce007366ad4f862eb74655661407485093b94b40)

  **updates:** - [github.com/psf/black: 23.1.0 → 23.3.0](https://github.com/psf/black/compare/23.1.0...23.3.0)

- Moved dependency management to pyproject.toml. [03c9242](https://github.com/callowayproject/generate-changelog/commit/03c92421d622b0e4017a8e99cb4387fa6da0e278)

- [pre-commit.ci] pre-commit autoupdate. [b815e58](https://github.com/callowayproject/generate-changelog/commit/b815e58b4ec72850a1ed83d1716d384311c4704a)

  **updates:** - [github.com/PyCQA/isort: 5.10.1 → 5.11.4](https://github.com/PyCQA/isort/compare/5.10.1...5.11.4)

- [pre-commit.ci] pre-commit autoupdate. [1ea58d2](https://github.com/callowayproject/generate-changelog/commit/1ea58d2f6aa0ae66e25806a8605932024e589d4e)

  **updates:** - [github.com/pre-commit/pre-commit-hooks: v4.3.0 → v4.4.0](https://github.com/pre-commit/pre-commit-hooks/compare/v4.3.0...v4.4.0)

- [pre-commit.ci] pre-commit autoupdate. [a188f99](https://github.com/callowayproject/generate-changelog/commit/a188f990009ed0d7e62013d57f00415ea2568713)

  **updates:** - [github.com/pre-commit/mirrors-mypy: v0.982 → v0.990](https://github.com/pre-commit/mirrors-mypy/compare/v0.982...v0.990)

### Updates

- Updated the github action versions. [c353b17](https://github.com/callowayproject/generate-changelog/commit/c353b17b85921ad9820568b264f4a2885859a1cf)

- Updated pre-commit. [ff668af](https://github.com/callowayproject/generate-changelog/commit/ff668af68f77cb9e78cc80e690f44c6d59c1996f)

## 0.9.2 (2022-10-20)

[Compare the full difference.](https://github.com/callowayproject/generate-changelog/compare/0.9.1...0.9.2)

### Fixes

- Fixed a logic error when generating incremental changelogs. [c6781b8](https://github.com/callowayproject/generate-changelog/commit/c6781b820a822881b6366a740e1e56a412814aa6)

## 0.9.1 (2022-10-20)

[Compare the full difference.](https://github.com/callowayproject/generate-changelog/compare/0.9.0...0.9.1)

### Fixes

- Fixed the notes including the header. [292a6b2](https://github.com/callowayproject/generate-changelog/commit/292a6b2154a9c4829d5c8aaa3ebe6ee44a37f590)

### Other

- [pre-commit.ci] pre-commit autoupdate. [17f5074](https://github.com/callowayproject/generate-changelog/commit/17f50747b6605e6334ff8791d6a636d53d0b8275)

  **updates:** - [github.com/psf/black: 22.6.0 → 22.10.0](https://github.com/psf/black/compare/22.6.0...22.10.0)

## 0.9.0 (2022-08-27)

[Compare the full difference.](https://github.com/callowayproject/generate-changelog/compare/0.8.0...0.9.0)

### Fixes

- Fixed a typing error that impacted tests. [4de2cf7](https://github.com/callowayproject/generate-changelog/commit/4de2cf78b94461ba4a53b6ea220a601f7fd38dc4)

- Fixed typing issues raised by mypy. [7479bb0](https://github.com/callowayproject/generate-changelog/commit/7479bb05a3082fb50a551ceca207ccbe292f6308)

### New

- Added ability to use the current branch in release hint rules. [0965dec](https://github.com/callowayproject/generate-changelog/commit/0965dec12a93f0fa45ef75a1890e92db4d932b0b)

### Other

- [pre-commit.ci] pre-commit autoupdate. [076d1a1](https://github.com/callowayproject/generate-changelog/commit/076d1a1c16ab2e50fc0f3d190d12407ca5e8691b)

  **updates:** - [github.com/PyCQA/flake8: 5.0.2 → 5.0.4](https://github.com/PyCQA/flake8/compare/5.0.2...5.0.4)

- [pre-commit.ci] pre-commit autoupdate. [eb7e105](https://github.com/callowayproject/generate-changelog/commit/eb7e105876c70be083cc34dc312e58798ba8d6c1)

  **updates:** - [github.com/PyCQA/flake8: 4.0.1 → 5.0.2](https://github.com/PyCQA/flake8/compare/4.0.1...5.0.2)

## 0.8.0 (2022-07-29)

[Compare the full difference.](https://github.com/callowayproject/generate-changelog/compare/0.7.6...0.8.0)

### Fixes

- Fixed the return values of several actions. [f679d62](https://github.com/callowayproject/generate-changelog/commit/f679d6203ffed04015e438e64422d958d239d038)

  - stdout now returns the input string
  - IncrementalFileInsert now returns the input string

### New

- Added release hinting functionality to CLI. [49eccc7](https://github.com/callowayproject/generate-changelog/commit/49eccc7159a8d046ec38503bb94fc9d56afcb09e)

- Added release hinting for commits. [ae4ade8](https://github.com/callowayproject/generate-changelog/commit/ae4ade88627ded694f515823c331d7c81aa9911c)

- Added ability to specify starting tag on the CLI. [ca4928e](https://github.com/callowayproject/generate-changelog/commit/ca4928ec588ff7956b62770dfbff82058b43a1d2)

- Added file processing action docs. [17123a4](https://github.com/callowayproject/generate-changelog/commit/17123a464a376e0149ca8e8c8ba5dfb6dbce4f43)

- Added diff linking and bump2version docs. [6178d2d](https://github.com/callowayproject/generate-changelog/commit/6178d2dda93fedabdca47f150bbfc3b50847cfa2)

- Added group_by configuration docs. [637a91e](https://github.com/callowayproject/generate-changelog/commit/637a91e55f3b7684879fe58ce8d1dd37a9d22326)

- Added typing_extensions requirement. [8abd74a](https://github.com/callowayproject/generate-changelog/commit/8abd74aa015e1e8082f4ec429531d6d8b10e0ca0)

- Added action to publish documentation on tagging. [30c8deb](https://github.com/callowayproject/generate-changelog/commit/30c8debdc3ca4a0e771c28707baf2f40eed4e03b)

### Other

- [pre-commit.ci] pre-commit autoupdate. [9b6c246](https://github.com/callowayproject/generate-changelog/commit/9b6c246854a3db1ca2eff534399f30c3965278ee)

  **updates:** - [github.com/psf/black: 22.3.0 → 22.6.0](https://github.com/psf/black/compare/22.3.0...22.6.0)

- [pre-commit.ci] pre-commit autoupdate. [d77419c](https://github.com/callowayproject/generate-changelog/commit/d77419c323a91fda00dc804f5c8ae6ca56e52da6)

  **updates:** - [github.com/pre-commit/pre-commit-hooks: v4.2.0 → v4.3.0](https://github.com/pre-commit/pre-commit-hooks/compare/v4.2.0...v4.3.0)

- Moved documentation requirements into requirements/docs.txt. [29382e5](https://github.com/callowayproject/generate-changelog/commit/29382e52648c13304905e5e2a7e4120900c3d71c)

- Create codeql-analysis workflow. [0982149](https://github.com/callowayproject/generate-changelog/commit/09821491f70f7f34fbfb489eae0fc9cec2543643)

### Updates

- Updated the readme. [9739ffb](https://github.com/callowayproject/generate-changelog/commit/9739ffb71b243602b4b19efc6c7dfd06cbb1e170)

- Updated the documentation for release hinting. [2302a26](https://github.com/callowayproject/generate-changelog/commit/2302a269338562c939f75a4dcc78f56278788eb0)

- Refactored how the user config and output. [84b54f9](https://github.com/callowayproject/generate-changelog/commit/84b54f92ed253e57200e0c2625be3d848f5af50b)

  - Added new method for getting the user config
  - Added generic output method that is aware of if output should be generated based on the -o flag

- Updated docs. [1bd0f12](https://github.com/callowayproject/generate-changelog/commit/1bd0f1234492545603f638b72e577cf2fede9e80)

- Removed unused configuration setting. [70a6d27](https://github.com/callowayproject/generate-changelog/commit/70a6d2711df0fbbbcffa50102d82806107515bd5)

  - release_hint_default ended up not being used

- Refactored templating to accept a version context. [094fa94](https://github.com/callowayproject/generate-changelog/commit/094fa94dd4d1aa4d3a8ef73fbf81a013199c673e)

- Refactored commit tests into new file. [d21c035](https://github.com/callowayproject/generate-changelog/commit/d21c03577999b5c5015fc684dd1b150924421ac4)

- Renamed render to render_changelog for clarity. [357ba9a](https://github.com/callowayproject/generate-changelog/commit/357ba9a28fee6d8bb001fa60e567c7fadb4477d9)

- Refactored commit processing to its own module. [e285ea5](https://github.com/callowayproject/generate-changelog/commit/e285ea590ae430881d591c2f4c3e77ecd2317c81)

  - All commit processing moved from the templating module to the commits module.

- Refactored a dict into a dataclass. [81c54de](https://github.com/callowayproject/generate-changelog/commit/81c54ded6268dc0610e216670074bcf462153b6b)

  - `get_commits_by_tag` now returns a list of `GitTag` objects

- Updated conventional commit docs. [af237cd](https://github.com/callowayproject/generate-changelog/commit/af237cd089ecdf1bf42faa81078fa4d47d97af59)

- Updated template docs. [ece7da5](https://github.com/callowayproject/generate-changelog/commit/ece7da5f8e5c4e7a60d7bcd5c45b83125a87979a)

- Renamed publish-docs workflow. [549703b](https://github.com/callowayproject/generate-changelog/commit/549703bdf81fa18762c8cf80af1637da48a63f6a)

## 0.7.6 (2022-05-25)

[Compare the full difference.](https://github.com/callowayproject/generate-changelog/compare/0.7.5...0.7.6)

### Fixes

- Fixes packaging. Now includes the templates!. [e298c03](https://github.com/callowayproject/generate-changelog/commit/e298c03d685a48266c7562efb912244295fec168)

## 0.7.5 (2022-05-24)

[Compare the full difference.](https://github.com/callowayproject/generate-changelog/compare/0.7.4...0.7.5)

### Updates

- Updated setup.cfg. [0a13c61](https://github.com/callowayproject/generate-changelog/commit/0a13c614d37d37ffee5b3da01baa8a9e92b2f4b5)

## 0.7.4 (2022-05-24)

[Compare the full difference.](https://github.com/callowayproject/generate-changelog/compare/0.7.3...0.7.4)

### Fixes

- Fixed manifest file. [7a2c8a5](https://github.com/callowayproject/generate-changelog/commit/7a2c8a582586b23664db76480e609e457dc5e11d)

### Updates

- Updated setup.cfg. [fca1d10](https://github.com/callowayproject/generate-changelog/commit/fca1d101392991e11b9dff851d45369083a990fc)

  - Replaces `...HEAD` with appropriate version
  - Sets the minimum required version of Python to 3.7
  - Improved package discovery

## 0.7.3 (2022-05-24)

[Compare the full difference.](https://github.com/callowayproject/generate-changelog/compare/0.7.2...0.7.3)

### Fixes

- Fixes a bug when generating an incremental changelog. [7cc3c16](https://github.com/callowayproject/generate-changelog/commit/7cc3c16d46ba64520d4d693c6866d984e588d272)

## 0.7.2 (2022-05-24)

[Compare the full difference.](https://github.com/callowayproject/generate-changelog/compare/0.7.1...0.7.2)

### Updates

- Updates the publish package workflow again. [4434571](https://github.com/callowayproject/generate-changelog/commit/44345711fca328760f2afcae5bcf702185656b91)

## 0.7.1 (2022-05-24)

[Compare the full difference.](https://github.com/callowayproject/generate-changelog/compare/0.7.0...0.7.1)

### Fixes

- Fixes the publish package workflow. [26743f0](https://github.com/callowayproject/generate-changelog/commit/26743f0bac632c581e90f4e1186d276298002234)

## 0.7.0 (2022-05-24)

[Compare the full difference.](https://github.com/callowayproject/generate-changelog/compare/0.6.1...0.7.0)

### New

- Added Python 3.7 compatibility. [263c3d6](https://github.com/callowayproject/generate-changelog/commit/263c3d656653ca834b224c9e109cc6cff091abbe)

- Added existence check for configuration file during generation. [9e00e1c](https://github.com/callowayproject/generate-changelog/commit/9e00e1c67390b2ed414dca2fa28ac87cb6b3d765)

  - Asks if you want to overwrite existing configuration

- Added tests for command line interface. [12837b6](https://github.com/callowayproject/generate-changelog/commit/12837b6e0ed4c5f1815bf25c667cd0a86351886e)

- Added tests for conventional commits. [6bac10b](https://github.com/callowayproject/generate-changelog/commit/6bac10b31c925eb9b40e5f228d19a92d0b32c8de)

- Added tests for matching and metadata. [7dac045](https://github.com/callowayproject/generate-changelog/commit/7dac04502081302fdd7893feab9d55dc627340ef)

- Added conventional commit actions. [34615cd](https://github.com/callowayproject/generate-changelog/commit/34615cd974ab0175acf09496490a00a447a4718e)

  - ParseConventionalCommit
  - ParseBreakingChangeFooter

### Other

- Reformatted the changelog output. [b7d0f61](https://github.com/callowayproject/generate-changelog/commit/b7d0f61a211c687e53c72e6f9f6b8c3db21b989e)

- - Updated tests to use new contexts. [b222e96](https://github.com/callowayproject/generate-changelog/commit/b222e96b70145a3f0485d7d21bb92d5b2edec7cf)

### Updates

- Updated documentation. [ec5dc40](https://github.com/callowayproject/generate-changelog/commit/ec5dc40839c11f853b5550c187d0f9ead33cc06d)

- Refactored the template contexts. [c5fbf68](https://github.com/callowayproject/generate-changelog/commit/c5fbf682752703d510be4442d80dd9cb800d3923)

  - Changed `GroupedCommit` to `GroupingContext`
  - Added `ChangelogContext` as a root context for templates.

- Removed the lazy objects. [abd0c96](https://github.com/callowayproject/generate-changelog/commit/abd0c96586105e210a954267e5901e5730462b2b)

- Removed the lazy objects. [75b2d35](https://github.com/callowayproject/generate-changelog/commit/75b2d3552fd976bf633d7797e2f62fd6ff9eb47f)

- Updated write_default_config to write comments. [60e66cd](https://github.com/callowayproject/generate-changelog/commit/60e66cdb45c4185636ca369868ae3f4b3011b13d)

- Updated configuration. [3c288d2](https://github.com/callowayproject/generate-changelog/commit/3c288d29cb4f1d55172578f25ce3946fef61c32c)

  - added `rendered_variables` property
  - added a default variable
  - updated docstrings
  - added default template directory

- Updated changelog configuration. [92d0a43](https://github.com/callowayproject/generate-changelog/commit/92d0a432a4d560b9588c825720af0f6cd8031b5a)

- Updated the rendering for new grouping method. [16dd292](https://github.com/callowayproject/generate-changelog/commit/16dd292d9a042842f6bcbcb0b0623b49ad1b1b1b)

  - Added `resolve_name` and `diff_index` utility methods
  - refactored the `get_context_from_tags` function
  - added `diff_index` function to template context
  - added `group_depth` variable to template context
  - refactored `first_matching` to use the commit_classifiers
  - Updated the `versions.md.jinja`, `section_heading.md.jinja`, and `commit.md.jinja` templates

- Changed the template contexts. [71d4e01](https://github.com/callowayproject/generate-changelog/commit/71d4e01cb8c0caed81bef91eead948f57c9f04f1)

  - `CommitContext` now has a `grouping` tuple
  - Replaced `SectionContext` with `GroupedCommmit`
  - Replaced `VersionContext.sections` with `VersionContext.grouped_commits`

- Changed method of grouping commits within versions. [78d9813](https://github.com/callowayproject/generate-changelog/commit/78d98136dfb791c420309d239faadcb7b73f803c)

  - added `group_by` to configuration
  - added `commit_classifiers` to configuration
  - added `SummaryRegexMatch` as a commit classifier to emulate previous functionality
  - added `MetadataMatch` to use commit metadata to assign to groups

## 0.6.1 (2022-05-02)

[Compare the full difference.](https://github.com/callowayproject/generate-changelog/compare/0.6.0...0.6.1)

### Fixes

- Fixed Makefile. [7f4384d](https://github.com/callowayproject/generate-changelog/commit/7f4384d4a38657ed84ffa7470ea95440c17cb322)

## 0.6.0 (2022-05-02)

[Compare the full difference.](https://github.com/callowayproject/generate-changelog/compare/0.5.0...0.6.0)

### Fixes

- Fixed Makefile. [1fa22f9](https://github.com/callowayproject/generate-changelog/commit/1fa22f9eb37ddf978c9edb71e08c8ae431638155)

- Fixed configuraation import. [23d437b](https://github.com/callowayproject/generate-changelog/commit/23d437bb22c6269d6b9ac3905a2b1dc35fcebf13)

- Fixed Python 3.10 spec in workflows. [cacd9e2](https://github.com/callowayproject/generate-changelog/commit/cacd9e2393c8efe45aecd4a0d1b6fa84b5a32764)

- Fixed primary branch name in workflows. [94e4203](https://github.com/callowayproject/generate-changelog/commit/94e4203f09c33071868b6b8d64f6e7b31c3d4c43)

### New

- Added Github Action CI configs. [4737ce8](https://github.com/callowayproject/generate-changelog/commit/4737ce800378113848edeef46a600d42850773b1)

- Added a test for cross-branch tags. [b5a523c](https://github.com/callowayproject/generate-changelog/commit/b5a523c8b58424b1a7bd0ad1339f30e71e9d6c8a)

### Other

- [pre-commit.ci] pre-commit autoupdate. [1e856c7](https://github.com/callowayproject/generate-changelog/commit/1e856c7ed2be8d1932d80a6b86c4e88ada0022aa)

  **updates:** - https://github.com/timothycrosley/isort → https://github.com/PyCQA/isort

- [pre-commit.ci] pre-commit autoupdate. [373c1dd](https://github.com/callowayproject/generate-changelog/commit/373c1dd87134a0381ccd19f0cf50ff324248b0b0)

  **updates:** - https://github.com/timothycrosley/isort → https://github.com/PyCQA/isort

### Updates

- Updated release script. [44d1b93](https://github.com/callowayproject/generate-changelog/commit/44d1b937ad41a1c964ef5fa57531a3967ff25814)

- Updated documentation. [9b56b4a](https://github.com/callowayproject/generate-changelog/commit/9b56b4a0bfe90bfd46eae58aa233abf1db18bc1f)

- Changed pre-commit to exclude tests. [0f9e56d](https://github.com/callowayproject/generate-changelog/commit/0f9e56dd09bde764583ff832c35b5ff49bada6cf)

- Changed and standardized to term 'summary'. [2bd7634](https://github.com/callowayproject/generate-changelog/commit/2bd7634b9202407fe55c6e65f67331d6e41602b4)

- Refactored context into new module. [5b1e921](https://github.com/callowayproject/generate-changelog/commit/5b1e92160c5878a02edf5ae0993ad866322f3e9d)

- Removed variable start string difference from pipeline env. [5dc5903](https://github.com/callowayproject/generate-changelog/commit/5dc59039da3a8c10fdfd84874da969d7c3f1f188)

  - Didn't make sense to have a different method of specifying variables in the pipeline from the default.

## 0.5.0 (2022-03-15)

[Compare the full difference.](https://github.com/callowayproject/generate-changelog/compare/0.4.0...0.5.0)

### New

- Added a minimal readme. [8ba2ec1](https://github.com/callowayproject/generate-changelog/commit/8ba2ec1133be3515720dbd6a20d2689ef4c96bba)

- Added issue parsing actions. [95e0e35](https://github.com/callowayproject/generate-changelog/commit/95e0e35dd49ba85b1f5befc327b92c7ac2493ecc)

  - ParseIssue: base class and generic issue parser
  - ParseGitHubIssue: parse GitHub issue patterns
  - ParseJiraIssue: parse Jira issue patterns
  - ParseAzureBoardIssue: parse Azure board issue patterns

- Added initial documentation for actions. [14ba3be](https://github.com/callowayproject/generate-changelog/commit/14ba3be844bb2af41c8e14d6d5d90bcfe730da6a)

### Updates

- Renamed processors module to actions. [99284e3](https://github.com/callowayproject/generate-changelog/commit/99284e3d42a35f91d17d417bae948c35364de49f)

## 0.4.0 (2022-03-13)

[Compare the full difference.](https://github.com/callowayproject/generate-changelog/compare/0.3.0...0.4.0)

### Fixes

- Fixed missing variables in render context. [0bed08e](https://github.com/callowayproject/generate-changelog/commit/0bed08eab48fd24a55b63b010c7cc8e665447cac)

### New

- Added support for `__contains__` in registry. [848421d](https://github.com/callowayproject/generate-changelog/commit/848421d8123738f7c876875301c114f4c8bc1087)

- Added action registry. [a363c25](https://github.com/callowayproject/generate-changelog/commit/a363c25588f2dff507150776d58fc4d876b1220c)

  - Accessing the registry ensures the built-in actions are loaded.

- Added changelog configuration and templates. [32f4f23](https://github.com/callowayproject/generate-changelog/commit/32f4f23635b06839c19b3f811a1e2058dc81764e)

- Added a `previous_tag` attribute to the version context. [5760576](https://github.com/callowayproject/generate-changelog/commit/576057668dfc90eba19070d6f94d14d60ca9ada6)

- Added lazy evaluation of Jinja environments. [f57d007](https://github.com/callowayproject/generate-changelog/commit/f57d007f71105f4f4d6e6d1a005f39e71f816dfe)

  - This allows for proper setup of the configuration.

- Added accessor for current configuration. [83a728f](https://github.com/callowayproject/generate-changelog/commit/83a728f6c09bf7c618f031820e35267504f5f866)

  - `get_config()` will instantiate a new configuration or return the existing configuration.

### Updates

- Updated processors doc strings. [9102ec7](https://github.com/callowayproject/generate-changelog/commit/9102ec757788f3210d381e57d41e64cd57d24718)

- Updated configuration doc strings. [ff818af](https://github.com/callowayproject/generate-changelog/commit/ff818aff84744fdea955e26f539ad9c8a3a953d2)

- Updated data_merge doc strings. [2840242](https://github.com/callowayproject/generate-changelog/commit/28402420496a0fb6403e7bed58eb0d74ee237457)

- Updated git_ops and lazy doc strings. [26ecd54](https://github.com/callowayproject/generate-changelog/commit/26ecd54bb3f2f38c1c2198afde0cedf296a18120)

- Updated pipeline doc strings. [2a2c052](https://github.com/callowayproject/generate-changelog/commit/2a2c05296541c71373b4f8d59ced3fd0d2fc4f35)

- Updated templating doc strings. [b942302](https://github.com/callowayproject/generate-changelog/commit/b942302c879f5dabfc0553f103d80864bd7ebadf)

- Updated utility doc strings. [a7ae93f](https://github.com/callowayproject/generate-changelog/commit/a7ae93f757792ebf4cabf5c51fc353f65d593fef)

- Removed ActionSpec. [29942ac](https://github.com/callowayproject/generate-changelog/commit/29942acbde3b7e4b9b9a68e2b840b38417643174)

  - It was unnecessary. Now Action classes are instantiated directly.

- Removed author rendering from commits. [e44de67](https://github.com/callowayproject/generate-changelog/commit/e44de6784a7e26422679a5597b4e21322ac49f08)

## 0.3.0 (2022-03-05)

[Compare the full difference.](https://github.com/callowayproject/generate-changelog/compare/0.2.0...0.3.0)

### Updates

- Changed the package name to `generate_changelog`. [1e4945a](https://github.com/callowayproject/generate-changelog/commit/1e4945adc762c20b9c450cd7234d9791897459e2)

- Change the configuration file base name to `.changelog-config`. [ac3fc2e](https://github.com/callowayproject/generate-changelog/commit/ac3fc2e2fb4fd609b9f0a995a7ef95f7b77d53dd)

## 0.2.0 (2022-03-05)

[Compare the full difference.](https://github.com/callowayproject/generate-changelog/compare/0.1.0...0.2.0)

### Fixes

- Fixed the merge handling in git_ops. [e9666f5](https://github.com/callowayproject/generate-changelog/commit/e9666f519fd2edea9c2b8e3fa97b4b9ee1d10042)

- Fixed the `include_merges` setting. [cf6c4f2](https://github.com/callowayproject/generate-changelog/commit/cf6c4f2bba26f3e50010fbf424ad4326d1fe45bc)

  Wasn't hooked up with the git_ops module.

- Fixed a bug in the capitalize action. [8fee744](https://github.com/callowayproject/generate-changelog/commit/8fee744bfedfea5850f7fa61d36f202815514210)

  Used to capitalize the first letter but also convert all other characters to lowercase.

### New

- Added release tooling in a Makefile. [8064d3d](https://github.com/callowayproject/generate-changelog/commit/8064d3de42435b65a61b9686231973240f80f558)

- Added `Slice` and `FirstRegExMatchPosition` actions. [19cf66e](https://github.com/callowayproject/generate-changelog/commit/19cf66ebacc275c4b15fb1b5371ca9190a4b85f7)

  - `Slice` will slice the input text when called
  - `FirstRegExMatchPosition` will return the position of the first match of the regular expression.

- Added `IncrementalFileInsert` action. [d40ba36](https://github.com/callowayproject/generate-changelog/commit/d40ba3624ae01350b63ec15613838c8d81825dd0)

  Simplifies incremental change log generation for the output action.

- Added `create_if_missing` option to `ReadFile`. [8d1eaef](https://github.com/callowayproject/generate-changelog/commit/8d1eaefaa3868d3322453ceeafa2a416a95e3a7a)

  Allows for the creation of an empty file when trying to read from a non-existent file.

- Added MIT license and entry point config for CLI. [579134b](https://github.com/callowayproject/generate-changelog/commit/579134bd497362c88e82593eb7fd2fe83a04718c)

### Other

- Moved `VALID_AUTHOR_TOKENS` from templating to configuration. [dc93fc3](https://github.com/callowayproject/generate-changelog/commit/dc93fc324a02cfda0aed53d2648726c6be130074)

### Updates

- Updated command line interface. [d8abd8d](https://github.com/callowayproject/generate-changelog/commit/d8abd8d3a8b1ab6d112423ee4ea2408f36a8b802)

- Updated configuration. [a8ded3f](https://github.com/callowayproject/generate-changelog/commit/a8ded3f3c8c20f5117f95ca3d0020f326d112db9)

  - Fixed `DEFAULT_IGNORE_PATTERNS` with commas
  - Updated `DEFAULT_STARTING_TAG_PIPELINE` with better pattern
  - Added `chg` to \`\`DEFAULT_SECTION_PATTERNS\`
  - Added `DEFAULT_OUTPUT_PIPELINE` for incremental changes
  - Added `valid_author_tokens` to configuration

- Updated tests for pipelines. [e280fb8](https://github.com/callowayproject/generate-changelog/commit/e280fb863d98450f48c35d7f2382770813271210)

- Updates the commit template and rendering. [e76fd3a](https://github.com/callowayproject/generate-changelog/commit/e76fd3ace753fc3244c38af89adcf589354e5b0f)

- Updated `eval_if_callable`. [ebab2cf](https://github.com/callowayproject/generate-changelog/commit/ebab2cf34f98cb06bfb485a8eb2c44717aa4f0be)

  - Will now instantiate actions or pipelines and run them.

- Renamed `GetFirstRegExMatch` to `FirstRegExMatch`. [82b907f](https://github.com/callowayproject/generate-changelog/commit/82b907faf481f1c7218cc29c82d7072a0014314f)

## 0.1.0 (2022-03-01)

[Compare the full difference.](https://github.com/callowayproject/generate-changelog/compare/None...0.1.0)

### Other

- Initial commit. [41ab840](https://github.com/callowayproject/generate-changelog/commit/41ab8402b7cd59f4d48da528f92664e4482b962d)
