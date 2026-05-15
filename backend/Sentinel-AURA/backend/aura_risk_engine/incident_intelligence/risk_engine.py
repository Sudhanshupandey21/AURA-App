"""
Incident Risk Calculation Engine

Handles:
- Risk scoring by combining severity, decay, and geographic impact
- Risk normalization and validation
- Risk aggregation
- Risk statistics and trending
"""

import logging
from typing import Dict, Any, Optional, List

from aura_risk_engine.incident_intelligence.severity_engine import SeverityEngine
from aura_risk_engine.incident_intelligence.decay_engine import TimeDecayEngine
from aura_risk_engine.incident_intelligence.geo_engine import GeoEngine
from aura_risk_engine.incident_intelligence.utils import clip_probability, get_current_timestamp

logger = logging.getLogger(__name__)


class RiskEngine:
    """
    Integrated risk calculation engine for incidents.
    
    Combines multiple risk factors:
    - Severity: Base threat level from incident type
    - Temporal Decay: How time reduces incident relevance
    - Geographic Impact: How distance affects other locations
    
    Risk Calculation Formula:
    
    incident_risk = severity * time_decay * geo_impact
    
    where all factors are normalized to [0, 1]
    
    Responsibilities:
    - Calculate integrated risk scores
    - Validate risk components
    - Aggregate risks from multiple incidents
    - Provide risk statistics and trends
    """
    
    def __init__(
        self,
        severity_engine: SeverityEngine = None,
        decay_engine: TimeDecayEngine = None,
        geo_engine: GeoEngine = None
    ):
        """
        Initialize risk engine with component engines.
        
        Args:
            severity_engine: SeverityEngine instance (creates default if None)
            decay_engine: TimeDecayEngine instance (creates default if None)
            geo_engine: GeoEngine instance (creates default if None)
        """
        self.severity_engine = severity_engine or SeverityEngine()
        self.decay_engine = decay_engine or TimeDecayEngine()
        self.geo_engine = geo_engine or GeoEngine()
        self.logger = logger
        
        self._risk_calculations_count = 0
        self._risk_cache = {}
    
    def calculate_incident_risk(
        self,
        incident_type: str,
        timestamp: float,
        incident_lat: float,
        incident_lon: float,
        target_lat: float,
        target_lon: float,
        custom_severity: Optional[float] = None,
        current_time: float = None,
        decay_model: str = "threshold",
        geo_model: str = "threshold",
        include_components: bool = False
    ) -> Dict[str, Any]:
        """
        Calculate integrated incident risk for a target location.
        
        Combines:
        1. Severity score (based on incident type)
        2. Time decay (based on incident age)
        3. Geographic impact (based on distance)
        
        Args:
            incident_type: Type of incident
            timestamp: Unix timestamp of incident
            incident_lat: Latitude of incident location
            incident_lon: Longitude of incident location
            target_lat: Latitude of target location to assess risk for
            target_lon: Longitude of target location
            custom_severity: Optional custom severity override
            current_time: Current timestamp (defaults to now)
            decay_model: Decay model for time ("threshold", "exponential")
            geo_model: Decay model for geography ("threshold", "linear", "exponential")
            include_components: If True, include component scores in output
        
        Returns:
            Dict with keys:
                - "risk": Overall incident risk (0 to 1)
                - "severity": Severity component
                - "decay": Time decay component
                - "geo_impact": Geographic impact component
                - "distance_meters": Distance to incident
                - "incident_type": Type of incident
                
        Example:
            >>> engine = RiskEngine()
            >>> result = engine.calculate_incident_risk(
            ...     incident_type="assault",
            ...     timestamp=1715154600,
            ...     incident_lat=21.25,
            ...     incident_lon=81.62,
            ...     target_lat=21.26,
            ...     target_lon=81.63
            ... )
            >>> result["risk"]
            0.595  # 59.5% risk impact
        """
        if current_time is None:
            current_time = get_current_timestamp()
        
        # Get severity component
        try:
            severity = self.severity_engine.get_severity_score(
                incident_type,
                custom_override=custom_severity
            )
        except ValueError as e:
            self.logger.error(f"Severity calculation failed: {e}")
            raise
        
        # Get time decay component
        decay = self.decay_engine.decay_incident(timestamp, current_time)
        
        # Get geographic impact component
        geo_impact = self.geo_engine.calculate_geo_impact(
            incident_lat, incident_lon,
            target_lat, target_lon,
            decay_model=geo_model
        )
        
        # Calculate integrated risk
        integrated_risk = severity * decay * geo_impact
        integrated_risk = clip_probability(integrated_risk)
        
        # Calculate distance
        distance = self.geo_engine.haversine_distance(
            incident_lat, incident_lon,
            target_lat, target_lon
        )
        
        self._risk_calculations_count += 1
        
        result = {
            "risk": integrated_risk,
            "distance_meters": distance,
            "incident_type": incident_type,
        }
        
        if include_components:
            result.update({
                "severity": severity,
                "decay": decay,
                "geo_impact": geo_impact,
            })
        
        self.logger.debug(
            f"Risk calculation: type={incident_type}, severity={severity:.3f}, "
            f"decay={decay:.3f}, geo={geo_impact:.3f}, risk={integrated_risk:.3f}"
        )
        
        return result
    
    def calculate_batch_risk(
        self,
        incidents: List[Dict[str, Any]],
        target_lat: float,
        target_lon: float,
        current_time: float = None,
        include_components: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Calculate risk for multiple incidents at target location.
        
        Args:
            incidents: List of incident dictionaries with:
                      - type, timestamp, latitude, longitude
                      - Optional: custom_severity_override
            target_lat: Target latitude
            target_lon: Target longitude
            current_time: Current timestamp
            include_components: Include detailed components
        
        Returns:
            List of risk calculation results, sorted by risk (highest first)
        """
        if current_time is None:
            current_time = get_current_timestamp()
        
        results = []
        
        for incident in incidents:
            try:
                risk_result = self.calculate_incident_risk(
                    incident_type=incident.get("type"),
                    timestamp=incident.get("timestamp"),
                    incident_lat=incident.get("latitude"),
                    incident_lon=incident.get("longitude"),
                    target_lat=target_lat,
                    target_lon=target_lon,
                    custom_severity=incident.get("custom_severity_override"),
                    current_time=current_time,
                    include_components=include_components
                )
                results.append(risk_result)
            except Exception as e:
                self.logger.warning(f"Failed to calculate risk for incident: {e}")
                continue
        
        # Sort by risk (highest first)
        results.sort(key=lambda x: x["risk"], reverse=True)
        
        return results
    
    def aggregate_incident_risks(
        self,
        risk_scores: List[float],
        aggregation_method: str = "maximum"
    ) -> float:
        """
        Aggregate multiple incident risk scores.
        
        Args:
            risk_scores: List of individual risk scores
            aggregation_method: How to combine scores
                              - "maximum": take highest risk
                              - "average": arithmetic mean
                              - "quadratic": sqrt of sum of squares (treats as independent)
                              - "weighted_sum": higher weights for larger values
        
        Returns:
            float: Aggregated risk between 0 and 1
            
        Raises:
            ValueError: If method not recognized
        """
        if not risk_scores:
            return 0.0
        
        if aggregation_method == "maximum":
            return max(risk_scores)
        
        elif aggregation_method == "average":
            return sum(risk_scores) / len(risk_scores)
        
        elif aggregation_method == "quadratic":
            # Root sum of squares (treats incidents as independent)
            sum_of_squares = sum(score ** 2 for score in risk_scores)
            aggregate = (sum_of_squares ** 0.5) / len(risk_scores) ** 0.5
            return clip_probability(aggregate)
        
        elif aggregation_method == "weighted_sum":
            # Weight by position (first = highest weight)
            total_weight = len(risk_scores) * (len(risk_scores) + 1) / 2
            weighted_sum = sum(
                score * (len(risk_scores) - i)
                for i, score in enumerate(risk_scores)
            )
            return weighted_sum / total_weight
        
        else:
            raise ValueError(
                f"Unknown aggregation method '{aggregation_method}'. "
                f"Valid: maximum, average, quadratic, weighted_sum"
            )
    
    def classify_risk_level(self, risk_score: float) -> str:
        """
        Classify risk score into human-readable level.
        
        Args:
            risk_score: Risk score between 0 and 1
        
        Returns:
            str: Risk level category
        """
        risk_score = clip_probability(risk_score)
        
        if risk_score < 0.2:
            return "Minimal"
        elif risk_score < 0.4:
            return "Low"
        elif risk_score < 0.6:
            return "Moderate"
        elif risk_score < 0.8:
            return "High"
        else:
            return "Critical"
    
    def get_risk_factors(
        self,
        incident_type: str,
        current_time: float = None
    ) -> Dict[str, Any]:
        """
        Get risk factor information for an incident type.
        
        Args:
            incident_type: Type of incident
            current_time: Current time (for decay examples)
        
        Returns:
            Dict: Risk factor information
        """
        if current_time is None:
            current_time = get_current_timestamp()
        
        try:
            base_severity = self.severity_engine.get_severity_score(incident_type)
        except ValueError:
            base_severity = None
        
        decay_stats = self.decay_engine.get_statistics()
        geo_stats = self.geo_engine.get_statistics()
        
        return {
            "incident_type": incident_type,
            "base_severity": base_severity,
            "severity_classification": (
                self.severity_engine.classify_severity(base_severity)
                if base_severity else None
            ),
            "decay_half_life_minutes": decay_stats["half_life_minutes"],
            "geo_thresholds": geo_stats["thresholds"],
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get risk engine statistics.
        
        Returns:
            Dict: Statistics and configuration info
        """
        severity_stats = self.severity_engine.get_severity_statistics()
        decay_stats = self.decay_engine.get_statistics()
        
        return {
            "total_calculations": self._risk_calculations_count,
            "severity_stats": severity_stats,
            "decay_stats": decay_stats,
            "incident_types_supported": len(
                self.severity_engine.get_all_incident_types()
            ),
        }
    
    def reset_statistics(self):
        """Reset engine statistics."""
        self._risk_calculations_count = 0
        self._risk_cache.clear()
        self.logger.info("Risk engine statistics reset")
