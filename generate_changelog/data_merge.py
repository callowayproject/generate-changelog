"""Tools for merging data."""

import copy
from functools import reduce
from typing import Any, Iterable


def deep_merge(*dicts: dict) -> dict:
    """
    Merges dicts deeply.

    Pass the dictionaries to merge as parameters to the function.

    Returns:
        dict: The merged dict
    """

    def merge_into(d1: dict, d2: dict) -> dict:
        for key, val in d2.items():
            if key not in d1 or not isinstance(d1[key], dict):
                d1[key] = copy.deepcopy(val)
            else:
                d1[key] = merge_into(d1[key], val)
        return d1

    return reduce(merge_into, dicts, {})


def merge_iterables(iter1: Iterable, iter2: Iterable) -> set:
    """
    Merge and de-duplicate a bunch of lists into a single list.

    Order is not guaranteed.

    Args:
        iter1: An Iterable
        iter2: An Iterable

    Returns:
        The merged, de-duplicated sequence as a set
    """
    from itertools import chain

    return set(chain(iter1, iter2))


def comprehensive_merge(*args: Any) -> Any:  # NOQA: C901
    """
    Merges data comprehensively.

    All arguments must be of the same type.

    - Scalars are overwritten by the new values
    - lists are merged and de-duplicated
    - dicts are recursively merged

    Returns:
        The merged data
    """

    def merge_into(d1: Any, d2: Any) -> Any:
        if type(d1) is not type(d2):
            raise ValueError(f"Cannot merge {type(d2)} into {type(d1)}.")

        if isinstance(d1, list):
            return list(merge_iterables(d1, d2))
        elif isinstance(d1, set):
            return merge_iterables(d1, d2)
        elif isinstance(d1, tuple):
            return tuple(merge_iterables(d1, d2))
        elif isinstance(d1, dict):
            for key in d2:
                d1[key] = merge_into(d1[key], d2[key]) if key in d1 else copy.deepcopy(d2[key])
            return d1
        else:
            return copy.deepcopy(d2)

    if isinstance(args[0], list):
        return reduce(merge_into, args, [])
    elif isinstance(args[0], tuple):
        return reduce(merge_into, args, ())
    elif isinstance(args[0], set):
        return reduce(merge_into, args, set())
    elif isinstance(args[0], dict):
        return reduce(merge_into, args, {})
    else:
        return reduce(merge_into, args)
