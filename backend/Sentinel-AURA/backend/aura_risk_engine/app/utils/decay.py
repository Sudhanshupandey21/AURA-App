import math


def exponential_decay(age_seconds: float, half_life_seconds: float = 3600.0) -> float:
    """Compute an exponential decay factor for incident age.

    A half-life of 3600 seconds means the incident's impact halves every hour.
    """
    if age_seconds <= 0:
        return 1.0
    if half_life_seconds <= 0:
        raise ValueError("half_life_seconds must be positive")
    return math.exp(-math.log(2) * age_seconds / half_life_seconds)
