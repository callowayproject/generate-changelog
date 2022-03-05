"""Utility methods."""
from typing import Any, Iterable


def is_action(value: Any) -> bool:
    """Is the value an action?"""
    return isinstance(value, dict) and "action" in value


def is_pipeline(value: Any) -> bool:
    """Is the value a pipeline?"""
    return value and isinstance(value, list) and is_action(value[0])


def eval_if_callable(value: Any) -> Any:
    """Return value or the result of calling value."""
    from generate_changelog.pipeline import pipeline_factory

    if is_action(value):
        # convert it into a single action and call it
        return pipeline_factory([value]).run()
    elif is_pipeline(value):
        return pipeline_factory(value).run()

    return value() if callable(value) else value


def pairs(iterable) -> Iterable:
    """
    Like pairwise in 3.10, but will always include the last element by itself.

    Example:
        ::
            >>> list(pairs("ABCD"))
            [("A", "B"), ("B", "C"), ("C", "D"), ("D", None)]
            >>> list(pairs("ABC"))
            [("A", "B"), ("B", "C"), ("C", None)]

    Args:
        iterable: The iterable to iterate over.

    Returns:
        An iterable of pairs.
    """
    from itertools import tee, zip_longest

    a, b = tee(iterable)
    next(b, None)
    return zip_longest(a, b)
