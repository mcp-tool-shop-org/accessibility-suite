"""Tests for report_md module."""

import pytest
from io import StringIO

from a11y_lint.report_md import (
    render_message_md,
    render_scorecard_md,
    render_report_md,
    MarkdownReporter,
    generate_badge_md,
)
from a11y_lint.errors import A11yMessage, Level, Location
from a11y_lint.scorecard import Scorecard


class TestRenderMessageMd:
    """Tests for render_message_md function."""

    def test_ok_message(self) -> None:
        msg = A11yMessage.ok("TST001", "Test passed")
        md = render_message_md(msg)
        assert "### " in md
        assert "[OK]" in md
        assert "TST001" in md
        assert "Test passed" in md

    def test_error_message_has_why_fix(self) -> None:
        msg = A11yMessage.error("TST001", "Error", "This is why", "This is fix")
        md = render_message_md(msg)
        assert "**Why:**" in md
        assert "This is why" in md
        assert "**Fix:**" in md
        assert "This is fix" in md

    def test_message_with_location(self) -> None:
        msg = A11yMessage.ok(
            "TST001",
            "Test",
            location=Location(file="test.py", line=10, column=5),
        )
        md = render_message_md(msg)
        assert "**Location:**" in md
        assert "test.py" in md
        assert "line 10" in md

    def test_message_with_context(self) -> None:
        msg = A11yMessage.ok(
            "TST001",
            "Test",
            location=Location(context="some code here"),
        )
        md = render_message_md(msg)
        assert "```" in md
        assert "some code here" in md

    def test_message_with_rule(self) -> None:
        msg = A11yMessage.ok("TST001", "Test", rule="test-rule")
        md = render_message_md(msg)
        assert "*Rule: `test-rule`*" in md


class TestRenderScorecardMd:
    """Tests for render_scorecard_md function."""

    def test_empty_scorecard(self) -> None:
        card = Scorecard(name="Test Card")
        md = render_scorecard_md(card)
        assert "# Test Card" in md
        assert "100.0% (A)" in md

    def test_scorecard_with_rules(self) -> None:
        card = Scorecard(name="Test")
        card.add_message(A11yMessage.ok("TST001", "Test", rule="rule-a"))
        card.add_message(A11yMessage.warn("TST002", "Test", "Why", rule="rule-b"))
        md = render_scorecard_md(card)
        assert "## Rules" in md
        assert "`rule-a`" in md
        assert "`rule-b`" in md

    def test_scorecard_summary_table(self) -> None:
        card = Scorecard(name="Test")
        card.add_message(A11yMessage.ok("TST001", "Test", rule="r"))
        md = render_scorecard_md(card)
        assert "| Metric | Count |" in md
        assert "| Total Checks | 1 |" in md


class TestRenderReportMd:
    """Tests for render_report_md function."""

    def test_empty_report(self) -> None:
        md = render_report_md([])
        assert "# Accessibility Report" in md
        assert "## Summary" in md
        assert "Passing" in md

    def test_report_with_errors(self) -> None:
        messages = [
            A11yMessage.error("TST001", "Error 1", "Why", "Fix", rule="r"),
        ]
        md = render_report_md(messages)
        assert "Failing" in md
        assert "## Errors" in md
        assert "Errors: 1" in md

    def test_report_with_warnings(self) -> None:
        messages = [
            A11yMessage.warn("TST001", "Warning 1", "Why", rule="r"),
        ]
        md = render_report_md(messages)
        assert "## Warnings" in md
        assert "Warnings: 1" in md

    def test_report_with_passed(self) -> None:
        messages = [
            A11yMessage.ok("TST001", "Passed 1", rule="r"),
        ]
        md = render_report_md(messages)
        assert "## Passed" in md
        assert "TST001" in md

    def test_custom_title(self) -> None:
        md = render_report_md([], title="Custom Title")
        assert "# Custom Title" in md

    def test_timestamp(self) -> None:
        md = render_report_md([], include_timestamp=True)
        assert "*Generated:" in md

    def test_no_timestamp(self) -> None:
        md = render_report_md([], include_timestamp=False)
        assert "*Generated:" not in md


class TestMarkdownReporter:
    """Tests for MarkdownReporter class."""

    def test_render(self) -> None:
        reporter = MarkdownReporter(title="Test Report")
        messages = [A11yMessage.ok("TST001", "Test")]
        md = reporter.render(messages)
        assert "# Test Report" in md

    def test_render_scorecard(self) -> None:
        reporter = MarkdownReporter()
        card = Scorecard(name="Test Card")
        md = reporter.render_scorecard(card)
        assert "# Test Card" in md

    def test_write_to_stream(self) -> None:
        reporter = MarkdownReporter()
        messages = [A11yMessage.ok("TST001", "Test")]
        stream = StringIO()
        reporter.write(messages, stream)
        output = stream.getvalue()
        assert "# Accessibility Report" in output


class TestGenerateBadgeMd:
    """Tests for generate_badge_md function."""

    def test_high_score_green(self) -> None:
        badge = generate_badge_md(95)
        assert "brightgreen" in badge
        assert "95%25" in badge

    def test_medium_score_yellow(self) -> None:
        badge = generate_badge_md(75)
        assert "yellow" in badge

    def test_low_score_orange(self) -> None:
        badge = generate_badge_md(55)
        assert "orange" in badge

    def test_very_low_score_red(self) -> None:
        badge = generate_badge_md(40)
        assert "red" in badge

    def test_custom_label(self) -> None:
        badge = generate_badge_md(90, label="accessibility")
        assert "accessibility" in badge

    def test_shields_io_format(self) -> None:
        badge = generate_badge_md(90)
        assert "shields.io/badge" in badge
        assert "![" in badge
        assert "](" in badge
