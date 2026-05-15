import numpy as np
from aura_risk_engine.crowd_intelligence.utils import clamp, validate_density


def normalize_crowd_density(value: float) -> float:
    """Normalize a crowd signal value to the standard 0.0-1.0 range."""
    value = validate_density(value)
    return float(np.clip(value, 0.0, 1.0))
