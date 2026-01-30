"""CLI entry point for a11y-lint.

Provides command-line interface for accessibility linting of CLI output.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import click

from . import __version__
from .errors import A11yMessage
from .render import Renderer, format_for_file
from .scan_cli_text import Scanner, get_rule_names
from .scorecard import create_scorecard
from .report_md import MarkdownReporter, generate_badge_md
from .validate import validate_json_file, MessageValidator


@click.group()
@click.version_option(version=__version__, prog_name="a11y-lint")
def main() -> None:
    """Accessibility linter for CLI output.

    Validates that CLI error messages follow accessible patterns
    with [OK]/[WARN]/[ERROR] + What/Why/Fix structure.
    """
    pass


@main.command()
@click.argument("input", type=click.Path(exists=True), required=False)
@click.option("--stdin", is_flag=True, help="Read from stdin instead of file.")
@click.option(
    "--color",
    type=click.Choice(["auto", "always", "never"]),
    default="auto",
    help="Color output mode: auto (respects NO_COLOR), always, or never.",
)
@click.option("--json", "json_output", is_flag=True, help="Output results as JSON.")
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["plain", "json", "markdown"]),
    default="plain",
    help="Output format.",
)
@click.option(
    "--disable",
    multiple=True,
    help="Disable specific rules (can be used multiple times).",
)
@click.option(
    "--enable",
    multiple=True,
    help="Enable only specific rules (can be used multiple times).",
)
@click.option("--strict", is_flag=True, help="Treat warnings as errors.")
def scan(
    input: str | None,
    stdin: bool,
    color: str,
    json_output: bool,
    output_format: str,
    disable: tuple[str, ...],
    enable: tuple[str, ...],
    strict: bool,
) -> None:
    """Scan CLI text for accessibility issues.

    Reads from a file or stdin and checks for common accessibility problems.

    Examples:

        a11y-lint scan output.txt

        echo "ERROR: It failed" | a11y-lint scan --stdin

        a11y-lint scan --format=json output.txt
    """
    # Get input text
    if stdin:
        text = sys.stdin.read()
        source = "<stdin>"
    elif input:
        path = Path(input)
        text = path.read_text(encoding="utf-8")
        source = str(path)
    else:
        click.echo("Error: Must specify INPUT file or --stdin.", err=True)
        sys.exit(1)

    # Configure scanner
    scanner = Scanner()

    # Handle rule filtering
    if enable:
        # Enable only specified rules
        scanner.rules = []
        for rule_name in enable:
            scanner.enable_rule(rule_name)
    for rule_name in disable:
        scanner.disable_rule(rule_name)

    # Run scan
    messages = scanner.scan_text(text, file=source)

    # Handle output format
    if json_output or output_format == "json":
        result = {
            "source": source,
            "messages": [msg.to_dict() for msg in messages],
            "summary": {
                "total": len(messages),
                "errors": scanner.error_count,
                "warnings": scanner.warn_count,
            },
        }
        click.echo(json.dumps(result, indent=2))
    elif output_format == "markdown":
        reporter = MarkdownReporter(title=f"Accessibility Report: {source}")
        click.echo(reporter.render(messages))
    else:
        # Plain text output
        # Resolve color mode: auto uses environment detection, always/never are explicit
        color_enabled: bool | None = None  # None = auto
        if color == "always":
            color_enabled = True
        elif color == "never":
            color_enabled = False
        # "auto" leaves it as None, which triggers should_use_color()

        renderer = Renderer(color=color_enabled)
        renderer.write_batch(messages)
        renderer.write_summary()

    # Exit with error if issues found
    exit_code = 0
    if scanner.error_count > 0:
        exit_code = 1
    elif strict and scanner.warn_count > 0:
        exit_code = 1

    sys.exit(exit_code)


@main.command()
@click.argument("input", type=click.Path(exists=True))
@click.option("--verbose", "-v", is_flag=True, help="Show detailed validation errors.")
def validate(input: str, verbose: bool) -> None:
    """Validate a JSON file against the CLI error schema.

    Checks that JSON messages conform to the ground truth schema.

    Examples:

        a11y-lint validate messages.json
    """
    path = Path(input)
    valid_messages, errors = validate_json_file(path)

    if errors:
        click.echo(f"[ERROR] {len(errors)} validation error(s) found:", err=True)
        if verbose:
            for err in errors:
                click.echo(f"  - {err}", err=True)
        sys.exit(1)
    else:
        click.echo(f"[OK] {len(valid_messages)} message(s) validated successfully.")
        sys.exit(0)


@main.command()
@click.argument("input", type=click.Path(exists=True), required=False)
@click.option("--stdin", is_flag=True, help="Read from stdin instead of file.")
@click.option("--name", default="CLI Assessment", help="Name for the scorecard.")
@click.option("--json", "json_output", is_flag=True, help="Output as JSON.")
@click.option("--badge", is_flag=True, help="Generate a shields.io badge markdown.")
def scorecard(
    input: str | None,
    stdin: bool,
    name: str,
    json_output: bool,
    badge: bool,
) -> None:
    """Generate an accessibility scorecard.

    Creates a summary scorecard from scan results.

    Examples:

        a11y-lint scorecard output.txt

        a11y-lint scorecard --badge output.txt
    """
    # Get input text
    if stdin:
        text = sys.stdin.read()
        source = "<stdin>"
    elif input:
        path = Path(input)
        text = path.read_text(encoding="utf-8")
        source = str(path)
    else:
        click.echo("Error: Must specify INPUT file or --stdin.", err=True)
        sys.exit(1)

    # Scan and create scorecard
    scanner = Scanner()
    messages = scanner.scan_text(text, file=source)
    card = create_scorecard(messages, name=name)

    if json_output:
        click.echo(json.dumps(card.to_dict(), indent=2))
    elif badge:
        click.echo(generate_badge_md(card.overall_score))
    else:
        click.echo(card.summary())

    # Exit with error if not passing
    sys.exit(0 if card.is_passing else 1)


@main.command()
@click.argument("input", type=click.Path(exists=True), required=False)
@click.option("--stdin", is_flag=True, help="Read from stdin instead of file.")
@click.option("--output", "-o", type=click.Path(), help="Output file path.")
@click.option("--title", default="Accessibility Report", help="Report title.")
def report(
    input: str | None,
    stdin: bool,
    output: str | None,
    title: str,
) -> None:
    """Generate a markdown accessibility report.

    Creates a detailed markdown report from scan results.

    Examples:

        a11y-lint report output.txt -o report.md

        a11y-lint report --stdin < cli_output.txt
    """
    # Get input text
    if stdin:
        text = sys.stdin.read()
        source = "<stdin>"
    elif input:
        path = Path(input)
        text = path.read_text(encoding="utf-8")
        source = str(path)
    else:
        click.echo("Error: Must specify INPUT file or --stdin.", err=True)
        sys.exit(1)

    # Scan and generate report
    scanner = Scanner()
    messages = scanner.scan_text(text, file=source)
    reporter = MarkdownReporter(title=title)
    markdown = reporter.render(messages)

    if output:
        Path(output).write_text(markdown, encoding="utf-8")
        click.echo(f"Report written to {output}")
    else:
        click.echo(markdown)

    sys.exit(0 if not scanner.has_errors else 1)


@main.command("list-rules")
@click.option("--verbose", "-v", is_flag=True, help="Show rule categories and WCAG refs.")
def list_rules(verbose: bool) -> None:
    """List all available accessibility rules.

    Shows the names of all rules that can be enabled/disabled.
    Rules are categorized as:
    - WCAG: Mapped to WCAG success criteria (accessibility violations)
    - Policy: Best practices for cognitive accessibility
    """
    from .scan_cli_text import RULES, RuleCategory

    if verbose:
        click.echo("Available rules:\n")
        click.echo("WCAG Rules (mapped to WCAG success criteria):")
        for rule in RULES:
            if rule.category == RuleCategory.WCAG:
                wcag = f" [WCAG {rule.wcag_ref}]" if rule.wcag_ref else ""
                click.echo(f"  - {rule.name}{wcag}: {rule.description}")

        click.echo("\nPolicy Rules (cognitive accessibility best practices):")
        for rule in RULES:
            if rule.category == RuleCategory.POLICY:
                click.echo(f"  - {rule.name}: {rule.description}")

        click.echo("\nNote: Policy rules are not WCAG requirements but improve")
        click.echo("accessibility for users with cognitive disabilities.")
    else:
        click.echo("Available rules:")
        for rule in RULES:
            click.echo(f"  - {rule.name}")


@main.command()
def schema() -> None:
    """Print the CLI error JSON schema.

    Outputs the ground truth schema for CLI error messages.
    """
    schema_path = Path(__file__).parent / "schemas" / "cli.error.schema.v0.1.json"
    click.echo(schema_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
