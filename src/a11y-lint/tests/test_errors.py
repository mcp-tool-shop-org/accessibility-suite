"""Tests for errors module."""

import pytest

from a11y_lint.errors import A11yMessage, Level, Location, ErrorCodes, CODE_PATTERN


class TestLevel:
    """Tests for Level enum."""

    def test_level_values(self) -> None:
        assert Level.OK.value == "OK"
        assert Level.WARN.value == "WARN"
        assert Level.ERROR.value == "ERROR"

    def test_level_str(self) -> None:
        assert str(Level.OK) == "OK"
        assert str(Level.WARN) == "WARN"
        assert str(Level.ERROR) == "ERROR"


class TestLocation:
    """Tests for Location dataclass."""

    def test_empty_location(self) -> None:
        loc = Location()
        assert str(loc) == "<unknown>"
        assert loc.to_dict() == {}

    def test_full_location(self) -> None:
        loc = Location(file="test.py", line=10, column=5, context="some text")
        assert "test.py" in str(loc)
        assert "line 10" in str(loc)
        assert "col 5" in str(loc)

        d = loc.to_dict()
        assert d["file"] == "test.py"
        assert d["line"] == 10
        assert d["column"] == 5
        assert d["context"] == "some text"

    def test_location_truncates_context(self) -> None:
        long_context = "x" * 300
        loc = Location(context=long_context)
        d = loc.to_dict()
        assert len(d["context"]) == 200


class TestCodePattern:
    """Tests for error code pattern validation."""

    def test_valid_codes(self) -> None:
        assert CODE_PATTERN.match("A11Y001")
        assert CODE_PATTERN.match("FMT123")
        assert CODE_PATTERN.match("CLR999")
        assert CODE_PATTERN.match("ABCD000")

    def test_invalid_codes(self) -> None:
        assert not CODE_PATTERN.match("A1")  # Too short
        assert not CODE_PATTERN.match("a11y001")  # Lowercase
        assert not CODE_PATTERN.match("A11Y01")  # Only 2 digits
        assert not CODE_PATTERN.match("A11Y0001")  # 4 digits
        assert not CODE_PATTERN.match("ABCDE001")  # 5 letters


class TestA11yMessage:
    """Tests for A11yMessage dataclass."""

    def test_ok_message(self) -> None:
        msg = A11yMessage.ok("TST001", "Test passed")
        assert msg.level == Level.OK
        assert msg.code == "TST001"
        assert msg.what == "Test passed"
        assert msg.why is None
        assert msg.fix is None

    def test_warn_message(self) -> None:
        msg = A11yMessage.warn(
            "TST002",
            "Test warning",
            "This is a warning reason",
            fix="Consider fixing this",
        )
        assert msg.level == Level.WARN
        assert msg.code == "TST002"
        assert msg.what == "Test warning"
        assert msg.why == "This is a warning reason"
        assert msg.fix == "Consider fixing this"

    def test_error_message(self) -> None:
        msg = A11yMessage.error(
            "TST003",
            "Test error",
            "This is an error reason",
            "Fix it like this",
        )
        assert msg.level == Level.ERROR
        assert msg.code == "TST003"
        assert msg.what == "Test error"
        assert msg.why == "This is an error reason"
        assert msg.fix == "Fix it like this"

    def test_error_requires_why(self) -> None:
        with pytest.raises(ValueError, match="must include 'why'"):
            A11yMessage(
                level=Level.ERROR,
                code="TST001",
                what="Test",
                fix="Some fix",
            )

    def test_error_requires_fix(self) -> None:
        with pytest.raises(ValueError, match="must include 'fix'"):
            A11yMessage(
                level=Level.ERROR,
                code="TST001",
                what="Test",
                why="Some reason",
            )

    def test_invalid_code_raises(self) -> None:
        with pytest.raises(ValueError, match="Invalid error code"):
            A11yMessage.ok("invalid", "Test")

    def test_empty_what_raises(self) -> None:
        with pytest.raises(ValueError, match="cannot be empty"):
            A11yMessage.ok("TST001", "")

    def test_whitespace_what_raises(self) -> None:
        with pytest.raises(ValueError, match="cannot be empty"):
            A11yMessage.ok("TST001", "   ")

    def test_to_dict(self) -> None:
        msg = A11yMessage.error(
            "TST001",
            "Test error",
            "Why",
            "Fix",
            rule="test-rule",
            location=Location(file="test.py", line=1),
            metadata={"key": "value"},
        )
        d = msg.to_dict()
        assert d["level"] == "ERROR"
        assert d["code"] == "TST001"
        assert d["what"] == "Test error"
        assert d["why"] == "Why"
        assert d["fix"] == "Fix"
        assert d["rule"] == "test-rule"
        assert d["location"]["file"] == "test.py"
        assert d["metadata"]["key"] == "value"

    def test_from_dict(self) -> None:
        data = {
            "level": "WARN",
            "code": "TST002",
            "what": "Test warning",
            "why": "Reason",
            "location": {"file": "test.py", "line": 5},
        }
        msg = A11yMessage.from_dict(data)
        assert msg.level == Level.WARN
        assert msg.code == "TST002"
        assert msg.what == "Test warning"
        assert msg.why == "Reason"
        assert msg.location is not None
        assert msg.location.file == "test.py"
        assert msg.location.line == 5

    def test_truncates_long_what(self) -> None:
        long_what = "x" * 300
        msg = A11yMessage.ok("TST001", long_what)
        assert len(msg.what) == 200

    def test_truncates_long_why(self) -> None:
        long_why = "y" * 600
        msg = A11yMessage.warn("TST001", "Test", long_why)
        assert len(msg.why) == 500


class TestErrorCodes:
    """Tests for ErrorCodes constants."""

    def test_all_codes_valid(self) -> None:
        for attr in dir(ErrorCodes):
            if not attr.startswith("_"):
                code = getattr(ErrorCodes, attr)
                assert CODE_PATTERN.match(code), f"{attr} = {code} is invalid"
