"""Route Safety Engine for AURA X.

This package provides real-time route safety analysis, route segmentation,
segment-level risk scoring, safest-route recommendation, dynamic rerouting,
and explainability for navigation systems.
"""

from aura_risk_engine.route_safety_engine.route_processor import process_routes, analyze_route, process_routes_with_analysis, choose_best_route
from aura_risk_engine.route_safety_engine.segmenter import segment_route
from aura_risk_engine.route_safety_engine.segment_risk import analyze_segment_risk
from aura_risk_engine.route_safety_engine.route_aggregator import calculate_route_risk
from aura_risk_engine.route_safety_engine.safest_route import select_safest_route
from aura_risk_engine.route_safety_engine.rerouting_engine import reroute_if_needed
from aura_risk_engine.route_safety_engine.explainability import generate_route_explanation
from aura_risk_engine.route_safety_engine.geo_utils import haversine_distance_meters, split_polyline_by_distance
from aura_risk_engine.route_safety_engine.utils import RouteDefinition, RouteSummary, RouteRiskProfile

__all__ = [
    "process_routes",
    "process_routes_with_analysis",
    "choose_best_route",
    "analyze_route",
    "segment_route",
    "analyze_segment_risk",
    "calculate_route_risk",
    "select_safest_route",
    "reroute_if_needed",
    "generate_route_explanation",
    "haversine_distance_meters",
    "split_polyline_by_distance",
    "RouteDefinition",
    "RouteSummary",
    "RouteRiskProfile",
]