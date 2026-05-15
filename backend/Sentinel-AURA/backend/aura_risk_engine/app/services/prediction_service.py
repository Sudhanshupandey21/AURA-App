from aura_risk_engine.app.models.trend_model import predict_trend


def evaluate_trend(hour: int, crowd_density: float, incident_risk: float) -> str:
    """Wrap the trend prediction logic for the risk engine."""
    return predict_trend(hour, crowd_density, incident_risk)
