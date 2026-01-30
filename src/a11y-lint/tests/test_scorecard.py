"""Tests for scorecard module."""

import pytest

from a11y_lint.scorecard import (
    RuleScore,
    Scorecard,
    ScorecardBuilder,
    create_scorecard,
)
from a11y_lint.errors import A11yMessage, Level


class TestRuleScore:
    """Tests for RuleScore dataclass."""

    def test_empty_score(self) -> None:
        score = RuleScore(rule="test")
        assert score.total == 0
        assert score.score == 100.0  # No failures = perfect
        assert score.grade == "A"

    def test_all_passed(self) -> None:
        score = RuleScore(rule="test", passed=10)
        assert score.total == 10
        assert score.score == 100.0
        assert score.grade == "A"

    def test_all_errors(self) -> None:
        score = RuleScore(rule="test", errors=10)
        assert score.total == 10
        assert score.score == 0.0
        assert score.grade == "F"

    def test_all_warnings(self) -> None:
        score = RuleScore(rule="test", warnings=10)
        assert score.total == 10
        assert score.score == 50.0  # Warnings = half points
        assert score.grade == "F"

    def test_mixed_results(self) -> None:
        score = RuleScore(rule="test", passed=7, warnings=2, errors=1)
        assert score.total == 10
        # 7 + (2 * 0.5) + 0 = 8 / 10 = 80%
        assert score.score == 80.0
        assert score.grade == "B"

    def test_grade_boundaries(self) -> None:
        # A: >= 90
        assert RuleScore(rule="t", passed=9, errors=1).grade == "A"
        # B: >= 80
        assert RuleScore(rule="t", passed=8, errors=2).grade == "B"
        # C: >= 70
        assert RuleScore(rule="t", passed=7, errors=3).grade == "C"
        # D: >= 60
        assert RuleScore(rule="t", passed=6, errors=4).grade == "D"
        # F: < 60
        assert RuleScore(rule="t", passed=5, errors=5).grade == "F"


class TestScorecard:
    """Tests for Scorecard class."""

    def test_empty_scorecard(self) -> None:
        card = Scorecard(name="Test")
        assert card.total_checks == 0
        assert card.overall_score == 100.0
        assert card.is_passing is True

    def test_add_ok_message(self) -> None:
        card = Scorecard(name="Test")
        card.add_message(A11yMessage.ok("TST001", "Passed", rule="test-rule"))
        assert card.total_passed == 1
        assert card.total_warnings == 0
        assert card.total_errors == 0
        assert "test-rule" in card.rule_scores

    def test_add_warn_message(self) -> None:
        card = Scorecard(name="Test")
        card.add_message(A11yMessage.warn("TST001", "Warning", "Why", rule="test-rule"))
        assert card.total_warnings == 1
        assert card.is_passing is True  # Warnings don't fail

    def test_add_error_message(self) -> None:
        card = Scorecard(name="Test")
        card.add_message(
            A11yMessage.error("TST001", "Error", "Why", "Fix", rule="test-rule")
        )
        assert card.total_errors == 1
        assert card.is_passing is False

    def test_add_messages_batch(self) -> None:
        card = Scorecard(name="Test")
        messages = [
            A11yMessage.ok("TST001", "Test 1", rule="rule-a"),
            A11yMessage.warn("TST002", "Test 2", "Why", rule="rule-b"),
            A11yMessage.error("TST003", "Test 3", "Why", "Fix", rule="rule-a"),
        ]
        card.add_messages(messages)
        assert card.total_checks == 3
        assert len(card.rule_scores) == 2

    def test_overall_score_calculation(self) -> None:
        card = Scorecard(name="Test")
        card.add_messages(
            [
                A11yMessage.ok("TST001", "Test 1", rule="r"),
                A11yMessage.ok("TST002", "Test 2", rule="r"),
                A11yMessage.warn("TST003", "Test 3", "Why", rule="r"),
                A11yMessage.error("TST004", "Test 4", "Why", "Fix", rule="r"),
            ]
        )
        # 2 passed + 0.5 warn + 0 error = 2.5 / 4 = 62.5%
        assert card.overall_score == 62.5
        assert card.overall_grade == "D"

    def test_summary(self) -> None:
        card = Scorecard(name="Test Card")
        card.add_message(A11yMessage.ok("TST001", "Test", rule="test"))
        summary = card.summary()
        assert "Test Card" in summary
        assert "Passed: 1" in summary

    def test_to_dict(self) -> None:
        card = Scorecard(name="Test")
        card.add_message(A11yMessage.ok("TST001", "Test", rule="test-rule"))
        d = card.to_dict()
        assert d["name"] == "Test"
        assert d["overall_score"] == 100.0
        assert d["overall_grade"] == "A"
        assert d["is_passing"] is True
        assert d["totals"]["passed"] == 1
        assert "test-rule" in d["rules"]
        assert len(d["messages"]) == 1

    def test_unknown_rule(self) -> None:
        card = Scorecard(name="Test")
        # Message without rule gets assigned to "unknown"
        card.add_message(A11yMessage.ok("TST001", "Test"))
        assert "unknown" in card.rule_scores


class TestScorecardBuilder:
    """Tests for ScorecardBuilder class."""

    def test_build_empty(self) -> None:
        builder = ScorecardBuilder()
        card = builder.build()
        assert card.total_checks == 0

    def test_custom_name(self) -> None:
        builder = ScorecardBuilder(name="Custom Name")
        card = builder.build()
        assert card.name == "Custom Name"

    def test_add_scan_result(self) -> None:
        messages = [
            A11yMessage.ok("TST001", "Test 1", rule="r"),
            A11yMessage.ok("TST002", "Test 2", rule="r"),
        ]
        builder = ScorecardBuilder()
        builder.add_scan_result(messages)
        card = builder.build()
        assert card.total_checks == 2

    def test_add_ok_check(self) -> None:
        builder = ScorecardBuilder()
        builder.add_ok_check("test-rule", "TST001", "Test passed")
        card = builder.build()
        assert card.total_passed == 1

    def test_chaining(self) -> None:
        card = (
            ScorecardBuilder(name="Chained")
            .add_ok_check("rule-1", "TST001", "Test 1")
            .add_ok_check("rule-2", "TST002", "Test 2")
            .build()
        )
        assert card.total_checks == 2


class TestCreateScorecard:
    """Tests for create_scorecard convenience function."""

    def test_create_from_messages(self) -> None:
        messages = [
            A11yMessage.ok("TST001", "Test", rule="r"),
            A11yMessage.warn("TST002", "Test", "Why", rule="r"),
        ]
        card = create_scorecard(messages)
        assert card.total_checks == 2

    def test_custom_name(self) -> None:
        card = create_scorecard([], name="Custom")
        assert card.name == "Custom"
