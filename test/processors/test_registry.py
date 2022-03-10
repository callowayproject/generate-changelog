"""Tests of the registry system."""

from generate_changelog.processors import Registry


def test_registry_get_key_loads_builtins():
    """Getting a key from the registry should load the built-ins."""
    r = Registry()
    r["new_attr"] = "foo"
    assert r.data["new_attr"] == "foo"
    assert "new_attr" in r
    assert not r._loaded
    assert r["new_attr"] == "foo"
    assert r._loaded
