"""Tests of the command line interface."""
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


def test_app_generate_config():
    result = runner.invoke(app, ["--generate-config"])
    if result.exit_code != 0:
        print(result.stdout)
    assert result.exit_code == 0
    assert "The configuration file was written to" in result.stdout


def test_app_generate_changelog(default_repo):
    config = Path(__file__).parent / "fixtures" / "sample_config.yml"
    result = runner.invoke(app, ["-r", default_repo.git_dir, "-c", str(config)])
    if result.exit_code != 0:
        print(result.stdout)
        traceback.print_exception(*result.exc_info)
    assert result.exit_code == 0
    assert f"Using configuration file: {config}" in result.stdout
