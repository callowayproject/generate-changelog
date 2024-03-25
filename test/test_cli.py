"""Tests of the command line interface."""

import json
import traceback
from pathlib import Path

from typer.testing import CliRunner

import generate_changelog
from generate_changelog.cli import app

runner = CliRunner()


def test_app_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert generate_changelog.__version__ in result.stdout


def test_app_generate_config(mocker):
    func = mocker.patch("generate_changelog.cli.write_default_config")
    result = runner.invoke(app, ["--generate-config"])
    if result.exit_code != 0:
        print(result.stdout)
        traceback.print_exception(*result.exc_info)
    assert result.exit_code == 0
    func.assert_called()
    assert "The configuration file was written to" in result.stdout


def test_app_generate_changelog(default_repo):
    config = Path(__file__).parent / "fixtures" / "std-out-config.yaml"
    result = runner.invoke(app, ["-r", default_repo.git_dir, "-c", str(config)])
    if result.exit_code != 0:
        print(result.stdout)
        traceback.print_exception(*result.exc_info)
    assert result.exit_code == 0
    assert f"Using configuration file: {config}" in result.stdout


def test_app_generate_release_hint(default_repo):
    config = Path(__file__).parent / "fixtures" / "std-out-config.yaml"
    result = runner.invoke(
        app, ["-r", default_repo.git_dir, "-c", str(config), "--skip-output-pipeline", "-o", "release-hint"]
    )
    if result.exit_code != 0:
        print(result.stdout)
        traceback.print_exception(*result.exc_info)
    assert result.exit_code == 0
    assert "minor" in result.stdout


def test_app_generate_release_hint_branch_override(default_repo):
    config = Path(__file__).parent / "fixtures" / "std-out-config.yaml"
    new_branch = default_repo.create_head("my-branch")
    default_repo.head.reference = new_branch
    assert default_repo.active_branch.name == "my-branch"

    # Check that the default behavior returns a "dev" release hint
    result = runner.invoke(
        app, ["-r", default_repo.git_dir, "-c", str(config), "--skip-output-pipeline", "-o", "release-hint"]
    )
    if result.exit_code != 0:
        print(result.stdout)
        traceback.print_exception(*result.exc_info)
    assert result.exit_code == 0
    assert "dev" in result.stdout

    # Check that the override returns a "minor" release hint
    result = runner.invoke(
        app,
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


def test_app_generate_notes(default_repo):
    config = Path(__file__).parent / "fixtures" / "std-out-config.yaml"
    result = runner.invoke(
        app, ["-r", default_repo.git_dir, "-c", str(config), "--skip-output-pipeline", "-o", "notes"]
    )
    if result.exit_code != 0:
        print(result.stdout)
        traceback.print_exception(*result.exc_info)
    assert result.exit_code == 0
    assert result.stdout.startswith("# Changelog")


def test_app_generate_all(default_repo):
    config = Path(__file__).parent / "fixtures" / "std-out-config.yaml"
    result = runner.invoke(app, ["-r", default_repo.git_dir, "-c", str(config), "--skip-output-pipeline", "-o", "all"])
    if result.exit_code != 0:
        print(result.stdout)
        traceback.print_exception(*result.exc_info)
    assert result.exit_code == 0
    output = json.loads(result.stdout)
    assert output["notes"].startswith("# Changelog")
    assert "minor" == output["release_hint"]
