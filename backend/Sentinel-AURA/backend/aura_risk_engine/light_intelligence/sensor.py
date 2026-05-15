import random
from typing import Optional
from aura_risk_engine.light_intelligence.utils import validate_lux


class SensorUnavailableError(Exception):
    """Raised when the ambient light sensor is unavailable."""


def read_light_sensor(sensor_available: bool = True, override_lux: Optional[float] = None) -> float:
    """Read ambient light from a mobile sensor or simulate a realistic value.

    This function is integration-ready for real mobile sensor systems via the
    `sensor_available` flag and optional `override_lux` value.
    """
    if not sensor_available:
        raise SensorUnavailableError("Ambient light sensor unavailable")

    if override_lux is not None:
        return validate_lux(override_lux)

    # Simulate realistic mobile ambient light readings in lux.
    # Very dark indoor or night: 0-20 lux
    # Dim environment: 20-100 lux
    # Bright indoor / day shadow: 100-1000 lux
    simulated = random.uniform(0.0, 1200.0)
    return validate_lux(simulated)
