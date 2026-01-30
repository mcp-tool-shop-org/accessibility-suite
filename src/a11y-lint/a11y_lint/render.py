"""Deterministic renderer for CLI accessibility messages.

Renders messages in the canonical [OK]/[WARN]/[ERROR] + What/Why/Fix format.
All output is deterministic and suitable for comparison/testing.

Color Philosophy:
- Colors are purely decorative; meaning NEVER depends on color
- Default: auto (respects NO_COLOR env var and terminal detection)
- The plain text output is always fully meaningful without colors
"""

from __future__ import annotations

import os
from typing import TextIO
import sys

from .errors import A11yMessage, Level


def should_use_color(stream: TextIO | None = None) -> bool:
    """Determine if color should be used based on environment.

    Respects:
    - NO_COLOR env var (https://no-color.org/)
    - FORCE_COLOR env var
    - Terminal detection (isatty)

    Args:
        stream: Output stream to check (default: stdout)

    Returns:
        True if colors should be used
    """
    # NO_COLOR takes precedence (https://no-color.org/)
    if os.environ.get("NO_COLOR"):
        return False

    # FORCE_COLOR overrides terminal detection
    if os.environ.get("FORCE_COLOR"):
        return True

    # Check if stream is a TTY
    stream = stream or sys.stdout
    return hasattr(stream, "isatty") and stream.isatty()


# ANSI color codes for terminal output
class Colors:
    """ANSI color codes for terminal rendering."""

    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"

    # Level colors
    OK = "\033[32m"  # Green
    WARN = "\033[33m"  # Yellow
    ERROR = "\033[31m"  # Red

    # Component colors
    CODE = "\033[36m"  # Cyan
    LOCATION = "\033[90m"  # Gray
    LABEL = "\033[1m"  # Bold


def get_level_color(level: Level) -> str:
    """Get the ANSI color code for a level."""
    return {
        Level.OK: Colors.OK,
        Level.WARN: Colors.WARN,
        Level.ERROR: Colors.ERROR,
    }[level]


def render_plain(message: A11yMessage, indent: int = 0) -> str:
    """Render a message as plain text (no colors).

    This is the canonical output format that all messages must follow:
    [LEVEL] CODE: What
      Why: explanation
      Fix: suggestion

    Args:
        message: The message to render
        indent: Number of spaces to indent

    Returns:
        Plain text representation
    """
    prefix = " " * indent
    lines = []

    # Main line: [LEVEL] CODE: What
    lines.append(f"{prefix}[{message.level}] {message.code}: {message.what}")

    # Location (if present)
    if message.location:
        lines.append(f"{prefix}  at {message.location}")

    # Why (if present)
    if message.why:
        lines.append(f"{prefix}  Why: {message.why}")

    # Fix (if present)
    if message.fix:
        lines.append(f"{prefix}  Fix: {message.fix}")

    return "\n".join(lines)


def render_colored(message: A11yMessage, indent: int = 0) -> str:
    """Render a message with ANSI colors for terminal display.

    Args:
        message: The message to render
        indent: Number of spaces to indent

    Returns:
        Colored text representation
    """
    prefix = " " * indent
    lines = []
    level_color = get_level_color(message.level)

    # Main line: [LEVEL] CODE: What
    level_str = f"{level_color}{Colors.BOLD}[{message.level}]{Colors.RESET}"
    code_str = f"{Colors.CODE}{message.code}{Colors.RESET}"
    lines.append(f"{prefix}{level_str} {code_str}: {message.what}")

    # Location (if present)
    if message.location:
        loc_str = f"{Colors.LOCATION}at {message.location}{Colors.RESET}"
        lines.append(f"{prefix}  {loc_str}")

    # Why (if present)
    if message.why:
        lines.append(f"{prefix}  {Colors.LABEL}Why:{Colors.RESET} {message.why}")

    # Fix (if present)
    if message.fix:
        lines.append(f"{prefix}  {Colors.LABEL}Fix:{Colors.RESET} {message.fix}")

    return "\n".join(lines)


def render(
    message: A11yMessage,
    *,
    color: bool = False,
    indent: int = 0,
) -> str:
    """Render a message to string.

    Args:
        message: The message to render
        color: Whether to include ANSI colors
        indent: Number of spaces to indent

    Returns:
        String representation
    """
    if color:
        return render_colored(message, indent)
    return render_plain(message, indent)


def render_batch(
    messages: list[A11yMessage],
    *,
    color: bool = False,
    separator: str = "\n",
) -> str:
    """Render multiple messages.

    Args:
        messages: Messages to render
        color: Whether to include ANSI colors
        separator: String between messages

    Returns:
        Combined string representation
    """
    return separator.join(render(msg, color=color) for msg in messages)


class Renderer:
    """Configurable message renderer with output stream support."""

    def __init__(
        self,
        *,
        color: bool | None = None,
        stream: TextIO | None = None,
        indent: int = 0,
    ) -> None:
        """Initialize the renderer.

        Args:
            color: Enable colors (None = auto-detect from terminal)
            stream: Output stream (default: stdout)
            indent: Base indentation level
        """
        self.stream = stream or sys.stdout
        self.indent = indent

        # Auto-detect color support (respects NO_COLOR env var)
        if color is None:
            self.color = should_use_color(self.stream)
        else:
            self.color = color

        self._counts = {Level.OK: 0, Level.WARN: 0, Level.ERROR: 0}

    def render(self, message: A11yMessage) -> str:
        """Render a message to string."""
        return render(message, color=self.color, indent=self.indent)

    def write(self, message: A11yMessage) -> None:
        """Render and write a message to the stream."""
        self._counts[message.level] += 1
        self.stream.write(self.render(message) + "\n")

    def write_batch(self, messages: list[A11yMessage]) -> None:
        """Render and write multiple messages."""
        for msg in messages:
            self.write(msg)

    @property
    def ok_count(self) -> int:
        """Number of OK messages written."""
        return self._counts[Level.OK]

    @property
    def warn_count(self) -> int:
        """Number of WARN messages written."""
        return self._counts[Level.WARN]

    @property
    def error_count(self) -> int:
        """Number of ERROR messages written."""
        return self._counts[Level.ERROR]

    @property
    def total_count(self) -> int:
        """Total number of messages written."""
        return sum(self._counts.values())

    def summary_line(self) -> str:
        """Get a summary line of counts."""
        parts = []
        if self.ok_count:
            parts.append(f"{self.ok_count} passed")
        if self.warn_count:
            parts.append(f"{self.warn_count} warnings")
        if self.error_count:
            parts.append(f"{self.error_count} errors")

        if not parts:
            return "No issues found"

        return ", ".join(parts)

    def write_summary(self) -> None:
        """Write a summary line to the stream."""
        summary = self.summary_line()
        if self.color:
            # Color the summary based on worst level
            if self.error_count:
                summary = f"{Colors.ERROR}{summary}{Colors.RESET}"
            elif self.warn_count:
                summary = f"{Colors.WARN}{summary}{Colors.RESET}"
            else:
                summary = f"{Colors.OK}{summary}{Colors.RESET}"

        self.stream.write(f"\n{summary}\n")


def format_for_file(messages: list[A11yMessage]) -> str:
    """Format messages for writing to a file (no colors, consistent format).

    Args:
        messages: Messages to format

    Returns:
        File-ready string
    """
    lines = []
    for msg in messages:
        lines.append(render_plain(msg))
        lines.append("")  # Blank line between messages

    return "\n".join(lines)
