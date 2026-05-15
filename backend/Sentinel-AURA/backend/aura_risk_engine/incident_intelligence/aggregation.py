"""
Real-Time Incident Aggregation Module

Handles:
- Aggregating multiple active incidents
- Dynamic risk updates
- Incident clustering by geographic proximity
- Real-time incident stream processing
"""

import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from collections import defaultdict
from datetime import datetime, timezone

from aura_risk_engine.incident_intelligence.risk_engine import RiskEngine
from aura_risk_engine.incident_intelligence.geo_engine import GeoEngine
from aura_risk_engine.incident_intelligence.decay_engine import TimeDecayEngine
from aura_risk_engine.incident_intelligence.utils import get_current_timestamp, clip_probability

logger = logging.getLogger(__name__)


@dataclass
class AggregatedIncidentInfo:
    """Information about aggregated incidents in a region."""
    region_id: str
    center_lat: float
    center_lon: float
    active_incidents: int
    aggregated_risk: float
    dominant_incident_type: str
    incident_types: Dict[str, int] = field(default_factory=dict)
    geographic_spread_meters: float = 0.0
    oldest_incident_age_minutes: float = 0.0
    newest_incident_age_minutes: float = 0.0
    incidents: List[Dict[str, Any]] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "region_id": self.region_id,
            "center_lat": self.center_lat,
            "center_lon": self.center_lon,
            "active_incidents": self.active_incidents,
            "aggregated_risk": self.aggregated_risk,
            "dominant_incident_type": self.dominant_incident_type,
            "incident_types": self.incident_types,
            "geographic_spread_meters": self.geographic_spread_meters,
            "oldest_incident_age_minutes": self.oldest_incident_age_minutes,
            "newest_incident_age_minutes": self.newest_incident_age_minutes,
        }


class IncidentAggregator:
    """
    Real-time incident aggregation engine.
    
    Aggregates multiple nearby incidents to:
    - Identify incident clusters
    - Calculate combined risk exposure
    - Detect patterns and trends
    - Support real-time updates
    
    Responsibilities:
    - Track active incidents in memory
    - Cluster incidents by geographic proximity
    - Calculate aggregated metrics
    - Provide real-time risk updates
    - Clean up stale incidents
    """
    
    def __init__(
        self,
        risk_engine: RiskEngine = None,
        geo_engine: GeoEngine = None,
        decay_engine: TimeDecayEngine = None,
        cluster_radius_meters: float = 500.0,
        max_incident_age_minutes: float = 480.0  # 8 hours
    ):
        """
        Initialize incident aggregator.
        
        Args:
            risk_engine: RiskEngine instance
            geo_engine: GeoEngine instance
            decay_engine: TimeDecayEngine instance
            cluster_radius_meters: Geographic radius for clustering (default 500m)
            max_incident_age_minutes: Remove incidents older than this (default 8 hours)
        """
        self.risk_engine = risk_engine or RiskEngine()
        self.geo_engine = geo_engine or GeoEngine()
        self.decay_engine = decay_engine or TimeDecayEngine()
        
        self.cluster_radius_meters = cluster_radius_meters
        self.max_incident_age_minutes = max_incident_age_minutes
        
        # Active incidents storage: {incident_id: incident_data}
        self.active_incidents: Dict[str, Dict[str, Any]] = {}
        
        # Regional clusters: {region_id: list of incident_ids}
        self.region_incidents: Dict[str, List[str]] = defaultdict(list)
        
        self.logger = logger
        self._aggregation_count = 0
    
    def add_incident(
        self,
        incident: Dict[str, Any],
        incident_id: str = None
    ) -> str:
        """
        Add a new incident to active tracking.
        
        Args:
            incident: Incident data with type, timestamp, latitude, longitude
            incident_id: Optional ID for incident (auto-generated if None)
        
        Returns:
            str: Incident ID
        """
        if incident_id is None:
            incident_id = f"incident_{len(self.active_incidents)}_{get_current_timestamp()}"
        
        self.active_incidents[incident_id] = incident
        
        self.logger.info(
            f"Added incident {incident_id}: "
            f"type={incident.get('type')}, "
            f"location=({incident.get('latitude')}, {incident.get('longitude')})"
        )
        
        return incident_id
    
    def remove_incident(self, incident_id: str) -> bool:
        """
        Remove incident from active tracking.
        
        Args:
            incident_id: ID of incident to remove
        
        Returns:
            bool: True if removed, False if not found
        """
        if incident_id in self.active_incidents:
            del self.active_incidents[incident_id]
            
            # Remove from region tracking
            for region_id in list(self.region_incidents.keys()):
                if incident_id in self.region_incidents[region_id]:
                    self.region_incidents[region_id].remove(incident_id)
            
            self.logger.info(f"Removed incident {incident_id}")
            return True
        
        return False
    
    def cleanup_stale_incidents(self, current_time: float = None) -> int:
        """
        Remove incidents older than max_incident_age_minutes.
        
        Args:
            current_time: Current timestamp (defaults to now)
        
        Returns:
            int: Number of incidents removed
        """
        if current_time is None:
            current_time = get_current_timestamp()
        
        removed_count = 0
        incident_ids_to_remove = []
        
        for incident_id, incident in self.active_incidents.items():
            age_minutes = (current_time - incident.get("timestamp", current_time)) / 60.0
            
            if age_minutes > self.max_incident_age_minutes:
                incident_ids_to_remove.append(incident_id)
        
        for incident_id in incident_ids_to_remove:
            self.remove_incident(incident_id)
            removed_count += 1
        
        if removed_count > 0:
            self.logger.info(f"Cleaned up {removed_count} stale incidents")
        
        return removed_count
    
    def get_incident(self, incident_id: str) -> Optional[Dict[str, Any]]:
        """
        Get incident by ID.
        
        Args:
            incident_id: ID of incident
        
        Returns:
            Dict: Incident data or None if not found
        """
        return self.active_incidents.get(incident_id)
    
    def aggregate_incidents(
        self,
        target_lat: float,
        target_lon: float,
        current_time: float = None
    ) -> Dict[str, Any]:
        """
        Aggregate all active incidents and calculate combined risk at target location.
        
        Args:
            target_lat: Target latitude for risk assessment
            target_lon: Target longitude for risk assessment
            current_time: Current timestamp (defaults to now)
        
        Returns:
            Dict with aggregated information:
                - active_incidents: Count of active incidents
                - aggregated_risk: Combined risk score
                - dominant_incident: Most severe active incident type
                - reason: Human-readable explanation
                - nearby_incidents: Incidents within cluster radius
                
        Example:
            >>> aggregator = IncidentAggregator()
            >>> aggregator.add_incident({...})
            >>> result = aggregator.aggregate_incidents(21.25, 81.62)
            >>> result["aggregated_risk"]
            0.82
        """
        if current_time is None:
            current_time = get_current_timestamp()
        
        # Clean up stale incidents first
        self.cleanup_stale_incidents(current_time)
        
        if not self.active_incidents:
            return {
                "active_incidents": 0,
                "aggregated_risk": 0.0,
                "dominant_incident": None,
                "reason": "No active incidents",
                "nearby_incidents": [],
            }
        
        # Calculate risk for each incident at target location
        incident_risks = []
        nearby_incidents = []
        dominant_incident_type = None
        max_severity = 0.0
        
        for incident_id, incident in self.active_incidents.items():
            # Calculate risk at target location
            risk_result = self.risk_engine.calculate_incident_risk(
                incident_type=incident.get("type"),
                timestamp=incident.get("timestamp"),
                incident_lat=incident.get("latitude"),
                incident_lon=incident.get("longitude"),
                target_lat=target_lat,
                target_lon=target_lon,
                custom_severity=incident.get("custom_severity_override"),
                current_time=current_time,
                include_components=True
            )
            
            incident_risks.append(risk_result["risk"])
            
            # Track nearby incidents
            if risk_result["distance_meters"] <= self.cluster_radius_meters:
                nearby_incidents.append({
                    "id": incident_id,
                    "type": incident.get("type"),
                    "risk": risk_result["risk"],
                    "distance_meters": risk_result["distance_meters"],
                    "severity": risk_result.get("severity", 0.0),
                    "decay": risk_result.get("decay", 0.0),
                })
            
            # Track dominant incident
            if risk_result.get("severity", 0.0) > max_severity:
                max_severity = risk_result.get("severity", 0.0)
                dominant_incident_type = incident.get("type")
        
        # Sort nearby incidents by risk
        nearby_incidents.sort(key=lambda x: x["risk"], reverse=True)
        
        # Aggregate risks
        aggregated_risk = self.risk_engine.aggregate_incident_risks(
            incident_risks,
            aggregation_method="quadratic"
        )
        aggregated_risk = clip_probability(aggregated_risk)
        
        self._aggregation_count += 1
        
        # Generate explanation
        reason = self._generate_aggregation_reason(
            len(self.active_incidents),
            len(nearby_incidents),
            aggregated_risk,
            dominant_incident_type
        )
        
        result = {
            "active_incidents": len(self.active_incidents),
            "nearby_incidents_count": len(nearby_incidents),
            "aggregated_risk": aggregated_risk,
            "dominant_incident_type": dominant_incident_type,
            "dominant_incident_severity": max_severity,
            "reason": reason,
            "nearby_incidents": nearby_incidents,
            "incident_distribution": self._get_incident_distribution(),
        }
        
        self.logger.debug(
            f"Aggregation: {len(self.active_incidents)} active incidents, "
            f"{len(nearby_incidents)} nearby, risk={aggregated_risk:.3f}"
        )
        
        return result
    
    def get_regional_aggregate(
        self,
        region_id: str,
        region_lat: float,
        region_lon: float,
        current_time: float = None
    ) -> AggregatedIncidentInfo:
        """
        Get aggregated incident information for a specific region.
        
        Args:
            region_id: Identifier for the region
            region_lat: Center latitude of region
            region_lon: Center longitude of region
            current_time: Current timestamp
        
        Returns:
            AggregatedIncidentInfo: Aggregated information for region
        """
        if current_time is None:
            current_time = get_current_timestamp()
        
        # Find incidents in region
        nearby = self.geo_engine.get_nearby_incidents(
            [
                {**incident, "incident_id": iid}
                for iid, incident in self.active_incidents.items()
            ],
            region_lat,
            region_lon,
            self.cluster_radius_meters
        )
        
        if not nearby:
            return AggregatedIncidentInfo(
                region_id=region_id,
                center_lat=region_lat,
                center_lon=region_lon,
                active_incidents=0,
                aggregated_risk=0.0,
                dominant_incident_type="none",
            )
        
        # Collect statistics
        incident_types = defaultdict(int)
        risks = []
        ages = []
        
        for item in nearby:
            incident = item["incident"]
            distance = item["distance"]
            
            risk_result = self.risk_engine.calculate_incident_risk(
                incident_type=incident.get("type"),
                timestamp=incident.get("timestamp"),
                incident_lat=incident.get("latitude"),
                incident_lon=incident.get("longitude"),
                target_lat=region_lat,
                target_lon=region_lon,
                current_time=current_time,
            )
            
            incident_types[incident.get("type")] += 1
            risks.append(risk_result["risk"])
            
            age_minutes = (current_time - incident.get("timestamp", current_time)) / 60.0
            ages.append(age_minutes)
        
        aggregated_risk = self.risk_engine.aggregate_incident_risks(
            risks,
            aggregation_method="quadratic"
        )
        
        # Find dominant incident type
        dominant_type = max(incident_types.items(), key=lambda x: x[1])[0]
        
        # Calculate geographic spread
        max_distance = max(
            self.geo_engine.haversine_distance(
                item["incident"].get("latitude"),
                item["incident"].get("longitude"),
                region_lat,
                region_lon
            )
            for item in nearby
        ) if nearby else 0.0
        
        return AggregatedIncidentInfo(
            region_id=region_id,
            center_lat=region_lat,
            center_lon=region_lon,
            active_incidents=len(nearby),
            aggregated_risk=clip_probability(aggregated_risk),
            dominant_incident_type=dominant_type,
            incident_types=dict(incident_types),
            geographic_spread_meters=max_distance,
            oldest_incident_age_minutes=max(ages) if ages else 0.0,
            newest_incident_age_minutes=min(ages) if ages else 0.0,
            incidents=[item["incident"] for item in nearby],
        )
    
    def _generate_aggregation_reason(
        self,
        total_incidents: int,
        nearby_count: int,
        risk_level: float,
        dominant_type: Optional[str]
    ) -> str:
        """
        Generate human-readable explanation for aggregated result.
        
        Args:
            total_incidents: Total active incidents
            nearby_count: Incidents nearby
            risk_level: Aggregated risk score
            dominant_type: Most prevalent incident type
        
        Returns:
            str: Human-readable reason
        """
        if total_incidents == 0:
            return "No active incidents in system"
        
        parts = []
        
        if nearby_count > 0:
            parts.append(f"{nearby_count} incident(s) nearby")
        else:
            parts.append(f"{total_incidents} incident(s) in area")
        
        if dominant_type:
            parts.append(f"dominated by {dominant_type}")
        
        if risk_level >= 0.8:
            parts.append("critical risk level")
        elif risk_level >= 0.6:
            parts.append("high risk level")
        elif risk_level >= 0.4:
            parts.append("moderate risk level")
        
        return ", ".join(parts) if parts else "Incidents aggregated"
    
    def _get_incident_distribution(self) -> Dict[str, int]:
        """
        Get distribution of incidents by type.
        
        Returns:
            Dict: Counts by incident type
        """
        distribution = defaultdict(int)
        for incident in self.active_incidents.values():
            incident_type = incident.get("type", "unknown")
            distribution[incident_type] += 1
        return dict(distribution)
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get aggregator statistics.
        
        Returns:
            Dict: Statistics about active tracking
        """
        return {
            "active_incidents": len(self.active_incidents),
            "total_aggregations": self._aggregation_count,
            "cluster_radius_meters": self.cluster_radius_meters,
            "max_incident_age_minutes": self.max_incident_age_minutes,
            "incident_distribution": self._get_incident_distribution(),
        }
    
    def reset(self):
        """Reset aggregator and clear all incidents."""
        self.active_incidents.clear()
        self.region_incidents.clear()
        self._aggregation_count = 0
        self.logger.info("Incident aggregator reset")
