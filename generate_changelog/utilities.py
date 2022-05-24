"""Utility methods."""
from typing import Any, Iterable, Optional


def is_action(value: Any) -> bool:
    """Returns ``True`` if the value is an action."""
    return isinstance(value, dict) and "action" in value


def is_pipeline(value: Any) -> bool:
    """Returns ``True`` if the value is a pipeline."""
    return value and isinstance(value, list) and is_action(value[0])


def eval_if_callable(value: Any) -> Any:
    """
    Tries to evaluate ``value`` as an action, a pipeline, or a callable if possible.

    Args:
        value: A callable, action dictionary, list of action dictionaries, or other.

    Returns:
        The original value if it can not be evaluated further.
    """
    from generate_changelog.configuration import get_config
    from generate_changelog.pipeline import pipeline_factory

    config = get_config()

    if is_action(value):
        # convert it into a single action and call it
        return pipeline_factory([value], **config.rendered_variables).run()
    elif is_pipeline(value):
        return pipeline_factory(value, **config.rendered_variables).run()

    return value() if callable(value) else value


def pairs(iterable) -> Iterable:
    """
    Return successive pairs taken from the input iterable.

    Like :py:func:`itertools.pairwise` in 3.10, but will always include the last element by itself.

    Example:

            >>> list(pairs("ABCD"))
            [("A", "B"), ("B", "C"), ("C", "D"), ("D", None)]
            >>> list(pairs("ABC"))
            [("A", "B"), ("B", "C"), ("C", None)]

    Args:
        iterable: The iterable to combine into pairs.

    Returns:
        An iterable of pairs.
    """
    from itertools import tee, zip_longest

    a, b = tee(iterable)
    next(b, None)
    return zip_longest(a, b)


def resolve_name(obj: Any, name: str, default=None) -> Any:
    """
    Get a key or attr ``name`` from obj or default value.

    Copied and modified from Django Template variable resolutions

    Resolution methods:

    - Mapping key lookup
    - Attribute lookup
    - Sequence index

    Args:
        obj: The object to access
        name: A dotted name to the value, such as ``mykey.0.name``
        default: If the name cannot be resolved from the object, return this value

    Returns:
        The value at the resolved name or the default value.

    # noqa: DAR401
    """
    lookups = name.split(".")
    current = obj
    try:  # catch-all for unexpected failures
        for bit in lookups:
            try:  # dictionary lookup
                current = current[bit]
                # ValueError/IndexError are for numpy.array lookup on
                # numpy < 1.9 and 1.9+ respectively
            except (TypeError, AttributeError, KeyError, ValueError, IndexError):
                try:  # attribute lookup
                    current = getattr(current, bit)
                except (TypeError, AttributeError):
                    # Reraise if the exception was raised by a @property
                    if bit in dir(current):
                        raise
                    try:  # list-index lookup
                        current = current[int(bit)]
                    except (
                        IndexError,  # list index out of range
                        ValueError,  # invalid literal for int()
                        KeyError,  # current is a dict without `int(bit)` key
                        TypeError,
                    ):  # un-subscript-able object
                        return default
        return current
    except Exception:  # NOQA  # pragma: no cover
        return default


def diff_index(iterable1, iterable2) -> Optional[int]:
    """Return the index where iterable2 is different from iterable1."""
    return next((index for index, (item1, item2) in enumerate(zip(iterable1, iterable2)) if item1 != item2), None)
