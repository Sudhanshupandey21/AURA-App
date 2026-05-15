"""Alert and response validation engine."""

import logging
from typing import Dict, Optional

from aura_risk_engine.testing_framework.utils import TestResult, TestScenario, AlertLevel

logger = logging.getLogger(__name__)


class AlertValidator:
    """Validates alert detection and response logic."""

    def __init__(self) -> None:
        self._alert_thresholds = {
            "danger_threshold": 75.0,
            "incident_spike_threshold": 2,
            "trend_acceleration_threshold": 0.15,
        }
        self._severity_thresholds = {
            AlertLevel.LOW: (0.0, 40.0),
            AlertLevel.MEDIUM: (40.0, 70.0),
            AlertLevel.HIGH: (70.0, 90.0),
            AlertLevel.CRITICAL: (90.0, 100.0),
        }

    def validate_alert_triggering(
        self,
        scenario: TestScenario,
        risk_score: float,
        incident_count: int,
        trend_acceleration: float,
        alert_triggered: bool,
    ) -> TestResult:
        """Validate if alert should be triggered based on conditions."""
        should_trigger = (
            risk_score >= self._alert_thresholds["danger_threshold"]
            or incident_count >= self._alert_thresholds["incident_spike_threshold"]
            or trend_acceleration >= self._alert_thresholds["trend_acceleration_threshold"]
        )

        trigger_valid = alert_triggered == should_trigger

        conditions = []
        if risk_score >= self._alert_thresholds["danger_threshold"]:
            conditions.append(f"risk >= {self._alert_thresholds['danger_threshold']}")
        if incident_count >= self._alert_thresholds["incident_spike_threshold"]:
            conditions.append(f"incidents >= {self._alert_thresholds['incident_spike_threshold']}")
        if trend_acceleration >= self._alert_thresholds["trend_acceleration_threshold"]:
            conditions.append(f"trend >= {self._alert_thresholds['trend_acceleration_threshold']}")

        condition_str = ", ".join(conditions) if conditions else "none"

        if trigger_valid:
            message = f"Alert triggering correct: {alert_triggered} ({condition_str})"
        else:
            expected = "trigger" if should_trigger else "no trigger"
            message = f"Alert triggering incorrect. Expected: {expected}, Got: {alert_triggered} ({condition_str})"

        return TestResult(
            test_name=f"alert_trigger_validation_{scenario.name}",
            passed=trigger_valid,
            message=message,
            expected=f"Trigger if: risk>={self._alert_thresholds['danger_threshold']} OR incidents>={self._alert_thresholds['incident_spike_threshold']} OR trend>={self._alert_thresholds['trend_acceleration_threshold']}",
            actual=f"Risk: {risk_score:.1f}, Incidents: {incident_count}, Trend: {trend_acceleration:.3f}, Triggered: {alert_triggered}",
        )

    def validate_severity_classification(
        self,
        scenario: TestScenario,
        risk_score: float,
        classified_severity: str,
    ) -> TestResult:
        """Validate severity classification based on risk score."""
        try:
            severity_level = AlertLevel(classified_severity)
        except ValueError:
            return TestResult(
                test_name=f"severity_validation_{scenario.name}",
                passed=False,
                message=f"Invalid severity level: {classified_severity}",
                expected="Valid AlertLevel enum value",
                actual=classified_severity,
            )

        min_score, max_score = self._severity_thresholds[severity_level]
        severity_valid = min_score <= risk_score <= max_score

        if severity_valid:
            message = f"Severity classification correct: {classified_severity}"
        else:
            expected_levels = [
                level.value for level, (min_s, max_s) in self._severity_thresholds.items()
                if min_s <= risk_score <= max_s
            ]
            expected_str = expected_levels[0] if expected_levels else "unknown"
            message = f"Severity classification incorrect. Expected: {expected_str}, Got: {classified_severity}"

        return TestResult(
            test_name=f"severity_validation_{scenario.name}",
            passed=severity_valid,
            message=message,
            expected=f"Risk {risk_score:.1f} should be in {min_score:.1f}-{max_score:.1f} for {severity_level.value}",
            actual=f"Classified as: {classified_severity}",
        )

    def validate_response_action(
        self,
        scenario: TestScenario,
        risk_score: float,
        severity_level: str,
        response_action: str,
    ) -> TestResult:
        """Validate appropriate response action for given conditions."""
        # Define expected actions based on risk/severity
        if risk_score >= 95 or severity_level == AlertLevel.CRITICAL.value:
            expected_actions = ["emergency_response", "sos_alert", "immediate_rerouting"]
        elif risk_score >= 80 or severity_level == AlertLevel.HIGH.value:
            expected_actions = ["high_alert", "rerouting", "increased_monitoring"]
        elif risk_score >= 65 or severity_level == AlertLevel.MEDIUM.value:
            expected_actions = ["medium_alert", "route_review", "monitoring"]
        else:
            expected_actions = ["low_alert", "normal_monitoring"]

        action_valid = response_action in expected_actions

        if action_valid:
            message = f"Response action appropriate: {response_action}"
        else:
            message = f"Response action inappropriate. Expected one of: {expected_actions}, Got: {response_action}"

        return TestResult(
            test_name=f"response_validation_{scenario.name}",
            passed=action_valid,
            message=message,
            expected=f"One of: {expected_actions}",
            actual=response_action,
        )

    def validate_sos_escalation(
        self,
        scenario: TestScenario,
        risk_score: float,
        severity_level: str,
        sos_triggered: bool,
    ) -> TestResult:
        """Validate SOS escalation logic."""
        should_trigger_sos = risk_score >= 95 or severity_level == AlertLevel.CRITICAL.value

        sos_valid = sos_triggered == should_trigger_sos

        if sos_valid:
            action = "triggered" if sos_triggered else "not triggered"
            message = f"SOS escalation correct: {action}"
        else:
            expected = "trigger" if should_trigger_sos else "not trigger"
            actual = "triggered" if sos_triggered else "not triggered"
            message = f"SOS escalation incorrect. Expected: {expected}, Got: {actual}"

        return TestResult(
            test_name=f"sos_validation_{scenario.name}",
            passed=sos_valid,
            message=message,
            expected=f"SOS if risk >= 95 or severity == CRITICAL",
            actual=f"Risk: {risk_score:.1f}, Severity: {severity_level}, SOS: {sos_triggered}",
        )


_default_validator = AlertValidator()


def validate_alert_triggering(
    scenario: TestScenario,
    risk_score: float,
    incident_count: int,
    trend_acceleration: float,
    alert_triggered: bool,
) -> TestResult:
    """Validate alert triggering."""
    return _default_validator.validate_alert_triggering(
        scenario, risk_score, incident_count, trend_acceleration, alert_triggered
    )


def validate_severity_classification(
    scenario: TestScenario,
    risk_score: float,
    classified_severity: str,
) -> TestResult:
    """Validate severity classification."""
    return _default_validator.validate_severity_classification(
        scenario, risk_score, classified_severity
    )


def validate_response_action(
    scenario: TestScenario,
    risk_score: float,
    severity_level: str,
    response_action: str,
) -> TestResult:
    """Validate response action."""
    return _default_validator.validate_response_action(
        scenario, risk_score, severity_level, response_action
    )
