"""Explainability and human-readable messaging system."""

import logging

from aura_risk_engine.alert_response_engine.utils import AlertLevel, ResponseAction

logger = logging.getLogger(__name__)


class AlertMessageGenerator:
    """Generates human-readable alert messages."""

    def __init__(self) -> None:
        self._alert_messages = {
            AlertLevel.LOW: "Area appears safe. Continue with normal caution.",
            AlertLevel.MEDIUM: "Moderate safety concerns detected. Stay aware.",
            AlertLevel.HIGH: "High-risk area detected. Consider alternative route.",
            AlertLevel.CRITICAL: "Critical danger. Immediate action required.",
        }

        self._action_messages = {
            ResponseAction.CONTINUE_MONITORING: "Monitoring situation. Stay alert.",
            ResponseAction.ISSUE_CAUTION: "⚠️ Caution alert: Conditions changing.",
            ResponseAction.RECOMMEND_REROUTE: "🚨 Safer route available. Consider switching.",
            ResponseAction.TRIGGER_EMERGENCY: "🚨🚨 EMERGENCY MODE ACTIVE. Extreme danger ahead.",
            ResponseAction.ACTIVATE_SOS: "🆘 SOS ACTIVATED. Authorities notified. Sharing location.",
        }

    def generate_alert_message(
        self,
        alert_level: AlertLevel,
        risk_score: float,
        reason: str = "",
    ) -> str:
        """Generate a message for an alert."""
        base = self._alert_messages.get(alert_level, "Alert triggered.")
        detail = f"Risk: {int(risk_score)}/100."
        message = f"{base} {detail}"

        if reason:
            message += f" {reason}"

        logger.info(f"Generated alert message: {message}")
        return message

    def generate_response_message(self, action: ResponseAction) -> str:
        """Generate a message for a response action."""
        message = self._action_messages.get(action, "System response triggered.")
        logger.info(f"Generated action message: {message}")
        return message

    def generate_contextual_alert(
        self,
        risk_score: float,
        risk_trend: str,
        active_incidents: int = 0,
        is_night: bool = False,
    ) -> str:
        """Generate a contextual alert message."""
        parts = []

        if active_incidents > 0:
            parts.append(f"Recent incident{'' if active_incidents == 1 else 's'} in area ({active_incidents}).")

        if risk_trend == "increasing":
            parts.append("Conditions deteriorating.")
        elif risk_trend == "decreasing":
            parts.append("Conditions improving.")

        if is_night:
            parts.append("Low visibility conditions.")

        if risk_score > 80:
            parts.append("Severe safety concerns.")
        elif risk_score > 60:
            parts.append("Elevated risk detected.")

        message = " ".join(parts)
        logger.debug(f"Generated contextual alert: {message}")
        return message

    def generate_rerouting_explanation(
        self,
        current_route_risk: float,
        new_route_risk: float,
        reason: str = "",
    ) -> str:
        """Generate an explanation for rerouting."""
        improvement = int(current_route_risk - new_route_risk)
        message = f"Rerouted to safer path. Risk reduced by {improvement} points ({int(new_route_risk)}/100)."

        if reason:
            message += f" Reason: {reason}."

        logger.info(f"Rerouting explanation: {message}")
        return message

    def generate_sos_notification(self, location: dict, reason: str = "") -> str:
        """Generate an SOS notification message."""
        lat = location.get("lat") or location.get("latitude")
        lng = location.get("lng") or location.get("longitude")
        message = f"🆘 EMERGENCY SOS ACTIVATED at ({lat:.4f}, {lng:.4f})."

        if reason:
            message += f" Reason: {reason}."

        message += " Location shared. Authorities alerted."
        logger.critical(f"SOS notification: {message}")
        return message

    def generate_safe_anchor_guidance(self, anchor_name: str, distance_m: float, anchor_type: str) -> str:
        """Generate a message guiding user to safe anchor."""
        direction = "nearby" if distance_m < 300 else "close" if distance_m < 600 else "accessible"
        message = f"Safe {anchor_type}: {anchor_name} ({direction}, {int(distance_m)}m away)."
        logger.info(f"Safe anchor guidance: {message}")
        return message


_default_message_generator = AlertMessageGenerator()


def generate_alert_message(
    alert_level: AlertLevel,
    risk_score: float,
    reason: str = "",
) -> str:
    """Generate an alert message."""
    return _default_message_generator.generate_alert_message(alert_level, risk_score, reason)


def generate_response_message(action: ResponseAction) -> str:
    """Generate a response action message."""
    return _default_message_generator.generate_response_message(action)


def generate_contextual_alert(
    risk_score: float,
    risk_trend: str,
    active_incidents: int = 0,
    is_night: bool = False,
) -> str:
    """Generate a contextual alert message."""
    return _default_message_generator.generate_contextual_alert(
        risk_score,
        risk_trend,
        active_incidents,
        is_night,
    )


def generate_rerouting_explanation(
    current_route_risk: float,
    new_route_risk: float,
    reason: str = "",
) -> str:
    """Generate a rerouting explanation."""
    return _default_message_generator.generate_rerouting_explanation(
        current_route_risk,
        new_route_risk,
        reason,
    )
