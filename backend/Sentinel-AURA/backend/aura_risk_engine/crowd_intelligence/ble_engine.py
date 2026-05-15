from aura_risk_engine.crowd_intelligence.utils import clamp, validate_device_count


def estimate_ble_crowd(device_count: int) -> float:
    """Estimate crowd density based on nearby BLE device counts."""
    device_count = validate_device_count(device_count)

    if device_count <= 2:
        normalized = 0.15
    elif device_count <= 8:
        normalized = 0.55
    else:
        normalized = 0.9

    return clamp(normalized)
