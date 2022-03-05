"""Processing module for changelog generation."""

from typing import Callable, Union

BUILT_INS = {}


def register_builtin(function_or_name: Union[Callable, str]) -> Callable:
    """A decorator that registers a function with an optional name."""
    name = ""

    def inner(f: Callable) -> Callable:
        """Register the function as a builtin."""
        BUILT_INS[name] = f
        return f

    if callable(function_or_name):
        name = function_or_name.__name__
        return inner(function_or_name)
    else:
        name = function_or_name
        return inner


def load_builtins():
    """Import all submodules so the decorated functions get registered."""
    import importlib

    importlib.import_module(".text_processing", "generate_changelog.processors")
    importlib.import_module(".file_processing", "generate_changelog.processors")
    importlib.import_module(".shell", "generate_changelog.processors")
    importlib.import_module(".metadata", "generate_changelog.processors")
