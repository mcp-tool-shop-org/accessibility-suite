"""Markdown report renderer for accessibility assessments.

Generates detailed markdown reports from scan results and scorecards.
"""

from __future__ import annotations

from datetime import datetime
from typing import TextIO
import io

from .errors import A11yMessage, Level
from .scorecard import Scorecard


def render_message_md(message: A11yMessage) -> str:
    """Render a single message as markdown.

    Args:
        message: Message to render

    Returns:
        Markdown string
    """
    # Choose emoji based on level
    emoji = {"OK": "✅", "WARN": "⚠️", "ERROR": "❌"}[message.level.value]

    lines = [f"### {emoji} [{message.level}] {message.code}: {message.what}"]

    if message.location:
        loc_parts = []
        if message.location.file:
            loc_parts.append(f"`{message.location.file}`")
        if message.location.line:
            loc_parts.append(f"line {message.location.line}")
        if message.location.column:
            loc_parts.append(f"col {message.location.column}")
        if loc_parts:
            lines.append(f"\n**Location:** {' : '.join(loc_parts)}")

    if message.location and message.location.context:
        lines.append(f"\n```\n{message.location.context}\n```")

    if message.why:
        lines.append(f"\n**Why:** {message.why}")

    if message.fix:
        lines.append(f"\n**Fix:** {message.fix}")

    if message.rule:
        lines.append(f"\n*Rule: `{message.rule}`*")

    return "\n".join(lines)


def render_scorecard_md(scorecard: Scorecard) -> str:
    """Render a scorecard as markdown.

    Args:
        scorecard: Scorecard to render

    Returns:
        Markdown string
    """
    lines = [
        f"# {scorecard.name}",
        "",
        f"**Overall Score:** {scorecard.overall_score:.1f}% ({scorecard.overall_grade})",
        "",
        "## Summary",
        "",
        "| Metric | Count |",
        "|--------|-------|",
        f"| Total Checks | {scorecard.total_checks} |",
        f"| Passed | {scorecard.total_passed} |",
        f"| Warnings | {scorecard.total_warnings} |",
        f"| Errors | {scorecard.total_errors} |",
        "",
    ]

    # Rule breakdown table
    if scorecard.rule_scores:
        lines.extend(
            [
                "## Rules",
                "",
                "| Rule | Score | Grade | Passed | Warnings | Errors |",
                "|------|-------|-------|--------|----------|--------|",
            ]
        )

        for name, score in sorted(scorecard.rule_scores.items()):
            lines.append(
                f"| `{name}` | {score.score:.1f}% | {score.grade} | "
                f"{score.passed} | {score.warnings} | {score.errors} |"
            )

        lines.append("")

    # Issues by level
    errors = [m for m in scorecard.messages if m.level == Level.ERROR]
    warnings = [m for m in scorecard.messages if m.level == Level.WARN]

    if errors:
        lines.extend(["## Errors", ""])
        for msg in errors:
            lines.append(render_message_md(msg))
            lines.append("")

    if warnings:
        lines.extend(["## Warnings", ""])
        for msg in warnings:
            lines.append(render_message_md(msg))
            lines.append("")

    return "\n".join(lines)


def render_report_md(
    messages: list[A11yMessage],
    *,
    title: str = "Accessibility Report",
    include_timestamp: bool = True,
    include_summary: bool = True,
) -> str:
    """Render a full report as markdown.

    Args:
        messages: Messages to include
        title: Report title
        include_timestamp: Whether to include generation timestamp
        include_summary: Whether to include a summary section

    Returns:
        Markdown string
    """
    lines = [f"# {title}", ""]

    if include_timestamp:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lines.extend([f"*Generated: {now}*", ""])

    if include_summary:
        error_count = sum(1 for m in messages if m.level == Level.ERROR)
        warn_count = sum(1 for m in messages if m.level == Level.WARN)
        ok_count = sum(1 for m in messages if m.level == Level.OK)

        status = "✅ Passing" if error_count == 0 else "❌ Failing"
        lines.extend(
            [
                "## Summary",
                "",
                f"**Status:** {status}",
                "",
                f"- Errors: {error_count}",
                f"- Warnings: {warn_count}",
                f"- Passed: {ok_count}",
                "",
            ]
        )

    # Group messages by level
    errors = [m for m in messages if m.level == Level.ERROR]
    warnings = [m for m in messages if m.level == Level.WARN]
    passed = [m for m in messages if m.level == Level.OK]

    if errors:
        lines.extend(["## Errors", ""])
        for msg in errors:
            lines.append(render_message_md(msg))
            lines.append("")

    if warnings:
        lines.extend(["## Warnings", ""])
        for msg in warnings:
            lines.append(render_message_md(msg))
            lines.append("")

    if passed:
        lines.extend(["## Passed", ""])
        for msg in passed:
            lines.append(f"- ✅ `{msg.code}`: {msg.what}")
        lines.append("")

    return "\n".join(lines)


class MarkdownReporter:
    """Reporter for generating markdown reports with configuration."""

    def __init__(
        self,
        *,
        title: str = "Accessibility Report",
        include_timestamp: bool = True,
        include_passed: bool = False,
    ) -> None:
        """Initialize the reporter.

        Args:
            title: Report title
            include_timestamp: Include generation timestamp
            include_passed: Include passed checks in detail
        """
        self.title = title
        self.include_timestamp = include_timestamp
        self.include_passed = include_passed

    def render(self, messages: list[A11yMessage]) -> str:
        """Render messages to markdown.

        Args:
            messages: Messages to render

        Returns:
            Markdown string
        """
        return render_report_md(
            messages,
            title=self.title,
            include_timestamp=self.include_timestamp,
            include_summary=True,
        )

    def render_scorecard(self, scorecard: Scorecard) -> str:
        """Render a scorecard to markdown.

        Args:
            scorecard: Scorecard to render

        Returns:
            Markdown string
        """
        return render_scorecard_md(scorecard)

    def write(self, messages: list[A11yMessage], stream: TextIO) -> None:
        """Write markdown report to a stream.

        Args:
            messages: Messages to render
            stream: Output stream
        """
        stream.write(self.render(messages))

    def write_file(self, messages: list[A11yMessage], path: str) -> None:
        """Write markdown report to a file.

        Args:
            messages: Messages to render
            path: Output file path
        """
        with open(path, "w", encoding="utf-8") as f:
            self.write(messages, f)


def generate_badge_md(score: float, label: str = "a11y") -> str:
    """Generate a markdown badge showing the accessibility score.

    NOTE: Badges are informational only. They do NOT imply WCAG conformance.
    The score reflects policy compliance, not accessibility certification.

    Args:
        score: Score percentage (0-100)
        label: Badge label

    Returns:
        Markdown image reference for shields.io badge
    """
    # Choose color based on score
    if score >= 90:
        color = "brightgreen"
    elif score >= 70:
        color = "yellow"
    elif score >= 50:
        color = "orange"
    else:
        color = "red"

    # URL-encode the label and value
    value = f"{score:.0f}%25"  # %25 is URL-encoded %
    return f"![{label}](https://img.shields.io/badge/{label}-{value}-{color})"


# Disclaimer for badges and scores
SCORE_DISCLAIMER = (
    "**Note:** Scores and badges are informational only. They do NOT imply "
    "WCAG conformance or accessibility certification. This tool checks policy "
    "rules beyond minimum WCAG requirements."
)
