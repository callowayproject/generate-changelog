"""File reading and writing actions."""

import re
from dataclasses import dataclass
from pathlib import Path

import rich_click as click

from generate_changelog.actions import register_builtin
from generate_changelog.configuration import StrOrCallable
from generate_changelog.utilities import eval_if_callable


@register_builtin
@dataclass(frozen=True)
class ReadFile:
    """Return a file's contents when called."""

    filename: StrOrCallable
    """The file name to read when called."""

    create_if_missing: bool = True
    """When True, create a missing file. Otherwise returns an error."""

    def __call__(self, *args, **kwargs) -> str:
        """Return the contents of the file."""
        filepath = Path(eval_if_callable(self.filename))

        if self.create_if_missing:
            filepath.touch()

        if not filepath.exists():
            raise click.UsageError(f"The file '{filepath}' does not exist.")

        return filepath.read_text() or ""


@register_builtin
@dataclass(frozen=True)
class WriteFile:
    """Write the passed string to a file when called."""

    filename: StrOrCallable
    """The file name to write when called."""

    def __call__(self, input_text: StrOrCallable) -> StrOrCallable:
        """Writes input_text to the pre-configured file."""
        filepath = Path(eval_if_callable(self.filename))
        text = eval_if_callable(input_text)
        filepath.write_text(text, encoding="utf-8")
        return input_text


@register_builtin
def stdout(content: str) -> str:
    """Write content to stdout."""
    click.echo(content)
    return content


@register_builtin
@dataclass(frozen=True)
class IncrementalFileInsert:
    """Replace the start of a file with text."""

    filename: StrOrCallable
    """The file name to write when called."""

    last_heading_pattern: StrOrCallable
    """A regular expression to detect the last heading. Content before this position is re-rendered and inserted."""

    def __call__(self, input_text: StrOrCallable) -> StrOrCallable:
        """
        Replace the beginning of the file up to `last_heading_pattern` with `input_text` .

        Args:
            input_text: The text to insert.

        Returns:
            The same `input_text`
        """
        filename = Path(eval_if_callable(self.filename))
        pattern = eval_if_callable(self.last_heading_pattern)
        text = eval_if_callable(input_text)
        existing_text = filename.read_text() if filename.exists() else ""

        match = re.search(pattern, existing_text, re.MULTILINE)
        new_text = f"{text}\n{existing_text[match.start() :]}" if match else text

        filename.write_text(new_text, encoding="utf-8")
        return input_text


@register_builtin
@dataclass(frozen=True)
class MDFormat:
    """Run `mdformat` on a file."""

    filename: StrOrCallable
    """The file name to format when called."""

    def __call__(self, *args, **kwargs) -> StrOrCallable:
        """
        Read the text into a buffer and write it back out with `mdformat`.

        Returns:
            The formatted text
        """
        from mdformat import text as mdformat_text

        filename = Path(eval_if_callable(self.filename))
        existing_text = filename.read_text() if filename.exists() else ""

        new_text = mdformat_text(existing_text)

        filename.write_text(new_text, encoding="utf-8")
        return new_text
