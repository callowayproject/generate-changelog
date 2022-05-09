"""Test configuration."""
from pathlib import Path

import click.exceptions
import pytest

from generate_changelog import configuration

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def test_update_from_file():
    """A configuration file should update the default configuration."""
    config_file_path = FIXTURES_DIR / "sample_config.yml"
    configuration.get_config().update_from_file(config_file_path)
    assert configuration.get_config().unreleased_label == "Not Done Yet"
    assert not hasattr(configuration.get_config(), "not_valid")

    with pytest.raises(click.exceptions.Exit):
        configuration.get_config().update_from_file(FIXTURES_DIR / "missing.yml")

    with pytest.raises(click.exceptions.Exit):
        configuration.get_config().update_from_file(FIXTURES_DIR)


def test_write_default_config(tmp_path):
    """Writing a default config should be accurate."""
    test_config_file = tmp_path / "test_config.yml"
    configuration.write_default_config(test_config_file)

    default_config = configuration.get_default_config()
    test_config = configuration.Configuration()
    assert default_config != test_config

    test_config.update_from_file(test_config_file)
    assert default_config == test_config


def test_rendered_variables():
    """Variables can contain templates to other variables."""
    config = configuration.get_default_config()

    config.variables = {"root_url": "https://www.example.com/", "sub_url": "{{ root_url }}sub_path/2"}

    assert config.rendered_variables["sub_url"] == "https://www.example.com/sub_path/2"
