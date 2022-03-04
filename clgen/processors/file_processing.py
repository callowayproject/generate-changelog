"""File reading and writing processors."""
import re
from dataclasses import dataclass
from pathlib import Path

import typer

from clgen.configuration import StrOrCallable
from clgen.processors import register_builtin
from clgen.utilities import eval_if_callable


@dataclass
@register_builtin
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
            typer.echo(f"The file '{filepath}' does not exist.", err=True)
            raise typer.Exit(1)

        return filepath.read_text() or ""


@dataclass
@register_builtin
class WriteFile:
    """Write the passed string to a file when called."""

    filename: StrOrCallable
    """The file name to write when called."""

    def __call__(self, input_text: StrOrCallable) -> str:
        """Writes input_text to the pre-configured file."""
        filepath = Path(eval_if_callable(self.filename))
        text = eval_if_callable(input_text)
        filepath.write_text(text)
        return input_text


@register_builtin
def stdout(content):
    """Write content to stdout."""
    typer.echo(content)


@dataclass(frozen=True)
@register_builtin
class IncrementalFileInsert:
    """Replace the start of a file with text."""

    filename: StrOrCallable
    """The file name to write when called."""

    last_heading_pattern: StrOrCallable
    """A regular expression to detect the last heading. Content before this position is re-rendered and inserted."""

    def __call__(self, input_text: StrOrCallable):
        """Replace the beigging of the file to last_heading_pattern with input_text."""
        filename = Path(eval_if_callable(self.filename))
        pattern = eval_if_callable(self.last_heading_pattern)
        text = eval_if_callable(input_text)
        existing_text = filename.read_text() if filename.exists() else ""

        if match := re.search(pattern, existing_text, re.MULTILINE):
            new_text = f"{text}\n{existing_text[match.start():]}"
        else:
            new_text = text

        filename.write_text(new_text)
