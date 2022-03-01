"""Utility methods."""
from typing import Any, Iterable


def eval_if_callable(value: Any) -> Any:
    """Return value or the result of calling value."""
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
