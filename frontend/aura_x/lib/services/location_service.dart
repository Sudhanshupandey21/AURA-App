import 'dart:async';
import 'dart:convert';
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
  Position? _currentPosition;
  final WebSocketService _wsService = WebSocketService();
  final http.Client _client = http.Client();
  String? _userId;

  Position? get currentPosition => _currentPosition;

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
      return false;
    }
  }

  Stream<Position> startLocationStream({String? userId}) {
    _userId = userId;
    const LocationSettings locationSettings = LocationSettings(
      accuracy: LocationAccuracy.bestForNavigation,
      distanceFilter: 5,
    );

    _positionStream = Geolocator.getPositionStream(
      locationSettings: locationSettings,
    );

    // Send location updates to backend
    _positionStream!.listen((position) {
      _currentPosition = position;
      _sendLocationToBackend(position);
    });

    return _positionStream!;
  }

  Future<void> _sendLocationToBackend(Position position) async {
    if (_userId == null) return;

    try {
      // Send via REST API
      await _client.post(
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
      );

      // Send via WebSocket for real-time updates
      _wsService.sendLocationUpdate(
        {'lat': position.latitude, 'lng': position.longitude},
        speed: position.speed,
        heading: position.heading,
      );
    } catch (e) {
      // Handle error silently to avoid interrupting location stream
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
    _positionStream = null;
    _currentPosition = null;
    _client.close();
  }
}
