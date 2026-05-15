def clamp_score(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    """Clamp a numerical value to a safe range."""
    if value is None:
        return minimum
    return max(minimum, min(maximum, value))
