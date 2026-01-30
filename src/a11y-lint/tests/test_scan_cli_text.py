"""Tests for scan_cli_text module."""

import pytest

from a11y_lint.scan_cli_text import (
    Scanner,
    scan,
    get_rule_names,
    RULES,
    check_line_length,
    check_all_caps,
    check_jargon,
    check_color_only,
    check_emoji_overuse,
    check_missing_punctuation,
    check_error_structure,
    check_ambiguous_pronouns,
    MAX_LINE_LENGTH,
)
from a11y_lint.errors import Level, ErrorCodes


class TestCheckLineLength:
    """Tests for line length check."""

    def test_short_line_ok(self) -> None:
        result = check_line_length("Short line", None, 1)
        assert result is None

    def test_long_line_warns(self) -> None:
        long_line = "x" * (MAX_LINE_LENGTH + 1)
        result = check_line_length(long_line, None, 1)
        assert result is not None
        assert result.level == Level.WARN
        assert result.code == ErrorCodes.LINE_TOO_LONG

    def test_exactly_max_length_ok(self) -> None:
        line = "x" * MAX_LINE_LENGTH
        result = check_line_length(line, None, 1)
        assert result is None


class TestCheckAllCaps:
    """Tests for all caps check."""

    def test_normal_text_ok(self) -> None:
        result = check_all_caps("This is normal text", None, 1)
        assert result is None

    def test_all_caps_warns(self) -> None:
        result = check_all_caps("THIS IS SHOUTING TEXT", None, 1)
        assert result is not None
        assert result.level == Level.WARN
        assert result.code == ErrorCodes.ALL_CAPS_MESSAGE

    def test_allowed_acronyms_ok(self) -> None:
        result = check_all_caps("ERROR: Something went wrong", None, 1)
        assert result is None

    def test_short_caps_ok(self) -> None:
        # Words with 4 or fewer caps are allowed
        result = check_all_caps("The HTML page", None, 1)
        assert result is None


class TestCheckJargon:
    """Tests for jargon check."""

    def test_plain_text_ok(self) -> None:
        result = check_jargon("File not found", None, 1)
        assert result is None

    def test_jargon_warns(self) -> None:
        result = check_jargon("Received EOF unexpectedly", None, 1)
        assert result is not None
        assert result.level == Level.WARN
        assert result.code == ErrorCodes.JARGON_DETECTED

    def test_stdin_jargon(self) -> None:
        result = check_jargon("Reading from STDIN", None, 1)
        assert result is not None
        assert "STDIN" in result.what

    def test_pid_jargon(self) -> None:
        result = check_jargon("Process PID: 12345", None, 1)
        assert result is not None
        assert "PID" in result.what


class TestCheckColorOnly:
    """Tests for color-only information check."""

    def test_normal_text_ok(self) -> None:
        result = check_color_only("Error: File not found", None, 1)
        assert result is None

    def test_color_only_errors(self) -> None:
        result = check_color_only("Errors are shown in red", None, 1)
        assert result is not None
        assert result.level == Level.ERROR
        assert result.code == ErrorCodes.COLOR_ONLY_INFO

    def test_color_indicates_errors(self) -> None:
        result = check_color_only("Green indicates success", None, 1)
        assert result is not None
        assert result.level == Level.ERROR

    def test_highlighted_in_color(self) -> None:
        result = check_color_only("Errors are highlighted in yellow", None, 1)
        assert result is not None


class TestCheckEmojiOveruse:
    """Tests for emoji overuse check."""

    def test_no_emoji_ok(self) -> None:
        result = check_emoji_overuse("Normal text", None, 1)
        assert result is None

    def test_few_emoji_ok(self) -> None:
        result = check_emoji_overuse("Hello \U0001F600\U0001F600\U0001F600", None, 1)
        assert result is None  # 3 or fewer is OK

    def test_many_emoji_warns(self) -> None:
        result = check_emoji_overuse(
            "Hello \U0001F600\U0001F600\U0001F600\U0001F600\U0001F600", None, 1
        )
        assert result is not None
        assert result.level == Level.WARN
        assert result.code == ErrorCodes.EMOJI_OVERUSE


class TestCheckMissingPunctuation:
    """Tests for missing punctuation check."""

    def test_normal_text_not_checked(self) -> None:
        # Only error-like messages are checked
        result = check_missing_punctuation("Normal text without punctuation", None, 1)
        assert result is None

    def test_error_with_punctuation_ok(self) -> None:
        result = check_missing_punctuation("ERROR: File not found.", None, 1)
        assert result is None

    def test_error_without_punctuation_warns(self) -> None:
        result = check_missing_punctuation("ERROR: File not found", None, 1)
        assert result is not None
        assert result.level == Level.WARN
        assert result.code == ErrorCodes.NO_PUNCTUATION

    def test_colon_counts_as_punctuation(self) -> None:
        result = check_missing_punctuation("ERROR:", None, 1)
        assert result is None


class TestCheckErrorStructure:
    """Tests for error structure check."""

    def test_normal_text_not_checked(self) -> None:
        result = check_error_structure("Normal text", None, 1)
        assert result is None

    def test_error_with_explanation_ok(self) -> None:
        result = check_error_structure(
            "ERROR: Failed because the file was not found", None, 1
        )
        assert result is None

    def test_error_with_fix_ok(self) -> None:
        result = check_error_structure(
            "ERROR: Failed. Try running as administrator.", None, 1
        )
        assert result is None

    def test_error_without_context_warns(self) -> None:
        result = check_error_structure("ERROR: Operation failed", None, 1)
        assert result is not None
        assert result.level == Level.WARN
        assert result.code == ErrorCodes.MISSING_WHY


class TestCheckAmbiguousPronouns:
    """Tests for ambiguous pronoun check."""

    def test_clear_text_ok(self) -> None:
        result = check_ambiguous_pronouns("The file was not found", None, 1)
        assert result is None

    def test_it_failed_warns(self) -> None:
        result = check_ambiguous_pronouns("It failed", None, 1)
        assert result is not None
        assert result.level == Level.WARN
        assert result.code == ErrorCodes.AMBIGUOUS_PRONOUN

    def test_this_is_invalid_warns(self) -> None:
        result = check_ambiguous_pronouns("This is invalid", None, 1)
        assert result is not None

    def test_pronoun_mid_sentence_ok(self) -> None:
        # Only check at start of line
        result = check_ambiguous_pronouns("The process failed because it ran out of memory", None, 1)
        assert result is None


class TestScanner:
    """Tests for Scanner class."""

    def test_scan_empty_text(self) -> None:
        scanner = Scanner()
        messages = scanner.scan_text("")
        assert messages == []

    def test_scan_clean_text(self) -> None:
        scanner = Scanner()
        # Use text that doesn't start with pronouns and has proper structure
        messages = scanner.scan_text("File processed successfully.\nAll checks passed.")
        assert len(messages) == 0

    def test_scan_problematic_text(self) -> None:
        scanner = Scanner()
        messages = scanner.scan_text("ERROR: It failed")
        # Should find: ambiguous pronoun, no punctuation, no explanation
        assert len(messages) >= 2

    def test_scan_with_source_file(self) -> None:
        scanner = Scanner()
        messages = scanner.scan_text("ERROR: It failed", file="test.txt")
        for msg in messages:
            if msg.location:
                assert msg.location.file == "test.txt"

    def test_disable_rule(self) -> None:
        scanner = Scanner()
        scanner.disable_rule("no-ambiguous-pronouns")
        messages = scanner.scan_text("It failed")
        # Should not find ambiguous pronoun warning
        assert not any(m.code == ErrorCodes.AMBIGUOUS_PRONOUN for m in messages)

    def test_enable_only_rule(self) -> None:
        scanner = Scanner()
        scanner.rules = []
        scanner.enable_rule("no-all-caps")
        messages = scanner.scan_text("THIS IS SHOUTING")
        assert len(messages) == 1
        assert messages[0].code == ErrorCodes.ALL_CAPS_MESSAGE

    def test_error_and_warn_counts(self) -> None:
        scanner = Scanner()
        # Color-only is an error, others are warnings
        scanner.scan_text("Errors are shown in red. THIS IS SHOUTING.")
        assert scanner.error_count >= 1
        assert scanner.warn_count >= 1

    def test_has_errors(self) -> None:
        scanner = Scanner()
        scanner.scan_text("Errors are shown in red")
        assert scanner.has_errors is True

        scanner2 = Scanner()
        scanner2.scan_text("Normal text.")
        assert scanner2.has_errors is False


class TestScanFunction:
    """Tests for scan convenience function."""

    def test_scan_returns_messages(self) -> None:
        messages = scan("ERROR: It failed")
        assert len(messages) >= 1

    def test_scan_with_file(self) -> None:
        messages = scan("ERROR: It failed", file="test.py")
        for msg in messages:
            if msg.location and msg.location.file:
                assert msg.location.file == "test.py"


class TestGetRuleNames:
    """Tests for get_rule_names function."""

    def test_returns_all_rules(self) -> None:
        names = get_rule_names()
        assert len(names) == len(RULES)

    def test_known_rules_present(self) -> None:
        names = get_rule_names()
        assert "line-length" in names
        assert "no-all-caps" in names
        assert "plain-language" in names
        assert "no-color-only" in names
