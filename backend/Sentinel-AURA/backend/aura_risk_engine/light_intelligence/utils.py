from typing import Any
import numpy as np


def clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    """Clamp a floating-point value to a normalized range."""
    if value is None:
        return minimum
    return float(np.clip(value, minimum, maximum))


def validate_hour(hour: int) -> int:
    """Validate that hour is in the 0-23 range."""
    if not isinstance(hour, int):
        raise TypeError("hour must be an integer")
    if hour < 0 or hour > 23:
        raise ValueError("hour must be between 0 and 23")
    return hour


def validate_area_type(area_type: str) -> str:
    """Validate the area type for fallback estimation."""
    allowed = {"market", "residential", "isolated"}
    if not isinstance(area_type, str):
        raise TypeError("area_type must be a string")
    normalized = area_type.strip().lower()
    if normalized not in allowed:
        raise ValueError(f"area_type must be one of {sorted(allowed)}")
    return normalized


def validate_normalized_light(normalized_light: float) -> float:
    """Ensure normalized light is between 0 and 1."""
    if not isinstance(normalized_light, (int, float)):
        raise TypeError("normalized_light must be a number")
    return clamp(float(normalized_light), 0.0, 1.0)


def validate_lux(lux: float) -> float:
    """Validate raw lux sensor input."""
    if not isinstance(lux, (int, float)):
        raise TypeError("lux must be a number")
    if lux < 0:
        raise ValueError("lux must be non-negative")
    return float(lux)
