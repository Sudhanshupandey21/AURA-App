"""Generate human-readable explanations for route safety decisions."""

from typing import Dict, Optional


def _build_route_factors_description(route_summary: Dict[str, any]) -> str:
    parts = []
    route_risk = float(route_summary.get("route_risk", 0.0))
    if route_risk >= 80:
        parts.append("contains high-risk segments and incident hotspots")
    elif route_risk >= 60:
        parts.append("includes moderate safety concerns and dense areas")
    else:
        parts.append("offers a safer passage with lower risk exposure")

    if route_summary.get("distance_km", 0.0) > 6.0:
        parts.append("but is longer in distance")
    if route_summary.get("duration_min", 0.0) > 18.0:
        parts.append("and takes more time to traverse")

    return ". ".join(parts)


def generate_route_explanation(
    route_summary: Dict[str, any],
    trigger: Optional[str] = None,
    incident_new: bool = False,
    crowd_change: float = 0.0,
    light_change: float = 0.0,
) -> str:
    """Generate an explanation for the safest route or rerouting decision."""
    route_id = route_summary.get("recommended_route") or route_summary.get("route_id", "Unknown")
    route_risk = float(route_summary.get("route_risk", 0.0))
    base = f"Route {route_id} selected with estimated risk {int(route_risk)}."

    factors = _build_route_factors_description(route_summary)
    if trigger == "reroute":
        reasons = [
            "Rerouted due to elevated route risk.",
            f"New incident detected: {incident_new}.",
            f"Crowd conditions worsened by {round(crowd_change * 100)}%.",
            f"Lighting conditions worsened by {round(light_change * 100)}%.",
            factors,
        ]
    elif trigger == "hold":
        reasons = [
            "Current active route remains safest.",
            factors,
        ]
    else:
        reasons = [
            f"Route summary: {factors}.",
        ]

    return " ".join([base] + [reason for reason in reasons if reason])
