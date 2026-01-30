"""a11y-lint: Accessibility linter for CLI output.

Validates that CLI error messages follow accessible patterns
with [OK]/[WARN]/[ERROR] + What/Why/Fix structure.
"""

__version__ = "0.1.0"

from .errors import A11yMessage, Level, Location, ErrorCodes
from .render import render, render_plain, render_colored, Renderer, should_use_color
from .scan_cli_text import Scanner, scan, get_rule_names, Rule, RULES, RuleCategory
from .scorecard import Scorecard, RuleScore, ScorecardBuilder, create_scorecard
from .report_md import (
    MarkdownReporter,
    render_report_md,
    render_scorecard_md,
    generate_badge_md,
)
from .validate import (
    validate_dict,
    validate_message,
    is_valid,
    validate_json_file,
    MessageValidator,
)

__all__ = [
    # Version
    "__version__",
    # Errors
    "A11yMessage",
    "Level",
    "Location",
    "ErrorCodes",
    # Rendering
    "render",
    "render_plain",
    "render_colored",
    "Renderer",
    "should_use_color",
    # Scanning
    "Scanner",
    "scan",
    "get_rule_names",
    "Rule",
    "RULES",
    "RuleCategory",
    # Scorecard
    "Scorecard",
    "RuleScore",
    "ScorecardBuilder",
    "create_scorecard",
    # Markdown Reports
    "MarkdownReporter",
    "render_report_md",
    "render_scorecard_md",
    "generate_badge_md",
    # Validation
    "validate_dict",
    "validate_message",
    "is_valid",
    "validate_json_file",
    "MessageValidator",
]
