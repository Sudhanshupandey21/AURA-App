"""Dynamic rerouting engine for real-time route safety adjustment."""

from typing import Dict, List, Optional

from aura_risk_engine.route_safety_engine.explainability import generate_route_explanation
from aura_risk_engine.route_safety_engine.safest_route import select_safest_route
from aura_risk_engine.route_safety_engine.utils import RouteSummary, RouteRiskProfile


def reroute_if_needed(
    active_route: RouteSummary,
    candidate_routes: List[RouteSummary],
    incident_new: bool = False,
    crowd_worsening: float = 0.0,
    light_worsening: float = 0.0,
    risk_threshold: float = 60.0,
    risk_profile: RouteRiskProfile = None,
) -> Dict[str, str | float | bool]:
    """Evaluate the active route and determine whether a safer alternative is available."""
    if not isinstance(active_route, dict):
        raise ValueError("active_route must be a route summary dictionary.")
    if not isinstance(candidate_routes, list) or len(candidate_routes) == 0:
        raise ValueError("candidate_routes must be a non-empty list of alternative routes.")

    current_risk = float(active_route.get("route_risk", 0.0))
    risk_improvement_threshold = 5.0
    reroute_required = current_risk >= risk_threshold or incident_new or crowd_worsening >= 0.15 or light_worsening >= 0.15

    best_alternative = select_safest_route(candidate_routes)
    best_alternative_risk = float(best_alternative["risk_score"])

    if reroute_required and best_alternative_risk + risk_improvement_threshold < current_risk:
        explanation = generate_route_explanation(
            best_alternative,
            trigger="reroute",
            incident_new=incident_new,
            crowd_change=crowd_worsening,
            light_change=light_worsening,
        )
        return {
            "rerouted": True,
            "recommended_route": best_alternative["recommended_route"],
            "risk_score": best_alternative_risk,
            "explanation": explanation,
        }

    return {
        "rerouted": False,
        "recommended_route": active_route.get("route_id", "unknown"),
        "risk_score": current_risk,
        "explanation": generate_route_explanation(active_route, trigger="hold"),
    }
