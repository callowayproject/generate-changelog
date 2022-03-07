"""Testing lazy objects."""

from dataclasses import dataclass

from generate_changelog import lazy


@dataclass
class DummyClass:
    """Just a dummy class."""

    attr1: str
    attr2: int


def test_lazy_object():
    """Access attributes of lazy objects should work."""
    obj = lazy.LazyObject(lambda: DummyClass("attribute", 45))
    assert obj._wrapped is None
    assert not obj._is_init

    assert obj.attr1 == "attribute"
    assert obj.attr2 == 45


def test_lazy_object_setattr():
    """Setting attributes of lazy objects should work."""
    obj = lazy.LazyObject(lambda: DummyClass("attribute", 45))
    assert obj._wrapped is None
    assert not obj._is_init
    obj.attr1 = "non-attribute"
    assert obj.attr1 == "non-attribute"
    assert obj.attr2 == 45
    obj.attr1 = "original recipe"
    assert obj.attr1 == "original recipe"


def test_lazy_object_delattr():
    """Setting attributes of lazy objects should work."""
    obj = lazy.LazyObject(lambda: DummyClass("attribute", 45))
    assert obj._wrapped is None
    assert not obj._is_init
    obj.attr3 = "I'm deletable"
    assert obj.attr1 == "attribute"
    assert obj.attr2 == 45
    assert obj.attr3 == "I'm deletable"
    delattr(obj, "attr3")
    assert not hasattr(obj, "attr3")
