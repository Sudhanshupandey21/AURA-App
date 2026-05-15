# AURA X - Flutter Frontend

A production-ready Flutter application for real-time safety and navigation, integrated with AI-powered risk assessment.

## Features

- 🗺️ Interactive map with OpenStreetMap
- 📍 Real-time GPS location tracking
- 🔴 Live risk assessment and safety scoring
- 🚨 SOS emergency alerts
- 📢 Incident reporting
- 🛣️ Route safety analysis
- 🔌 WebSocket real-time communication
- 📱 Provider-based state management

## Architecture

```
lib/
├── core/
│   ├── config/
│   │   └── api_config.dart
│   ├── services/
│   │   ├── websocket_service.dart
│   │   ├── risk_service.dart
│   │   ├── route_service.dart
│   │   ├── incident_service.dart
│   │   └── sos_service.dart
│   └── utils/
│       └── constants.dart
├── models/
│   └── models.dart
├── providers/
│   ├── websocket_provider.dart
│   ├── risk_provider.dart
│   ├── location_provider.dart
│   ├── incident_provider.dart
│   └── sos_provider.dart
├── repositories/
│   └── api_repository.dart
├── realtime/
│   └── realtime_manager.dart
└── pages/ (existing FlutterFlow pages)
```

## Setup

1. Install dependencies:
```bash
flutter pub get
```

2. Configure API endpoints in `lib/core/config/api_config.dart`

3. Run the app:
```bash
flutter run
```

For Android emulator, use `10.0.2.2` as the backend IP.
For physical devices, use your computer's IP address.

## Integration

The app connects to the Sentinel-AURA backend via:

- **REST APIs**: Risk prediction, route analysis, incident reporting, SOS
- **WebSocket**: Real-time location updates and risk assessments
- **Location Services**: Continuous GPS tracking with backend sync

## State Management

Uses Provider pattern for state management:

- `WebSocketProvider`: WebSocket connection and real-time updates
- `RiskProvider`: Risk assessment and route analysis
- `LocationProvider`: GPS location tracking
- `IncidentProvider`: Incident reporting
- `SOSProvider`: Emergency alerts

## Real-time Flow

1. User enables location tracking
2. GPS coordinates sent to backend via WebSocket
3. AI engines analyze risk in real-time
4. Risk scores and recommendations pushed back via WebSocket
5. UI updates with live safety information

## Performance Optimizations

- WebSocket connection pooling
- Location update throttling (5m distance filter)
- Async API calls with error handling
- Efficient map rendering with flutter_map
- Provider-based selective rebuilds