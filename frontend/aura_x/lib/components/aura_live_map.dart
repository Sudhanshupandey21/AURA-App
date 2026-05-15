import 'dart:async';
import 'dart:ui' as ui;

import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:geolocator/geolocator.dart';
import 'package:latlong2/latlong.dart';

import '../services/location_service.dart';

class AuraLiveMap extends StatefulWidget {
  const AuraLiveMap({
    super.key,
    this.mapController,
    this.initialCenter = fallbackCenter,
    this.initialZoom = 14.0,
    this.followCurrentLocation = false,
    this.autoInitializeLocation = true,
    this.showCurrentLocation = true,
    this.showControls = false,
    this.showStatusPill = false,
    this.showLoadingFallback = true,
    this.userId,
    this.extraMarkers = const [],
    this.routes = const [],
  });

  static const LatLng fallbackCenter = LatLng(21.2514, 81.6296);

  final MapController? mapController;
  final LatLng initialCenter;
  final double initialZoom;
  final bool followCurrentLocation;
  final bool autoInitializeLocation;
  final bool showCurrentLocation;
  final bool showControls;
  final bool showStatusPill;
  final bool showLoadingFallback;
  final String? userId;
  final List<Marker> extraMarkers;
  final List<Polyline> routes;

  @override
  State<AuraLiveMap> createState() => _AuraLiveMapState();
}

class _AuraLiveMapState extends State<AuraLiveMap> {
  final LocationService _locationService = LocationService();
  late final MapController _mapController =
      widget.mapController ?? MapController();

  StreamSubscription<Position>? _positionSubscription;
  Timer? _cameraTimer;
  Timer? _debounceTimer;

  late LatLng _currentLocation;
  late double _zoom;
  bool _mapReady = false;
  bool _isLocating = false;
  bool _hasLocation = false;
  bool _useFallbackTiles = false;
  bool _tileLayerLogged = false;
  int _tileErrorCount = 0;
  String? _statusMessage;

  @override
  void initState() {
    super.initState();
    _currentLocation = widget.initialCenter;
    _zoom = widget.initialZoom;
    debugPrint('AURA MAP: map initialized');
    if (widget.autoInitializeLocation) {
      unawaited(_initializeLocation());
    }
  }

  @override
  void dispose() {
    _cameraTimer?.cancel();
    _positionSubscription?.cancel();
    _debounceTimer?.cancel();
    super.dispose();
  }

  Future<void> _initializeLocation() async {
    if (!mounted || _isLocating) return;

    setState(() {
      _isLocating = true;
      _statusMessage = null;
    });

    final initialized = await _locationService.initializeLocation();
    if (!mounted) return;

    if (!initialized) {
      setState(() {
        _isLocating = false;
        _hasLocation = false;
        _statusMessage = 'Location unavailable. Showing default safety zone.';
      });
      return;
    }

    final position = _locationService.currentPosition;
    if (position != null) {
      debugPrint(
        'AURA MAP: location received ${position.latitude}, ${position.longitude}',
      );
      _applyPosition(position, animate: widget.followCurrentLocation);
    }

    _positionSubscription?.cancel();
    _positionSubscription =
        _locationService.startLocationStream(userId: widget.userId).listen(
      (position) {
        debugPrint(
          'AURA MAP: location received ${position.latitude}, ${position.longitude}',
        );
        _applyPosition(position, animate: widget.followCurrentLocation);
      },
      onError: (_) {
        if (!mounted) return;
        setState(() {
          _statusMessage = 'Live GPS paused. Map remains available.';
        });
      },
    );

    if (mounted) {
      setState(() {
        _isLocating = false;
        _hasLocation = position != null;
      });
    }
  }

  void _applyPosition(Position position, {required bool animate}) {
    if (!mounted) return;

    final next = LatLng(position.latitude, position.longitude);
    final distance = Geolocator.distanceBetween(
      _currentLocation.latitude,
      _currentLocation.longitude,
      next.latitude,
      next.longitude,
    );

    if (_hasLocation && distance < 5.0) {
      return; // Increased threshold to reduce updates
    }

    // Debounce the state update to avoid excessive rebuilds
    _debounceTimer?.cancel();
    _debounceTimer = Timer(const Duration(milliseconds: 300), () {
      if (!mounted) return;

      final previous = _currentLocation;
      _currentLocation = next;
      _hasLocation = true;
      _statusMessage = null;

      if (widget.followCurrentLocation && _mapReady) {
        if (animate) {
          _animateCamera(previous, next, _zoom);
        } else {
          _mapController.move(next, _zoom);
        }
      }

      // Only call setState when necessary, not on every GPS update
      setState(() {});
    });
  }

  void _animateCamera(LatLng from, LatLng to, double zoom) {
    _cameraTimer?.cancel();

    const frames = 18;
    var frame = 0;
    _cameraTimer = Timer.periodic(const Duration(milliseconds: 16), (timer) {
      if (!_mapReady || !mounted) {
        timer.cancel();
        return;
      }

      frame += 1;
      final t = Curves.easeOutCubic.transform(frame / frames);
      final point = LatLng(
        ui.lerpDouble(from.latitude, to.latitude, t)!,
        ui.lerpDouble(from.longitude, to.longitude, t)!,
      );
      _mapController.move(point, zoom);

      if (frame >= frames) {
        timer.cancel();
      }
    });
  }

  void _recenter() {
    if (!_mapReady) return;
    _animateCamera(
      _mapController.camera.center,
      _hasLocation ? _currentLocation : widget.initialCenter,
      _zoom,
    );
  }

  void _zoomBy(double delta) {
    if (!_mapReady) return;
    setState(() {
      _zoom = (_mapController.camera.zoom + delta).clamp(1.0, 19.0);
    });
    _mapController.move(_mapController.camera.center, _zoom);
  }

  @override
  Widget build(BuildContext context) {
    final userLayers = _buildUserLocationLayers();
    _logTileLayerReady();

    return RepaintBoundary(
      child: SizedBox.expand(
        child: Stack(
          fit: StackFit.expand,
          children: [
            FlutterMap(
              mapController: _mapController,
              options: MapOptions(
                initialCenter: widget.initialCenter,
                initialZoom: widget.initialZoom,
                minZoom: 1.0,
                maxZoom: 19.0,
                backgroundColor: const Color(0xFF081018),
                onMapReady: () {
                  debugPrint('AURA MAP: FlutterMap ready');
                  _mapReady = true;
                  if (widget.followCurrentLocation && _hasLocation) {
                    _mapController.move(_currentLocation, _zoom);
                  }
                },
                onPositionChanged: (position, hasGesture) {
                  if (hasGesture) {
                    _zoom = position.zoom;
                  }
                },
              ),
              children: [
                TileLayer(
                  key: ValueKey(_useFallbackTiles),
                  urlTemplate: _useFallbackTiles
                      ? 'https://a.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png'
                      : 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
                  userAgentPackageName: 'com.aurax.app',
                  maxZoom: 19,
                  errorTileCallback: (tile, error, stackTrace) {
                    debugPrint('AURA MAP: tile error $error');
                    if (!mounted || _useFallbackTiles) return;
                    _tileErrorCount += 1;
                    if (_tileErrorCount >= 3) {
                      debugPrint('AURA MAP: switching to fallback tile server');
                      setState(() {
                        _useFallbackTiles = true;
                      });
                    }
                  },
                ),
                if (widget.routes.isNotEmpty)
                  PolylineLayer(polylines: widget.routes),
                ...userLayers,
                if (widget.extraMarkers.isNotEmpty)
                  MarkerLayer(markers: widget.extraMarkers),
              ],
            ),
            const IgnorePointer(child: _CyberpunkMapTint()),
            if (widget.showStatusPill) _StatusPill(active: _hasLocation),
            if (_statusMessage != null && widget.showLoadingFallback)
              _MapMessage(message: _statusMessage!),
            if (_isLocating && !_hasLocation && widget.showLoadingFallback)
              const _LocatingHint(),
            if (widget.showControls)
              _MapControls(
                onRecenter: _recenter,
                onZoomIn: () => _zoomBy(1),
                onZoomOut: () => _zoomBy(-1),
              ),
          ],
        ),
      ),
    );
  }

  void _logTileLayerReady() {
    if (_tileLayerLogged) return;
    _tileLayerLogged = true;
    debugPrint('AURA MAP: tile layer loaded');
  }

  List<Widget> _buildUserLocationLayers() {
    if (!widget.showCurrentLocation || !_hasLocation) {
      return const [];
    }

    return [
      CircleLayer(
        circles: [
          CircleMarker(
            point: _currentLocation,
            radius: 24,
            color: Colors.cyanAccent.withValues(alpha: 0.16),
            borderColor: Colors.cyanAccent.withValues(alpha: 0.58),
            borderStrokeWidth: 2,
          ),
        ],
      ),
      MarkerLayer(
        markers: [
          Marker(
            point: _currentLocation,
            width: 44,
            height: 44,
            child: const _CurrentLocationMarker(),
          ),
        ],
      ),
    ];
  }
}

class _CurrentLocationMarker extends StatelessWidget {
  const _CurrentLocationMarker();

  @override
  Widget build(BuildContext context) {
    return const RepaintBoundary(
      child: DecoratedBox(
        decoration: BoxDecoration(
          shape: BoxShape.circle,
          color: Color(0xFF041C24),
          border: Border.fromBorderSide(
            BorderSide(color: Colors.cyanAccent, width: 2),
          ),
        ),
        child: SizedBox(
          width: 44,
          height: 44,
          child: Center(
            child: Icon(Icons.my_location, color: Colors.cyanAccent, size: 22),
          ),
        ),
      ),
    );
  }
}

class _CyberpunkMapTint extends StatelessWidget {
  const _CyberpunkMapTint();

  @override
  Widget build(BuildContext context) {
    return DecoratedBox(
      decoration: BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topCenter,
          end: Alignment.bottomCenter,
          colors: [
            const Color(0xFF00131A).withValues(alpha: 0.06),
            Colors.transparent,
            const Color(0xFF030712).withValues(alpha: 0.10),
          ],
        ),
      ),
    );
  }
}

class _StatusPill extends StatelessWidget {
  const _StatusPill({required this.active});

  final bool active;

  @override
  Widget build(BuildContext context) {
    return Positioned(
      top: 14,
      right: 14,
      child: SafeArea(
        child: DecoratedBox(
          decoration: BoxDecoration(
            color: const Color(0xD9060B12),
            borderRadius: BorderRadius.circular(999),
            border: Border.all(
              color: active ? Colors.cyanAccent : Colors.redAccent,
              width: 1,
            ),
          ),
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Icon(
                  active ? Icons.gps_fixed : Icons.gps_off,
                  color: active ? Colors.cyanAccent : Colors.redAccent,
                  size: 16,
                ),
                const SizedBox(width: 6),
                Text(
                  active ? 'GPS LIVE' : 'DEFAULT ZONE',
                  style: const TextStyle(
                    color: Colors.white,
                    fontSize: 11,
                    fontWeight: FontWeight.w800,
                    letterSpacing: 0,
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class _MapMessage extends StatelessWidget {
  const _MapMessage({required this.message});

  final String message;

  @override
  Widget build(BuildContext context) {
    return Positioned(
      left: 16,
      right: 16,
      top: 16,
      child: SafeArea(
        child: DecoratedBox(
          decoration: BoxDecoration(
            color: const Color(0xE6081018),
            borderRadius: BorderRadius.circular(12),
            border: Border.all(color: Colors.cyanAccent.withValues(alpha: 0.5)),
          ),
          child: Padding(
            padding: const EdgeInsets.all(12),
            child: Row(
              children: [
                const Icon(Icons.info_outline, color: Colors.cyanAccent),
                const SizedBox(width: 10),
                Expanded(
                  child: Text(
                    message,
                    style: const TextStyle(color: Colors.white, fontSize: 12),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class _LocatingHint extends StatelessWidget {
  const _LocatingHint();

  @override
  Widget build(BuildContext context) {
    return const Positioned(
      left: 16,
      bottom: 16,
      child: SafeArea(
        child: DecoratedBox(
          decoration: BoxDecoration(
            color: Color(0xD9081018),
            borderRadius: BorderRadius.all(Radius.circular(999)),
          ),
          child: Padding(
            padding: EdgeInsets.symmetric(horizontal: 12, vertical: 8),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                SizedBox(
                  width: 14,
                  height: 14,
                  child: CircularProgressIndicator(
                    color: Colors.cyanAccent,
                    strokeWidth: 2,
                  ),
                ),
                SizedBox(width: 8),
                Text(
                  'Acquiring GPS',
                  style: TextStyle(color: Colors.white, fontSize: 12),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class _MapControls extends StatelessWidget {
  const _MapControls({
    required this.onRecenter,
    required this.onZoomIn,
    required this.onZoomOut,
  });

  final VoidCallback onRecenter;
  final VoidCallback onZoomIn;
  final VoidCallback onZoomOut;

  @override
  Widget build(BuildContext context) {
    return Positioned(
      right: 16,
      bottom: 22,
      child: SafeArea(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            _ControlButton(icon: Icons.my_location, onPressed: onRecenter),
            const SizedBox(height: 10),
            _ControlButton(icon: Icons.add, onPressed: onZoomIn),
            const SizedBox(height: 10),
            _ControlButton(icon: Icons.remove, onPressed: onZoomOut),
          ],
        ),
      ),
    );
  }
}

class _ControlButton extends StatelessWidget {
  const _ControlButton({required this.icon, required this.onPressed});

  final IconData icon;
  final VoidCallback onPressed;

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 46,
      height: 46,
      child: IconButton(
        onPressed: onPressed,
        style: IconButton.styleFrom(
          backgroundColor: const Color(0xE6081018),
          foregroundColor: Colors.cyanAccent,
          side: BorderSide(color: Colors.cyanAccent.withValues(alpha: 0.5)),
        ),
        icon: Icon(icon, size: 21),
      ),
    );
  }
}
