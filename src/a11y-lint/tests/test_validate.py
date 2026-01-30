"""Tests for validate module."""

import json
import pytest
from pathlib import Path
import tempfile

from a11y_lint.validate import (
    validate_dict,
    validate_message,
    is_valid,
    validate_json_file,
    validate_and_convert,
    MessageValidator,
    load_schema,
)
from a11y_lint.errors import A11yMessage, Level


class TestLoadSchema:
    """Tests for schema loading."""

    def test_schema_loads(self) -> None:
        schema = load_schema()
        assert schema["title"] == "CLI Ground Truth Message"
        assert "properties" in schema
        assert "level" in schema["properties"]


class TestValidateDict:
    """Tests for validate_dict function."""

    def test_valid_ok_message(self) -> None:
        data = {
            "level": "OK",
            "code": "TST001",
            "what": "Test passed",
        }
        errors = validate_dict(data)
        assert errors == []

    def test_valid_error_message(self) -> None:
        data = {
            "level": "ERROR",
            "code": "TST001",
            "what": "Test failed",
            "why": "Reason",
            "fix": "Fix it",
        }
        errors = validate_dict(data)
        assert errors == []

    def test_missing_required_field(self) -> None:
        data = {
            "level": "OK",
            "what": "Test",
        }
        errors = validate_dict(data)
        assert len(errors) > 0
        assert any("code" in e for e in errors)

    def test_invalid_level(self) -> None:
        data = {
            "level": "INVALID",
            "code": "TST001",
            "what": "Test",
        }
        errors = validate_dict(data)
        assert len(errors) > 0
        assert any("level" in e.lower() for e in errors)

    def test_invalid_code_pattern(self) -> None:
        data = {
            "level": "OK",
            "code": "invalid",
            "what": "Test",
        }
        errors = validate_dict(data)
        assert len(errors) > 0
        assert any("code" in e for e in errors)

    def test_what_too_long(self) -> None:
        data = {
            "level": "OK",
            "code": "TST001",
            "what": "x" * 300,  # Exceeds maxLength of 200
        }
        errors = validate_dict(data)
        assert len(errors) > 0

    def test_additional_properties_rejected(self) -> None:
        data = {
            "level": "OK",
            "code": "TST001",
            "what": "Test",
            "unknown_field": "value",
        }
        errors = validate_dict(data)
        assert len(errors) > 0


class TestValidateMessage:
    """Tests for validate_message function."""

    def test_valid_message(self) -> None:
        msg = A11yMessage.ok("TST001", "Test passed")
        errors = validate_message(msg)
        assert errors == []

    def test_message_with_all_fields(self) -> None:
        msg = A11yMessage.error(
            "TST001",
            "Test error",
            "Why",
            "Fix",
            rule="test-rule",
            metadata={"key": "value"},
        )
        errors = validate_message(msg)
        assert errors == []


class TestIsValid:
    """Tests for is_valid function."""

    def test_valid_dict(self) -> None:
        data = {"level": "OK", "code": "TST001", "what": "Test"}
        assert is_valid(data) is True

    def test_invalid_dict(self) -> None:
        data = {"level": "INVALID", "code": "TST001", "what": "Test"}
        assert is_valid(data) is False

    def test_valid_message(self) -> None:
        msg = A11yMessage.ok("TST001", "Test")
        assert is_valid(msg) is True


class TestValidateJsonFile:
    """Tests for validate_json_file function."""

    def test_valid_single_message(self) -> None:
        data = {"level": "OK", "code": "TST001", "what": "Test"}
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json.dump(data, f)
            f.flush()
            valid, errors = validate_json_file(f.name)
            assert len(valid) == 1
            assert errors == []
        Path(f.name).unlink()

    def test_valid_array_messages(self) -> None:
        data = [
            {"level": "OK", "code": "TST001", "what": "Test 1"},
            {"level": "WARN", "code": "TST002", "what": "Test 2", "why": "Reason"},
        ]
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json.dump(data, f)
            f.flush()
            valid, errors = validate_json_file(f.name)
            assert len(valid) == 2
            assert errors == []
        Path(f.name).unlink()

    def test_partial_valid_messages(self) -> None:
        data = [
            {"level": "OK", "code": "TST001", "what": "Test 1"},
            {"level": "INVALID", "code": "TST002", "what": "Test 2"},
        ]
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json.dump(data, f)
            f.flush()
            valid, errors = validate_json_file(f.name)
            assert len(valid) == 1
            assert len(errors) > 0
        Path(f.name).unlink()

    def test_invalid_json(self) -> None:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            f.write("not valid json")
            f.flush()
            valid, errors = validate_json_file(f.name)
            assert valid == []
            assert len(errors) == 1
            assert "Invalid JSON" in errors[0]
        Path(f.name).unlink()

    def test_file_not_found(self) -> None:
        valid, errors = validate_json_file("nonexistent.json")
        assert valid == []
        assert len(errors) == 1
        assert "File not found" in errors[0]


class TestValidateAndConvert:
    """Tests for validate_and_convert function."""

    def test_valid_returns_message(self) -> None:
        data = {"level": "OK", "code": "TST001", "what": "Test"}
        result = validate_and_convert(data)
        assert isinstance(result, A11yMessage)
        assert result.level == Level.OK
        assert result.code == "TST001"

    def test_invalid_returns_errors(self) -> None:
        data = {"level": "INVALID", "code": "TST001", "what": "Test"}
        result = validate_and_convert(data)
        assert isinstance(result, list)
        assert len(result) > 0


class TestMessageValidator:
    """Tests for MessageValidator class."""

    def test_validate_batch(self) -> None:
        messages = [
            {"level": "OK", "code": "TST001", "what": "Test 1"},
            {"level": "WARN", "code": "TST002", "what": "Test 2", "why": "Reason"},
            {"level": "INVALID", "code": "TST003", "what": "Test 3"},
        ]
        validator = MessageValidator()
        validator.validate_batch(messages)

        assert validator.valid_count == 2
        assert validator.invalid_count == 1
        assert validator.total_count == 3
        assert not validator.is_all_valid
        assert len(validator.messages) == 2
        assert len(validator.errors) == 1

    def test_summary(self) -> None:
        validator = MessageValidator()
        assert validator.summary() == "No messages validated"

        validator.validate({"level": "OK", "code": "TST001", "what": "Test"})
        assert "All 1 messages valid" in validator.summary()

        validator.validate({"level": "INVALID"}, index=1)
        assert "1 valid" in validator.summary()
        assert "1 invalid" in validator.summary()

    def test_error_report(self) -> None:
        validator = MessageValidator()
        assert validator.error_report() == "No errors"

        validator.validate({"level": "INVALID"}, index=0)
        report = validator.error_report()
        assert "1 invalid" in report
        assert "Message 0" in report
