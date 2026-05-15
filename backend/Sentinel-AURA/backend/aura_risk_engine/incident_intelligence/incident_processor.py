"""
Incident Input Processing Module

Handles:
- Incident data validation
- Input normalization
- Data sanitization
- Error handling for malformed incidents
"""

import logging
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timezone

from aura_risk_engine.incident_intelligence.utils import (
    validate_severity,
    validate_coordinates,
    validate_timestamp,
    validate_incident_type,
    get_current_timestamp,
    log_incident_validation,
    incident_to_dict,
    INCIDENT_TYPES,
)

logger = logging.getLogger(__name__)


@dataclass
class ProcessedIncident:
    """Standardized processed incident data."""
    incident_id: str
    incident_type: str
    severity: float
    timestamp: float
    latitude: float
    longitude: float
    custom_severity_override: Optional[float] = None
    description: str = ""
    source: str = "unknown"
    is_valid: bool = True
    validation_errors: List[str] = None
    
    def __post_init__(self):
        """Initialize validation_errors as empty list if None."""
        if self.validation_errors is None:
            self.validation_errors = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "incident_id": self.incident_id,
            "type": self.incident_type,
            "severity": self.severity,
            "timestamp": self.timestamp,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "custom_severity_override": self.custom_severity_override,
            "description": self.description,
            "source": self.source,
            "is_valid": self.is_valid,
            "validation_errors": self.validation_errors,
        }


class IncidentProcessor:
    """
    Processes and validates incident input data.
    
    Responsibilities:
    - Validate incident structure
    - Normalize incident data
    - Sanitize inputs
    - Generate incident IDs
    - Handle validation errors
    """
    
    def __init__(self):
        """Initialize the incident processor."""
        self.processed_count = 0
        self.validation_failed_count = 0
        self.logger = logger
    
    def process_incident(
        self,
        incident: Dict[str, Any],
        incident_id: str = None,
        current_time: float = None
    ) -> ProcessedIncident:
        """
        Process and validate an incident report.
        
        Args:
            incident: Raw incident data dictionary
            incident_id: Optional ID for the incident (auto-generated if None)
            current_time: Current timestamp for validation (defaults to now)
        
        Returns:
            ProcessedIncident: Validated and normalized incident
            
        Example:
            >>> processor = IncidentProcessor()
            >>> incident = {
            ...     "type": "harassment",
            ...     "severity": 0.8,
            ...     "timestamp": 1715154600,
            ...     "latitude": 21.25,
            ...     "longitude": 81.62
            ... }
            >>> result = processor.process_incident(incident)
        """
        if current_time is None:
            current_time = get_current_timestamp()
        
        # Generate incident ID if not provided
        if incident_id is None:
            incident_id = self._generate_incident_id(incident, current_time)
        
        # Normalize incident data
        normalized = incident_to_dict(incident)
        
        # Validate incident
        errors = self._validate_incident(normalized, current_time)
        is_valid = len(errors) == 0
        
        # Create processed incident
        processed = ProcessedIncident(
            incident_id=incident_id,
            incident_type=normalized["type"],
            severity=float(normalized.get("severity", 0.5)),
            timestamp=float(normalized.get("timestamp")),
            latitude=float(normalized.get("latitude")),
            longitude=float(normalized.get("longitude")),
            custom_severity_override=normalized.get("custom_severity_override"),
            description=normalized.get("description", ""),
            source=normalized.get("source", "unknown"),
            is_valid=is_valid,
            validation_errors=errors,
        )
        
        # Update statistics
        self.processed_count += 1
        if not is_valid:
            self.validation_failed_count += 1
        
        # Log validation result
        log_incident_validation(incident_id, is_valid, errors)
        
        return processed
    
    def process_incidents(
        self,
        incidents: List[Dict[str, Any]],
        current_time: float = None
    ) -> List[ProcessedIncident]:
        """
        Process multiple incident reports.
        
        Args:
            incidents: List of incident dictionaries
            current_time: Current timestamp for validation
        
        Returns:
            List[ProcessedIncident]: List of processed incidents
        """
        if current_time is None:
            current_time = get_current_timestamp()
        
        return [
            self.process_incident(incident, current_time=current_time)
            for incident in incidents
        ]
    
    def _validate_incident(
        self,
        incident: Dict[str, Any],
        current_time: float
    ) -> List[str]:
        """
        Validate incident data and collect errors.
        
        Args:
            incident: Normalized incident dictionary
            current_time: Current timestamp for validation
        
        Returns:
            List[str]: List of validation errors (empty if valid)
        """
        errors = []
        
        # Check required fields
        required_fields = ["type", "severity", "timestamp", "latitude", "longitude"]
        for field in required_fields:
            if field not in incident or incident[field] is None:
                errors.append(f"Missing required field: {field}")
        
        if errors:
            return errors
        
        # Validate incident type
        if not validate_incident_type(incident["type"]):
            errors.append(
                f"Invalid incident type '{incident['type']}'. "
                f"Valid types: {', '.join(INCIDENT_TYPES.keys())}"
            )
        
        # Validate severity
        try:
            severity = float(incident["severity"])
            if not validate_severity(severity):
                errors.append(
                    f"Severity {severity} out of range [0, 1]"
                )
        except (ValueError, TypeError):
            errors.append(f"Severity must be numeric, got {incident['severity']}")
        
        # Validate timestamp
        try:
            timestamp = float(incident["timestamp"])
            if not validate_timestamp(timestamp, current_time):
                errors.append(
                    f"Timestamp {timestamp} is invalid or too old"
                )
        except (ValueError, TypeError):
            errors.append(f"Timestamp must be numeric, got {incident['timestamp']}")
        
        # Validate coordinates
        try:
            lat = float(incident["latitude"])
            lon = float(incident["longitude"])
            if not validate_coordinates(lat, lon):
                errors.append(
                    f"Coordinates ({lat}, {lon}) out of valid range"
                )
        except (ValueError, TypeError):
            errors.append(
                f"Latitude/Longitude must be numeric, "
                f"got ({incident.get('latitude')}, {incident.get('longitude')})"
            )
        
        # Validate custom severity override if provided
        if incident.get("custom_severity_override") is not None:
            try:
                override = float(incident["custom_severity_override"])
                if not validate_severity(override):
                    errors.append(
                        f"Custom severity override {override} out of range [0, 1]"
                    )
            except (ValueError, TypeError):
                errors.append(
                    f"Custom severity override must be numeric, "
                    f"got {incident['custom_severity_override']}"
                )
        
        return errors
    
    def _generate_incident_id(self, incident: Dict[str, Any], current_time: float) -> str:
        """
        Generate a unique incident ID.
        
        Args:
            incident: Incident data
            current_time: Current timestamp
        
        Returns:
            str: Generated incident ID
        """
        # Format: incident_{type}_{timestamp}_{processed_count}
        incident_type = incident.get("type", "unknown")[:4].upper()
        timestamp_ms = int(current_time * 1000)
        
        incident_id = f"incident_{incident_type}_{timestamp_ms}_{self.processed_count}"
        return incident_id
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get processing statistics.
        
        Returns:
            Dict: Statistics including counts and validation rate
        """
        total = self.processed_count
        failed = self.validation_failed_count
        success = total - failed
        success_rate = (success / total * 100) if total > 0 else 0.0
        
        return {
            "total_processed": total,
            "valid_incidents": success,
            "invalid_incidents": failed,
            "success_rate": success_rate,
        }
    
    def reset_statistics(self):
        """Reset processor statistics."""
        self.processed_count = 0
        self.validation_failed_count = 0
        self.logger.info("Incident processor statistics reset")
