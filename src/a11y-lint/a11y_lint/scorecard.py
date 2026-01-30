"""Scorecard builder for accessibility assessments.

Generates scorecards summarizing accessibility check results.

Philosophy:
- Grades (A-F) are DERIVED summaries for executive reporting
- Grades are NEVER primary - CI gates should be based on:
  - Specific rule failures (especially WCAG-mapped rules)
  - Error count thresholds
  - Regressions from baseline
- Grades compress nuance; always check underlying rule failures
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .errors import A11yMessage, Level


@dataclass
class RuleScore:
    """Score for a single rule."""

    rule: str
    passed: int = 0
    warnings: int = 0
    errors: int = 0

    @property
    def total(self) -> int:
        """Total number of checks for this rule."""
        return self.passed + self.warnings + self.errors

    @property
    def score(self) -> float:
        """Score as a percentage (0-100)."""
        if self.total == 0:
            return 100.0
        # Passed = full points, warnings = half points, errors = no points
        points = self.passed + (self.warnings * 0.5)
        return (points / self.total) * 100

    @property
    def grade(self) -> str:
        """Letter grade based on score."""
        s = self.score
        if s >= 90:
            return "A"
        elif s >= 80:
            return "B"
        elif s >= 70:
            return "C"
        elif s >= 60:
            return "D"
        else:
            return "F"


@dataclass
class Scorecard:
    """Accessibility scorecard summarizing check results."""

    name: str
    rule_scores: dict[str, RuleScore] = field(default_factory=dict)
    messages: list[A11yMessage] = field(default_factory=list)

    def add_message(self, message: A11yMessage) -> None:
        """Add a message to the scorecard."""
        self.messages.append(message)

        # Get or create rule score
        rule_name = message.rule or "unknown"
        if rule_name not in self.rule_scores:
            self.rule_scores[rule_name] = RuleScore(rule=rule_name)

        score = self.rule_scores[rule_name]
        if message.level == Level.OK:
            score.passed += 1
        elif message.level == Level.WARN:
            score.warnings += 1
        elif message.level == Level.ERROR:
            score.errors += 1

    def add_messages(self, messages: list[A11yMessage]) -> None:
        """Add multiple messages to the scorecard."""
        for msg in messages:
            self.add_message(msg)

    @property
    def total_passed(self) -> int:
        """Total number of passed checks."""
        return sum(s.passed for s in self.rule_scores.values())

    @property
    def total_warnings(self) -> int:
        """Total number of warnings."""
        return sum(s.warnings for s in self.rule_scores.values())

    @property
    def total_errors(self) -> int:
        """Total number of errors."""
        return sum(s.errors for s in self.rule_scores.values())

    @property
    def total_checks(self) -> int:
        """Total number of checks performed."""
        return self.total_passed + self.total_warnings + self.total_errors

    @property
    def overall_score(self) -> float:
        """Overall accessibility score (0-100)."""
        if self.total_checks == 0:
            return 100.0
        points = self.total_passed + (self.total_warnings * 0.5)
        return (points / self.total_checks) * 100

    @property
    def overall_grade(self) -> str:
        """Overall letter grade."""
        s = self.overall_score
        if s >= 90:
            return "A"
        elif s >= 80:
            return "B"
        elif s >= 70:
            return "C"
        elif s >= 60:
            return "D"
        else:
            return "F"

    @property
    def is_passing(self) -> bool:
        """Check if the scorecard represents a passing assessment."""
        return self.total_errors == 0

    def summary(self) -> str:
        """Get a text summary of the scorecard."""
        lines = [
            f"Accessibility Scorecard: {self.name}",
            "=" * 40,
            f"Overall Score: {self.overall_score:.1f}% ({self.overall_grade})",
            f"Total Checks: {self.total_checks}",
            f"  Passed: {self.total_passed}",
            f"  Warnings: {self.total_warnings}",
            f"  Errors: {self.total_errors}",
            "",
            "By Rule:",
        ]

        for rule_name, score in sorted(self.rule_scores.items()):
            lines.append(
                f"  {rule_name}: {score.score:.1f}% ({score.grade}) "
                f"[{score.passed}P/{score.warnings}W/{score.errors}E]"
            )

        return "\n".join(lines)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "name": self.name,
            "overall_score": round(self.overall_score, 2),
            "overall_grade": self.overall_grade,
            "is_passing": self.is_passing,
            "totals": {
                "checks": self.total_checks,
                "passed": self.total_passed,
                "warnings": self.total_warnings,
                "errors": self.total_errors,
            },
            "rules": {
                name: {
                    "score": round(score.score, 2),
                    "grade": score.grade,
                    "passed": score.passed,
                    "warnings": score.warnings,
                    "errors": score.errors,
                }
                for name, score in self.rule_scores.items()
            },
            "messages": [msg.to_dict() for msg in self.messages],
        }


class ScorecardBuilder:
    """Builder for creating scorecards from scan results."""

    def __init__(self, name: str = "CLI Accessibility Assessment") -> None:
        """Initialize the builder.

        Args:
            name: Name for the scorecard
        """
        self.scorecard = Scorecard(name=name)

    def add_scan_result(self, messages: list[A11yMessage]) -> ScorecardBuilder:
        """Add scan results to the scorecard.

        Args:
            messages: Messages from scanning

        Returns:
            Self for chaining
        """
        self.scorecard.add_messages(messages)
        return self

    def add_ok_check(self, rule: str, code: str, what: str) -> ScorecardBuilder:
        """Record a passing check.

        Args:
            rule: Rule name
            code: Error code
            what: Description of what was checked

        Returns:
            Self for chaining
        """
        self.scorecard.add_message(A11yMessage.ok(code, what, rule=rule))
        return self

    def build(self) -> Scorecard:
        """Build and return the scorecard."""
        return self.scorecard


def create_scorecard(
    messages: list[A11yMessage], name: str = "CLI Accessibility Assessment"
) -> Scorecard:
    """Convenience function to create a scorecard from messages.

    Args:
        messages: Messages to include
        name: Name for the scorecard

    Returns:
        Built scorecard
    """
    builder = ScorecardBuilder(name)
    builder.add_scan_result(messages)
    return builder.build()
