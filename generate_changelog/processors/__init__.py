"""Processing module for changelog generation."""
from typing import Callable, Union

from collections import UserDict


class Registry(UserDict):
    """
    Built-in action registry.

    This allows setting keys normally. When getting a key, it makes sure the
    appropriate modules are imported to fill the internal dictionary before
    getting the key.
    """

    def __init__(self, initialdata=None):
        super().__init__(initialdata)
        self._loaded = False

    def __getitem__(self, key):
        """Make sure the built-in actions are loaded."""
        if not self._loaded:
            self.load_builtins()
        return super().__getitem__(key)

    def load_builtins(self):
        """Import all submodules so the decorated functions get registered."""
        import importlib

        importlib.import_module(".text_processing", "generate_changelog.processors")
        importlib.import_module(".file_processing", "generate_changelog.processors")
        importlib.import_module(".shell", "generate_changelog.processors")
        importlib.import_module(".metadata", "generate_changelog.processors")

        self._loaded = True


BUILT_INS = Registry()
"""The registered actions that are considered to be built-in."""


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
