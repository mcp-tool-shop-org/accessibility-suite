"""CLI text scanner for accessibility issues.

Scans CLI output text and detects common accessibility problems.

Rule Categories:
- WCAG: Rules mapped to WCAG success criteria (failures are accessibility violations)
- Policy: Cognitive accessibility and best practice rules (not WCAG requirements)

This distinction matters: "WCAG doesn't forbid all caps" is true, but this tool
enforces accessibility policy beyond minimum WCAG compliance.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable

from .errors import A11yMessage, ErrorCodes, Level, Location


class RuleCategory(Enum):
    """Category of accessibility rule."""

    WCAG = "wcag"  # Mapped to WCAG success criteria
    POLICY = "policy"  # Best practice / cognitive accessibility


@dataclass
class Rule:
    """An accessibility rule that can be checked against text.

    Attributes:
        name: Rule identifier (e.g., "no-color-only")
        code: Error code (e.g., "CLR001")
        description: Human-readable description
        check: Function that performs the check
        category: WCAG or Policy
        wcag_ref: WCAG success criterion reference (if applicable)
    """

    name: str
    code: str
    description: str
    check: Callable[[str, str | None, int], A11yMessage | None]
    category: RuleCategory = RuleCategory.POLICY
    wcag_ref: str | None = None

    def __call__(
        self, text: str, file: str | None = None, line: int = 1
    ) -> A11yMessage | None:
        """Run the rule check."""
        return self.check(text, file, line)


# Common jargon and technical terms that may be unclear
JARGON_PATTERNS = [
    (r"\bNaN\b", "NaN (Not a Number)"),
    (r"\bEOF\b", "EOF (End of File)"),
    (r"\bEOL\b", "EOL (End of Line)"),
    (r"\bSTDIN\b", "STDIN (standard input)"),
    (r"\bSTDOUT\b", "STDOUT (standard output)"),
    (r"\bSTDERR\b", "STDERR (standard error)"),
    (r"\bSIGKILL\b", "SIGKILL signal"),
    (r"\bSIGTERM\b", "SIGTERM signal"),
    (r"\bOOM\b", "OOM (Out of Memory)"),
    (r"\bTTY\b", "TTY (terminal)"),
    (r"\bPID\b", "PID (process ID)"),
    (r"\bUID\b", "UID (user ID)"),
    (r"\bGID\b", "GID (group ID)"),
]

# Patterns that suggest color-only information
COLOR_ONLY_PATTERNS = [
    r"shown in (red|green|yellow|blue)",
    r"(red|green|yellow|blue) indicates",
    r"highlighted in (red|green|yellow|blue)",
    r"marked (red|green|yellow|blue)",
]

# Maximum recommended line length for readability
MAX_LINE_LENGTH = 120

# Emoji regex (simplified, catches common emoji ranges)
EMOJI_PATTERN = re.compile(
    r"[\U0001F300-\U0001F9FF]|[\U00002600-\U000027BF]|[\U0001FA00-\U0001FAFF]"
)


def _make_location(
    file: str | None, line: int, column: int | None = None, context: str | None = None
) -> Location:
    """Create a Location object."""
    return Location(file=file, line=line, column=column, context=context)


def check_line_length(text: str, file: str | None, line_num: int) -> A11yMessage | None:
    """Check if any line exceeds the maximum recommended length."""
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if len(line) > MAX_LINE_LENGTH:
            return A11yMessage.warn(
                code=ErrorCodes.LINE_TOO_LONG,
                what=f"Line {line_num + i} is {len(line)} characters long",
                why=(
                    "Long lines are difficult to read, especially for users with "
                    "cognitive disabilities or those using screen magnification."
                ),
                fix=f"Break the line into multiple lines of {MAX_LINE_LENGTH} characters or fewer.",
                rule="line-length",
                location=_make_location(file, line_num + i, context=line[:80] + "..."),
            )
    return None


def check_all_caps(text: str, file: str | None, line_num: int) -> A11yMessage | None:
    """Check for all-caps messages (excluding short acronyms)."""
    # Find words that are all caps and longer than 4 characters
    words = re.findall(r"\b[A-Z]{5,}\b", text)
    # Filter out common acronyms
    acronyms = {"ERROR", "WARN", "DEBUG", "FATAL", "TRACE", "HTTPS", "HTTP"}
    long_caps = [w for w in words if w not in acronyms]

    if long_caps:
        return A11yMessage.warn(
            code=ErrorCodes.ALL_CAPS_MESSAGE,
            what=f"All-caps text detected: {', '.join(long_caps[:3])}",
            why=(
                "All-caps text is harder to read and may be interpreted as shouting. "
                "Screen readers may spell out each letter instead of reading words."
            ),
            fix="Use sentence case or title case instead of all caps.",
            rule="no-all-caps",
            location=_make_location(file, line_num),
        )
    return None


def check_jargon(text: str, file: str | None, line_num: int) -> A11yMessage | None:
    """Check for technical jargon that may be unclear."""
    for pattern, term in JARGON_PATTERNS:
        match = re.search(pattern, text)
        if match:
            return A11yMessage.warn(
                code=ErrorCodes.JARGON_DETECTED,
                what=f"Technical jargon detected: '{match.group()}'",
                why=(
                    "Technical abbreviations may be unfamiliar to new users or those "
                    "using assistive technologies that read text literally."
                ),
                fix=f"Consider expanding or explaining the term: {term}",
                rule="plain-language",
                location=_make_location(
                    file, line_num, column=match.start() + 1, context=match.group()
                ),
            )
    return None


def check_color_only(text: str, file: str | None, line_num: int) -> A11yMessage | None:
    """Check for information conveyed only through color."""
    text_lower = text.lower()
    for pattern in COLOR_ONLY_PATTERNS:
        match = re.search(pattern, text_lower)
        if match:
            return A11yMessage.error(
                code=ErrorCodes.COLOR_ONLY_INFO,
                what="Information conveyed only through color",
                why=(
                    "Users who are colorblind or using monochrome displays cannot "
                    "perceive color-based information. This violates WCAG 2.1 SC 1.4.1."
                ),
                fix=(
                    "Supplement color with text indicators like [ERROR], [OK], or icons. "
                    "Never rely solely on color to convey meaning."
                ),
                rule="no-color-only",
                location=_make_location(file, line_num, context=match.group()),
            )
    return None


def check_emoji_overuse(text: str, file: str | None, line_num: int) -> A11yMessage | None:
    """Check for excessive emoji use that may confuse screen readers."""
    emojis = EMOJI_PATTERN.findall(text)
    if len(emojis) > 3:
        return A11yMessage.warn(
            code=ErrorCodes.EMOJI_OVERUSE,
            what=f"Excessive emoji use ({len(emojis)} emojis in message)",
            why=(
                "Screen readers announce each emoji by name, which can be verbose "
                "and interrupt the flow of information."
            ),
            fix="Limit emojis to 1-2 per message and ensure meaning is also conveyed in text.",
            rule="emoji-moderation",
            location=_make_location(file, line_num),
            metadata={"emoji_count": len(emojis)},
        )
    return None


def check_missing_punctuation(
    text: str, file: str | None, line_num: int
) -> A11yMessage | None:
    """Check if error messages lack proper punctuation."""
    # Only check lines that look like error messages
    if not any(
        marker in text.upper() for marker in ["ERROR", "WARN", "FAIL", "INVALID"]
    ):
        return None

    # Check if the message ends with punctuation
    stripped = text.rstrip()
    if stripped and stripped[-1] not in ".!?:":
        return A11yMessage.warn(
            code=ErrorCodes.NO_PUNCTUATION,
            what="Error message lacks ending punctuation",
            why=(
                "Proper punctuation helps screen readers use appropriate pauses and "
                "intonation, improving comprehension."
            ),
            fix="End error messages with appropriate punctuation (period, exclamation, or colon).",
            rule="punctuation",
            location=_make_location(file, line_num, context=stripped[-50:]),
        )
    return None


def check_error_structure(
    text: str, file: str | None, line_num: int
) -> A11yMessage | None:
    """Check if error messages follow the What/Why/Fix structure."""
    # Look for error indicators
    if not any(marker in text.upper() for marker in ["ERROR", "FAIL", "EXCEPTION"]):
        return None

    # Check for explanation (why/because/since)
    has_why = any(
        word in text.lower() for word in ["because", "since", "due to", "reason"]
    )
    # Check for fix suggestion
    has_fix = any(
        word in text.lower()
        for word in ["try", "fix", "resolve", "solution", "to fix", "you can"]
    )

    if not has_why and not has_fix:
        return A11yMessage.warn(
            code=ErrorCodes.MISSING_WHY,
            what="Error message lacks explanation or fix suggestion",
            why=(
                "Users benefit from understanding why an error occurred and how to "
                "fix it. This is especially important for users with cognitive disabilities."
            ),
            fix="Add context explaining why the error occurred and suggest how to resolve it.",
            rule="error-structure",
            location=_make_location(file, line_num),
        )
    return None


def check_ambiguous_pronouns(
    text: str, file: str | None, line_num: int
) -> A11yMessage | None:
    """Check for ambiguous pronouns without clear referents."""
    # Patterns like "it failed" or "this is invalid" at the start
    ambiguous = re.search(
        r"^(it|this|that|these|those)\s+(is|was|are|were|failed|error)",
        text.lower().strip(),
    )
    if ambiguous:
        return A11yMessage.warn(
            code=ErrorCodes.AMBIGUOUS_PRONOUN,
            what=f"Ambiguous pronoun '{ambiguous.group(1)}' without clear referent",
            why=(
                "Pronouns without clear referents can confuse users, especially those "
                "with cognitive disabilities or those using screen readers."
            ),
            fix="Replace the pronoun with the specific thing being referenced.",
            rule="no-ambiguous-pronouns",
            location=_make_location(file, line_num, context=ambiguous.group()),
        )
    return None


# Registry of all rules
# WCAG rules: Mapped to specific success criteria - failures are accessibility violations
# Policy rules: Best practices for cognitive accessibility - not WCAG requirements
RULES: list[Rule] = [
    # Policy rules (cognitive accessibility, best practices)
    Rule(
        "line-length", ErrorCodes.LINE_TOO_LONG, "Check line length",
        check_line_length, RuleCategory.POLICY
    ),
    Rule(
        "no-all-caps", ErrorCodes.ALL_CAPS_MESSAGE, "Check for all caps",
        check_all_caps, RuleCategory.POLICY
    ),
    Rule(
        "plain-language", ErrorCodes.JARGON_DETECTED, "Check for jargon",
        check_jargon, RuleCategory.POLICY
    ),
    Rule(
        "emoji-moderation", ErrorCodes.EMOJI_OVERUSE, "Check emoji overuse",
        check_emoji_overuse, RuleCategory.POLICY
    ),
    Rule(
        "punctuation", ErrorCodes.NO_PUNCTUATION, "Check punctuation",
        check_missing_punctuation, RuleCategory.POLICY
    ),
    Rule(
        "error-structure", ErrorCodes.MISSING_WHY, "Check error structure",
        check_error_structure, RuleCategory.POLICY
    ),
    Rule(
        "no-ambiguous-pronouns", ErrorCodes.AMBIGUOUS_PRONOUN, "Check ambiguous pronouns",
        check_ambiguous_pronouns, RuleCategory.POLICY
    ),
    # WCAG rules (mapped to success criteria)
    Rule(
        "no-color-only", ErrorCodes.COLOR_ONLY_INFO, "Check color-only info",
        check_color_only, RuleCategory.WCAG, wcag_ref="1.4.1"
    ),
]


class Scanner:
    """Scanner that runs accessibility rules against CLI text."""

    def __init__(self, rules: list[Rule] | None = None) -> None:
        """Initialize the scanner.

        Args:
            rules: Rules to use (default: all rules)
        """
        self.rules = rules or RULES.copy()
        self.messages: list[A11yMessage] = []

    def enable_rule(self, name: str) -> None:
        """Enable a rule by name."""
        for rule in RULES:
            if rule.name == name and rule not in self.rules:
                self.rules.append(rule)
                break

    def disable_rule(self, name: str) -> None:
        """Disable a rule by name."""
        self.rules = [r for r in self.rules if r.name != name]

    def scan_line(self, line: str, file: str | None = None, line_num: int = 1) -> list[A11yMessage]:
        """Scan a single line of text.

        Args:
            line: Line to scan
            file: Source file path (for error reporting)
            line_num: Line number (for error reporting)

        Returns:
            List of issues found
        """
        issues = []
        for rule in self.rules:
            result = rule(line, file, line_num)
            if result:
                issues.append(result)
        return issues

    def scan_text(self, text: str, file: str | None = None) -> list[A11yMessage]:
        """Scan a block of text.

        Args:
            text: Text to scan
            file: Source file path (for error reporting)

        Returns:
            List of issues found
        """
        self.messages = []
        lines = text.split("\n")

        for i, line in enumerate(lines, start=1):
            if line.strip():  # Skip empty lines
                issues = self.scan_line(line, file, i)
                self.messages.extend(issues)

        return self.messages

    def scan_file(self, path: str) -> list[A11yMessage]:
        """Scan a file for accessibility issues.

        Args:
            path: Path to file to scan

        Returns:
            List of issues found
        """
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        return self.scan_text(text, file=path)

    @property
    def error_count(self) -> int:
        """Number of ERROR-level issues found."""
        return sum(1 for m in self.messages if m.level == Level.ERROR)

    @property
    def warn_count(self) -> int:
        """Number of WARN-level issues found."""
        return sum(1 for m in self.messages if m.level == Level.WARN)

    @property
    def has_errors(self) -> bool:
        """Check if any ERROR-level issues were found."""
        return self.error_count > 0


def scan(text: str, file: str | None = None) -> list[A11yMessage]:
    """Convenience function to scan text with default rules.

    Args:
        text: Text to scan
        file: Source file path (for error reporting)

    Returns:
        List of issues found
    """
    scanner = Scanner()
    return scanner.scan_text(text, file)


def get_rule_names() -> list[str]:
    """Get the names of all available rules."""
    return [r.name for r in RULES]
