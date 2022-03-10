"""Utility methods."""
from typing import Any, Iterable


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
        return pipeline_factory([value], **config.variables).run()
    elif is_pipeline(value):
        return pipeline_factory(value, **config.variables).run()

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
