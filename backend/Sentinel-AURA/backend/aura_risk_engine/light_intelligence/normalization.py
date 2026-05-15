import numpy as np
from aura_risk_engine.light_intelligence.utils import clamp, validate_lux


def normalize_light(lux: float, max_lux: float = 1000.0) -> float:
    """Normalize raw lux values to a 0.0-1.0 brightness range."""
    lux = validate_lux(lux)
    if max_lux <= 0:
        raise ValueError("max_lux must be positive")

    normalized = lux / float(max_lux)
    return clamp(float(np.clip(normalized, 0.0, 1.0)))
