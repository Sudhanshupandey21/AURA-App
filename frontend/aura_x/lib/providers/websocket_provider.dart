import 'package:flutter/foundation.dart';
import '../core/services/websocket_service.dart';
import '../models/models.dart';

class WebSocketProvider with ChangeNotifier {
  final WebSocketService _wsService = WebSocketService();
  bool _isConnected = false;
  RiskData? _latestRiskUpdate;
  String? _userId;

  bool get isConnected => _isConnected;
  RiskData? get latestRiskUpdate => _latestRiskUpdate;

  Future<void> connect(String userId) async {
    _userId = userId;
    await _wsService.connect(userId);
    _isConnected = _wsService.isConnected;
    notifyListeners();

    // Listen for messages
    _wsService.messages.listen((message) {
      _handleMessage(message);
    });
  }

  void _handleMessage(Map<String, dynamic> message) {
    final type = message['type'];

    switch (type) {
      case 'risk_update':
        _latestRiskUpdate = RiskData.fromJson(message['data']);
        notifyListeners();
        break;
      case 'emergency_alert':
        // Handle emergency alerts
        notifyListeners();
        break;
      case 'heartbeat_ack':
        // Heartbeat acknowledged
        break;
    }
  }

  void sendLocationUpdate(Map<String, double> location,
      {double? speed, double? heading}) {
    _wsService.sendLocationUpdate(location, speed: speed, heading: heading);
  }

  void disconnect() {
    _wsService.disconnect();
    _isConnected = false;
    _latestRiskUpdate = null;
    notifyListeners();
  }

  @override
  void dispose() {
    _wsService.dispose();
    super.dispose();
  }
}
