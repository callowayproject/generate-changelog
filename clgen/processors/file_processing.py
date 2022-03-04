"""File reading and writing processors."""
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
