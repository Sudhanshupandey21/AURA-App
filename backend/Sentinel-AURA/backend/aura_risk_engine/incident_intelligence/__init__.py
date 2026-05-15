"""
Incident Intelligence Module for AURA X
Real-time urban safety incident analysis and risk assessment system.

This module provides:
- Incident input validation and processing
- Severity modeling based on incident types
- Time decay modeling for temporal relevance
- Geographic impact calculation using Haversine distance
- Integrated incident risk scoring
- Real-time incident aggregation
- Explainable outputs for system transparency

Author: AURA X Development Team
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "AURA X Development Team"

from aura_risk_engine.incident_intelligence.incident_processor import IncidentProcessor
from aura_risk_engine.incident_intelligence.severity_engine import SeverityEngine
from aura_risk_engine.incident_intelligence.decay_engine import TimeDecayEngine
from aura_risk_engine.incident_intelligence.geo_engine import GeoEngine
from aura_risk_engine.incident_intelligence.risk_engine import RiskEngine
from aura_risk_engine.incident_intelligence.aggregation import IncidentAggregator
from aura_risk_engine.incident_intelligence.explain import ExplainabilityEngine

__all__ = [
    "IncidentProcessor",
    "SeverityEngine",
    "TimeDecayEngine",
    "GeoEngine",
    "RiskEngine",
    "IncidentAggregator",
    "ExplainabilityEngine",
]
