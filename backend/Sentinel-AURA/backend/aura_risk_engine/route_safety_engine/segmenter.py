"""Segmentation engine for breaking navigation routes into analyzable units."""

from typing import Dict, List

from aura_risk_engine.route_safety_engine.geo_utils import split_polyline_by_distance
from aura_risk_engine.route_safety_engine.utils import RouteDefinition, validate_route


def segment_route(route: RouteDefinition, segment_length_m: float = 200.0) -> List[Dict[str, float]]:
    """Divide a route polyline into fixed-size geographic segments."""
    validated_route = validate_route(route)
    anchors = split_polyline_by_distance(validated_route["polyline"], segment_length_m)

    segments: List[Dict[str, float]] = []
    for index, point in enumerate(anchors, start=1):
        segments.append(
            {
                "segment_id": index,
                "lat": point["lat"],
                "lng": point["lng"],
                "route_id": validated_route["route_id"],
            }
        )

    if len(segments) < 2:
        raise ValueError("Route segmentation must produce at least two analyzable segments.")

    return segments
