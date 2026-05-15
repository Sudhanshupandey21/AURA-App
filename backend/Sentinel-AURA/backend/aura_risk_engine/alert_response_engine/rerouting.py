"""Dynamic rerouting trigger engine."""

import logging
from typing import Dict, List, Optional

from aura_risk_engine.alert_response_engine.utils import ResponseAction, validate_risk_score

logger = logging.getLogger(__name__)


class ReroutingEngine:
    """Triggers dynamic rerouting when route becomes unsafe."""

    def __init__(self, reroute_threshold: float = 70.0, improvement_threshold: float = 10.0) -> None:
        self.reroute_threshold = validate_risk_score(reroute_threshold)
        self.improvement_threshold = improvement_threshold
        self._active_route: Optional[Dict] = None
        self._last_reroute_score: float = 0.0

    def trigger_rerouting(
        self,
        current_route_risk: float,
        available_alternatives: List[Dict],
        incident_ahead: bool = False,
        darkness_increase: float = 0.0,
        crowd_increase: float = 0.0,
    ) -> Optional[Dict]:
        """Determine if rerouting is needed and select best alternative."""
        current_route_risk = validate_risk_score(current_route_risk)

        trigger_conditions = [
            current_route_risk > self.reroute_threshold,
            incident_ahead,
            darkness_increase > 0.15,
            crowd_increase > 0.2,
        ]

        if not any(trigger_conditions):
            logger.debug("Rerouting not triggered: conditions stable.")
            return None

        if not available_alternatives:
            logger.warning("Rerouting requested but no alternatives available.")
            return None

        # Find safest alternative
        safest_alternative = min(
            available_alternatives,
            key=lambda route: float(route.get("risk_score", 100.0)),
        )

        safest_risk = float(safest_alternative.get("risk_score", 100.0))

        # Check if improvement is significant
        if safest_risk + self.improvement_threshold < current_route_risk:
            logger.info(f"Rerouting triggered: {safest_risk:.1f} << {current_route_risk:.1f}")
            self._last_reroute_score = current_route_risk
            return {
                "route_id": safest_alternative.get("route_id"),
                "risk_score": safest_risk,
                "reason": self._explain_reroute(incident_ahead, darkness_increase, crowd_increase),
            }

        logger.debug(f"No significant improvement: {safest_risk:.1f} vs {current_route_risk:.1f}")
        return None

    def _explain_reroute(self, incident_ahead: bool, darkness: float, crowd: float) -> str:
        """Generate an explanation for rerouting."""
        reasons = []
        if incident_ahead:
            reasons.append("incident ahead")
        if darkness > 0.15:
            reasons.append(f"darkness increased {darkness:.0%}")
        if crowd > 0.2:
            reasons.append(f"crowd increased {crowd:.0%}")
        return ", ".join(reasons) if reasons else "route safety degraded"


_default_rerouting_engine = ReroutingEngine()


def trigger_rerouting(
    current_route_risk: float,
    available_alternatives: List[Dict],
    incident_ahead: bool = False,
    darkness_increase: float = 0.0,
    crowd_increase: float = 0.0,
) -> Optional[Dict]:
    """Trigger dynamic rerouting if needed."""
    return _default_rerouting_engine.trigger_rerouting(
        current_route_risk,
        available_alternatives,
        incident_ahead,
        darkness_increase,
        crowd_increase,
    )
