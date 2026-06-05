import 'package:flutter/foundation.dart';
import 'package:geolocator/geolocator.dart';
import 'package:latlong2/latlong.dart' as maplib;
import '../services/route_service.dart';
import '../services/websocket_service.dart';

class NavigationProvider with ChangeNotifier {
  static const String _defaultUserId = 'demo_user';

  final RouteService _routeService = RouteService();
  final WebSocketService _wsService = WebSocketService();

  // Current location
  Position? _currentPosition;
  Position? get currentPosition => _currentPosition;

  // Route data
  List<maplib.LatLng> _currentRoute = [];
  List<maplib.LatLng> get currentRoute => _currentRoute;

  double _riskScore = 0.0;
  double get riskScore => _riskScore;

  List<String> _warnings = [];
  List<String> get warnings => _warnings;

  String _estimatedTime = '';
  String get estimatedTime => _estimatedTime;

  String _distance = '';
  String get distance => _distance;

  // Navigation state
  bool _isNavigating = false;
  bool get isNavigating => _isNavigating;

  bool _isLoading = false;
  bool get isLoading => _isLoading;

  // Destination
  maplib.LatLng? _destination;
  maplib.LatLng? get destination => _destination;

  String _destinationAddress = '';
  String get destinationAddress => _destinationAddress;

  NavigationProvider() {
    _initializeLocation();
    _initializeWebSocket();
  }

  Future<void> _initializeLocation() async {
    try {
      _currentPosition = await Geolocator.getCurrentPosition(
        desiredAccuracy: LocationAccuracy.high,
      );
      notifyListeners();
    } catch (e) {
      debugPrint('Error getting current location: $e');
    }
  }

  Future<void> _initializeWebSocket() async {
    try {
      await _wsService.connect(_defaultUserId);
      _wsService.messages.listen((message) {
        // Handle real-time updates
        if (message['type'] == 'risk_alert') {
          _handleRiskAlert(message);
        }
      });
    } catch (e) {
      debugPrint('WebSocket initialization failed: $e');
    }
  }

  void _handleRiskAlert(Map<String, dynamic> alert) {
    // Update warnings and potentially reroute
    final newWarning = alert['message'] ?? 'Risk alert received';
    if (!_warnings.contains(newWarning)) {
      _warnings.add(newWarning);
      notifyListeners();
    }
  }

  Future<bool> startNavigation({
    required double destLat,
    required double destLng,
    String? destinationAddress,
  }) async {
    if (_currentPosition == null) {
      return false;
    }

    _isLoading = true;
    notifyListeners();

    try {
      // Analyze route with AI
      final analysis = await _routeService.analyzeRoute(
        userId: _defaultUserId,
        sourceLat: _currentPosition!.latitude,
        sourceLng: _currentPosition!.longitude,
        destLat: destLat,
        destLng: destLng,
      );

      if (analysis['success'] == true) {
        // Parse route points
        final routePoints = analysis['safe_route'] as List<dynamic>;
        _currentRoute = routePoints.map((point) {
          return maplib.LatLng(point['lat'], point['lng']);
        }).toList();

        // Update other data
        _riskScore = (analysis['risk_score'] as num?)?.toDouble() ?? 0.0;
        _warnings = List<String>.from(analysis['warnings'] ?? []);
        _estimatedTime = analysis['estimated_time'] ?? '';
        _distance = analysis['distance'] ?? '';

        // Set destination
        _destination = maplib.LatLng(destLat, destLng);
        _destinationAddress = destinationAddress ?? '';

        _isNavigating = true;
        _isLoading = false;
        notifyListeners();

        return true;
      } else {
        _isLoading = false;
        notifyListeners();
        return false;
      }
    } catch (e) {
      debugPrint('Navigation start failed: $e');
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  Future<void> updateCurrentLocation(Position position) async {
    _currentPosition = position;

    // Send location update via WebSocket
    try {
      _wsService.sendMessage({
        'type': 'location_update',
        'user_id': _defaultUserId,
        'location': {
          'lat': position.latitude,
          'lng': position.longitude,
          'speed': position.speed,
          'heading': position.heading,
        },
        'timestamp': DateTime.now().toIso8601String(),
      });
    } catch (e) {
      debugPrint('Location update failed: $e');
    }

    notifyListeners();
  }

  void stopNavigation() {
    _isNavigating = false;
    _currentRoute = [];
    _destination = null;
    _destinationAddress = '';
    _warnings = [];
    notifyListeners();
  }

  void clearWarnings() {
    _warnings.clear();
    notifyListeners();
  }

  @override
  void dispose() {
    _wsService.disconnect();
    super.dispose();
  }
}
