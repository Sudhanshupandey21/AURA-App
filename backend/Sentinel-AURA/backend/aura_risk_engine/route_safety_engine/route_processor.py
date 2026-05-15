"""Route processing and end-to-end route safety analysis pipeline."""

from typing import Dict, List, Optional

from aura_risk_engine.route_safety_engine.segmenter import segment_route
from aura_risk_engine.route_safety_engine.segment_risk import analyze_segment_risk
from aura_risk_engine.route_safety_engine.route_aggregator import calculate_route_risk
from aura_risk_engine.route_safety_engine.safest_route import select_safest_route
from aura_risk_engine.route_safety_engine.utils import RouteDefinition, RouteRiskProfile, RouteSummary, process_routes


def analyze_route(
    route: RouteDefinition,
    segment_length_m: float = 200.0,
    risk_profile: Optional[RouteRiskProfile] = None,
) -> RouteSummary:
    """Analyze a single route and return a route summary with risk metrics."""
    segments = segment_route(route, segment_length_m=segment_length_m)
    segment_risks: List[int] = []
    for _ in segments:
        segment_risks.append(
            analyze_segment_risk(
                time_risk=risk_profile.time_risk if risk_profile else 0.2,
                crowd_risk=risk_profile.crowd_risk if risk_profile else 0.2,
                light_risk=risk_profile.light_risk if risk_profile else 0.2,
                incident_risk=risk_profile.incident_risk if risk_profile else 0.1,
                area_risk=risk_profile.area_risk if risk_profile else 0.2,
                profile=risk_profile,
            )
        )

    route_risk = calculate_route_risk(segment_risks)
    return {
        "route_id": route["route_id"],
        "distance_km": route["distance_km"],
        "duration_min": route["duration_min"],
        "segment_count": len(segments),
        "segment_risks": segment_risks,
        "route_risk": float(route_risk),
    }


def process_routes_with_analysis(
    raw_routes: List[RouteDefinition],
    segment_length_m: float = 200.0,
    risk_profile: Optional[RouteRiskProfile] = None,
) -> List[RouteSummary]:
    """Validate raw route input and analyze all routes for safety scoring."""
    routes = process_routes(raw_routes)
    summaries: List[RouteSummary] = []
    for route in routes:
        summaries.append(analyze_route(route, segment_length_m=segment_length_m, risk_profile=risk_profile))
    return summaries


def choose_best_route(
    raw_routes: List[RouteDefinition],
    segment_length_m: float = 200.0,
    risk_profile: Optional[RouteRiskProfile] = None,
) -> Dict[str, str | float]:
    """Process candidate routes and return the safest route recommendation."""
    summaries = process_routes_with_analysis(raw_routes, segment_length_m=segment_length_m, risk_profile=risk_profile)
    return select_safest_route(summaries)
