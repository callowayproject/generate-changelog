"""Metadata callback and processing functions."""
from typing import Callable

import re
import textwrap
from collections import defaultdict
from dataclasses import dataclass, field

from clgen.data_merge import comprehensive_merge
from clgen.processors import register_builtin

REGEX_RFC822_KEY_VALUE = r"(?:^|\n)(?P<key>[-\w]*)\s*:\s*(?P<value>[^\n]*(?:\n\s+[^\n]*)*)"


@dataclass
class MetadataCollector:
    """Creates a callable to collect key-value metadata."""

    metadata: dict = field(default_factory=dict)

    def __call__(self, **kwargs):
        """
        Put keyword arguments into metadata storage.

        Args:
            **kwargs: keyword arguments to update metadata
        """
        self.metadata = comprehensive_merge(self.metadata, kwargs)


@register_builtin
class ParseTrailers:
    """Parse and extract trailers from a commit message."""

    def __init__(self, commit_metadata: Callable):
        self.commit_metadata = commit_metadata

    def __call__(self, message: str) -> str:
        """Parse and extract trailers from a commit message."""
        pos = len(message)
        trailers = defaultdict(list)
        for match in re.finditer(REGEX_RFC822_KEY_VALUE, message, re.MULTILINE | re.IGNORECASE):
            pos = min(pos, match.start())
            dct = match.groupdict()
            key = dct["key"].lower()
            value = dct["value"]
            if "\n" in value:
                first_line, remaining = value.split("\n", 1)
                value = f"{first_line}\n{textwrap.dedent(remaining)}"

            trailers[key].append(value)
        self.commit_metadata(trailers=trailers)
        return message[:pos]
