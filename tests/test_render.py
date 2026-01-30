"""Tests for render module."""

import io
import pytest

from a11y_lint.render import (
    render,
    render_plain,
    render_colored,
    render_batch,
    Renderer,
    format_for_file,
    Colors,
    get_level_color,
)
from a11y_lint.errors import A11yMessage, Level, Location


class TestRenderPlain:
    """Tests for render_plain function."""

    def test_ok_message(self) -> None:
        msg = A11yMessage.ok("TST001", "Test passed")
        output = render_plain(msg)
        assert "[OK] TST001: Test passed" in output

    def test_warn_message(self) -> None:
        msg = A11yMessage.warn("TST002", "Test warning", "This is why")
        output = render_plain(msg)
        assert "[WARN] TST002: Test warning" in output
        assert "Why: This is why" in output

    def test_error_message(self) -> None:
        msg = A11yMessage.error("TST003", "Test error", "Reason", "Fix this")
        output = render_plain(msg)
        assert "[ERROR] TST003: Test error" in output
        assert "Why: Reason" in output
        assert "Fix: Fix this" in output

    def test_message_with_location(self) -> None:
        msg = A11yMessage.ok(
            "TST001",
            "Test",
            location=Location(file="test.py", line=10, column=5),
        )
        output = render_plain(msg)
        assert "at test.py" in output
        assert "line 10" in output
        assert "col 5" in output

    def test_indentation(self) -> None:
        msg = A11yMessage.ok("TST001", "Test")
        output = render_plain(msg, indent=4)
        assert output.startswith("    [OK]")


class TestRenderColored:
    """Tests for render_colored function."""

    def test_contains_color_codes(self) -> None:
        msg = A11yMessage.ok("TST001", "Test")
        output = render_colored(msg)
        assert Colors.OK in output
        assert Colors.RESET in output

    def test_error_uses_red(self) -> None:
        msg = A11yMessage.error("TST001", "Test", "Why", "Fix")
        output = render_colored(msg)
        assert Colors.ERROR in output

    def test_warn_uses_yellow(self) -> None:
        msg = A11yMessage.warn("TST001", "Test", "Why")
        output = render_colored(msg)
        assert Colors.WARN in output


class TestRender:
    """Tests for render function."""

    def test_default_no_color(self) -> None:
        msg = A11yMessage.ok("TST001", "Test")
        output = render(msg)
        assert Colors.OK not in output

    def test_color_enabled(self) -> None:
        msg = A11yMessage.ok("TST001", "Test")
        output = render(msg, color=True)
        assert Colors.OK in output

    def test_color_disabled(self) -> None:
        msg = A11yMessage.ok("TST001", "Test")
        output = render(msg, color=False)
        assert Colors.OK not in output


class TestRenderBatch:
    """Tests for render_batch function."""

    def test_multiple_messages(self) -> None:
        messages = [
            A11yMessage.ok("TST001", "Test 1"),
            A11yMessage.ok("TST002", "Test 2"),
        ]
        output = render_batch(messages)
        assert "TST001" in output
        assert "TST002" in output

    def test_custom_separator(self) -> None:
        messages = [
            A11yMessage.ok("TST001", "Test 1"),
            A11yMessage.ok("TST002", "Test 2"),
        ]
        output = render_batch(messages, separator="\n\n")
        assert "\n\n" in output


class TestGetLevelColor:
    """Tests for get_level_color function."""

    def test_ok_green(self) -> None:
        assert get_level_color(Level.OK) == Colors.OK

    def test_warn_yellow(self) -> None:
        assert get_level_color(Level.WARN) == Colors.WARN

    def test_error_red(self) -> None:
        assert get_level_color(Level.ERROR) == Colors.ERROR


class TestRenderer:
    """Tests for Renderer class."""

    def test_render_to_stream(self) -> None:
        stream = io.StringIO()
        renderer = Renderer(color=False, stream=stream)
        msg = A11yMessage.ok("TST001", "Test")
        renderer.write(msg)
        output = stream.getvalue()
        assert "[OK] TST001: Test" in output

    def test_counts_messages(self) -> None:
        stream = io.StringIO()
        renderer = Renderer(color=False, stream=stream)

        renderer.write(A11yMessage.ok("TST001", "Test 1"))
        renderer.write(A11yMessage.warn("TST002", "Test 2", "Why"))
        renderer.write(A11yMessage.error("TST003", "Test 3", "Why", "Fix"))

        assert renderer.ok_count == 1
        assert renderer.warn_count == 1
        assert renderer.error_count == 1
        assert renderer.total_count == 3

    def test_summary_line(self) -> None:
        renderer = Renderer(color=False, stream=io.StringIO())
        assert renderer.summary_line() == "No issues found"

        renderer.write(A11yMessage.ok("TST001", "Test"))
        assert "1 passed" in renderer.summary_line()

        renderer.write(A11yMessage.warn("TST002", "Test", "Why"))
        assert "1 warnings" in renderer.summary_line()

        renderer.write(A11yMessage.error("TST003", "Test", "Why", "Fix"))
        assert "1 errors" in renderer.summary_line()

    def test_write_batch(self) -> None:
        stream = io.StringIO()
        renderer = Renderer(color=False, stream=stream)
        messages = [
            A11yMessage.ok("TST001", "Test 1"),
            A11yMessage.ok("TST002", "Test 2"),
        ]
        renderer.write_batch(messages)
        output = stream.getvalue()
        assert "TST001" in output
        assert "TST002" in output
        assert renderer.total_count == 2

    def test_auto_detect_color(self) -> None:
        # StringIO doesn't have isatty, so should default to no color
        stream = io.StringIO()
        renderer = Renderer(stream=stream)
        assert renderer.color is False


class TestFormatForFile:
    """Tests for format_for_file function."""

    def test_no_colors(self) -> None:
        messages = [A11yMessage.ok("TST001", "Test")]
        output = format_for_file(messages)
        assert Colors.OK not in output

    def test_blank_lines_between(self) -> None:
        messages = [
            A11yMessage.ok("TST001", "Test 1"),
            A11yMessage.ok("TST002", "Test 2"),
        ]
        output = format_for_file(messages)
        # Should have blank line between messages
        assert "\n\n" in output
