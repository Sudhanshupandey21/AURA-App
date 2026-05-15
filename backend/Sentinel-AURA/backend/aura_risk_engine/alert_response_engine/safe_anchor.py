"""Safe anchor guidance system for finding nearby shelter."""

import logging
import math
from typing import Dict, List, Optional

from aura_risk_engine.alert_response_engine.utils import AnchorType, SafeAnchor, validate_coordinate

logger = logging.getLogger(__name__)

EARTH_RADIUS_METERS = 6371000.0


def _haversine_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """Calculate distance between two coordinates in meters."""
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lng = math.radians(lng2 - lng1)

    a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lng / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return EARTH_RADIUS_METERS * c


class SafeAnchorGuidanceEngine:
    """Recommends nearby safe anchors during emergencies."""

    def __init__(self) -> None:
        self._anchors: Dict[str, SafeAnchor] = {}

    def register_anchor(self, anchor: SafeAnchor) -> None:
        """Register a safe anchor location."""
        if not anchor.verified:
            logger.warning(f"Registering unverified anchor: {anchor.name}")
        self._anchors[anchor.anchor_id] = anchor
        logger.debug(f"Registered anchor: {anchor.name}")

    def find_nearest_safe_anchor(
        self,
        current_location: Dict[str, float],
        anchor_type: Optional[AnchorType] = None,
        max_distance_m: float = 1000.0,
    ) -> Optional[SafeAnchor]:
        """Find the nearest safe anchor within specified distance."""
        lat = current_location.get("latitude") or current_location.get("lat")
        lng = current_location.get("longitude") or current_location.get("lng")
        validate_coordinate(lat, lng)

        candidates: List[tuple] = []
        for anchor in self._anchors.values():
            if anchor_type and anchor.anchor_type != anchor_type:
                continue

            distance = _haversine_distance(lat, lng, anchor.latitude, anchor.longitude)
            if distance <= max_distance_m:
                candidates.append((distance, anchor))

        if not candidates:
            logger.warning(f"No safe anchors within {max_distance_m}m.")
            return None

        candidates.sort(key=lambda x: x[0])
        nearest_distance, nearest_anchor = candidates[0]

        logger.info(f"Found nearest anchor: {nearest_anchor.name} ({nearest_distance:.0f}m)")
        return SafeAnchor(
            anchor_id=nearest_anchor.anchor_id,
            anchor_type=nearest_anchor.anchor_type,
            name=nearest_anchor.name,
            latitude=nearest_anchor.latitude,
            longitude=nearest_anchor.longitude,
            distance_m=nearest_distance,
            verified=nearest_anchor.verified,
            contact_info=nearest_anchor.contact_info,
        )

    def find_all_safe_anchors_nearby(
        self,
        current_location: Dict[str, float],
        max_distance_m: float = 500.0,
        limit: int = 5,
    ) -> List[SafeAnchor]:
        """Find all nearby safe anchors ranked by distance."""
        lat = current_location.get("latitude") or current_location.get("lat")
        lng = current_location.get("longitude") or current_location.get("lng")
        validate_coordinate(lat, lng)

        candidates: List[tuple] = []
        for anchor in self._anchors.values():
            distance = _haversine_distance(lat, lng, anchor.latitude, anchor.longitude)
            if distance <= max_distance_m:
                candidates.append((distance, anchor))

        candidates.sort(key=lambda x: x[0])
        result = []
        for distance, anchor in candidates[:limit]:
            result.append(
                SafeAnchor(
                    anchor_id=anchor.anchor_id,
                    anchor_type=anchor.anchor_type,
                    name=anchor.name,
                    latitude=anchor.latitude,
                    longitude=anchor.longitude,
                    distance_m=distance,
                    verified=anchor.verified,
                    contact_info=anchor.contact_info,
                )
            )

        logger.info(f"Found {len(result)} nearby safe anchors.")
        return result

    def get_anchor_count(self) -> int:
        """Get total number of registered anchors."""
        return len(self._anchors)


_default_guidance_engine = SafeAnchorGuidanceEngine()


def find_nearest_safe_anchor(
    current_location: Dict[str, float],
    anchor_type: Optional[AnchorType] = None,
    max_distance_m: float = 1000.0,
) -> Optional[SafeAnchor]:
    """Find the nearest safe anchor."""
    return _default_guidance_engine.find_nearest_safe_anchor(
        current_location,
        anchor_type,
        max_distance_m,
    )


def find_all_safe_anchors_nearby(
    current_location: Dict[str, float],
    max_distance_m: float = 500.0,
    limit: int = 5,
) -> List[SafeAnchor]:
    """Find all nearby safe anchors."""
    return _default_guidance_engine.find_all_safe_anchors_nearby(
        current_location,
        max_distance_m,
        limit,
    )
