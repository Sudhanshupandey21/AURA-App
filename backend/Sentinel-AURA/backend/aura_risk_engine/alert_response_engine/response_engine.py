"""Response decision engine for determining appropriate actions."""

import logging

from aura_risk_engine.alert_response_engine.utils import AlertLevel, ResponseAction, validate_risk_score

logger = logging.getLogger(__name__)


class ResponseDecisionEngine:
    """Determines the best response action based on risk and conditions."""

    def __init__(
        self,
        reroute_threshold: float = 65.0,
        emergency_threshold: float = 80.0,
        sos_threshold: float = 95.0,
    ) -> None:
        self.reroute_threshold = validate_risk_score(reroute_threshold)
        self.emergency_threshold = validate_risk_score(emergency_threshold)
        self.sos_threshold = validate_risk_score(sos_threshold)

    def decide_response_action(
        self,
        risk_score: float,
        alert_level: AlertLevel,
        risk_trend: str = "stable",
        active_incidents: int = 0,
        is_night: bool = False,
    ) -> ResponseAction:
        """Decide the best response action based on current conditions."""
        risk_score = validate_risk_score(risk_score)

        # Critical immediate SOS
        if risk_score >= self.sos_threshold:
            logger.warning(f"Automatic SOS triggered: risk {risk_score} at critical level.")
            return ResponseAction.ACTIVATE_SOS

        # Emergency mode
        if risk_score >= self.emergency_threshold or (active_incidents >= 3 and is_night):
            logger.warning(f"Emergency mode triggered: risk {risk_score}, incidents {active_incidents}.")
            return ResponseAction.TRIGGER_EMERGENCY

        # Recommend reroute
        if risk_score >= self.reroute_threshold or (risk_trend == "increasing" and alert_level in [AlertLevel.HIGH, AlertLevel.CRITICAL]):
            logger.info(f"Rerouting recommended: risk {risk_score}, trend {risk_trend}.")
            return ResponseAction.RECOMMEND_REROUTE

        # Issue caution
        if alert_level in [AlertLevel.MEDIUM, AlertLevel.HIGH]:
            logger.info(f"Caution alert issued: level {alert_level}.")
            return ResponseAction.ISSUE_CAUTION

        # Continue monitoring
        logger.debug(f"Continuing monitoring: risk {risk_score}, level {alert_level}.")
        return ResponseAction.CONTINUE_MONITORING


_default_response_engine = ResponseDecisionEngine()


def decide_response_action(
    risk_score: float,
    alert_level: AlertLevel,
    risk_trend: str = "stable",
    active_incidents: int = 0,
    is_night: bool = False,
) -> ResponseAction:
    """Decide the best response action."""
    return _default_response_engine.decide_response_action(
        risk_score,
        alert_level,
        risk_trend,
        active_incidents,
        is_night,
    )
