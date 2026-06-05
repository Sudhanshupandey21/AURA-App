import 'package:flutter/foundation.dart';

class ApiConfig {
  // Platform-aware base URL
  static String get baseUrl {
    if (kIsWeb) {
      // Web platform: use localhost
      return 'http://localhost:8000';
    } else {
      // Android emulator: use 10.0.2.2
      // Physical device: configure via environment or settings
      return 'http://10.0.2.2:8000';
    }
  }

  // Platform-aware WebSocket URL
  static String get wsUrl {
    if (kIsWeb) {
      return 'ws://localhost:8000/ws/live-tracking';
    } else {
      return 'ws://10.0.2.2:8000/ws/live-tracking';
    }
  }

  // API Endpoints
  static const String health = "/api/health";
  static const String systemStatus = "/api/system-status";
  static const String predictRisk = "/api/predict-risk";
  static const String routeAnalysis = "/api/route-analysis";
  static const String incidentReport = "/api/incident-report";
  static const String sos = "/api/sos";
  static const String liveLocation = "/api/live-location";

  // WebSocket endpoint
  static const String liveTracking = "/ws/live-tracking";

  // Timeout configurations
  static const Duration connectionTimeout = Duration(seconds: 10);
  static const Duration receiveTimeout = Duration(seconds: 30);

  // Demo mode flag (enable when backend is unavailable)
  static const bool useDemoMode = false;
}
