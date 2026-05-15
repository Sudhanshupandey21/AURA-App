# Sentinel-AURA Backend

A production-ready FastAPI backend for the AURA X Flutter app, integrating AI risk engines for real-time safety analysis.

## Features

- 🚀 FastAPI backend with async support
- 🔌 WebSocket real-time communication
- 🤖 AI engine integration (risk prediction, route safety, incident intelligence)
- 🍃 MongoDB database integration
- 📍 Real-time location tracking
- 🚨 SOS emergency system
- 📊 Health monitoring and logging
- 🔒 CORS enabled for Flutter integration

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up MongoDB (local or cloud)

3. Configure environment variables in `.env`

4. Run the server:
```bash
uvicorn app.main:app --reload
```

Or use the startup scripts:
- Linux/Mac: `./start.sh`
- Windows: `start.bat`

## API Endpoints

### REST APIs

- `POST /api/predict-risk` - AI risk prediction
- `POST /api/route-analysis` - Route safety analysis
- `POST /api/incident-report` - Report incidents
- `POST /api/sos` - Emergency SOS alerts
- `POST /api/live-location` - Update live location
- `GET /api/health` - Health check
- `GET /api/system-status` - System status

### WebSocket

- `/ws/live-tracking?user_id={user_id}` - Real-time location and risk updates

## API Examples

### Risk Prediction
```bash
curl -X POST "http://localhost:8000/api/predict-risk" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "location": {"lat": 40.7128, "lng": -74.0060},
    "context": {"time_of_day": "night", "weather": "clear"}
  }'
```

Response:
```json
{
  "success": true,
  "risk_score": 75,
  "risk_level": "HIGH",
  "recommendation": "Avoid this area - high incident rate",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Route Analysis
```bash
curl -X POST "http://localhost:8000/api/route-analysis" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "route_points": [
      {"lat": 40.7128, "lng": -74.0060},
      {"lat": 40.7589, "lng": -73.9851}
    ]
  }'
```

### Incident Report
```bash
curl -X POST "http://localhost:8000/api/incident-report" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "location": {"lat": 40.7128, "lng": -74.0060},
    "type": "harassment",
    "description": "Suspicious activity reported",
    "severity": "medium"
  }'
```

### SOS Alert
```bash
curl -X POST "http://localhost:8000/api/sos" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "location": {"lat": 40.7128, "lng": -74.0060},
    "message": "Emergency situation"
  }'
```

## WebSocket Usage

Connect to WebSocket:
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/live-tracking?user_id=user123');

// Send location updates
ws.send(JSON.stringify({
  type: 'location_update',
  data: {
    location: { lat: 40.7128, lng: -74.0060 },
    speed: 5.2,
    heading: 90
  }
}));

// Receive risk updates
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.type === 'risk_update') {
    console.log('Risk update:', data.data);
  }
};
```

## Flutter Integration

### HTTP Requests
```dart
import 'package:http/http.dart' as http;

Future<Map<String, dynamic>> predictRisk(double lat, double lng) async {
  final response = await http.post(
    Uri.parse('http://localhost:8000/api/predict-risk'),
    headers: {'Content-Type': 'application/json'},
    body: jsonEncode({
      'user_id': 'user123',
      'location': {'lat': lat, 'lng': lng}
    }),
  );

  if (response.statusCode == 200) {
    return jsonDecode(response.body);
  } else {
    throw Exception('Failed to predict risk');
  }
}
```

### WebSocket Connection
```dart
import 'package:web_socket_channel/web_socket_channel.dart';

class LocationService {
  late WebSocketChannel channel;

  void connect(String userId) {
    channel = WebSocketChannel.connect(
      Uri.parse('ws://localhost:8000/ws/live-tracking?user_id=$userId'),
    );

    channel.stream.listen((message) {
      final data = jsonDecode(message);
      if (data['type'] == 'risk_update') {
        // Handle risk update
        print('Risk: ${data['data']['risk_score']}');
      }
    });
  }

  void sendLocation(double lat, double lng) {
    channel.sink.add(jsonEncode({
      'type': 'location_update',
      'data': {'location': {'lat': lat, 'lng': lng}}
    }));
  }

  void disconnect() {
    channel.sink.close();
  }
}
```

## Architecture

The backend integrates existing AI engines without modification:
- `risk_engine` - Core risk assessment
- `route_safety_engine` - Route analysis
- `crowd_intelligence` - Crowd-sourced data
- `incident_intelligence` - Incident processing
- `alert_response_engine` - Alert handling
- `realtime_orchestrator` - Real-time coordination

## Database Schema

### Collections
- `users` - User profiles
- `incidents` - Reported incidents
- `location_history` - Location tracking
- `sos_alerts` - Emergency alerts
- `prediction_history` - Risk predictions

## Development

- Modular architecture for scalability
- Async operations for performance
- Comprehensive logging with structlog
- Production-ready configuration
- Pydantic models for validation

## Environment Variables

```env
APP_NAME=Sentinel-AURA Backend
APP_VERSION=1.0.0
DEBUG=True
HOST=0.0.0.0
PORT=8000
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=aura_db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:8080"]
LOG_LEVEL=INFO
```