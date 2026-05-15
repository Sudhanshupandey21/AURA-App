"""
Severity Modeling Engine

Handles:
- Incident type to severity mapping
- Custom severity overrides
- Severity aggregation
- Severity validation
"""

import logging
from typing import Dict, Optional, List
from enum import Enum

from aura_risk_engine.incident_intelligence.utils import clip_probability, INCIDENT_TYPES, SEVERITY_MIN, SEVERITY_MAX

logger = logging.getLogger(__name__)


class IncidentTypeEnum(str, Enum):
    """Enumeration of supported incident types."""
    SUSPICIOUS_ACTIVITY = "suspicious_activity"
    HARASSMENT = "harassment"
    THEFT = "theft"
    ASSAULT = "assault"
    VIOLENCE = "violence"


class SeverityEngine:
    """
    Severity modeling for incidents.
    
    Responsibilities:
    - Map incident types to base severity scores
    - Handle custom severity overrides
    - Aggregate multiple incident severities
    - Validate severity values
    
    Severity Scale:
    - 0.0-0.3: Low severity (suspicious_activity)
    - 0.3-0.6: Medium severity (harassment)
    - 0.6-0.8: High severity (theft, assault)
    - 0.8-1.0: Critical severity (violence)
    """
    
    def __init__(self, custom_severity_map: Dict[str, float] = None):
        """
        Initialize severity engine.
        
        Args:
            custom_severity_map: Optional custom mapping of incident types to severity.
                               If not provided, uses default INCIDENT_TYPES mapping.
        """
        self.severity_map = custom_severity_map or INCIDENT_TYPES.copy()
        self.logger = logger
        self._validate_severity_map()
    
    def _validate_severity_map(self):
        """Validate all severity values are in valid range."""
        for incident_type, severity in self.severity_map.items():
            if not (SEVERITY_MIN <= severity <= SEVERITY_MAX):
                raise ValueError(
                    f"Invalid severity {severity} for type '{incident_type}'. "
                    f"Must be between {SEVERITY_MIN} and {SEVERITY_MAX}"
                )
    
    def get_severity_score(
        self,
        incident_type: str,
        custom_override: Optional[float] = None
    ) -> float:
        """
        Get severity score for an incident type.
        
        Args:
            incident_type: Type of incident (e.g., "harassment", "violence")
            custom_override: Optional custom severity to override default
        
        Returns:
            float: Severity score between 0 and 1
            
        Raises:
            ValueError: If incident_type not found and no override provided
            
        Example:
            >>> engine = SeverityEngine()
            >>> severity = engine.get_severity_score("harassment")
            >>> severity
            0.6
            >>> custom_severity = engine.get_severity_score("unknown", custom_override=0.75)
            >>> custom_severity
            0.75
        """
        # Use custom override if provided
        if custom_override is not None:
            if not (SEVERITY_MIN <= custom_override <= SEVERITY_MAX):
                raise ValueError(
                    f"Custom severity override {custom_override} out of range "
                    f"[{SEVERITY_MIN}, {SEVERITY_MAX}]"
                )
            self.logger.debug(
                f"Using custom severity override {custom_override} "
                f"for incident type '{incident_type}'"
            )
            return custom_override
        
        # Normalize incident type to lowercase
        incident_type_lower = incident_type.lower().strip()
        
        # Look up in severity map
        if incident_type_lower in self.severity_map:
            severity = self.severity_map[incident_type_lower]
            self.logger.debug(
                f"Retrieved severity {severity} for incident type '{incident_type}'"
            )
            return severity
        
        # Unknown incident type
        self.logger.warning(f"Unknown incident type '{incident_type}'")
        raise ValueError(
            f"Unknown incident type '{incident_type}'. "
            f"Valid types: {', '.join(self.severity_map.keys())}"
        )
    
    def update_severity_mapping(
        self,
        incident_type: str,
        severity: float
    ) -> None:
        """
        Update the severity score for an incident type.
        
        Args:
            incident_type: Type of incident
            severity: New severity score between 0 and 1
            
        Raises:
            ValueError: If severity out of range
        """
        if not (SEVERITY_MIN <= severity <= SEVERITY_MAX):
            raise ValueError(
                f"Invalid severity {severity}. "
                f"Must be between {SEVERITY_MIN} and {SEVERITY_MAX}"
            )
        
        incident_type_lower = incident_type.lower().strip()
        old_severity = self.severity_map.get(incident_type_lower)
        self.severity_map[incident_type_lower] = severity
        
        self.logger.info(
            f"Updated severity mapping: '{incident_type}' "
            f"from {old_severity} to {severity}"
        )
    
    def aggregate_severities(
        self,
        severities: List[float],
        aggregation_method: str = "maximum"
    ) -> float:
        """
        Aggregate multiple severity scores.
        
        Args:
            severities: List of severity scores
            aggregation_method: How to combine severities
                              - "maximum": use highest severity
                              - "average": use average severity
                              - "weighted_max": weighted combination
        
        Returns:
            float: Aggregated severity score between 0 and 1
            
        Raises:
            ValueError: If method not recognized or list empty
        """
        if not severities:
            raise ValueError("Cannot aggregate empty severity list")
        
        if aggregation_method == "maximum":
            return max(severities)
        
        elif aggregation_method == "average":
            return sum(severities) / len(severities)
        
        elif aggregation_method == "weighted_max":
            # Weight by position (earlier incidents in list weighted higher)
            total_weight = len(severities) * (len(severities) + 1) / 2
            weighted_sum = sum(
                severity * (len(severities) - i)
                for i, severity in enumerate(severities)
            )
            return weighted_sum / total_weight
        
        else:
            raise ValueError(
                f"Unknown aggregation method '{aggregation_method}'. "
                f"Valid methods: maximum, average, weighted_max"
            )
    
    def classify_severity(self, severity: float) -> str:
        """
        Classify severity into human-readable category.
        
        Args:
            severity: Severity score between 0 and 1
        
        Returns:
            str: Severity category name
        """
        severity = clip_probability(severity)
        
        if severity < 0.3:
            return "Low"
        elif severity < 0.6:
            return "Medium"
        elif severity < 0.8:
            return "High"
        else:
            return "Critical"
    
    def get_severity_description(self, severity: float) -> str:
        """
        Get human-readable description for severity score.
        
        Args:
            severity: Severity score between 0 and 1
        
        Returns:
            str: Detailed description
        """
        severity = clip_probability(severity)
        category = self.classify_severity(severity)
        
        descriptions = {
            "Low": "Minor incident with low impact on safety",
            "Medium": "Moderate incident requiring attention",
            "High": "Serious incident with significant safety impact",
            "Critical": "Critical incident requiring immediate response",
        }
        
        return descriptions.get(category, "Unknown severity")
    
    def get_all_incident_types(self) -> List[str]:
        """
        Get list of all supported incident types.
        
        Returns:
            List[str]: Sorted list of incident types
        """
        return sorted(self.severity_map.keys())
    
    def get_severity_statistics(self) -> Dict[str, float]:
        """
        Get statistics about severity mappings.
        
        Returns:
            Dict: Statistics including min, max, average severity
        """
        severities = list(self.severity_map.values())
        
        return {
            "min_severity": min(severities),
            "max_severity": max(severities),
            "average_severity": sum(severities) / len(severities),
            "count": len(self.severity_map),
        }
