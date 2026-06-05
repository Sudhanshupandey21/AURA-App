import 'dart:async';
import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:geolocator/geolocator.dart';
import 'package:latlong2/latlong.dart';
import 'package:http/http.dart' as http;
import '../core/config/api_config.dart';
import '../core/services/websocket_service.dart';

class LocationService {
  static final LocationService _instance = LocationService._internal();
  factory LocationService() => _instance;
  LocationService._internal();

  Stream<Position>? _positionStream;
  StreamSubscription<Position>? _positionSubscription;
  Position? _currentPosition;
  final WebSocketService _wsService = WebSocketService();
  final http.Client _client = http.Client();
  String? _userId;
  final StreamController<Position> _locationController =
      StreamController<Position>.broadcast();

  Position? get currentPosition => _currentPosition;
  Stream<Position> get positionStream => _locationController.stream;

  void _log(String message) {
    debugPrint('LocationService: $message');
  }

  Future<bool> initializeLocation() async {
    try {
      bool serviceEnabled = await Geolocator.isLocationServiceEnabled();
      if (!serviceEnabled) {
        return false;
      }

      LocationPermission permission = await Geolocator.checkPermission();
      if (permission == LocationPermission.denied) {
        permission = await Geolocator.requestPermission();
        if (permission == LocationPermission.denied) {
          return false;
        }
      }

      if (permission == LocationPermission.deniedForever) {
        return false;
      }

      _currentPosition = await Geolocator.getCurrentPosition(
        desiredAccuracy: LocationAccuracy.bestForNavigation,
      );

      return true;
    } catch (e) {
      _log('Initialize failed: $e');
      return false;
    }
  }

  void startLocationStream({String? userId}) {
    _userId = userId;
    _log('Starting location stream for user: $userId');

    if (_positionSubscription != null) {
      _log('Location stream already active');
      return;
    }

    const LocationSettings locationSettings = LocationSettings(
      accuracy: LocationAccuracy.bestForNavigation,
      distanceFilter: 5,
    );

    _positionStream = Geolocator.getPositionStream(
      locationSettings: locationSettings,
    );

    // Subscribe to position stream (only once)
    _positionSubscription = _positionStream!.listen(
      (position) {
        _currentPosition = position;
        _log('Location received ${position.latitude}, ${position.longitude}');
        _locationController.add(position);
        _sendLocationToBackend(position);
      },
      onError: (error) {
        _log('Location stream error: $error');
      },
    );
  }

  Future<void> _sendLocationToBackend(Position position) async {
    if (_userId == null) return;

    try {
      // Send via REST API
      final response = await _client
          .post(
            Uri.parse('${ApiConfig.baseUrl}${ApiConfig.liveLocation}'),
            headers: {'Content-Type': 'application/json'},
            body: jsonEncode({
              'user_id': _userId,
              'location': {
                'lat': position.latitude,
                'lng': position.longitude,
              },
              'speed': position.speed,
              'heading': position.heading,
            }),
          )
          .timeout(ApiConfig.connectionTimeout);

      if (response.statusCode == 200) {
        _log('Location sent to backend');
      } else {
        _log('Backend returned ${response.statusCode}');
      }
    } catch (e) {
      _log('Error sending location: $e');
    }

    // Always attempt WebSocket send regardless of REST API result
    try {
      _wsService.sendLocationUpdate(
        {'lat': position.latitude, 'lng': position.longitude},
        speed: position.speed,
        heading: position.heading,
      );
    } catch (e) {
      _log('WebSocket send failed: $e');
    }
  }

  void updateCurrentPosition(Position position) {
    _currentPosition = position;
  }

  LatLng getCurrentLatLng() {
    if (_currentPosition != null) {
      return LatLng(_currentPosition!.latitude, _currentPosition!.longitude);
    }
    return const LatLng(21.2514, 81.6296);
  }

  double getCurrentHeading() {
    return _currentPosition?.heading ?? 0.0;
  }

  void dispose() {
    _positionSubscription?.cancel();
    _positionStream = null;
    _currentPosition = null;
    _locationController.close();
    _client.close();
    _log('LocationService disposed');
  }
}
