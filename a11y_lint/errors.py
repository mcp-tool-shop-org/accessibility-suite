"""Ground truth error dataclasses for CLI accessibility messages.

All error messages follow the What/Why/Fix structure for maximum accessibility.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Level(Enum):
    """Severity level of an accessibility check result."""

    OK = "OK"
    WARN = "WARN"
    ERROR = "ERROR"

    def __str__(self) -> str:
        return self.value


# Pattern for valid error codes: 2-4 alphanumeric chars (starting with letter) followed by 3 digits
# Examples: A11Y001, FMT001, CLI002, TST123
CODE_PATTERN = re.compile(r"^[A-Z][A-Z0-9]{1,3}[0-9]{3}$")


@dataclass(frozen=True)
class Location:
    """Location of an issue in the source text."""

    file: str | None = None
    line: int | None = None
    column: int | None = None
    context: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary, omitting None values."""
        result: dict[str, Any] = {}
        if self.file is not None:
            result["file"] = self.file
        if self.line is not None:
            result["line"] = self.line
        if self.column is not None:
            result["column"] = self.column
        if self.context is not None:
            # Truncate context to schema max
            result["context"] = self.context[:200]
        return result

    def __str__(self) -> str:
        parts = []
        if self.file:
            parts.append(self.file)
        if self.line is not None:
            parts.append(f"line {self.line}")
        if self.column is not None:
            parts.append(f"col {self.column}")
        return ":".join(parts) if parts else "<unknown>"


@dataclass(frozen=True)
class A11yMessage:
    """An accessibility check result with What/Why/Fix structure.

    Attributes:
        level: Severity (OK, WARN, ERROR)
        code: Unique identifier (e.g., A11Y001)
        what: Brief description of what happened
        why: Why this matters for accessibility (required for ERROR)
        fix: How to fix the issue (required for ERROR)
        location: Where the issue was found
        rule: Name of the rule that was checked
        metadata: Additional rule-specific data
    """

    level: Level
    code: str
    what: str
    why: str | None = None
    fix: str | None = None
    location: Location | None = None
    rule: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate the message structure."""
        # Validate code format
        if not CODE_PATTERN.match(self.code):
            raise ValueError(
                f"Invalid error code '{self.code}': must match pattern [A-Z]{{2,4}}[0-9]{{3}}"
            )

        # Validate what is not empty
        if not self.what or not self.what.strip():
            raise ValueError("'what' field cannot be empty")

        # Truncate what to schema max
        if len(self.what) > 200:
            object.__setattr__(self, "what", self.what[:200])

        # ERROR level requires why and fix
        if self.level == Level.ERROR:
            if not self.why:
                raise ValueError("ERROR level messages must include 'why'")
            if not self.fix:
                raise ValueError("ERROR level messages must include 'fix'")

        # Truncate why/fix to schema max
        if self.why and len(self.why) > 500:
            object.__setattr__(self, "why", self.why[:500])
        if self.fix and len(self.fix) > 500:
            object.__setattr__(self, "fix", self.fix[:500])

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary matching the JSON schema."""
        result: dict[str, Any] = {
            "level": self.level.value,
            "code": self.code,
            "what": self.what,
        }

        if self.why:
            result["why"] = self.why
        if self.fix:
            result["fix"] = self.fix
        if self.location:
            result["location"] = self.location.to_dict()
        if self.rule:
            result["rule"] = self.rule
        if self.metadata:
            result["metadata"] = self.metadata

        return result

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> A11yMessage:
        """Create from a dictionary (e.g., parsed JSON)."""
        location = None
        if "location" in data:
            loc_data = data["location"]
            location = Location(
                file=loc_data.get("file"),
                line=loc_data.get("line"),
                column=loc_data.get("column"),
                context=loc_data.get("context"),
            )

        return cls(
            level=Level(data["level"]),
            code=data["code"],
            what=data["what"],
            why=data.get("why"),
            fix=data.get("fix"),
            location=location,
            rule=data.get("rule"),
            metadata=data.get("metadata", {}),
        )

    @classmethod
    def ok(
        cls,
        code: str,
        what: str,
        *,
        rule: str | None = None,
        location: Location | None = None,
    ) -> A11yMessage:
        """Create an OK (passing) check result."""
        return cls(level=Level.OK, code=code, what=what, rule=rule, location=location)

    @classmethod
    def warn(
        cls,
        code: str,
        what: str,
        why: str,
        *,
        fix: str | None = None,
        rule: str | None = None,
        location: Location | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> A11yMessage:
        """Create a WARN (advisory) check result."""
        return cls(
            level=Level.WARN,
            code=code,
            what=what,
            why=why,
            fix=fix,
            rule=rule,
            location=location,
            metadata=metadata or {},
        )

    @classmethod
    def error(
        cls,
        code: str,
        what: str,
        why: str,
        fix: str,
        *,
        rule: str | None = None,
        location: Location | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> A11yMessage:
        """Create an ERROR (failing) check result."""
        return cls(
            level=Level.ERROR,
            code=code,
            what=what,
            why=why,
            fix=fix,
            rule=rule,
            location=location,
            metadata=metadata or {},
        )


# Pre-defined error codes for common accessibility issues
class ErrorCodes:
    """Standard error codes for accessibility checks."""

    # Structure errors (A11Y0xx)
    MISSING_ERROR_CODE = "A11Y001"
    MISSING_WHAT = "A11Y002"
    MISSING_WHY = "A11Y003"
    MISSING_FIX = "A11Y004"
    INVALID_LEVEL = "A11Y005"

    # Format errors (FMT0xx)
    LINE_TOO_LONG = "FMT001"
    NO_NEWLINE_END = "FMT002"
    INCONSISTENT_INDENT = "FMT003"

    # Language errors (LNG0xx)
    JARGON_DETECTED = "LNG001"
    ALL_CAPS_MESSAGE = "LNG002"
    NO_PUNCTUATION = "LNG003"
    AMBIGUOUS_PRONOUN = "LNG004"

    # Color/contrast (CLR0xx)
    COLOR_ONLY_INFO = "CLR001"
    LOW_CONTRAST = "CLR002"

    # Screen reader (SCR0xx)
    EMOJI_OVERUSE = "SCR001"
    UNICODE_ISSUE = "SCR002"
    MISSING_ALT_TEXT = "SCR003"
