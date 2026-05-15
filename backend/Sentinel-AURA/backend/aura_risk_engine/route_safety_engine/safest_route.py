"""Select the safest navigation route given route risk summaries."""

from typing import Dict, List

from aura_risk_engine.route_safety_engine.utils import RouteSummary, safe_weighted_cost


def select_safest_route(route_summaries: List[RouteSummary]) -> Dict[str, str | float]:
    """Select the safest route based on risk, distance, and duration."""
    if not isinstance(route_summaries, list) or len(route_summaries) == 0:
        raise ValueError("route_summaries must be a non-empty list.")

    for summary in route_summaries:
        if "route_id" not in summary or "route_risk" not in summary:
            raise ValueError("Each route summary must include route_id and route_risk.")

    safe_route = min(
        route_summaries,
        key=lambda route: (
            float(route["route_risk"]),
            safe_weighted_cost(route),
        ),
    )

    return {
        "recommended_route": safe_route["route_id"],
        "risk_score": float(safe_route["route_risk"]),
        "distance_km": float(safe_route.get("distance_km", 0.0)),
        "duration_min": float(safe_route.get("duration_min", 0.0)),
    }
