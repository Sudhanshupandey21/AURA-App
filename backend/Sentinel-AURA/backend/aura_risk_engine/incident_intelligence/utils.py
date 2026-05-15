"""
Utility functions and constants for the Incident Intelligence Module.

Provides:
- Constants and configuration
- Validation helpers
- Data transformation utilities
- Logging utilities
"""

import logging
from typing import Dict, List, Tuple, Any
from datetime import datetime, timezone
import math

# Configure logging
logger = logging.getLogger(__name__)

# ==================== CONSTANTS ====================

# Incident Types
INCIDENT_TYPES = {
    "suspicious_activity": 0.3,
    "harassment": 0.6,
    "theft": 0.7,
    "assault": 0.85,
    "violence": 1.0,
}

# Geographic Impact Radius Configuration (in meters)
GEO_IMPACT_THRESHOLDS = {
    "very_high": (0, 50),        # 0-50m: very high impact (1.0)
    "high": (50, 200),            # 50-200m: high impact (0.7)
    "medium": (200, 500),         # 200-500m: medium impact (0.4)
    "low": (500, 1000),           # 500m-1km: low impact (0.1)
    "negligible": (1000, float('inf'))  # 1km+: negligible (0)
}

# Time Decay Configuration
TIME_DECAY_LAMBDA = 1.0 / 60  # Decay factor per minute
TIME_DECAY_HALF_LIFE_MINUTES = 60  # Half-life of incident relevance

# Validation Constraints
SEVERITY_MIN = 0.0
SEVERITY_MAX = 1.0

LATITUDE_MIN = -90.0
LATITUDE_MAX = 90.0

LONGITUDE_MIN = -180.0
LONGITUDE_MAX = 180.0

# Incident data must be within this many seconds of current time
MAX_INCIDENT_AGE_SECONDS = 86400 * 7  # 7 days

# ==================== VALIDATION FUNCTIONS ====================

def validate_severity(severity: float) -> bool:
    """
    Validate incident severity is within acceptable range.
    
    Args:
        severity: Severity score between 0 and 1
        
    Returns:
        bool: True if valid, False otherwise
    """
    return SEVERITY_MIN <= severity <= SEVERITY_MAX


def validate_coordinates(latitude: float, longitude: float) -> bool:
    """
    Validate geographic coordinates are within valid ranges.
    
    Args:
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        
    Returns:
        bool: True if coordinates are valid, False otherwise
    """
    return (LATITUDE_MIN <= latitude <= LATITUDE_MAX and 
            LONGITUDE_MIN <= longitude <= LONGITUDE_MAX)


def validate_timestamp(timestamp: float, current_time: float = None) -> bool:
    """
    Validate timestamp is reasonable (not too old, not in future).
    
    Args:
        timestamp: Unix timestamp in seconds
        current_time: Current time (defaults to now)
        
    Returns:
        bool: True if timestamp is valid, False otherwise
    """
    if current_time is None:
        current_time = datetime.now(timezone.utc).timestamp()
    
    time_diff = current_time - timestamp
    
    # Reject future timestamps (allow 60 seconds clock skew)
    if time_diff < -60:
        return False
    
    # Reject very old timestamps
    if time_diff > MAX_INCIDENT_AGE_SECONDS:
        return False
    
    return True


def validate_incident_type(incident_type: str) -> bool:
    """
    Validate incident type is in allowed list.
    
    Args:
        incident_type: Type of incident
        
    Returns:
        bool: True if incident type is valid, False otherwise
    """
    return incident_type.lower() in INCIDENT_TYPES


def get_current_timestamp() -> float:
    """
    Get current Unix timestamp in seconds.
    
    Returns:
        float: Current timestamp
    """
    return datetime.now(timezone.utc).timestamp()


def minutes_elapsed(timestamp: float, current_time: float = None) -> float:
    """
    Calculate minutes elapsed since timestamp.
    
    Args:
        timestamp: Unix timestamp in seconds
        current_time: Current time (defaults to now)
        
    Returns:
        float: Minutes elapsed
    """
    if current_time is None:
        current_time = get_current_timestamp()
    
    return (current_time - timestamp) / 60.0


def normalize_value(value: float, min_val: float = 0.0, max_val: float = 1.0) -> float:
    """
    Normalize a value to a range.
    
    Args:
        value: Value to normalize
        min_val: Minimum of output range
        max_val: Maximum of output range
        
    Returns:
        float: Normalized value clamped to [min_val, max_val]
    """
    return max(min_val, min(max_val, value))


def clip_probability(value: float) -> float:
    """
    Clip value to probability range [0, 1].
    
    Args:
        value: Value to clip
        
    Returns:
        float: Clipped value between 0 and 1
    """
    return normalize_value(value, 0.0, 1.0)


# ==================== DATA TRANSFORMATION ====================

def incident_to_dict(incident: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert incident object to standardized dictionary format.
    
    Args:
        incident: Incident data
        
    Returns:
        dict: Standardized incident dictionary
    """
    return {
        "type": incident.get("type", "unknown").lower(),
        "severity": incident.get("severity"),
        "timestamp": incident.get("timestamp"),
        "latitude": incident.get("latitude"),
        "longitude": incident.get("longitude"),
        "custom_severity_override": incident.get("custom_severity_override"),
        "description": incident.get("description", ""),
        "source": incident.get("source", "unknown"),
    }


# ==================== LOGGING UTILITIES ====================

def log_incident_validation(incident_id: str, is_valid: bool, errors: List[str] = None):
    """
    Log incident validation results.
    
    Args:
        incident_id: Identifier for the incident
        is_valid: Whether incident passed validation
        errors: List of validation errors (if any)
    """
    if is_valid:
        logger.info(f"Incident {incident_id} passed validation")
    else:
        error_msg = ", ".join(errors) if errors else "Unknown errors"
        logger.warning(f"Incident {incident_id} validation failed: {error_msg}")


def log_risk_calculation(incident_id: str, risk_score: float, components: Dict[str, float]):
    """
    Log incident risk calculation details.
    
    Args:
        incident_id: Identifier for the incident
        risk_score: Calculated risk score
        components: Component scores (severity, decay, geo_impact)
    """
    logger.debug(
        f"Risk calculation for {incident_id}: score={risk_score:.4f}, "
        f"components={components}"
    )
