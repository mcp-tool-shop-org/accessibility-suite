"""Tests for CLI module."""

import json
import pytest
import tempfile
from pathlib import Path
from click.testing import CliRunner

from a11y_lint.cli import main


@pytest.fixture
def runner() -> CliRunner:
    """Create a CLI test runner."""
    return CliRunner()


@pytest.fixture
def sample_file(tmp_path: Path) -> Path:
    """Create a sample file with some text."""
    file = tmp_path / "sample.txt"
    file.write_text("This is a test file.\nERROR: Something went wrong.\n")
    return file


@pytest.fixture
def clean_file(tmp_path: Path) -> Path:
    """Create a clean file with no issues."""
    file = tmp_path / "clean.txt"
    file.write_text("This is a clean file with no accessibility issues.\n")
    return file


@pytest.fixture
def json_file(tmp_path: Path) -> Path:
    """Create a valid JSON messages file."""
    file = tmp_path / "messages.json"
    data = [
        {"level": "OK", "code": "TST001", "what": "Test passed"},
        {"level": "WARN", "code": "TST002", "what": "Test warning", "why": "Reason"},
    ]
    file.write_text(json.dumps(data))
    return file


class TestMainCommand:
    """Tests for main CLI group."""

    def test_help(self, runner: CliRunner) -> None:
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "Accessibility linter" in result.output

    def test_version(self, runner: CliRunner) -> None:
        result = runner.invoke(main, ["--version"])
        assert result.exit_code == 0
        assert "0.1.0" in result.output


class TestScanCommand:
    """Tests for scan command."""

    def test_scan_file(self, runner: CliRunner, sample_file: Path) -> None:
        result = runner.invoke(main, ["scan", str(sample_file)])
        # Should find issues with "ERROR: Something went wrong"
        assert "WARN" in result.output or "ERROR" in result.output

    def test_scan_clean_file(self, runner: CliRunner, clean_file: Path) -> None:
        result = runner.invoke(main, ["scan", str(clean_file)])
        assert result.exit_code == 0

    def test_scan_stdin(self, runner: CliRunner) -> None:
        result = runner.invoke(main, ["scan", "--stdin"], input="Clean text.\n")
        assert result.exit_code == 0

    def test_scan_json_output(self, runner: CliRunner, sample_file: Path) -> None:
        result = runner.invoke(main, ["scan", "--json", str(sample_file)])
        data = json.loads(result.output)
        assert "messages" in data
        assert "summary" in data

    def test_scan_markdown_output(self, runner: CliRunner, sample_file: Path) -> None:
        result = runner.invoke(main, ["scan", "--format=markdown", str(sample_file)])
        assert "# Accessibility Report" in result.output

    def test_scan_no_input(self, runner: CliRunner) -> None:
        result = runner.invoke(main, ["scan"])
        assert result.exit_code == 1
        assert "Must specify" in result.output

    def test_scan_disable_rule(self, runner: CliRunner, tmp_path: Path) -> None:
        file = tmp_path / "test.txt"
        file.write_text("ERROR: It failed")
        result = runner.invoke(
            main,
            ["scan", "--disable=no-ambiguous-pronouns", str(file)],
        )
        # Should not find ambiguous pronoun warning
        assert "LNG004" not in result.output

    def test_scan_strict_mode(self, runner: CliRunner, sample_file: Path) -> None:
        # Strict mode treats warnings as errors
        result = runner.invoke(main, ["scan", "--strict", str(sample_file)])
        # If there are warnings, exit code should be 1
        if "WARN" in result.output:
            assert result.exit_code == 1


class TestValidateCommand:
    """Tests for validate command."""

    def test_validate_valid_file(self, runner: CliRunner, json_file: Path) -> None:
        result = runner.invoke(main, ["validate", str(json_file)])
        assert result.exit_code == 0
        assert "[OK]" in result.output

    def test_validate_invalid_file(self, runner: CliRunner, tmp_path: Path) -> None:
        file = tmp_path / "invalid.json"
        file.write_text(json.dumps({"level": "INVALID", "code": "bad", "what": "x"}))
        result = runner.invoke(main, ["validate", str(file)])
        assert result.exit_code == 1
        assert "[ERROR]" in result.output

    def test_validate_verbose(self, runner: CliRunner, tmp_path: Path) -> None:
        file = tmp_path / "invalid.json"
        file.write_text(json.dumps({"level": "INVALID", "code": "bad", "what": "x"}))
        result = runner.invoke(main, ["validate", "-v", str(file)])
        assert result.exit_code == 1
        # Verbose should show detailed errors
        assert "level" in result.output.lower() or "code" in result.output.lower()


class TestScorecardCommand:
    """Tests for scorecard command."""

    def test_scorecard_file(self, runner: CliRunner, sample_file: Path) -> None:
        result = runner.invoke(main, ["scorecard", str(sample_file)])
        assert "Scorecard" in result.output
        assert "Score:" in result.output

    def test_scorecard_json(self, runner: CliRunner, sample_file: Path) -> None:
        result = runner.invoke(main, ["scorecard", "--json", str(sample_file)])
        data = json.loads(result.output)
        assert "overall_score" in data
        assert "rules" in data

    def test_scorecard_badge(self, runner: CliRunner, clean_file: Path) -> None:
        result = runner.invoke(main, ["scorecard", "--badge", str(clean_file)])
        assert "shields.io" in result.output

    def test_scorecard_custom_name(self, runner: CliRunner, clean_file: Path) -> None:
        result = runner.invoke(
            main, ["scorecard", "--name=Custom Name", str(clean_file)]
        )
        assert "Custom Name" in result.output


class TestReportCommand:
    """Tests for report command."""

    def test_report_stdout(self, runner: CliRunner, sample_file: Path) -> None:
        result = runner.invoke(main, ["report", str(sample_file)])
        assert "# Accessibility Report" in result.output

    def test_report_to_file(
        self, runner: CliRunner, sample_file: Path, tmp_path: Path
    ) -> None:
        output = tmp_path / "report.md"
        result = runner.invoke(main, ["report", str(sample_file), "-o", str(output)])
        assert result.exit_code == 0 or result.exit_code == 1  # Depends on errors
        assert output.exists()
        assert "# Accessibility Report" in output.read_text(encoding="utf-8")

    def test_report_custom_title(self, runner: CliRunner, clean_file: Path) -> None:
        result = runner.invoke(
            main, ["report", "--title=Custom Title", str(clean_file)]
        )
        assert "# Custom Title" in result.output


class TestListRulesCommand:
    """Tests for list-rules command."""

    def test_list_rules(self, runner: CliRunner) -> None:
        result = runner.invoke(main, ["list-rules"])
        assert result.exit_code == 0
        assert "line-length" in result.output
        assert "no-all-caps" in result.output
        assert "plain-language" in result.output


class TestSchemaCommand:
    """Tests for schema command."""

    def test_schema(self, runner: CliRunner) -> None:
        result = runner.invoke(main, ["schema"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["title"] == "CLI Ground Truth Message"
        assert "properties" in data
