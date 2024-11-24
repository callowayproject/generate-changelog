"""Tests of the registry system."""

from generate_changelog.actions import Registry


def test_registry_get_key_loads_builtins():
    """Getting a key from the registry should load the built-ins."""
    r = Registry()
    r["new_attr"] = "foo"
    assert r.data["new_attr"] == "foo"
    assert not r._loaded
    assert r["new_attr"] == "foo"
    assert r._loaded


def test_registry_contains_loads_builtins():
    """Testing for a key in the registry should load the built-ins."""
    r = Registry()
    assert not r._loaded
    assert "foo" not in r
    assert r._loaded
