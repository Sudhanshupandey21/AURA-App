"""Alert severity classification engine."""

import logging

from aura_risk_engine.alert_response_engine.utils import AlertLevel, validate_risk_score

logger = logging.getLogger(__name__)


class SeverityClassifier:
    """Classifies alerts into severity levels."""

    def __init__(
        self,
        low_threshold: float = 40.0,
        medium_threshold: float = 70.0,
        high_threshold: float = 90.0,
    ) -> None:
        self.low_threshold = validate_risk_score(low_threshold)
        self.medium_threshold = validate_risk_score(medium_threshold)
        self.high_threshold = validate_risk_score(high_threshold)

    def classify_alert_level(self, risk_score: float) -> AlertLevel:
        """Classify a risk score into an alert level."""
        risk_score = validate_risk_score(risk_score)

        if risk_score >= self.high_threshold:
            level = AlertLevel.CRITICAL
        elif risk_score >= self.medium_threshold:
            level = AlertLevel.HIGH
        elif risk_score >= self.low_threshold:
            level = AlertLevel.MEDIUM
        else:
            level = AlertLevel.LOW

        logger.debug(f"Risk score {risk_score} classified as {level}")
        return level

    def get_alert_color(self, alert_level: AlertLevel) -> str:
        """Get UI color for alert level."""
        colors = {
            AlertLevel.LOW: "green",
            AlertLevel.MEDIUM: "yellow",
            AlertLevel.HIGH: "orange",
            AlertLevel.CRITICAL: "red",
        }
        return colors.get(alert_level, "gray")

    def get_alert_priority(self, alert_level: AlertLevel) -> int:
        """Get priority rank for alert level (lower = higher priority)."""
        priorities = {
            AlertLevel.CRITICAL: 1,
            AlertLevel.HIGH: 2,
            AlertLevel.MEDIUM: 3,
            AlertLevel.LOW: 4,
        }
        return priorities.get(alert_level, 5)


_default_classifier = SeverityClassifier()


def classify_alert_level(risk_score: float) -> AlertLevel:
    """Classify a risk score into an alert level."""
    return _default_classifier.classify_alert_level(risk_score)
