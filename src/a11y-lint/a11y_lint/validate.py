"""Schema validation for CLI accessibility messages.

Validates that messages conform to the ground truth schema.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import jsonschema
from jsonschema import Draft202012Validator, ValidationError

from .errors import A11yMessage, Level

# Path to the schema file
SCHEMA_PATH = Path(__file__).parent / "schemas" / "cli.error.schema.v0.1.json"


def load_schema() -> dict[str, Any]:
    """Load the CLI error schema from disk."""
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


# Cache the schema and validator
_schema: dict[str, Any] | None = None
_validator: Draft202012Validator | None = None


def get_validator() -> Draft202012Validator:
    """Get or create the cached schema validator."""
    global _schema, _validator
    if _validator is None:
        _schema = load_schema()
        _validator = Draft202012Validator(_schema)
    return _validator


def validate_dict(data: dict[str, Any]) -> list[str]:
    """Validate a dictionary against the CLI error schema.

    Args:
        data: Dictionary to validate

    Returns:
        List of validation error messages (empty if valid)
    """
    validator = get_validator()
    errors = []

    for error in validator.iter_errors(data):
        # Build a human-readable path to the error
        path = ".".join(str(p) for p in error.path) if error.path else "root"
        errors.append(f"{path}: {error.message}")

    return errors


def validate_message(message: A11yMessage) -> list[str]:
    """Validate an A11yMessage against the schema.

    Args:
        message: Message to validate

    Returns:
        List of validation error messages (empty if valid)
    """
    return validate_dict(message.to_dict())


def is_valid(data: dict[str, Any] | A11yMessage) -> bool:
    """Check if data is valid against the schema.

    Args:
        data: Dictionary or A11yMessage to validate

    Returns:
        True if valid, False otherwise
    """
    if isinstance(data, A11yMessage):
        data = data.to_dict()
    return len(validate_dict(data)) == 0


def validate_json_file(path: Path | str) -> tuple[list[dict[str, Any]], list[str]]:
    """Validate a JSON file containing messages.

    The file can contain either a single message object or an array of messages.

    Args:
        path: Path to the JSON file

    Returns:
        Tuple of (valid messages, validation errors)
    """
    path = Path(path)
    errors: list[str] = []

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return [], [f"Invalid JSON: {e}"]
    except FileNotFoundError:
        return [], [f"File not found: {path}"]

    # Handle both single object and array
    if isinstance(data, dict):
        messages = [data]
    elif isinstance(data, list):
        messages = data
    else:
        return [], ["JSON must be an object or array of objects"]

    valid_messages = []
    for i, msg in enumerate(messages):
        if not isinstance(msg, dict):
            errors.append(f"Message {i}: expected object, got {type(msg).__name__}")
            continue

        msg_errors = validate_dict(msg)
        if msg_errors:
            for err in msg_errors:
                errors.append(f"Message {i}: {err}")
        else:
            valid_messages.append(msg)

    return valid_messages, errors


def validate_and_convert(data: dict[str, Any]) -> A11yMessage | list[str]:
    """Validate and convert a dictionary to an A11yMessage.

    Args:
        data: Dictionary to validate and convert

    Returns:
        A11yMessage if valid, list of errors otherwise
    """
    errors = validate_dict(data)
    if errors:
        return errors

    try:
        return A11yMessage.from_dict(data)
    except (ValueError, KeyError) as e:
        return [str(e)]


class MessageValidator:
    """Validator for batches of messages with summary statistics."""

    def __init__(self) -> None:
        self.valid_count = 0
        self.invalid_count = 0
        self.errors: list[tuple[int, list[str]]] = []
        self.messages: list[A11yMessage] = []

    def validate(self, data: dict[str, Any], index: int = 0) -> bool:
        """Validate a single message.

        Args:
            data: Message dictionary to validate
            index: Index for error reporting

        Returns:
            True if valid, False otherwise
        """
        result = validate_and_convert(data)
        if isinstance(result, list):
            self.invalid_count += 1
            self.errors.append((index, result))
            return False
        else:
            self.valid_count += 1
            self.messages.append(result)
            return True

    def validate_batch(self, messages: list[dict[str, Any]]) -> None:
        """Validate a batch of messages.

        Args:
            messages: List of message dictionaries to validate
        """
        for i, msg in enumerate(messages):
            self.validate(msg, i)

    @property
    def is_all_valid(self) -> bool:
        """Check if all validated messages were valid."""
        return self.invalid_count == 0

    @property
    def total_count(self) -> int:
        """Get total number of validated messages."""
        return self.valid_count + self.invalid_count

    def summary(self) -> str:
        """Get a summary of validation results."""
        total = self.total_count
        if total == 0:
            return "No messages validated"

        if self.is_all_valid:
            return f"All {total} messages valid"

        return (
            f"Validated {total} messages: "
            f"{self.valid_count} valid, {self.invalid_count} invalid"
        )

    def error_report(self) -> str:
        """Get detailed error report."""
        if not self.errors:
            return "No errors"

        lines = [f"Found {len(self.errors)} invalid messages:"]
        for index, errs in self.errors:
            lines.append(f"\n  Message {index}:")
            for err in errs:
                lines.append(f"    - {err}")

        return "\n".join(lines)
