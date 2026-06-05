import 'package:flutter/foundation.dart';
import 'package:geolocator/geolocator.dart';
import '../services/location_service.dart';

class LocationProvider with ChangeNotifier {
  final LocationService _locationService = LocationService();
  Position? _currentPosition;
  bool _isTracking = false;
  Stream<Position>? _positionStream;

  Position? get currentPosition => _currentPosition;
  bool get isTracking => _isTracking;

  Future<bool> initializeLocation() async {
    final success = await _locationService.initializeLocation();
    if (success) {
      _currentPosition = _locationService.currentPosition;
      notifyListeners();
    }
    return success;
  }

  void startTracking({String? userId}) {
    if (_isTracking) return;

    _positionStream = _locationService.positionStream;
    _positionStream?.listen((position) {
      _currentPosition = position;
      notifyListeners();
    });

    _isTracking = true;
    notifyListeners();
  }

  void stopTracking() {
    _isTracking = false;
    _positionStream = null;
    notifyListeners();
  }

  @override
  void dispose() {
    _locationService.dispose();
    super.dispose();
  }
}
