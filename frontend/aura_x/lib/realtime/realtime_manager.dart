import 'dart:async';
import '../core/services/websocket_service.dart';
import '../providers/websocket_provider.dart';
import '../providers/risk_provider.dart';
import '../providers/location_provider.dart';

class RealtimeManager {
  static final RealtimeManager _instance = RealtimeManager._internal();
  factory RealtimeManager() => _instance;
  RealtimeManager._internal();

  final WebSocketService _wsService = WebSocketService();
  StreamSubscription? _wsSubscription;

  void initialize({
    required WebSocketProvider wsProvider,
    required RiskProvider riskProvider,
    required LocationProvider locationProvider,
    required String userId,
  }) {
    // Connect WebSocket
    wsProvider.connect(userId);

    // Start location tracking
    locationProvider.startTracking(userId: userId);

    // Listen for WebSocket messages
    _wsSubscription = _wsService.messages.listen((message) {
      _handleRealtimeMessage(message, wsProvider, riskProvider);
    });
  }

  void _handleRealtimeMessage(
    Map<String, dynamic> message,
    WebSocketProvider wsProvider,
    RiskProvider riskProvider,
  ) {
    final type = message['type'];

    switch (type) {
      case 'risk_update':
        // Update risk data in provider
        wsProvider._handleMessage(message);
        break;
cd 
      case 'emergency_alert':
        // Handle emergency alerts
        _handleEmergencyAlert(message);
        break;

      case 'system_alert':
        // Handle system alerts
        break;
    }
  }

  void _handleEmergencyAlert(Map<String, dynamic> message) {
    final alertData = message['data'];
    // Show emergency notification or alert
    // This could trigger UI updates or notifications
  }

  void sendLocationUpdate(Map<String, double> location,
      {double? speed, double? heading}) {
    _wsService.sendLocationUpdate(location, speed: speed, heading: heading);
  }

  void dispose() {
    _wsSubscription?.cancel();
    _wsService.disconnect();
  }
}
