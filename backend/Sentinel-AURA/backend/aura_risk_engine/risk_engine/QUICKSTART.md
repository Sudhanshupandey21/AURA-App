# Risk Engine Quick Start Guide

## 5-Minute Setup

### Installation

The Risk Engine requires only Python 3.8+ with no external dependencies.

1. Copy the `risk_engine` folder to your project
2. Import components as needed:

```python
from risk_engine import RiskAggregator, RiskScorer, RiskClassifier
```

## Basic Example: Assess a Location

```python
from risk_engine import RealtimeRiskEngine, OutputBuilder

# Create a real-time engine (includes all components)
engine = RealtimeRiskEngine()
builder = OutputBuilder()

# Define risk factors for a location (all 0-1 scale)
output = engine.update_factors(
    time_risk=0.8,       # Late night (high temporal risk)
    crowd_risk=0.2,      # Many people present (low crowd risk)
    light_risk=0.9,      # Very dark (high light risk)
    incident_risk=0.6,   # Some incidents nearby (medium incident risk)
    area_risk=0.1        # Safe neighborhood (low area risk)
)

# Get the result
print(f"Risk Score: {output.risk_score}/100")
print(f"Risk Level: {output.risk_level}")
print(f"Trend: {output.trend}")
print(f"Top Reasons: {output.reasons}")

# Format for display
alert = builder.build_alert_message(
    risk_score=output.risk_score,
    risk_level=output.risk_level,
    top_reasons=output.reasons
)
print(alert)
```

**Output**:
```
Risk Score: 74/100
Risk Level: HIGH
Trend: stable
Top Reasons: ['Dark environment detected', 'Recent incident activity', 'Late night elevated risk']

⚠️ HIGH RISK
Risk Score: 74/100

Key Factors:
  • Dark environment detected
  • Recent incident activity
  • Late night elevated risk

🚨 Exercise caution. Consider alternative actions. Alert authorities if appropriate.
```

## Understanding Risk Factors

Each factor should be provided as a value between 0 (safe/low) and 1 (risky/high):

| Factor | Low (0) | High (1) | Typical Values |
|--------|---------|----------|-----------------|
| `time_risk` | Daytime | Late night | 0.2 (morning) → 0.9 (midnight) |
| `crowd_risk` | Many people | Isolated | 0.1 (crowded) → 0.9 (empty) |
| `light_risk` | Well-lit | Total dark | 0.2 (bright) → 0.95 (dark) |
| `incident_risk` | No incidents | Active crime | 0.0 (safe) → 0.9 (high crime) |
| `area_risk` | Good area | Bad area | 0.1 (safe) → 0.8 (unsafe) |

## Understanding Risk Output

### Risk Score (0-100)
- **0-10**: Very safe
- **20-40**: Safe
- **40-60**: Neutral/moderate
- **60-80**: Risky
- **80-100**: Very risky/dangerous

### Risk Level
- **SAFE**: Score 0-40 (Green) - Normal operations
- **MEDIUM**: Score 40-70 (Yellow) - Heightened awareness
- **HIGH**: Score 70-100 (Red) - Extreme caution/alert

### Trend
- **increasing**: Risk is getting worse
- **stable**: Risk is steady
- **decreasing**: Risk is improving

### Reasons
Ranked list of factors contributing to the risk score (sorted by importance).

## Common Scenarios

### Scenario 1: Safe, Busy Daytime Area

```python
engine.update_factors(
    time_risk=0.2,       # Day (safe time)
    crowd_risk=0.1,      # Crowded (safe)
    light_risk=0.1,      # Bright (safe)
    incident_risk=0.0,   # No incidents
    area_risk=0.1        # Good area
)
# Expected: ~10/100 (SAFE)
```

### Scenario 2: Empty, Dark Location Late at Night

```python
engine.update_factors(
    time_risk=0.9,       # Midnight (risky)
    crowd_risk=0.9,      # Isolated (risky)
    light_risk=0.95,     # Very dark (risky)
    incident_risk=0.2,   # Few incidents
    area_risk=0.1        # Good area
)
# Expected: ~65/100 (MEDIUM/HIGH)
```

### Scenario 3: Recent Violent Crime Incident

```python
engine.update_factors(
    time_risk=0.6,       # Evening
    crowd_risk=0.3,      # Moderate activity
    light_risk=0.4,      # Decent lighting
    incident_risk=0.95,  # RECENT VIOLENT CRIME
    area_risk=0.2
)
# Expected: ~80/100 (HIGH) - Incident dominates
```

### Scenario 4: Improving Conditions Over Time

```python
# Initial: Risky conditions
engine.update_factors(
    time_risk=0.8, crowd_risk=0.7, light_risk=0.8,
    incident_risk=0.8, area_risk=0.3
)
output1 = engine.current_output
# Score: 75/100, Trend: stable

# Later: Conditions improve
engine.update_factors(
    time_risk=0.3, crowd_risk=0.4, light_risk=0.3,
    incident_risk=0.2, area_risk=0.2
)
output2 = engine.current_output
# Score: 28/100, Trend: decreasing
```

## Setting Up Alerts

```python
from risk_engine import RealtimeRiskEngine

engine = RealtimeRiskEngine()

# Alert when risk level changes to HIGH
def alert_high_risk(output):
    print(f"⚠️ RISK ELEVATED TO {output.risk_level}")
    print(f"Score: {output.risk_score}/100")
    print(f"Notify authorities if needed")

engine.set_on_high_risk(alert_high_risk)

# Alert when risk score changes significantly
def alert_score_change(old_score, new_score):
    change = new_score - old_score
    print(f"Risk changed: {old_score} → {new_score} ({change:+d})")

engine.set_on_risk_changed(alert_score_change)

# Now updates will trigger callbacks
engine.update_factors(..., force_recalculate=True)
```

## Batch Processing Multiple Locations

```python
from risk_engine import RealtimeRiskEngine, OutputBuilder

engine = RealtimeRiskEngine()
builder = OutputBuilder()

# Process multiple locations
locations = [
    {"name": "Park Downtown", "time": 0.2, "crowd": 0.8, "light": 0.3, "incident": 0.1, "area": 0.2},
    {"name": "Alley Late Night", "time": 0.95, "crowd": 0.1, "light": 0.95, "incident": 0.7, "area": 0.4},
    {"name": "Shopping Mall", "time": 0.5, "crowd": 0.2, "light": 0.1, "incident": 0.0, "area": 0.1},
]

for loc in locations:
    output = engine.update_factors(
        time_risk=loc["time"],
        crowd_risk=loc["crowd"],
        light_risk=loc["light"],
        incident_risk=loc["incident"],
        area_risk=loc["area"],
        force_recalculate=True
    )
    
    print(f"\n{loc['name']}:")
    print(f"  Score: {output.risk_score}/100 ({output.risk_level})")
    print(f"  Trend: {output.trend}")
```

## Monitoring Trends Over Time

```python
from risk_engine import TrendEngine

engine = TrendEngine()

# Simulate hourly readings
readings = [
    (0, 25),   # Midnight: 25/100
    (1, 30),   # 1 AM: 30/100
    (2, 35),   # 2 AM: 35/100
    (5, 40),   # 5 AM: 40/100 (increasing trend)
    (8, 20),   # 8 AM: 20/100 (decreasing trend)
]

for hour, score in readings:
    engine.add_data_point(float(score))
    
    if hour > 0:
        trend = engine.predict_trend(float(score))
        velocity = engine.get_trend_velocity()
        print(f"{hour:02d}:00 - Score: {score}, Trend: {trend}, Velocity: {velocity:.2f}")
```

## Customization Examples

### Custom Risk Weights

```python
from risk_engine import RiskAggregator

# For a system that prioritizes incident detection less
custom_weights = {
    "time_risk": 0.25,
    "crowd_risk": 0.25,
    "light_risk": 0.25,
    "incident_risk": 0.20,  # Lower priority
    "area_risk": 0.05,
}

aggregator = RiskAggregator(weights=custom_weights)
```

### Custom Classification Thresholds

```python
from risk_engine import RiskClassifier

# For a more sensitive system
sensitive_classifier = RiskClassifier(
    thresholds={
        "SAFE": (0, 30),
        "MEDIUM": (30, 60),
        "HIGH": (60, 100),
    }
)
```

### Real-time with Custom Threshold

```python
from risk_engine import RealtimeRiskEngine

# Only recalculate if change > 5%
engine = RealtimeRiskEngine(recalculation_threshold=5.0)

# Small changes won't trigger recalculation
engine.update_factors(0.51, 0.51, 0.51, 0.51, 0.51)  # 2% change: skip
engine.update_factors(0.60, 0.60, 0.60, 0.60, 0.60)  # 10% change: recalculate
```

## Exporting Results

### JSON Export

```python
from risk_engine import OutputBuilder

builder = OutputBuilder()

output_dict = builder.build_final_output(
    risk_score=75,
    risk_level="HIGH",
    trend="increasing",
    reasons=["Recent incident", "Dark conditions"],
    component_scores={
        "time_risk": 80,
        "crowd_risk": 20,
        "light_risk": 90,
        "incident_risk": 75,
        "area_risk": 10,
    }
)

import json
print(json.dumps(output_dict, indent=2))
```

### CSV Export

```python
builder = OutputBuilder()

# Write header
with open("risk_readings.csv", "w") as f:
    f.write("timestamp,risk_score,risk_level,trend,time_risk,crowd_risk,light_risk,incident_risk,area_risk\n")
    
    # Write rows
    row = builder.build_csv_row(
        risk_score=75,
        risk_level="HIGH",
        trend="increasing",
        time_risk=0.8,
        crowd_risk=0.2,
        light_risk=0.9,
        incident_risk=0.75,
        area_risk=0.1
    )
    f.write(row + "\n")
```

## Performance Tips

1. **Reuse Engine Instances**: Don't create new engines for every calculation
2. **Batch Process**: Use single engine for multiple locations
3. **Adjust History Size**: Smaller history = lower memory
4. **Use Callbacks**: More efficient than polling
5. **Clear History Periodically**: Prevent unbounded memory growth

```python
from risk_engine import RealtimeRiskEngine

# Create once
engine = RealtimeRiskEngine()

# Reuse for many updates
for update in incoming_updates:
    engine.update_factors(**update)
```

## Debugging

### Check Engine Statistics

```python
engine = RealtimeRiskEngine()

# ... perform operations ...

print(engine.get_statistics())
# {
#     'total_updates': 100,
#     'total_recalculations': 45,
#     'recalculation_rate': 45.0,
#     'recalculation_threshold': 2.0
# }
```

### Enable Logging

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('risk_engine')

# Now you'll see detailed logs of all calculations
```

### Trace Component Contribution

```python
from risk_engine import ExplainabilityEngine

explainer = ExplainabilityEngine()

factors = {
    "time_risk": 0.8,
    "crowd_risk": 0.2,
    "light_risk": 0.9,
    "incident_risk": 0.7,
    "area_risk": 0.1,
}

contribution = explainer.get_factor_contribution(
    factor_name="incident_risk",
    factor_value=0.7,
    aggregated_score=64.5
)

print(contribution)
# {
#     'absolute_contribution': 0.245,
#     'percent_of_total': 37.9,
#     'importance_weight': 0.35,
#     'factor_value': 0.7
# }
```

## Common Issues & Solutions

### Issue: Score seems too high for relatively safe area

**Solution**: Check incident_risk - it has highest weight (0.35). Even small incident values have large impact.

```python
# This will score ~53, not 20, because incident_risk is weighted heavily
engine.update_factors(0.1, 0.1, 0.1, 0.9, 0.1)  # incident_risk=0.9
```

### Issue: Trend always "stable"

**Solution**: Changes need to be > 15% to register as increasing/decreasing.

```python
# Need large change to detect trend
engine.predict_trend(50.0, previous_score=45.0)  # 11% change → "stable"
engine.predict_trend(50.0, previous_score=40.0)  # 25% change → "increasing"
```

### Issue: Alerts not firing

**Solution**: Ensure you're using `force_recalculate=True` or have changes > recalculation_threshold.

```python
# This might not recalculate if change < 2%
engine.update_factors(0.51, 0.51, 0.51, 0.51, 0.51)

# Force recalculation to trigger callbacks
engine.update_factors(0.51, 0.51, 0.51, 0.51, 0.51, force_recalculate=True)
```

## Next Steps

- Review [README.md](README.md) for complete API reference
- Run [tests](../tests/test_risk_engine.py) to see more examples
- Explore individual module docstrings for detailed API info
- Integrate with your application's data pipeline

## Support

For detailed documentation, see the complete API reference in README.md
