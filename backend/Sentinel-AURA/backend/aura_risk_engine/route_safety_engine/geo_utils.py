"""Geographic utilities for route segmenting and distance calculations."""

import math
from typing import Dict, List

Coordinate = Dict[str, float]

EARTH_RADIUS_METERS = 6371000.0


def haversine_distance_meters(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """Return the great-circle distance in meters between two points."""
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lng = math.radians(lng2 - lng1)

    a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lng / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return EARTH_RADIUS_METERS * c


def interpolate_point(point_a: Coordinate, point_b: Coordinate, fraction: float) -> Coordinate:
    """Interpolate a point between two coordinates by fractional distance."""
    return {
        "lat": point_a["lat"] + (point_b["lat"] - point_a["lat"]) * fraction,
        "lng": point_a["lng"] + (point_b["lng"] - point_a["lng"]) * fraction,
    }


def split_polyline_by_distance(polyline: List[Coordinate], segment_length_m: float) -> List[Coordinate]:
    """Split a polyline into regular geographic segment anchor points."""
    if segment_length_m <= 0:
        raise ValueError("segment_length_m must be greater than 0.")
    if len(polyline) < 2:
        raise ValueError("Polyline must contain at least two points.")

    anchors: List[Coordinate] = [polyline[0]]
    accumulated = 0.0
    previous_point = polyline[0]

    for current_point in polyline[1:]:
        leg_distance = haversine_distance_meters(
            previous_point["lat"], previous_point["lng"], current_point["lat"], current_point["lng"]
        )
        if leg_distance == 0:
            previous_point = current_point
            continue

        remaining_leg = leg_distance
        start_point = previous_point
        while accumulated + remaining_leg >= segment_length_m:
            needed = segment_length_m - accumulated
            fraction = needed / remaining_leg
            anchor = interpolate_point(start_point, current_point, fraction)
            anchors.append(anchor)
            start_point = anchor
            remaining_leg -= needed
            accumulated = 0.0
        accumulated += remaining_leg
        previous_point = current_point

    if len(anchors) == 1 or anchors[-1] != polyline[-1]:
        anchors.append(polyline[-1])

    return anchors
