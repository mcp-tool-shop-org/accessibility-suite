
import json
import pytest
from click.testing import CliRunner
from a11y_ci.cli import main
from a11y_ci.pr_comment import render_pr_comment

FIXTURES = "tests/fixtures"

def test_gate_top_flag():
    """Test --top limits the output lines."""
    runner = CliRunner()
    result = runner.invoke(main, [
        "gate",
        "--current", f"{FIXTURES}/current_failures_many.json",
        "--fail-on", "minor", # Ensure we have failures
        "--top", "1"
    ])
    assert result.exit_code == 3
    # Should see the first blocking ID
    assert "Blocking IDs (Top 1):" in result.output
    # Should see "and X more"
    assert "... and 2 more" in result.output

def test_comment_top_flag():
    """Test --top limits PR comment output."""
    payload = {
        "gate": {"decision": "fail"},
        "blocking": [{"id": f"ID.{i}", "severity": "serious"} for i in range(20)]
    }
    
    # IDs will sort string-wise: ID.0, ID.1, ID.10, ID.11, ID.12 ...
    # So top 5 are: ID.0, ID.1, ID.10, ID.11, ID.12
    
    # Render with top=5
    md = render_pr_comment(payload, top=5)
    assert "_Showing first 5 of 20 violations_" in md
    
    assert "ID.0" in md
    assert "ID.12" in md
    assert "ID.2" not in md # Comes later lexicographically


def test_graceful_missing_fields():
    """Render PR comment with minimal payload should not crash."""
    minimal = {
        "gate": {}
        # Missing blocking, artifacts, counts, etc.
    }
    md = render_pr_comment(minimal)
    assert "# ❌ Accessibility Gate: FAIL" in md # default decision unknown -> fail
    assert "| Findings | 0 | - |" in md

    # Finding without optional fields
    payload_partial = {
        "gate": {"decision": "fail"},
        "blocking": [{"id": "A"}] # Missing severity, message, location
    }
    md = render_pr_comment(payload_partial)
    assert "### [INFO] A" in md # default severity info
    assert "No message provided" in md
    assert "Unknown location" in md

def test_determinism(tmp_path):
    """Running gate twice on same input should produce identical output."""
    runner = CliRunner()
    
    # Run 1
    res1 = runner.invoke(main, [
        "gate",
        "--current", f"{FIXTURES}/current_fail.json",
        "--format", "json"
    ])
    
    # Run 2
    res2 = runner.invoke(main, [
        "gate",
        "--current", f"{FIXTURES}/current_fail.json",
        "--format", "json"
    ])
    
    assert res1.exit_code == res2.exit_code
    assert res1.output == res2.output
