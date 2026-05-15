"""
Final Risk Engine for AURA X
Real-time urban safety risk assessment system.

Combines multiple environmental and contextual intelligence modules
to determine comprehensive urban safety risk.

This module provides:
- Weighted risk aggregation from multiple sources
- Final risk scoring and classification
- Trend prediction and analysis
- Explainable outputs with ranked reasons
- Real-time recalculation support

Author: AURA X Development Team
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "AURA X Development Team"

# Core components
from aura_risk_engine.risk_engine.aggregator import RiskAggregator
from aura_risk_engine.risk_engine.scoring import RiskScorer
from aura_risk_engine.risk_engine.classifier import RiskClassifier
from aura_risk_engine.risk_engine.trend_engine import TrendEngine
from aura_risk_engine.risk_engine.explainability import ExplainabilityEngine
from aura_risk_engine.risk_engine.realtime_engine import RealtimeRiskEngine
from aura_risk_engine.risk_engine.output_builder import OutputBuilder

# Utilities and data structures
from aura_risk_engine.risk_engine.utils import (
    RiskFactors,
    RiskOutput,
    normalize_to_range,
    clip_score,
    validate_risk_factors,
)

__all__ = [
    # Core components
    "RiskAggregator",
    "RiskScorer",
    "RiskClassifier",
    "TrendEngine",
    "ExplainabilityEngine",
    "RealtimeRiskEngine",
    "OutputBuilder",
    # Data structures
    "RiskFactors",
    "RiskOutput",
    # Utilities
    "normalize_to_range",
    "clip_score",
    "validate_risk_factors",
]
