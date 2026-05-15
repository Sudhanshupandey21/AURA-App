"""
Explainability Engine

Handles:
- Generating human-readable explanations for incidents
- Risk factor articulation
- Impact analysis
- Transparency and auditability
"""

import logging
from typing import Dict, List, Any, Optional

from aura_risk_engine.incident_intelligence.severity_engine import SeverityEngine
from aura_risk_engine.incident_intelligence.decay_engine import TimeDecayEngine
from aura_risk_engine.incident_intelligence.geo_engine import GeoEngine
from aura_risk_engine.incident_intelligence.utils import minutes_elapsed, get_current_timestamp

logger = logging.getLogger(__name__)


class ExplainabilityEngine:
    """
    Explainability layer for incident intelligence system.
    
    Provides:
    - Human-readable incident explanations
    - Risk factor breakdowns
    - Impact analysis narratives
    - Decision transparency
    
    Responsibilities:
    - Generate incident summaries
    - Explain risk calculations
    - Articulate contributing factors
    - Provide audit trails
    """
    
    def __init__(
        self,
        severity_engine: SeverityEngine = None,
        decay_engine: TimeDecayEngine = None,
        geo_engine: GeoEngine = None
    ):
        """
        Initialize explainability engine.
        
        Args:
            severity_engine: SeverityEngine instance
            decay_engine: TimeDecayEngine instance
            geo_engine: GeoEngine instance
        """
        self.severity_engine = severity_engine or SeverityEngine()
        self.decay_engine = decay_engine or TimeDecayEngine()
        self.geo_engine = geo_engine or GeoEngine()
        self.logger = logger
    
    def explain_incident(
        self,
        incident_type: str,
        timestamp: float,
        latitude: float,
        longitude: float,
        severity: float = None,
        current_time: float = None
    ) -> str:
        """
        Generate natural language explanation for an incident.
        
        Args:
            incident_type: Type of incident
            timestamp: Unix timestamp of incident
            latitude: Latitude of incident
            longitude: Longitude of incident
            severity: Optional severity override
            current_time: Current timestamp
        
        Returns:
            str: Natural language explanation
            
        Example:
            >>> engine = ExplainabilityEngine()
            >>> explanation = engine.explain_incident(
            ...     incident_type="harassment",
            ...     timestamp=1715154600,
            ...     latitude=21.25,
            ...     longitude=81.62
            ... )
            >>> print(explanation)
            "Recent harassment incident at location (21.25, 81.62) - reported 2.5 hours ago"
        """
        if current_time is None:
            current_time = get_current_timestamp()
        
        # Get incident details
        severity_score = severity or self.severity_engine.get_severity_score(incident_type)
        severity_class = self.severity_engine.classify_severity(severity_score)
        
        # Get temporal information
        age_minutes = minutes_elapsed(timestamp, current_time)
        temporal_class = self.decay_engine.classify_temporal_relevance(timestamp, current_time)
        
        # Build explanation
        parts = []
        
        # Time component
        if age_minutes < 5:
            time_str = "Just reported"
        elif age_minutes < 30:
            time_str = f"Reported {int(age_minutes)} minutes ago"
        elif age_minutes < 120:
            hours = int(age_minutes / 60)
            minutes = int(age_minutes % 60)
            time_str = f"Reported {hours} hour{'s' if hours > 1 else ''} ago"
        else:
            hours = int(age_minutes / 60)
            time_str = f"Reported {hours} hours ago"
        
        parts.append(time_str)
        
        # Type and severity component
        parts.append(f"{severity_class} severity {incident_type} incident")
        
        # Location component
        parts.append(f"at location ({latitude:.4f}, {longitude:.4f})")
        
        # Temporal relevance component
        if temporal_class != "Fresh":
            parts.append(f"[{temporal_class} - declining relevance]")
        
        explanation = " - ".join(parts)
        
        return explanation
    
    def explain_risk_components(
        self,
        severity: float,
        decay: float,
        geo_impact: float,
        integrated_risk: float
    ) -> Dict[str, str]:
        """
        Explain individual risk components.
        
        Args:
            severity: Severity component (0-1)
            decay: Time decay component (0-1)
            geo_impact: Geographic impact component (0-1)
            integrated_risk: Final integrated risk (0-1)
        
        Returns:
            Dict with explanations for each component
            
        Example:
            >>> explanations = engine.explain_risk_components(0.85, 0.60, 0.70, 0.36)
            >>> for key, text in explanations.items():
            ...     print(f"{key}: {text}")
            severity: Critical severity (85%) - indicates serious incident
            decay: 60% impact remaining - 1 hour has passed since incident
            geo_impact: High geographic impact (70%) - nearby location
            integrated_risk: Moderate risk (36%) - combined factors create moderate exposure
        """
        
        def percentize(val):
            return int(val * 100)
        
        severity_pct = percentize(severity)
        decay_pct = percentize(decay)
        geo_pct = percentize(geo_impact)
        risk_pct = percentize(integrated_risk)
        
        # Severity explanation
        severity_class = self.severity_engine.classify_severity(severity)
        if severity < 0.3:
            severity_text = f"Minor severity ({severity_pct}%) - low-impact incident"
        elif severity < 0.6:
            severity_text = f"Moderate severity ({severity_pct}%) - concerning incident"
        elif severity < 0.8:
            severity_text = f"High severity ({severity_pct}%) - serious incident"
        else:
            severity_text = f"Critical severity ({severity_pct}%) - indicates serious incident"
        
        # Decay explanation
        if decay > 0.7:
            decay_text = f"Fresh incident ({decay_pct}%) - high immediate relevance"
        elif decay > 0.4:
            decay_text = f"Recent incident ({decay_pct}%) - still relevant"
        elif decay > 0.15:
            decay_text = f"Aging incident ({decay_pct}%) - declining relevance"
        else:
            decay_text = f"Stale incident ({decay_pct}%) - low current relevance"
        
        # Geo impact explanation
        if geo_impact > 0.7:
            geo_text = f"Very high geographic impact ({geo_pct}%) - incident nearby"
        elif geo_impact > 0.4:
            geo_text = f"High geographic impact ({geo_pct}%) - incident in vicinity"
        elif geo_impact > 0.15:
            geo_text = f"Moderate geographic impact ({geo_pct}%) - incident in area"
        else:
            geo_text = f"Low geographic impact ({geo_pct}%) - incident at distance"
        
        # Integrated risk explanation
        if integrated_risk < 0.2:
            risk_text = f"Minimal risk ({risk_pct}%) - combined factors create low exposure"
        elif integrated_risk < 0.4:
            risk_text = f"Low risk ({risk_pct}%) - limited safety concern"
        elif integrated_risk < 0.6:
            risk_text = f"Moderate risk ({risk_pct}%) - should monitor situation"
        elif integrated_risk < 0.8:
            risk_text = f"High risk ({risk_pct}%) - significant safety concern"
        else:
            risk_text = f"Critical risk ({risk_pct}%) - immediate attention required"
        
        return {
            "severity": severity_text,
            "decay": decay_text,
            "geo_impact": geo_text,
            "integrated_risk": risk_text,
        }
    
    def explain_aggregation(
        self,
        active_incidents: int,
        nearby_incidents: int,
        aggregated_risk: float,
        dominant_incident_type: str,
        incident_distribution: Dict[str, int]
    ) -> str:
        """
        Generate explanation for aggregated incident results.
        
        Args:
            active_incidents: Total active incidents
            nearby_incidents: Incidents nearby to target
            aggregated_risk: Aggregated risk score
            dominant_incident_type: Most prevalent type
            incident_distribution: Count by type
        
        Returns:
            str: Natural language explanation
        """
        parts = []
        
        # Incident count
        if active_incidents == 0:
            return "No active incidents in system"
        elif active_incidents == 1:
            parts.append("1 active incident")
        else:
            parts.append(f"{active_incidents} active incidents")
        
        # Nearby vs distant
        if nearby_incidents > 0:
            if nearby_incidents == active_incidents:
                parts.append(f"all nearby")
            else:
                distant = active_incidents - nearby_incidents
                parts.append(f"{nearby_incidents} nearby, {distant} at distance")
        else:
            parts.append("all at distance")
        
        # Incident type distribution
        if len(incident_distribution) == 1:
            incident_type = list(incident_distribution.keys())[0]
            parts.append(f"all {incident_type}")
        else:
            types_str = ", ".join(
                f"{count} {itype}"
                for itype, count in sorted(
                    incident_distribution.items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:3]  # Show top 3
            )
            parts.append(f"types: {types_str}")
        
        # Risk level
        if aggregated_risk < 0.2:
            risk_desc = "minimal aggregated risk"
        elif aggregated_risk < 0.4:
            risk_desc = "low aggregated risk"
        elif aggregated_risk < 0.6:
            risk_desc = "moderate aggregated risk"
        elif aggregated_risk < 0.8:
            risk_desc = "high aggregated risk"
        else:
            risk_desc = "critical aggregated risk"
        
        parts.append(risk_desc)
        
        explanation = " → ".join(parts)
        return explanation
    
    def explain_distance_impact(
        self,
        distance_meters: float,
        impact_factor: float
    ) -> str:
        """
        Explain how distance affects incident impact.
        
        Args:
            distance_meters: Distance in meters
            impact_factor: Geographic impact factor (0-1)
        
        Returns:
            str: Explanation of distance impact
        """
        if distance_meters < 50:
            distance_desc = f"Very close ({distance_meters:.1f}m)"
            impact_desc = "Extremely high impact"
        elif distance_meters < 200:
            distance_desc = f"Close ({distance_meters:.1f}m)"
            impact_desc = "High impact"
        elif distance_meters < 500:
            distance_desc = f"Nearby ({distance_meters:.1f}m / {distance_meters/1000:.1f}km)"
            impact_desc = "Moderate impact"
        elif distance_meters < 1000:
            distance_desc = f"Adjacent ({distance_meters/1000:.2f}km)"
            impact_desc = "Low impact"
        else:
            distance_desc = f"Distant ({distance_meters/1000:.2f}km)"
            impact_desc = "Minimal impact"
        
        impact_pct = int(impact_factor * 100)
        
        return f"{distance_desc} - {impact_desc} ({impact_pct}% factor)"
    
    def explain_temporal_relevance(
        self,
        timestamp: float,
        decay_factor: float,
        current_time: float = None
    ) -> str:
        """
        Explain temporal relevance of incident.
        
        Args:
            timestamp: Incident timestamp
            decay_factor: Time decay factor (0-1)
            current_time: Current timestamp
        
        Returns:
            str: Temporal relevance explanation
        """
        if current_time is None:
            current_time = get_current_timestamp()
        
        age_minutes = minutes_elapsed(timestamp, current_time)
        
        if age_minutes < 5:
            age_desc = "just occurred"
            decay_desc = "Maximum relevance"
        elif age_minutes < 30:
            age_desc = f"occurred {int(age_minutes)} minutes ago"
            decay_desc = "High relevance"
        elif age_minutes < 120:
            hours = int(age_minutes / 60)
            age_desc = f"occurred {hours} hour(s) ago"
            decay_desc = "Moderate relevance"
        elif age_minutes < 480:
            hours = int(age_minutes / 60)
            age_desc = f"occurred {hours} hours ago"
            decay_desc = "Low relevance"
        else:
            days = int(age_minutes / 1440)
            age_desc = f"occurred {days} day(s) ago"
            decay_desc = "Very low relevance"
        
        decay_pct = int(decay_factor * 100)
        
        return f"Incident {age_desc} - {decay_desc} ({decay_pct}% impact remaining)"
    
    def generate_incident_report(
        self,
        incident_data: Dict[str, Any],
        risk_components: Dict[str, float],
        location_context: str = None
    ) -> Dict[str, str]:
        """
        Generate comprehensive incident report with all explanations.
        
        Args:
            incident_data: Incident information
            risk_components: Risk calculation components
            location_context: Optional location description
        
        Returns:
            Dict: Multi-part report with explanations
        """
        report = {
            "incident_summary": self.explain_incident(
                incident_data.get("type"),
                incident_data.get("timestamp"),
                incident_data.get("latitude"),
                incident_data.get("longitude"),
                incident_data.get("severity")
            ),
            "risk_breakdown": self._format_risk_breakdown(risk_components),
            "temporal_analysis": self.explain_temporal_relevance(
                incident_data.get("timestamp"),
                risk_components.get("decay", 0.0)
            ),
            "location_analysis": self.explain_distance_impact(
                risk_components.get("distance_meters", 0.0),
                risk_components.get("geo_impact", 0.0)
            ),
        }
        
        if location_context:
            report["location_context"] = location_context
        
        return report
    
    def _format_risk_breakdown(self, risk_components: Dict[str, float]) -> str:
        """Format risk components as readable breakdown."""
        explanations = self.explain_risk_components(
            risk_components.get("severity", 0.5),
            risk_components.get("decay", 1.0),
            risk_components.get("geo_impact", 1.0),
            risk_components.get("risk", 0.5)
        )
        
        return "\n".join(
            f"  • {label}: {text}"
            for label, text in explanations.items()
        )
