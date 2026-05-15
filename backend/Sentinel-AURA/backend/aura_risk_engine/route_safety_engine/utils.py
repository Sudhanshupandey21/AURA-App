"""Utility helpers for the Route Safety Engine."""

import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Sequence, Tuple, Union

import numpy as np

logger = logging.getLogger(__name__)

Coordinate = Union[List[float], Tuple[float, float], Dict[str, float]]
RouteDefinition = Dict[str, Any]
RouteSummary = Dict[str, Any]


@dataclass(frozen=True)
class RouteRiskProfile:
    time_risk: float = 0.2
    crowd_risk: float = 0.2
    light_risk: float = 0.2
    incident_risk: float = 0.1
    area_risk: float = 0.2


def clip_score(value: float, minimum: float = 0.0, maximum: float = 100.0) -> float:
    """Clip a score to a fixed numeric range."""
    return float(max(minimum, min(maximum, value)))


def validate_coordinate(coordinate: Coordinate) -> Tuple[float, float]:
    """Normalize and validate a single geographic coordinate."""
    if isinstance(coordinate, dict):
        lat = coordinate.get("lat")
        lng = coordinate.get("lng") or coordinate.get("lon")
    elif isinstance(coordinate, (list, tuple)) and len(coordinate) == 2:
        lat, lng = coordinate
    else:
        raise ValueError("Route coordinates must be a [lat, lng] pair or {lat, lng} dict.")

    try:
        lat = float(lat)
        lng = float(lng)
    except (TypeError, ValueError):
        raise ValueError("Coordinate latitude and longitude must be numeric.")

    if not (-90.0 <= lat <= 90.0 and -180.0 <= lng <= 180.0):
        raise ValueError(f"Coordinate out of bounds: ({lat}, {lng}).")

    return lat, lng


def normalize_polyline(polyline: Sequence[Coordinate]) -> List[Dict[str, float]]:
    """Validate and normalize a polyline into standard latitude/longitude points."""
    if polyline is None or len(polyline) < 2:
        raise ValueError("Route polyline must contain at least two coordinate points.")

    normalized: List[Dict[str, float]] = []
    for point in polyline:
        lat, lng = validate_coordinate(point)
        normalized.append({"lat": lat, "lng": lng})

    return normalized


def validate_route(route: RouteDefinition) -> RouteDefinition:
    """Validate a route definition dictionary and normalize its shape."""
    if not isinstance(route, dict):
        raise ValueError("Route definition must be a dictionary.")

    route_id = route.get("route_id")
    if not route_id or not isinstance(route_id, str):
        raise ValueError("Route definition requires a non-empty string route_id.")

    distance_km = route.get("distance_km")
    duration_min = route.get("duration_min")
    polyline = route.get("polyline")

    if distance_km is None or float(distance_km) < 0.0:
        raise ValueError("Route distance_km must be a non-negative number.")
    if duration_min is None or float(duration_min) < 0.0:
        raise ValueError("Route duration_min must be a non-negative number.")

    return {
        "route_id": route_id,
        "distance_km": float(distance_km),
        "duration_min": float(duration_min),
        "polyline": normalize_polyline(polyline),
    }


def process_routes(raw_routes: Sequence[RouteDefinition]) -> List[RouteDefinition]:
    """Validate and normalize a list of routes for analysis."""
    if raw_routes is None:
        raise ValueError("No routes provided.")
    if not isinstance(raw_routes, (list, tuple)) or len(raw_routes) == 0:
        raise ValueError("Route input must be a non-empty list of route definitions.")

    cleaned_routes: List[RouteDefinition] = []
    seen_ids = set()
    for raw_route in raw_routes:
        route = validate_route(raw_route)
        if route["route_id"] in seen_ids:
            raise ValueError(f"Duplicate route_id found: {route['route_id']}")
        seen_ids.add(route["route_id"])
        cleaned_routes.append(route)

    return cleaned_routes


def validate_risk_factors(**factors: float) -> None:
    """Validate realtime risk factor values are in the expected range."""
    for name, value in factors.items():
        if not isinstance(value, (int, float)):
            raise ValueError(f"Risk factor {name} must be numeric.")
        if not (0.0 <= float(value) <= 1.0):
            raise ValueError(f"Risk factor {name} must be between 0.0 and 1.0.")


def safe_weighted_cost(route_summary: RouteSummary, distance_weight: float = 1.5, duration_weight: float = 0.4) -> float:
    """Compute a combined safety and efficiency cost for route selection."""
    return (
        float(route_summary["route_risk"]) +
        float(route_summary["distance_km"]) * distance_weight +
        float(route_summary["duration_min"]) * duration_weight
    )


def normalize_score(value: float, minimum: float = 0.0, maximum: float = 100.0) -> int:
    """Normalize a numeric value to an integer risk score."""
    return int(clip_score(round(value, 2), minimum, maximum))
