#!/bin/bash
set -e # Increase bash strictness
set -o pipefail

function parse_boolean() {
  local value="false"
  value=$(echo "${1}" | awk '{print tolower($0)}')  # Convert to lowercase
  case "$value" in
    "true" | "yes" | "1")
      echo 1
      ;;
    *)
      echo 0
      ;;
  esac
}

changelog_args=("-o" "release-hint" "-d" "/tmp/debug-report.txt")

if [[ -n ${INPUT_STARTING_TAG} ]]; then
  changelog_args+=("-t" "${INPUT_STARTING_TAG}")
fi

if [[ -n ${INPUT_SKIP_OUTPUT_PIPELINE} && $(parse_boolean "${INPUT_SKIP_OUTPUT_PIPELINE}") -eq 1 ]]; then
  changelog_args+=("--skip-output-pipeline")
fi

if [[ -n ${INPUT_BRANCH_OVERRIDE} ]]; then
  changelog_args+=("-b" "${INPUT_BRANCH_OVERRIDE}")
fi

cd /github/workspace
echo "[action-generate-changelog] Generating the changelog with arguments '${changelog_args[*]}'"

RELEASE_HINT=$(generate-changelog ${changelog_args[*]})
echo "::group::Release hint details"
cat /tmp/debug-report.txt
echo "::endgroup::"
echo "::notice::Suggested release type for this branch is: ${RELEASE_HINT}"
echo "release_hint=$RELEASE_HINT" >> $GITHUB_OUTPUT
