"""Text functions."""
from typing import Optional

import re
import textwrap
from dataclasses import dataclass

from generate_changelog.actions import register_builtin
from generate_changelog.configuration import IntOrCallable, StrOrCallable
from generate_changelog.utilities import eval_if_callable


@dataclass(frozen=True)
@register_builtin
class SetDefault:
    """Return a default value when called with an empty value."""

    default: StrOrCallable = ""

    def __call__(self, input_text: StrOrCallable) -> str:
        """Return a default value when called with an empty value."""
        default = eval_if_callable(self.default)
        text = eval_if_callable(input_text)
        return text or default


@dataclass(frozen=True)
@register_builtin
class PrefixString:
    """Prefix a string to the input when called."""

    prefix: StrOrCallable = ""
    """The string to prefix"""

    def __call__(self, input_text: StrOrCallable) -> str:
        """Prefix input_text."""
        text = eval_if_callable(input_text) or ""
        prefix = eval_if_callable(self.prefix) or ""
        return f"{prefix}{text}"


@dataclass(frozen=True)
@register_builtin
class AppendString:
    """Create a callable that can append a string to the input."""

    postfix: StrOrCallable = ""
    """The string to append."""

    def __call__(self, input_text: StrOrCallable) -> str:
        """Append a string to the input_text."""
        text = eval_if_callable(input_text) or ""
        postfix = eval_if_callable(self.postfix) or ""

        return f"{text}{postfix}"


@dataclass(frozen=True)
@register_builtin
class Strip:
    """Create a callable that will strip a string from the ends of an input."""

    chars: StrOrCallable = " "

    def __call__(self, input_text: StrOrCallable) -> str:
        """Strip characters from the ends of the input."""
        text = eval_if_callable(input_text) or ""
        chars = eval_if_callable(self.chars) or " "

        return text.strip(chars)


@dataclass(frozen=True)
@register_builtin
class RegExCommand:
    """A base class to hold regular expression information."""

    pattern: StrOrCallable
    """The regular expression to match against."""

    ascii_flag: bool = False
    ignorecase_flag: bool = False
    locale_flag: bool = False
    multiline_flag: bool = False
    dotall_flag: bool = False
    verbose_flag: bool = False

    @property
    def flags(self) -> re.RegexFlag:
        """The combined RegexFlags."""
        from functools import reduce

        flags = [
            (self.ascii_flag, re.ASCII),
            (self.ignorecase_flag, re.IGNORECASE),
            (self.locale_flag, re.LOCALE),
            (self.multiline_flag, re.MULTILINE),
            (self.dotall_flag, re.DOTALL),
            (self.verbose_flag, re.VERBOSE),
        ]
        return reduce(lambda x, y: x | y, [value for use, value in flags if use], 0)  # NOQA


@dataclass(frozen=True)
@register_builtin
class FirstRegExMatch(RegExCommand):
    """When called, returns the first match in a string using a predefined regex."""

    named_subgroup: Optional[str] = None
    """The named subgroup defined in the pattern to return."""

    default_value: StrOrCallable = ""
    """The value to return if no match is found."""

    def __call__(self, input_text: StrOrCallable) -> str:
        """Search the input_text for the predefined pattern and return it."""
        text = eval_if_callable(input_text)
        pattern = eval_if_callable(self.pattern)
        match = re.search(pattern, text, self.flags)
        if match is None:
            return eval_if_callable(self.default_value)

        group_dict = match.groupdict()
        if self.named_subgroup and self.named_subgroup in group_dict:
            return group_dict[self.named_subgroup] or eval_if_callable(self.default_value)

        return match.group(0)


@dataclass(frozen=True)
@register_builtin
class FirstRegExMatchPosition(RegExCommand):
    """When called, returns the position of the first match in a string using a predefined regex."""

    def __call__(self, input_text: StrOrCallable) -> int:
        """Search the input_text for the predefined pattern and return its position."""
        text = eval_if_callable(input_text)
        pattern = eval_if_callable(self.pattern)
        match = re.search(pattern, text, self.flags)
        return match.start() if match else 0


@dataclass(frozen=True)
@register_builtin
class RegexSub(RegExCommand):
    """Create a callable that will make substitutions using regular expressions."""

    replacement: StrOrCallable = ""
    """The replacement string for matches."""

    def __call__(self, input_text: StrOrCallable) -> str:
        """Do the substitution on the input_text."""
        text = eval_if_callable(input_text)
        pattern = eval_if_callable(self.pattern)
        replacement = eval_if_callable(self.replacement)
        replacement = re.sub(r"\\([\d+])", r"\\g<\1>", replacement)  # Replace back-references of type '\1' to '\g<1>'

        return re.sub(pattern, replacement, text, flags=self.flags)


@dataclass(frozen=True)
@register_builtin
class PrefixLines:
    """Creates a callable to prefix lines to input text."""

    prefix: StrOrCallable
    """The characters to put in front of each line."""

    first_line: Optional[StrOrCallable] = None
    """Prefix the first line with these characters."""

    def __call__(self, input_text: StrOrCallable) -> str:
        """Prepend characters to the lines in input text."""
        text = eval_if_callable(input_text) or ""
        prefix = eval_if_callable(self.prefix) or ""
        first_line_prefix = eval_if_callable(self.first_line) or prefix

        lines = text.splitlines()

        if not lines:
            return ""

        first_line = f"{first_line_prefix}{lines[0]}".rstrip(" ")
        prefixed_lines = [f"{prefix}{line}".rstrip(" ") for line in lines[1:]]
        prefixed_lines.insert(0, first_line)

        return "\n".join(prefixed_lines) + "\n"


@dataclass(frozen=True)
@register_builtin
class WrapParagraphs:
    """Create a callable to wrap the paragraphs of a string."""

    paragraph_pattern: StrOrCallable = "\n\n"
    """Pattern to detect paragraphs."""

    paragraph_join: StrOrCallable = "\n\n"
    """Join the wrapped paragraphs with this string."""

    width: int = 88
    """The maximum width of each line of the paragraph."""

    def __call__(self, input_text: StrOrCallable) -> str:
        """Wrap each paragraph of the input text."""
        paragraph_pattern = eval_if_callable(self.paragraph_pattern)
        pattern = re.compile(paragraph_pattern, re.MULTILINE)
        text = eval_if_callable(input_text)
        paragraph_join = eval_if_callable(self.paragraph_join)

        paragraphs = pattern.split(text)

        wrapped_paragraphs = [textwrap.fill(p, width=self.width) for p in paragraphs]
        return paragraph_join.join(wrapped_paragraphs)


register_builtin("prefix_caret")(PrefixString("^"))
register_builtin("append_dot")(AppendString("."))
register_builtin("noop")(lambda txt: txt)  # NOQA
register_builtin("strip_spaces")(Strip())


@register_builtin
def capitalize(msg: str) -> str:
    """
    Capitalize the first character for a string.

    Args:
        msg: The string to capitalize

    Returns:
        The capitalized string
    """
    return msg[0].upper() + msg[1:]


@register_builtin
@dataclass
class Slice:
    """When called, return a slice of the sequence."""

    start: Optional[IntOrCallable] = None
    """The start of the slice. None means the beginning of the sequence."""

    stop: Optional[IntOrCallable] = None
    """The end of the slice. None means the end of the sequence."""

    step: Optional[IntOrCallable] = None
    """Slice using this step betweeen indices. None means don't use the step."""

    def __call__(self, input_text: StrOrCallable) -> str:
        """Slice the sequence."""
        text = eval_if_callable(input_text)
        start = eval_if_callable(self.start)
        stop = eval_if_callable(self.stop)
        step = eval_if_callable(self.step)

        return text[start:stop:step]
