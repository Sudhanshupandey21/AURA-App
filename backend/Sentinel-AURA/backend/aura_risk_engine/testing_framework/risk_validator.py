"""Risk calculation validation engine."""

import logging
from typing import Dict, Optional, Tuple

from aura_risk_engine.testing_framework.utils import TestScenario, TestResult, RiskLevel

logger = logging.getLogger(__name__)


class RiskValidator:
    """Validates risk calculations against expected patterns."""

    def __init__(self) -> None:
        self._validation_rules = self._build_validation_rules()

    def _build_validation_rules(self) -> Dict[str, Dict[str, Tuple[float, float]]]:
        """Build expected risk ranges for different scenario types."""
        return {
            "safe_daytime": {
                "risk_score": (0.0, 30.0),
                "risk_level": (RiskLevel.SAFE.value, RiskLevel.LOW.value),
            },
            "crowded_daytime": {
                "risk_score": (20.0, 50.0),
                "risk_level": (RiskLevel.LOW.value, RiskLevel.MEDIUM.value),
            },
            "nighttime_low_crowd": {
                "risk_score": (40.0, 70.0),
                "risk_level": (RiskLevel.MEDIUM.value, RiskLevel.HIGH.value),
            },
            "isolated_dark": {
                "risk_score": (70.0, 95.0),
                "risk_level": (RiskLevel.HIGH.value, RiskLevel.CRITICAL.value),
            },
            "incident_nearby": {
                "risk_score": (60.0, 90.0),
                "risk_level": (RiskLevel.MEDIUM.value, RiskLevel.CRITICAL.value),
            },
            "emergency_situation": {
                "risk_score": (80.0, 100.0),
                "risk_level": (RiskLevel.CRITICAL.value, RiskLevel.CRITICAL.value),
            },
        }

    def _classify_scenario_type(self, scenario: TestScenario) -> str:
        """Classify scenario into validation categories."""
        if scenario.incident_severity > 0.8:
            return "emergency_situation"
        elif scenario.incident_severity > 0.5:
            return "incident_nearby"
        elif scenario.light_intensity < 0.2 and scenario.crowd_density < 0.2:
            return "isolated_dark"
        elif scenario.hour >= 22 or scenario.hour <= 5:
            if scenario.crowd_density < 0.3:
                return "nighttime_low_crowd"
            else:
                return "crowded_daytime"
        elif scenario.crowd_density > 0.7 and scenario.light_intensity > 0.7:
            return "crowded_daytime"
        else:
            return "safe_daytime"

    def validate_risk_calculation(
        self,
        scenario: TestScenario,
        calculated_risk_score: float,
        calculated_risk_level: str,
    ) -> TestResult:
        """Validate risk calculation against expected patterns."""
        scenario_type = self._classify_scenario_type(scenario)
        expected_ranges = self._validation_rules.get(scenario_type, {})

        if not expected_ranges:
            return TestResult(
                test_name=f"risk_validation_{scenario.name}",
                passed=False,
                message=f"Unknown scenario type: {scenario_type}",
                expected="Valid risk ranges",
                actual=f"Scenario type: {scenario_type}",
            )

        # Validate risk score
        score_min, score_max = expected_ranges["risk_score"]
        score_valid = score_min <= calculated_risk_score <= score_max

        # Validate risk level
        level_min, level_max = expected_ranges["risk_level"]
        level_valid = level_min <= RiskLevel(calculated_risk_level).value <= level_max

        passed = score_valid and level_valid

        if passed:
            message = f"Risk calculation valid for {scenario_type}"
        else:
            issues = []
            if not score_valid:
                issues.append(f"Risk score {calculated_risk_score:.1f} not in [{score_min:.1f}, {score_max:.1f}]")
            if not level_valid:
                issues.append(f"Risk level '{calculated_risk_level}' not in expected range")
            message = f"Risk validation failed: {'; '.join(issues)}"

        return TestResult(
            test_name=f"risk_validation_{scenario.name}",
            passed=passed,
            message=message,
            expected=f"Score: [{score_min:.1f}, {score_max:.1f}], Level: [{level_min}, {level_max}]",
            actual=f"Score: {calculated_risk_score:.1f}, Level: {calculated_risk_level}",
        )

    def validate_trend_calculation(
        self,
        scenario: TestScenario,
        calculated_trend: float,
        expected_trend_direction: Optional[str] = None,
    ) -> TestResult:
        """Validate trend calculation."""
        # Basic trend validation - trend should be reasonable
        trend_valid = -1.0 <= calculated_trend <= 1.0

        if expected_trend_direction:
            if expected_trend_direction == "increasing" and calculated_trend <= 0:
                trend_valid = False
            elif expected_trend_direction == "decreasing" and calculated_trend >= 0:
                trend_valid = False

        return TestResult(
            test_name=f"trend_validation_{scenario.name}",
            passed=trend_valid,
            message=f"Trend validation {'passed' if trend_valid else 'failed'}",
            expected=f"Trend in range [-1.0, 1.0]{f', direction: {expected_trend_direction}' if expected_trend_direction else ''}",
            actual=f"Trend: {calculated_trend:.3f}",
        )


_default_validator = RiskValidator()


def validate_risk_calculation(
    scenario: TestScenario,
    calculated_risk_score: float,
    calculated_risk_level: str,
) -> TestResult:
    """Validate risk calculation."""
    return _default_validator.validate_risk_calculation(
        scenario, calculated_risk_score, calculated_risk_level
    )


def validate_trend_calculation(
    scenario: TestScenario,
    calculated_trend: float,
    expected_trend_direction: Optional[str] = None,
) -> TestResult:
    """Validate trend calculation."""
    return _default_validator.validate_trend_calculation(
        scenario, calculated_trend, expected_trend_direction
    )
