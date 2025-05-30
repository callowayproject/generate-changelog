"""Tests of the command line interface."""

import json
import traceback
from pathlib import Path

from click.testing import CliRunner

import generate_changelog
from generate_changelog.cli import cli
from generate_changelog.configuration import write_default_config
from tests.conftest import inside_dir

runner = CliRunner()


class TestCLI:
    """Tests of the command line interface."""

    def test_version_option_displays_version(self):
        """The version option displays the version number."""
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert generate_changelog.__version__ in result.stdout

    def test_generate_config_option_generates_config(self, tmp_path: Path):
        """The generate-config option should write a default configuration file to the current directory."""
        # Assemble and Act
        with inside_dir(tmp_path):
            result = runner.invoke(cli, ["--generate-config"])

        # Assert
        if result.exit_code != 0:
            print(result.stdout)
            traceback.print_exception(*result.exc_info)
        assert result.exit_code == 0
        assert "The configuration file was written to" in result.stdout

    def test_generate_changelog_to_stdout(self, default_repo, tmp_path: Path):
        """Generate a changelog to standard out from the default repository."""
        # Assemble
        config = Path(__file__).parent / "fixtures" / "std-out-config.yaml"

        # Act
        with inside_dir(tmp_path):
            result = runner.invoke(cli, ["-r", default_repo.git_dir, "-c", str(config)])

        # Assert
        if result.exit_code != 0:
            print(result.stdout)
            traceback.print_exception(*result.exc_info)

        assert result.exit_code == 0
        assert f"Using configuration file: {config}" in result.stdout
        assert "# Changelog" in result.stdout

    def test_generate_release_hint_only(self, default_repo):
        """Generate a release hint and no changelog from the default repository."""
        # Assemble
        config = Path(__file__).parent / "fixtures" / "std-out-config.yaml"

        # Act
        result = runner.invoke(
            cli, ["-r", default_repo.git_dir, "-c", str(config), "--skip-output-pipeline", "-o", "release-hint"]
        )

        # Assert
        if result.exit_code != 0:
            print(result.stdout)
            traceback.print_exception(*result.exc_info)
        assert result.exit_code == 0
        assert "minor" in result.stdout

    def test_generate_release_hint_branch_override(self, default_repo):
        """Can override the branch to generate the release hint from, if different from the current branch."""
        # Assemble
        config = Path(__file__).parent / "fixtures" / "std-out-config.yaml"
        new_branch = default_repo.create_head("my-branch")
        default_repo.head.reference = new_branch
        assert default_repo.active_branch.name == "my-branch"

        # Check for the default release hint
        result = runner.invoke(
            cli, ["-r", default_repo.git_dir, "-c", str(config), "--skip-output-pipeline", "-o", "release-hint"]
        )

        if result.exit_code != 0:
            print(result.stdout)
            traceback.print_exception(*result.exc_info)
        assert result.exit_code == 0
        assert "dev" in result.stdout

        # Check that the override returns a "minor" release hint
        result = runner.invoke(
            cli,
            [
                "-r",
                default_repo.git_dir,
                "-c",
                str(config),
                "-b",
                "master",
                "--skip-output-pipeline",
                "-o",
                "release-hint",
            ],
        )
        if result.exit_code != 0:
            print(result.stdout)
            traceback.print_exception(*result.exc_info)
        assert result.exit_code == 0
        assert "minor" in result.stdout

    def test_generate_notes(self, default_repo):
        """Generate changelog notes."""
        # Assemble
        config = Path(__file__).parent / "fixtures" / "std-out-config.yaml"

        # Act
        result = runner.invoke(
            cli, ["-r", default_repo.git_dir, "-c", str(config), "--skip-output-pipeline", "-o", "notes"]
        )

        # Assemble
        if result.exit_code != 0:
            print(result.stdout)
            traceback.print_exception(*result.exc_info)
        assert result.exit_code == 0
        assert result.stdout.startswith("# Changelog")

    def test_generate_notes_and_hint(self, default_repo):
        """Generate changelog notes and release hint."""
        # Assemble
        config = Path(__file__).parent / "fixtures" / "std-out-config.yaml"

        # Act
        result = runner.invoke(
            cli, ["-r", default_repo.git_dir, "-c", str(config), "--skip-output-pipeline", "-o", "all"]
        )

        # Assert
        if result.exit_code != 0:
            print(result.stdout)
            traceback.print_exception(*result.exc_info)
        assert result.exit_code == 0
        output = json.loads(result.stdout)
        assert output["notes"].startswith("# Changelog")
        assert output["release_hint"] == "minor"


def test_alternative_changelog_path(default_repo):
    """You should be able to specify an alternative changelog path."""
    # Assemble
    working_dir = Path(default_repo.working_dir)
    changelog_path = working_dir / "somedir" / "CHANGELOG.md"
    changelog_path.parent.mkdir(exist_ok=True)
    # changelog_path.write_text("# Changelog\n\n## 0.1.0 (2024-07-23)")

    settings_path = working_dir / ".changelog-config.yaml"
    write_default_config(settings_path)
    config_text = settings_path.read_text()
    config_text = config_text.replace("  changelog_filename: CHANGELOG.md", f"  changelog_filename: {changelog_path}")
    settings_path.write_text(config_text)

    with inside_dir(default_repo.working_dir):
        result = runner.invoke(cli, ["-r", default_repo.git_dir, "-c", str(settings_path)])

    if result.exit_code != 0:
        print(result.stdout)
        traceback.print_exception(*result.exc_info)
    assert result.exit_code == 0
    assert f"Using configuration file: {settings_path}" in result.stdout

    assert changelog_path.exists()
    assert not Path(working_dir / "CHANGELOG.md").exists()
