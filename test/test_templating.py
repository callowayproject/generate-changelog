"""Tests of temmplating functions."""

import textwrap
from pathlib import Path

from generate_changelog import configuration, templating
from generate_changelog.commits import get_context_from_tags

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def test_render(default_repo, capsys):
    """Render should render the changelog."""
    config = configuration.get_default_config()
    config.template_dirs = []
    version_context = get_context_from_tags(default_repo, config, None)
    output = templating.render_changelog(version_context, config, False)
    expected = (FIXTURES_DIR / "rendered_default_repo.md").read_text()
    assert output.full.strip() == expected.strip()


def test_render_from_tag(default_repo, capsys):
    """Render should render the changelog."""
    config = configuration.get_default_config()
    config.template_dirs = []
    version_context = get_context_from_tags(default_repo, config, "0.0.3")
    output = templating.render_changelog(version_context, config, True)
    expected = textwrap.dedent(
        """
        # Changelog
        
        ## Unreleased (2022-01-06)
        
        ### Updates
        
        - Chg: modified ``b`` XXX.    

    """
    )
    assert output.full.strip() == expected.strip()


def test_incremental_context(default_repo, capsys):
    """Make sure the incremental changelog includes the previous version."""
    config = configuration.get_default_config()
    config.template_dirs = [FIXTURES_DIR / "templates"]
    version_context = get_context_from_tags(default_repo, config, "0.0.2")
    output = templating.render_changelog(version_context, config, True)
    expected = textwrap.dedent(
        """
        # Changelog
        
        ## Unreleased (2022-01-06) 0.0.3...HEAD
        
        ### Updates
        
        commit
        ## 0.0.3 (2022-01-05) 0.0.2...0.0.3
        
        ### New
        
        commit
        commit
        """
    )
    assert output.full.strip() == expected.strip()
