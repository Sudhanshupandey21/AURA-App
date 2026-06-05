import 'dart:async';
import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:web_socket_channel/web_socket_channel.dart';
import 'package:web_socket_channel/status.dart' as status;
import '../config/api_config.dart';

class WebSocketService {
  static final WebSocketService _instance = WebSocketService._internal();
  factory WebSocketService() => _instance;
  WebSocketService._internal();

  WebSocketChannel? _channel;
  StreamSubscription? _subscription;
  final StreamController<Map<String, dynamic>> _messageController =
      StreamController<Map<String, dynamic>>.broadcast();

  bool _isConnected = false;
  String? _userId;
  Timer? _reconnectTimer;
  int _reconnectAttempts = 0;
  static const int maxReconnectAttempts = 5;

  Stream<Map<String, dynamic>> get messages => _messageController.stream;
  bool get isConnected => _isConnected;

  void _log(String message) {
    debugPrint('WebSocketService: $message');
  }

  Future<void> connect(String userId) async {
    if (_isConnected && _userId == userId) {
      _log('Already connected with same user: $userId');
      return;
    }

    _userId = userId;
    _disconnect();

    try {
      final wsUrl = '${ApiConfig.wsUrl}?user_id=$userId';
      _log('Connecting to $wsUrl');
      _channel = WebSocketChannel.connect(Uri.parse(wsUrl));

      await _channel!.ready;
      _isConnected = true;
      _reconnectAttempts = 0;
      _log('websocket connected');

      _subscription = _channel!.stream.listen(
        _onMessage,
        onError: _onError,
        onDone: _onDisconnected,
      );

      // Start heartbeat
      _startHeartbeat();
    } catch (e) {
      _log('Connection failed: $e');
      _isConnected = false;
      _scheduleReconnect();
    }
  }

  void _onMessage(dynamic message) {
    try {
      final data = jsonDecode(message);
      _log('Message received: ${data['type'] ?? 'unknown'}');
      _messageController.add(data);
    } catch (e) {
      _log('Failed to parse message: $e');
    }
  }

  void _onError(Object error) {
    _log('WebSocket error: $error');
    _isConnected = false;
    _scheduleReconnect();
  }

  void _onDisconnected() {
    _log('websocket disconnected');
    _isConnected = false;
    if (_reconnectAttempts < maxReconnectAttempts) {
      _scheduleReconnect();
    }
  }

  void _scheduleReconnect() {
    if (_reconnectTimer != null) return;

    _reconnectAttempts++;
    final delay = Duration(seconds: _reconnectAttempts * 2);

    _log(
        'websocket reconnecting (attempt $_reconnectAttempts/$maxReconnectAttempts) in ${delay.inSeconds}s');
    _reconnectTimer = Timer(delay, () {
      _reconnectTimer = null;
      if (_userId != null) {
        connect(_userId!);
      }
    });
  }

  void _startHeartbeat() {
    Timer.periodic(const Duration(seconds: 30), (timer) {
      if (_isConnected && _channel != null) {
        sendMessage({
          'type': 'heartbeat',
          'timestamp': DateTime.now().millisecondsSinceEpoch,
        });
      } else {
        timer.cancel();
      }
    });
  }

  void sendMessage(Map<String, dynamic> message) {
    if (_isConnected && _channel != null) {
      try {
        _channel!.sink.add(jsonEncode(message));
        _log('Message sent: ${message['type'] ?? 'unknown'}');
      } catch (e) {
        _log('Failed to send message: $e');
      }
    } else {
      _log('Cannot send - not connected');
    }
  }

  void sendLocationUpdate(Map<String, double> location,
      {double? speed, double? heading}) {
    sendMessage({
      'type': 'location_update',
      'data': {
        'location': location,
        'speed': speed,
        'heading': heading,
        'timestamp': DateTime.now().millisecondsSinceEpoch,
      },
    });
  }

  void _disconnect() {
    _reconnectTimer?.cancel();
    _reconnectTimer = null;
    _subscription?.cancel();
    _channel?.sink.close(status.goingAway);
    _channel = null;
    _isConnected = false;
  }

  void disconnect() {
    _log('Disconnecting');
    _disconnect();
    _userId = null;
  }

  void dispose() {
    disconnect();
    _messageController.close();
    _log('WebSocketService disposed');
  }
}
