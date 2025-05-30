"""A logger adapter that adds an indent to the beginning of each message."""

import logging
import logging.config
import sys
from contextvars import ContextVar
from typing import Any, MutableMapping, Optional, Tuple, Union

import click
from rich.console import Console, RenderableType
from rich.padding import Padding
from rich.text import Text

CURRENT_INDENT = ContextVar("current_indent", default=0)
PYTHON_3_10_OR_GREATER = sys.version_info >= (3, 10)


class IndentedLoggerAdapter(logging.LoggerAdapter):
    """
    Logger adapter that adds an indent to the beginning of each message.

    Parameters:
        logger: The logger to adapt.
        extra: Extra values to add to the logging context.
        depth: The number of `indent_char` to generate for each indent level.
        indent_char: The character or string to use for indenting.
        reset: `True` if the indent level should be reset to zero.
    """

    def __init__(
        self,
        logger: logging.Logger,
        extra: Optional[dict] = None,
        depth: int = 2,
        indent_char: str = " ",
        reset: bool = False,
    ):
        super().__init__(logger, extra or {})
        self.console = Console(force_terminal=True)
        self._depth = depth
        self._indent_char = indent_char
        if reset:
            self.reset()

    @property
    def current_indent(self) -> int:
        """
        The current indent level.
        """
        return CURRENT_INDENT.get()

    def indent(self, amount: int = 1) -> None:
        """
        Increase the indent level by `amount`.
        """
        CURRENT_INDENT.set(CURRENT_INDENT.get() + amount)

    def dedent(self, amount: int = 1) -> None:
        """
        Decrease the indent level by `amount`.
        """
        CURRENT_INDENT.set(max(0, CURRENT_INDENT.get() - amount))

    def reset(self) -> None:
        """
        Reset the indent level to zero.
        """
        CURRENT_INDENT.set(0)

    @property
    def indent_str(self) -> str:
        """
        The indent string.
        """
        return (self._indent_char * self._depth) * CURRENT_INDENT.get()

    def process(
        self, msg: Union[str, RenderableType], kwargs: Optional[MutableMapping[str, Any]]
    ) -> Tuple[str, MutableMapping[str, Any]]:
        """
        Process the message and add the indent.

        Args:
            msg: The logging message.
            kwargs: Keyword arguments passed to the logger.

        Returns:
            A tuple containing the message and keyword arguments.
        """
        if PYTHON_3_10_OR_GREATER and isinstance(msg, RenderableType):
            with self.console.capture() as capture:
                self.console.print(Padding(msg, (0, 0, 0, len(self.indent_str))))
            msg = Text.from_ansi(capture.get())
        else:
            msg = self.indent_str + msg

        return msg, kwargs


VERBOSITY = {
    0: (logging.WARNING, "%(message)s"),
    1: (logging.INFO, "%(message)s"),
    2: (logging.DEBUG, "%(message)s"),
    3: (logging.DEBUG, "%(message)s %(pathname)s:%(lineno)d"),
}


def get_indented_logger(name: str) -> IndentedLoggerAdapter:
    """Get a logger with indentation."""
    return IndentedLoggerAdapter(logging.getLogger(name))


def setup_logging(verbose: int = 0) -> None:
    """Configure the logging."""
    logging.config.dictConfig(get_config(verbose))
    root_logger = get_indented_logger("")
    root_logger.setLevel(logging.WARNING)


def get_config(verbose: int = 0) -> dict:
    """Get the loggic config."""
    verbosity, log_format = VERBOSITY.get(verbose, VERBOSITY[3])
    return {
        "version": 1,
        "formatters": {
            "default": {
                "format": log_format,
                "datefmt": "[%X]",
            }
        },
        "handlers": {
            "default": {
                "class": "rich.logging.RichHandler",
                "markup": True,
                "rich_tracebacks": True,
                "show_level": False,
                "show_path": False,
                "show_time": False,
                "tracebacks_suppress": [click],
                "formatter": "default",
            }
        },
        "loggers": {
            "generate_changelog": {
                "handlers": ["default"],
                "level": verbosity,
            }
        },
    }
