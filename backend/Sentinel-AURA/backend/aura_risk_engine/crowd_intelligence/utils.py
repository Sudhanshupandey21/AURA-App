from typing import Any
import numpy as np


def clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    """Clamp a value to a normalized range between minimum and maximum."""
    if value is None:
        return minimum
    return float(np.clip(value, minimum, maximum))


def validate_device_count(device_count: int) -> int:
    """Validate the BLE device count input."""
    if not isinstance(device_count, int):
        raise TypeError("device_count must be an integer")
    if device_count < 0:
        raise ValueError("device_count must be non-negative")
    return device_count


def validate_area_type(area_type: str) -> str:
    """Validate supported area type values."""
    if not isinstance(area_type, str):
        raise TypeError("area_type must be a string")
    normalized = area_type.strip().lower()
    allowed = {"market", "residential", "isolated", "transport_hub"}
    if normalized not in allowed:
        raise ValueError(f"area_type must be one of {sorted(allowed)}")
    return normalized


def validate_hour(hour: int) -> int:
    """Validate hour is within the 0-23 range."""
    if not isinstance(hour, int):
        raise TypeError("hour must be an integer")
    if hour < 0 or hour > 23:
        raise ValueError("hour must be between 0 and 23")
    return hour


def validate_density(value: float) -> float:
    """Validate density values and ensure they normalize to 0.0-1.0."""
    if not isinstance(value, (int, float)):
        raise TypeError("density value must be a number")
    return clamp(float(value), 0.0, 1.0)
