import '/components/route_card/route_card_widget.dart';
import '/components/aura_live_map.dart';
import '/core/services/route_service.dart';
import '/flutter_flow/flutter_flow_icon_button.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'dart:ui';
import '/index.dart';
import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart' as maplib;
import 'package:lottie/lottie.dart';
import 'package:material_palette/material_palette.dart';
import 'route_comparison_model.dart';
export 'route_comparison_model.dart';

class RouteComparisonWidget extends StatefulWidget {
  const RouteComparisonWidget({super.key});

  static String routeName = 'RouteComparison';
  static String routePath = '/routeComparison';

  @override
  State<RouteComparisonWidget> createState() => _RouteComparisonWidgetState();
}

class _RouteComparisonWidgetState extends State<RouteComparisonWidget> {
  static const String _defaultUserId = 'demo_user';
  final RouteService _routeService = RouteService();
  bool _isAnalyzingRoute = false;
  final List<maplib.LatLng> _originalRoute = const [
    AuraLiveMap.fallbackCenter,
    maplib.LatLng(21.256, 81.636),
    maplib.LatLng(21.263, 81.642),
  ];
  List<maplib.LatLng> _safeRoute = const [
    AuraLiveMap.fallbackCenter,
    maplib.LatLng(21.246, 81.624),
    maplib.LatLng(21.239, 81.618),
  ];

  late RouteComparisonModel _model;

  final scaffoldKey = GlobalKey<ScaffoldState>();

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => RouteComparisonModel());
  }

  @override
  void dispose() {
    _model.dispose();

    super.dispose();
  }

  Future<void> _analyzeRouteSafety() async {
    if (_isAnalyzingRoute) return;

    setState(() {
      _isAnalyzingRoute = true;
    });

    try {
      final response = await _routeService.analyzeRoute(
        userId: _defaultUserId,
        routePoints: _originalRoute
            .map((point) => {'lat': point.latitude, 'lng': point.longitude})
            .toList(),
      );

      final safestRoute = _parseRoutePoints(response['safest_route'] ?? []);
      if (safestRoute.isNotEmpty) {
        setState(() {
          _safeRoute = safestRoute;
        });
      }

      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('AI route analysis completed. Safer route displayed.'),
          duration: Duration(seconds: 3),
        ),
      );
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Route analysis failed: ${e.toString()}'),
          duration: const Duration(seconds: 4),
        ),
      );
    } finally {
      if (mounted) {
        setState(() {
          _isAnalyzingRoute = false;
        });
      }
    }
  }

  List<maplib.LatLng> _parseRoutePoints(dynamic routePoints) {
    if (routePoints is! List) {
      return [];
    }

    return routePoints
        .map<maplib.LatLng>((dynamic point) {
          if (point is Map) {
            final lat = (point['lat'] as num?)?.toDouble() ?? 0.0;
            final lng = (point['lng'] as num?)?.toDouble() ?? 0.0;
            return maplib.LatLng(lat, lng);
          }
          return const maplib.LatLng(0.0, 0.0);
        })
        .where((point) => point.latitude != 0.0 || point.longitude != 0.0)
        .toList();
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () {
        FocusScope.of(context).unfocus();
        FocusManager.instance.primaryFocus?.unfocus();
      },
      child: Scaffold(
        key: scaffoldKey,
        resizeToAvoidBottomInset: false,
        backgroundColor: const Color(0xFF080808),
        body: Stack(
          alignment: const AlignmentDirectional(-1.0, -1.0),
          children: [
            LayoutBuilder(
              builder: (context, constraints) {
                return FbmGradientShaderFill(
                  width: constraints.maxWidth.isFinite
                      ? constraints.maxWidth
                      : 200.0,
                  height: 200.0,
                  params: ShaderParams(values: {
                    'gradientAngle': 180.0,
                    'gradientScale': 0.89,
                    'gradientOffset': 0.0,
                    'noiseIntensity': 0.32,
                    'ditherStrength': 2.51,
                    'ditherScale': 0.29,
                    'animSpeed': 1.46,
                    'octaves': 6.06,
                    'lacunarity': 2.35,
                    'persistence': 0.5,
                    'noiseScale': 6.36,
                    'colorCount': 7.0,
                    'softness': 0.0,
                    'exposure': 1.0,
                    'contrast': 1.0,
                    'bumpStrength': 0.0,
                    'lightDirX': 0.55,
                    'lightDirY': 0.45,
                    'lightDirZ': 1.0,
                    'lightIntensity': 1.15,
                    'ambient': 0.7,
                    'specular': 0.29,
                    'shininess': 40.76,
                    'metallic': 1.0,
                    'roughness': 1.0,
                    'edgeFade': 1.72,
                    'edgeFadeMode': 0.0,
                    'sharpness': 2.2
                  }, colors: {
                    'color0': FlutterFlowTheme.of(context).onPrimary,
                    'color1': const Color(0xFF0A1220),
                    'color2': const Color(0xFF1A0B0B),
                    'color3': FlutterFlowTheme.of(context).onPrimary,
                    'color4': FlutterFlowTheme.of(context).onPrimary,
                    'color5': FlutterFlowTheme.of(context).onPrimary,
                    'color6': FlutterFlowTheme.of(context).onPrimary,
                    'color7': const Color(0x00808080),
                    'color8': const Color(0x00808080),
                    'color9': const Color(0x00808080)
                  }),
                  animationMode: ShaderAnimationMode.continuous,
                  cache: false,
                );
              },
            ),
            Column(
              mainAxisSize: MainAxisSize.max,
              mainAxisAlignment: MainAxisAlignment.start,
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                ClipRRect(
                  borderRadius: const BorderRadius.only(),
                  child: BackdropFilter(
                    filter: ImageFilter.blur(
                      sigmaX: 10.0,
                      sigmaY: 10.0,
                    ),
                    child: Container(
                      decoration: const BoxDecoration(
                        shape: BoxShape.rectangle,
                      ),
                      child: Column(
                        mainAxisSize: MainAxisSize.min,
                        crossAxisAlignment: CrossAxisAlignment.stretch,
                        children: [
                          Padding(
                            padding: const EdgeInsets.all(24.0),
                            child: Container(
                              child: Row(
                                mainAxisSize: MainAxisSize.max,
                                mainAxisAlignment:
                                    MainAxisAlignment.spaceBetween,
                                crossAxisAlignment: CrossAxisAlignment.center,
                                children: [
                                  FlutterFlowIconButton(
                                    borderRadius: 8.0,
                                    buttonSize: 40.0,
                                    fillColor: Colors.transparent,
                                    icon: Icon(
                                      Icons.arrow_back_ios_new_rounded,
                                      color: FlutterFlowTheme.of(context)
                                          .primaryText,
                                      size: 24.0,
                                    ),
                                    onPressed: () async {
                                      context.goNamed(HomeMapWidget.routeName);
                                    },
                                  ),
                                  Column(
                                    mainAxisSize: MainAxisSize.min,
                                    mainAxisAlignment: MainAxisAlignment.start,
                                    crossAxisAlignment:
                                        CrossAxisAlignment.center,
                                    children: [
                                      Text(
                                        'ROUTE ANALYSIS',
                                        style: FlutterFlowTheme.of(context)
                                            .titleMedium
                                            .override(
                                              font: TextStyle(
                                                fontFamily: 'Inter',
                                                fontWeight: FontWeight.w800,
                                                fontStyle:
                                                    FlutterFlowTheme.of(context)
                                                        .titleMedium
                                                        .fontStyle,
                                              ),
                                              color:
                                                  FlutterFlowTheme.of(context)
                                                      .primaryText,
                                              letterSpacing: 0.0,
                                              fontWeight: FontWeight.w800,
                                              fontStyle:
                                                  FlutterFlowTheme.of(context)
                                                      .titleMedium
                                                      .fontStyle,
                                              lineHeight: 1.4,
                                            ),
                                      ),
                                      Text(
                                        'AI-OPTIMIZED FOR SAFETY',
                                        style: FlutterFlowTheme.of(context)
                                            .labelSmall
                                            .override(
                                              font: TextStyle(
                                                fontFamily: 'Orbitron',
                                                fontWeight: FontWeight.bold,
                                                fontStyle:
                                                    FlutterFlowTheme.of(context)
                                                        .labelSmall
                                                        .fontStyle,
                                              ),
                                              color:
                                                  FlutterFlowTheme.of(context)
                                                      .tertiary,
                                              letterSpacing: 0.0,
                                              fontWeight: FontWeight.bold,
                                              fontStyle:
                                                  FlutterFlowTheme.of(context)
                                                      .labelSmall
                                                      .fontStyle,
                                              lineHeight: 1.2,
                                            ),
                                      ),
                                    ].divide(const SizedBox(height: 4.0)),
                                  ),
                                  FlutterFlowIconButton(
                                    borderRadius: 8.0,
                                    buttonSize: 40.0,
                                    fillColor: Colors.transparent,
                                    icon: Icon(
                                      Icons.tune_rounded,
                                      color: FlutterFlowTheme.of(context)
                                          .primaryText,
                                      size: 24.0,
                                    ),
                                    onPressed: () {
                                      print('IconButton pressed ...');
                                    },
                                  ),
                                ],
                              ),
                            ),
                          ),
                          Container(
                            height: 1.0,
                            decoration: const BoxDecoration(
                              color: Colors.transparent,
                              shape: BoxShape.rectangle,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
                Padding(
                  padding: const EdgeInsets.all(24.0),
                  child: Container(
                    child: ClipRRect(
                      borderRadius: BorderRadius.circular(24.0),
                      child: Container(
                        height: 280.0,
                        decoration: BoxDecoration(
                          borderRadius: BorderRadius.circular(24.0),
                          shape: BoxShape.rectangle,
                          border: Border.all(
                            color: Colors.transparent,
                            width: 1.0,
                          ),
                        ),
                        child: Stack(
                          alignment: const AlignmentDirectional(-1.0, -1.0),
                          children: [
                            SizedBox(
                              height: 280.0,
                              child: AuraLiveMap(
                                autoInitializeLocation: false,
                                showCurrentLocation: false,
                                userId: _defaultUserId,
                                routes: [
                                  Polyline(
                                    points: _originalRoute,
                                    color: Colors.cyanAccent,
                                    strokeWidth: 4,
                                  ),
                                  Polyline(
                                    points: _safeRoute,
                                    color: Colors.redAccent,
                                    strokeWidth: 3,
                                  ),
                                ],
                              ),
                            ),
                            Align(
                              alignment: const AlignmentDirectional(-1.0, -1.0),
                              child: Container(
                                child: Padding(
                                  padding: const EdgeInsets.all(16.0),
                                  child: Container(
                                    child: Column(
                                      mainAxisSize: MainAxisSize.min,
                                      mainAxisAlignment:
                                          MainAxisAlignment.start,
                                      crossAxisAlignment:
                                          CrossAxisAlignment.start,
                                      children: [
                                        Container(
                                          decoration: BoxDecoration(
                                            color: FlutterFlowTheme.of(context)
                                                .onPrimary67,
                                            borderRadius:
                                                BorderRadius.circular(8.0),
                                            shape: BoxShape.rectangle,
                                            border: Border.all(
                                              color:
                                                  FlutterFlowTheme.of(context)
                                                      .success50,
                                              width: 1.0,
                                            ),
                                          ),
                                          child: Padding(
                                            padding: const EdgeInsetsDirectional
                                                .fromSTEB(8.0, 4.0, 8.0, 4.0),
                                            child: Container(
                                              child: Row(
                                                mainAxisSize: MainAxisSize.max,
                                                mainAxisAlignment:
                                                    MainAxisAlignment.start,
                                                crossAxisAlignment:
                                                    CrossAxisAlignment.center,
                                                children: [
                                                  Container(
                                                    width: 8.0,
                                                    height: 8.0,
                                                    decoration: BoxDecoration(
                                                      color:
                                                          FlutterFlowTheme.of(
                                                                  context)
                                                              .success,
                                                      borderRadius:
                                                          BorderRadius.circular(
                                                              9999.0),
                                                      shape: BoxShape.rectangle,
                                                    ),
                                                  ),
                                                  Text(
                                                    'SAFE ZONE: HIGH LIGHTING',
                                                    style: FlutterFlowTheme.of(
                                                            context)
                                                        .labelSmall
                                                        .override(
                                                          font: TextStyle(
                                                            fontFamily:
                                                                'Orbitron',
                                                            fontWeight:
                                                                FlutterFlowTheme.of(
                                                                        context)
                                                                    .labelSmall
                                                                    .fontWeight,
                                                            fontStyle:
                                                                FlutterFlowTheme.of(
                                                                        context)
                                                                    .labelSmall
                                                                    .fontStyle,
                                                          ),
                                                          color: FlutterFlowTheme
                                                                  .of(context)
                                                              .success,
                                                          letterSpacing: 0.0,
                                                          fontWeight:
                                                              FlutterFlowTheme.of(
                                                                      context)
                                                                  .labelSmall
                                                                  .fontWeight,
                                                          fontStyle:
                                                              FlutterFlowTheme.of(
                                                                      context)
                                                                  .labelSmall
                                                                  .fontStyle,
                                                          lineHeight: 1.2,
                                                        ),
                                                  ),
                                                ].divide(
                                                    const SizedBox(width: 4.0)),
                                              ),
                                            ),
                                          ),
                                        ),
                                      ].divide(const SizedBox(height: 4.0)),
                                    ),
                                  ),
                                ),
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                  ),
                ),
                Expanded(
                  flex: 1,
                  child: SingleChildScrollView(
                    primary: false,
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      mainAxisAlignment: MainAxisAlignment.start,
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: [
                        Padding(
                          padding: const EdgeInsetsDirectional.fromSTEB(
                              24.0, 0.0, 24.0, 24.0),
                          child: Container(
                            child: Column(
                              mainAxisSize: MainAxisSize.min,
                              mainAxisAlignment: MainAxisAlignment.start,
                              crossAxisAlignment: CrossAxisAlignment.center,
                              children: [
                                Text(
                                  'AVAILABLE PATHS',
                                  style: FlutterFlowTheme.of(context)
                                      .labelLarge
                                      .override(
                                        font: TextStyle(
                                          fontFamily: 'Orbitron',
                                          fontWeight: FontWeight.bold,
                                          fontStyle:
                                              FlutterFlowTheme.of(context)
                                                  .labelLarge
                                                  .fontStyle,
                                        ),
                                        color: FlutterFlowTheme.of(context)
                                            .secondaryText,
                                        letterSpacing: 0.0,
                                        fontWeight: FontWeight.bold,
                                        fontStyle: FlutterFlowTheme.of(context)
                                            .labelLarge
                                            .fontStyle,
                                        lineHeight: 1.3,
                                      ),
                                ),
                                wrapWithModel(
                                  model: _model.routeCardModel1,
                                  updateCallback: () => safeSetState(() {}),
                                  child: RouteCardWidget(
                                    confidence: '96',
                                    crowd: 'High',
                                    duration: '14 MIN',
                                    label: 'SAFEST',
                                    lighting: 'Excellent',
                                    riskScore: '0.8',
                                    verified: '98%',
                                    isSafe: true,
                                    onPressed: () {
                                      ScaffoldMessenger.of(context)
                                          .showSnackBar(
                                        const SnackBar(
                                          content: Text(
                                              'Safe route selected! Navigation starting...'),
                                          duration: Duration(seconds: 2),
                                        ),
                                      );
                                      // TODO: Implement navigation with safe route
                                      context.goNamed(HomeMapWidget.routeName);
                                    },
                                  ),
                                ),
                                wrapWithModel(
                                  model: _model.routeCardModel2,
                                  updateCallback: () => safeSetState(() {}),
                                  child: RouteCardWidget(
                                    confidence: '68',
                                    crowd: 'Low',
                                    duration: '9 MIN',
                                    label: 'FASTEST',
                                    lighting: 'Moderate',
                                    riskScore: '4.2',
                                    verified: '62%',
                                    isSafe: false,
                                    onPressed: () {
                                      ScaffoldMessenger.of(context)
                                          .showSnackBar(
                                        const SnackBar(
                                          content: Text(
                                              'Fast route selected! Navigation starting...'),
                                          duration: Duration(seconds: 2),
                                        ),
                                      );
                                      // TODO: Implement navigation with fast route
                                      context.goNamed(HomeMapWidget.routeName);
                                    },
                                  ),
                                ),
                              ].divide(const SizedBox(height: 16.0)),
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
                Padding(
                  padding: const EdgeInsets.all(24.0),
                  child: Container(
                    child: Container(
                      decoration: BoxDecoration(
                        color: const Color(0xFF1A1A2E),
                        borderRadius: BorderRadius.circular(16.0),
                        shape: BoxShape.rectangle,
                        border: Border.all(
                          color: FlutterFlowTheme.of(context).info30,
                          width: 1.0,
                        ),
                      ),
                      child: Padding(
                        padding: const EdgeInsets.all(16.0),
                        child: Container(
                          child: Row(
                            mainAxisSize: MainAxisSize.max,
                            mainAxisAlignment: MainAxisAlignment.start,
                            crossAxisAlignment: CrossAxisAlignment.center,
                            children: [
                              Lottie.asset(
                                'assets/lottie/wave_pulse.json',
                                width: 40.0,
                                height: 40.0,
                                fit: BoxFit.contain,
                                animate: true,
                              ),
                              Expanded(
                                flex: 1,
                                child: Column(
                                  mainAxisSize: MainAxisSize.min,
                                  mainAxisAlignment: MainAxisAlignment.start,
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Text(
                                      'AURA X RECOMMENDATION',
                                      style: FlutterFlowTheme.of(context)
                                          .labelSmall
                                          .override(
                                            font: TextStyle(
                                              fontFamily: 'Orbitron',
                                              fontWeight: FontWeight.bold,
                                              fontStyle:
                                                  FlutterFlowTheme.of(context)
                                                      .labelSmall
                                                      .fontStyle,
                                            ),
                                            color: FlutterFlowTheme.of(context)
                                                .info,
                                            letterSpacing: 0.0,
                                            fontWeight: FontWeight.bold,
                                            fontStyle:
                                                FlutterFlowTheme.of(context)
                                                    .labelSmall
                                                    .fontStyle,
                                            lineHeight: 1.2,
                                          ),
                                    ),
                                    Text(
                                      'The \'Safest\' route adds 5 mins but avoids 3 unlit alleyways currently flagged by local sensors.',
                                      maxLines: 2,
                                      style: FlutterFlowTheme.of(context)
                                          .bodySmall
                                          .override(
                                            font: TextStyle(
                                              fontFamily: 'Inter',
                                              fontWeight:
                                                  FlutterFlowTheme.of(context)
                                                      .bodySmall
                                                      .fontWeight,
                                              fontStyle:
                                                  FlutterFlowTheme.of(context)
                                                      .bodySmall
                                                      .fontStyle,
                                            ),
                                            color: FlutterFlowTheme.of(context)
                                                .primaryText,
                                            letterSpacing: 0.0,
                                            fontWeight:
                                                FlutterFlowTheme.of(context)
                                                    .bodySmall
                                                    .fontWeight,
                                            fontStyle:
                                                FlutterFlowTheme.of(context)
                                                    .bodySmall
                                                    .fontStyle,
                                            lineHeight: 1.5,
                                          ),
                                      overflow: TextOverflow.ellipsis,
                                    ),
                                  ].divide(const SizedBox(height: 4.0)),
                                ),
                              ),
                            ].divide(const SizedBox(width: 16.0)),
                          ),
                        ),
                      ),
                    ),
                  ),
                ),
              ],
            ),
            Align(
              alignment: const AlignmentDirectional(0.0, 1.0),
              child: ClipRRect(
                borderRadius: const BorderRadius.only(),
                child: BackdropFilter(
                  filter: ImageFilter.blur(
                    sigmaX: 8.0,
                    sigmaY: 8.0,
                  ),
                  child: Container(
                    height: 90.0,
                    decoration: BoxDecoration(
                      color: FlutterFlowTheme.of(context).onPrimary67,
                      shape: BoxShape.rectangle,
                    ),
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: [
                        Container(
                          height: 1.0,
                          decoration: const BoxDecoration(
                            color: Colors.transparent,
                            shape: BoxShape.rectangle,
                          ),
                        ),
                        Container(
                          height: 89.0,
                          alignment: const AlignmentDirectional(0.0, 0.0),
                          child: Padding(
                            padding: const EdgeInsetsDirectional.fromSTEB(
                                0.0, 0.0, 0.0, 20.0),
                            child: Row(
                              mainAxisSize: MainAxisSize.max,
                              mainAxisAlignment: MainAxisAlignment.spaceAround,
                              crossAxisAlignment: CrossAxisAlignment.center,
                              children: [
                                FlutterFlowIconButton(
                                  borderRadius: 8.0,
                                  buttonSize: 40.0,
                                  fillColor: Colors.transparent,
                                  icon: Icon(
                                    Icons.grid_view_rounded,
                                    color: FlutterFlowTheme.of(context)
                                        .secondaryText,
                                    size: 24.0,
                                  ),
                                  onPressed: () async {
                                    context.goNamed(HomeMapWidget.routeName);
                                  },
                                ),
                                FlutterFlowIconButton(
                                  borderRadius: 8.0,
                                  buttonSize: 48.0,
                                  fillColor: Colors.transparent,
                                  icon: Icon(
                                    Icons.directions_rounded,
                                    color: FlutterFlowTheme.of(context).primary,
                                    size: 32.0,
                                  ),
                                  onPressed: () async {
                                    await _analyzeRouteSafety();
                                  },
                                ),
                                Padding(
                                  padding: const EdgeInsetsDirectional.fromSTEB(
                                      0.0, 0.0, 0.0, 30.0),
                                  child: Container(
                                    child: Container(
                                      width: 64.0,
                                      height: 64.0,
                                      decoration: BoxDecoration(
                                        color: FlutterFlowTheme.of(context)
                                            .error20,
                                        borderRadius:
                                            BorderRadius.circular(9999.0),
                                        shape: BoxShape.rectangle,
                                        border: Border.all(
                                          color: FlutterFlowTheme.of(context)
                                              .error,
                                          width: 2.0,
                                        ),
                                      ),
                                      alignment:
                                          const AlignmentDirectional(0.0, 0.0),
                                      child: Container(
                                        width: 50.0,
                                        height: 50.0,
                                        decoration: BoxDecoration(
                                          color: FlutterFlowTheme.of(context)
                                              .error,
                                          boxShadow: [
                                            BoxShadow(
                                              blurRadius: 20.0,
                                              color:
                                                  FlutterFlowTheme.of(context)
                                                      .error,
                                              offset: const Offset(
                                                0.0,
                                                0.0,
                                              ),
                                              spreadRadius: 5.0,
                                            )
                                          ],
                                          borderRadius:
                                              BorderRadius.circular(9999.0),
                                          shape: BoxShape.rectangle,
                                        ),
                                        alignment: const AlignmentDirectional(
                                            0.0, 0.0),
                                        child: Icon(
                                          Icons.sos_rounded,
                                          color: FlutterFlowTheme.of(context)
                                              .onError,
                                          size: 24.0,
                                        ),
                                      ),
                                    ),
                                  ),
                                ),
                                FlutterFlowIconButton(
                                  borderRadius: 8.0,
                                  buttonSize: 40.0,
                                  fillColor: Colors.transparent,
                                  icon: Icon(
                                    Icons.notifications_active_rounded,
                                    color: FlutterFlowTheme.of(context)
                                        .secondaryText,
                                    size: 24.0,
                                  ),
                                  onPressed: () async {
                                    context.goNamed(RiskAlertWidget.routeName);
                                  },
                                ),
                                FlutterFlowIconButton(
                                  borderRadius: 8.0,
                                  buttonSize: 40.0,
                                  fillColor: Colors.transparent,
                                  icon: Icon(
                                    Icons.account_circle_rounded,
                                    color: FlutterFlowTheme.of(context)
                                        .secondaryText,
                                    size: 24.0,
                                  ),
                                  onPressed: () async {
                                    context.goNamed(
                                        ProfileSafetyAnalyticsWidget.routeName);
                                  },
                                ),
                              ],
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
