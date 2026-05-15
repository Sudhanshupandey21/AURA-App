"""
Geographic Impact Engine

Handles:
- Haversine distance calculation
- Geographic impact radius modeling
- Distance-based decay
- Geospatial analysis
"""

import logging
import math
from typing import Dict, Tuple, Optional

from aura_risk_engine.incident_intelligence.utils import clip_probability, GEO_IMPACT_THRESHOLDS

logger = logging.getLogger(__name__)

# Earth radius in meters
EARTH_RADIUS_METERS = 6371000.0


class GeoEngine:
    """
    Geographic impact modeling for incidents.
    
    Uses Haversine distance formula to calculate distance between
    incident location and target location, then applies distance-based
    decay to model geographic impact.
    
    Responsibilities:
    - Calculate Haversine distance
    - Model geographic impact radius
    - Apply distance-based decay
    - Classify geographic relevance
    
    Distance-Based Impact Scale:
    - 0-50m: 1.0 (very high)
    - 50-200m: 0.7 (high)
    - 200-500m: 0.4 (medium)
    - 500m-1km: 0.1 (low)
    - 1km+: 0.0 (negligible)
    """
    
    def __init__(self, impact_thresholds: Dict[str, Tuple[float, float]] = None):
        """
        Initialize geographic impact engine.
        
        Args:
            impact_thresholds: Optional custom distance thresholds in meters.
                             Maps category names to (min_distance, max_distance) tuples.
                             If not provided, uses default GEO_IMPACT_THRESHOLDS.
        """
        self.impact_thresholds = impact_thresholds or GEO_IMPACT_THRESHOLDS.copy()
        self.logger = logger
        self._validate_thresholds()
    
    def _validate_thresholds(self):
        """Validate threshold configuration."""
        for category, (min_dist, max_dist) in self.impact_thresholds.items():
            if min_dist < 0 or max_dist < 0:
                raise ValueError(
                    f"Invalid thresholds for '{category}': "
                    f"distances must be non-negative"
                )
            if min_dist > max_dist and max_dist != float('inf'):
                raise ValueError(
                    f"Invalid thresholds for '{category}': "
                    f"min_distance ({min_dist}) > max_distance ({max_dist})"
                )
    
    @staticmethod
    def haversine_distance(
        lat1: float,
        lon1: float,
        lat2: float,
        lon2: float
    ) -> float:
        """
        Calculate great-circle distance between two points on Earth.
        
        Uses Haversine formula for accurate distance calculation:
        a = sin²(Δφ/2) + cos φ1 ⋅ cos φ2 ⋅ sin²(Δλ/2)
        c = 2 ⋅ atan2(√a, √(1−a))
        d = R ⋅ c
        
        Args:
            lat1: Latitude of first point (degrees)
            lon1: Longitude of first point (degrees)
            lat2: Latitude of second point (degrees)
            lon2: Longitude of second point (degrees)
        
        Returns:
            float: Distance in meters
            
        Example:
            >>> # Distance from Mumbai to Delhi (approximate)
            >>> dist = GeoEngine.haversine_distance(19.08, 72.88, 28.61, 77.23)
            >>> dist
            1401819.5...  # ~1401 km
        """
        # Convert degrees to radians
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)
        
        # Differences
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        
        # Haversine formula
        a = (math.sin(dlat / 2) ** 2 +
             math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2)
        
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = EARTH_RADIUS_METERS * c
        
        return distance
    
    def calculate_geo_impact(
        self,
        incident_lat: float,
        incident_lon: float,
        target_lat: float,
        target_lon: float,
        decay_model: str = "linear"
    ) -> float:
        """
        Calculate geographic impact of incident on target location.
        
        Args:
            incident_lat: Latitude of incident
            incident_lon: Longitude of incident
            target_lat: Latitude of target location
            target_lon: Longitude of target location
            decay_model: How to decay impact with distance
                        - "linear": linear decay
                        - "exponential": exponential decay
                        - "threshold": step-based thresholds
        
        Returns:
            float: Geographic impact factor between 0 and 1
            
        Example:
            >>> engine = GeoEngine()
            >>> # Incident 100m away
            >>> impact = engine.calculate_geo_impact(21.25, 81.62, 21.2502, 81.6202)
            >>> impact
            0.7  # high impact for nearby location
        """
        # Calculate distance
        distance = self.haversine_distance(
            incident_lat, incident_lon,
            target_lat, target_lon
        )
        
        if decay_model == "threshold":
            return self._threshold_decay(distance)
        elif decay_model == "linear":
            return self._linear_decay(distance)
        elif decay_model == "exponential":
            return self._exponential_decay(distance)
        else:
            raise ValueError(
                f"Unknown decay model '{decay_model}'. "
                f"Valid models: linear, exponential, threshold"
            )
    
    def _threshold_decay(self, distance: float) -> float:
        """
        Step-based geographic impact decay.
        
        Uses distance thresholds to classify impact into discrete levels.
        
        Args:
            distance: Distance in meters
        
        Returns:
            float: Impact factor (0 to 1)
        """
        # Define impact levels for each threshold category
        impact_levels = {
            "very_high": 1.0,
            "high": 0.7,
            "medium": 0.4,
            "low": 0.1,
            "negligible": 0.0,
        }
        
        # Find which threshold this distance falls into
        for category in ["very_high", "high", "medium", "low", "negligible"]:
            if category in self.impact_thresholds:
                min_dist, max_dist = self.impact_thresholds[category]
                if min_dist <= distance < max_dist:
                    impact = impact_levels.get(category, 0.0)
                    self.logger.debug(
                        f"Threshold decay: distance={distance}m, "
                        f"category={category}, impact={impact}"
                    )
                    return clip_probability(impact)
        
        return 0.0
    
    def _linear_decay(self, distance: float, max_range: float = 1000.0) -> float:
        """
        Linear distance-based impact decay.
        
        impact = max(0, 1 - distance / max_range)
        
        Args:
            distance: Distance in meters
            max_range: Distance at which impact becomes 0 (default 1000m)
        
        Returns:
            float: Impact factor (0 to 1)
        """
        if distance >= max_range:
            return 0.0
        
        impact = 1.0 - (distance / max_range)
        self.logger.debug(
            f"Linear decay: distance={distance}m, max_range={max_range}m, "
            f"impact={impact:.4f}"
        )
        return clip_probability(impact)
    
    def _exponential_decay(
        self,
        distance: float,
        half_distance: float = 200.0
    ) -> float:
        """
        Exponential distance-based impact decay.
        
        impact = exp(-λ * distance) where λ chosen based on half_distance
        
        Args:
            distance: Distance in meters
            half_distance: Distance at which impact is 0.5 (default 200m)
        
        Returns:
            float: Impact factor (0 to 1)
        """
        # Calculate decay constant: λ = ln(2) / half_distance
        lambda_decay = math.log(2) / half_distance
        
        impact = math.exp(-lambda_decay * distance)
        self.logger.debug(
            f"Exponential decay: distance={distance}m, "
            f"half_distance={half_distance}m, impact={impact:.4f}"
        )
        return clip_probability(impact)
    
    def classify_geo_relevance(
        self,
        incident_lat: float,
        incident_lon: float,
        target_lat: float,
        target_lon: float
    ) -> str:
        """
        Classify geographic relevance of incident to target.
        
        Args:
            incident_lat: Latitude of incident
            incident_lon: Longitude of incident
            target_lat: Latitude of target
            target_lon: Longitude of target
        
        Returns:
            str: Relevance category (Immediate, Nearby, Adjacent, Distant)
        """
        distance = self.haversine_distance(
            incident_lat, incident_lon,
            target_lat, target_lon
        )
        
        if distance < 50:
            return "Immediate"
        elif distance < 200:
            return "Nearby"
        elif distance < 500:
            return "Adjacent"
        elif distance < 1000:
            return "Close"
        else:
            return "Distant"
    
    def get_nearby_incidents(
        self,
        incidents: list,
        center_lat: float,
        center_lon: float,
        radius_meters: float = 500.0
    ) -> list:
        """
        Filter incidents within geographic radius.
        
        Args:
            incidents: List of incident dicts with lat/lon
            center_lat: Center latitude
            center_lon: Center longitude
            radius_meters: Search radius in meters (default 500m)
        
        Returns:
            list: Incidents within radius, sorted by distance
        """
        nearby = []
        
        for incident in incidents:
            distance = self.haversine_distance(
                incident.get("latitude"),
                incident.get("longitude"),
                center_lat,
                center_lon
            )
            
            if distance <= radius_meters:
                nearby.append({
                    "incident": incident,
                    "distance": distance,
                })
        
        # Sort by distance
        nearby.sort(key=lambda x: x["distance"])
        
        return nearby
    
    def update_threshold(
        self,
        category: str,
        min_distance: float,
        max_distance: float
    ) -> None:
        """
        Update distance threshold for impact category.
        
        Args:
            category: Impact category name
            min_distance: Minimum distance for category (meters)
            max_distance: Maximum distance for category (meters)
            
        Raises:
            ValueError: If thresholds invalid
        """
        if min_distance < 0 or max_distance < 0:
            raise ValueError("Distances must be non-negative")
        if min_distance > max_distance and max_distance != float('inf'):
            raise ValueError("min_distance cannot exceed max_distance")
        
        old_threshold = self.impact_thresholds.get(category)
        self.impact_thresholds[category] = (min_distance, max_distance)
        
        self.logger.info(
            f"Updated threshold for '{category}': "
            f"{old_threshold} → ({min_distance}, {max_distance})"
        )
    
    def get_statistics(self) -> Dict:
        """
        Get geographic engine statistics.
        
        Returns:
            Dict: Configuration and threshold statistics
        """
        return {
            "earth_radius_meters": EARTH_RADIUS_METERS,
            "impact_categories": len(self.impact_thresholds),
            "thresholds": {
                k: {"min": v[0], "max": v[1]}
                for k, v in self.impact_thresholds.items()
            },
        }
