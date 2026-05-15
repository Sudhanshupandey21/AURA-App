import '/components/button/button_widget.dart';
import '/components/emergency_stat_card/emergency_stat_card_widget.dart';
import '/components/aura_live_map.dart';
import '/components/pulsing_sos_button/pulsing_sos_button_widget.dart';
import '/flutter_flow/flutter_flow_icon_button.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/core/services/sos_service.dart';
import '/services/location_service.dart';
import 'package:geolocator/geolocator.dart';
import 'dart:ui';
import '/index.dart';
import 'package:flutter/material.dart';
import 'package:lottie/lottie.dart';
import 'package:material_palette/material_palette.dart';
import 'package:percent_indicator/percent_indicator.dart';
import 's_o_s_emergency_model.dart';
export 's_o_s_emergency_model.dart';

class SOSEmergencyWidget extends StatefulWidget {
  const SOSEmergencyWidget({super.key});

  static String routeName = 'SOSEmergency';
  static String routePath = '/sOSEmergency';

  @override
  State<SOSEmergencyWidget> createState() => _SOSEmergencyWidgetState();
}

class _SOSEmergencyWidgetState extends State<SOSEmergencyWidget> {
  static const String _defaultUserId = 'demo_user';
  final LocationService _locationService = LocationService();
  final SOSService _sosService = SOSService();
  bool _sendingSOS = false;
  late SOSEmergencyModel _model;

  final scaffoldKey = GlobalKey<ScaffoldState>();

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => SOSEmergencyModel());
  }

  @override
  void dispose() {
    _model.dispose();

    super.dispose();
  }

  Future<void> _triggerSosAlert(
      {String message = 'Emergency SOS activated'}) async {
    if (_sendingSOS) return;

    setState(() {
      _sendingSOS = true;
    });

    try {
      final currentPosition = _locationService.currentPosition;
      final Position position = currentPosition ??
          await Geolocator.getCurrentPosition(
            desiredAccuracy: LocationAccuracy.bestForNavigation,
          );

      final response = await _sosService.sendSOSAlert(
        userId: _defaultUserId,
        location: {
          'lat': position.latitude,
          'lng': position.longitude,
        },
        message: message,
      );

      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(response['message'] ?? 'SOS alert sent successfully'),
          duration: const Duration(seconds: 4),
        ),
      );
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Failed to send SOS: ${e.toString()}'),
          duration: const Duration(seconds: 4),
        ),
      );
    } finally {
      if (mounted) {
        setState(() {
          _sendingSOS = false;
        });
      }
    }
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
        backgroundColor: FlutterFlowTheme.of(context).primaryBackground,
        body: Stack(
          alignment: const AlignmentDirectional(-1.0, -1.0),
          children: [
            LayoutBuilder(
              builder: (context, constraints) {
                return TurbulenceGradientShaderFill(
                  width: constraints.maxWidth.isFinite
                      ? constraints.maxWidth
                      : 200.0,
                  height: 200.0,
                  params: ShaderParams(values: {
                    'gradientAngle': 180.0,
                    'gradientScale': 1.05,
                    'gradientOffset': 0.35,
                    'noiseIntensity': 0.56,
                    'ditherStrength': 0.0,
                    'ditherScale': 0.68,
                    'animSpeed': 0.81,
                    'octaves': 3.89,
                    'baseFrequency': 1.69,
                    'noiseScale': 3.1,
                    'colorCount': 8.0,
                    'softness': 1.0,
                    'exposure': 1.26,
                    'contrast': 1.74,
                    'bumpStrength': 0.05,
                    'lightDirX': 0.4,
                    'lightDirY': -0.38,
                    'lightDirZ': 1.95,
                    'lightIntensity': 1.26,
                    'ambient': 0.31,
                    'specular': 0.63,
                    'shininess': 75.47,
                    'metallic': 0.39,
                    'roughness': 0.85,
                    'edgeFade': 0.0,
                    'edgeFadeMode': 0.0
                  }, colors: {
                    'color0': FlutterFlowTheme.of(context).onPrimary,
                    'color1': const Color(0xFF1A0000),
                    'color2': const Color(0xFF330000),
                    'color3': FlutterFlowTheme.of(context).onPrimary,
                    'color4': FlutterFlowTheme.of(context).onPrimary,
                    'color5': FlutterFlowTheme.of(context).onPrimary,
                    'color6': FlutterFlowTheme.of(context).onPrimary,
                    'color7': FlutterFlowTheme.of(context).onPrimary,
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
                Container(
                  decoration: const BoxDecoration(
                    color: Colors.transparent,
                    shape: BoxShape.rectangle,
                  ),
                  child: Padding(
                    padding: const EdgeInsetsDirectional.fromSTEB(
                        24.0, 60.0, 24.0, 16.0),
                    child: Container(
                      child: Row(
                        mainAxisSize: MainAxisSize.max,
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        crossAxisAlignment: CrossAxisAlignment.center,
                        children: [
                          FlutterFlowIconButton(
                            borderRadius: 12.0,
                            buttonSize: 40.0,
                            fillColor: FlutterFlowTheme.of(context).surface20,
                            icon: Icon(
                              Icons.arrow_back_ios_new_rounded,
                              color: FlutterFlowTheme.of(context).onBackground,
                              size: 24.0,
                            ),
                            onPressed: () async {
                              context.goNamed(HomeMapWidget.routeName);
                            },
                          ),
                          Column(
                            mainAxisSize: MainAxisSize.min,
                            mainAxisAlignment: MainAxisAlignment.start,
                            crossAxisAlignment: CrossAxisAlignment.center,
                            children: [
                              Text(
                                'EMERGENCY MODE',
                                style: FlutterFlowTheme.of(context)
                                    .labelLarge
                                    .override(
                                      font: TextStyle(
                                        fontFamily: 'Orbitron',
                                        fontWeight: FontWeight.w800,
                                        fontStyle: FlutterFlowTheme.of(context)
                                            .labelLarge
                                            .fontStyle,
                                      ),
                                      color: FlutterFlowTheme.of(context).error,
                                      letterSpacing: 0.0,
                                      fontWeight: FontWeight.w800,
                                      fontStyle: FlutterFlowTheme.of(context)
                                          .labelLarge
                                          .fontStyle,
                                      lineHeight: 1.3,
                                    ),
                              ),
                              Text(
                                'Live Tracking Active',
                                style: FlutterFlowTheme.of(context)
                                    .bodySmall
                                    .override(
                                      font: TextStyle(
                                        fontFamily: 'Inter',
                                        fontWeight: FlutterFlowTheme.of(context)
                                            .bodySmall
                                            .fontWeight,
                                        fontStyle: FlutterFlowTheme.of(context)
                                            .bodySmall
                                            .fontStyle,
                                      ),
                                      color: FlutterFlowTheme.of(context)
                                          .secondaryText,
                                      letterSpacing: 0.0,
                                      fontWeight: FlutterFlowTheme.of(context)
                                          .bodySmall
                                          .fontWeight,
                                      fontStyle: FlutterFlowTheme.of(context)
                                          .bodySmall
                                          .fontStyle,
                                      lineHeight: 1.5,
                                    ),
                              ),
                            ].divide(const SizedBox(height: 4.0)),
                          ),
                          FlutterFlowIconButton(
                            borderRadius: 12.0,
                            buttonSize: 40.0,
                            fillColor: FlutterFlowTheme.of(context).surface20,
                            icon: Icon(
                              Icons.settings_rounded,
                              color: FlutterFlowTheme.of(context).onBackground,
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
                ),
                Padding(
                  padding: const EdgeInsets.all(24.0),
                  child: Container(
                    child: ClipRRect(
                      borderRadius: BorderRadius.circular(24.0),
                      child: Container(
                        height: 200.0,
                        decoration: BoxDecoration(
                          borderRadius: BorderRadius.circular(24.0),
                          shape: BoxShape.rectangle,
                          border: Border.all(
                            color: FlutterFlowTheme.of(context).error30,
                            width: 1.0,
                          ),
                        ),
                        child: Stack(
                          alignment: const AlignmentDirectional(-1.0, -1.0),
                          children: [
                            Container(
                              child: const AuraLiveMap(
                                userId: _defaultUserId,
                                initialZoom: 15,
                                followCurrentLocation: true,
                                showStatusPill: true,
                                showLoadingFallback: false,
                              ),
                            ),
                            Container(
                              decoration: BoxDecoration(
                                gradient: LinearGradient(
                                  colors: [
                                    Colors.transparent,
                                    FlutterFlowTheme.of(context).error10,
                                    Colors.transparent
                                  ],
                                  stops: const [0.0, 0.5, 1.0],
                                  begin: const AlignmentDirectional(0.0, -1.0),
                                  end: const AlignmentDirectional(0, 1.0),
                                ),
                                shape: BoxShape.rectangle,
                              ),
                            ),
                            Align(
                              alignment: const AlignmentDirectional(0.0, 0.0),
                              child: Container(
                                child: Lottie.asset(
                                  'assets/lottie/location_pulse.json',
                                  width: 60.0,
                                  height: 60.0,
                                  fit: BoxFit.contain,
                                  animate: true,
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
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    mainAxisAlignment: MainAxisAlignment.center,
                    crossAxisAlignment: CrossAxisAlignment.center,
                    children: [
                      GestureDetector(
                        onLongPress: () => _triggerSosAlert(),
                        behavior: HitTestBehavior.opaque,
                        child: wrapWithModel(
                          model: _model.pulsingSosButtonModel,
                          updateCallback: () => safeSetState(() {}),
                          child: const PulsingSosButtonWidget(),
                        ),
                      ),
                      Column(
                        mainAxisSize: MainAxisSize.min,
                        mainAxisAlignment: MainAxisAlignment.start,
                        crossAxisAlignment: CrossAxisAlignment.center,
                        children: [
                          Text(
                            'Press and hold for 3 seconds',
                            style: FlutterFlowTheme.of(context)
                                .bodyMedium
                                .override(
                                  font: TextStyle(
                                    fontFamily: 'Inter',
                                    fontWeight: FlutterFlowTheme.of(context)
                                        .bodyMedium
                                        .fontWeight,
                                    fontStyle: FlutterFlowTheme.of(context)
                                        .bodyMedium
                                        .fontStyle,
                                  ),
                                  color: FlutterFlowTheme.of(context)
                                      .secondaryText,
                                  letterSpacing: 0.0,
                                  fontWeight: FlutterFlowTheme.of(context)
                                      .bodyMedium
                                      .fontWeight,
                                  fontStyle: FlutterFlowTheme.of(context)
                                      .bodyMedium
                                      .fontStyle,
                                  lineHeight: 1.5,
                                ),
                          ),
                          Text(
                            'Broadcasting to 5 Emergency Contacts',
                            style: FlutterFlowTheme.of(context)
                                .labelMedium
                                .override(
                                  font: TextStyle(
                                    fontFamily: 'Orbitron',
                                    fontWeight: FlutterFlowTheme.of(context)
                                        .labelMedium
                                        .fontWeight,
                                    fontStyle: FlutterFlowTheme.of(context)
                                        .labelMedium
                                        .fontStyle,
                                  ),
                                  color: FlutterFlowTheme.of(context).error,
                                  letterSpacing: 0.0,
                                  fontWeight: FlutterFlowTheme.of(context)
                                      .labelMedium
                                      .fontWeight,
                                  fontStyle: FlutterFlowTheme.of(context)
                                      .labelMedium
                                      .fontStyle,
                                  lineHeight: 1.3,
                                ),
                          ),
                        ].divide(const SizedBox(height: 8.0)),
                      ),
                    ].divide(const SizedBox(height: 32.0)),
                  ),
                ),
                Padding(
                  padding: const EdgeInsets.all(24.0),
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    mainAxisAlignment: MainAxisAlignment.start,
                    crossAxisAlignment: CrossAxisAlignment.center,
                    children: [
                      Row(
                        mainAxisSize: MainAxisSize.max,
                        mainAxisAlignment: MainAxisAlignment.start,
                        crossAxisAlignment: CrossAxisAlignment.center,
                        children: [
                          Expanded(
                            flex: 1,
                            child: wrapWithModel(
                              model: _model.emergencyStatCardModel1,
                              updateCallback: () => safeSetState(() {}),
                              child: EmergencyStatCardWidget(
                                color: FlutterFlowTheme.of(context).info,
                                icon: Icon(
                                  Icons.my_location_rounded,
                                  color: FlutterFlowTheme.of(context).info,
                                  size: 18.0,
                                ),
                                label: 'ACCURACY',
                                value: '2.4m',
                              ),
                            ),
                          ),
                          Expanded(
                            flex: 1,
                            child: wrapWithModel(
                              model: _model.emergencyStatCardModel2,
                              updateCallback: () => safeSetState(() {}),
                              child: EmergencyStatCardWidget(
                                color: FlutterFlowTheme.of(context).error,
                                icon: Icon(
                                  Icons.shield_rounded,
                                  color: FlutterFlowTheme.of(context).info,
                                  size: 18.0,
                                ),
                                label: 'STATUS',
                                value: 'Alerting',
                              ),
                            ),
                          ),
                          Expanded(
                            flex: 1,
                            child: wrapWithModel(
                              model: _model.emergencyStatCardModel3,
                              updateCallback: () => safeSetState(() {}),
                              child: EmergencyStatCardWidget(
                                color: FlutterFlowTheme.of(context).success,
                                icon: Icon(
                                  Icons.battery_charging_full_rounded,
                                  color: FlutterFlowTheme.of(context).info,
                                  size: 18.0,
                                ),
                                label: 'PHONE',
                                value: '84%',
                              ),
                            ),
                          ),
                        ].divide(const SizedBox(width: 16.0)),
                      ),
                      Column(
                        mainAxisSize: MainAxisSize.min,
                        mainAxisAlignment: MainAxisAlignment.start,
                        crossAxisAlignment: CrossAxisAlignment.center,
                        children: [
                          Container(
                            decoration: BoxDecoration(
                              color: FlutterFlowTheme.of(context).surface30,
                              borderRadius: BorderRadius.circular(16.0),
                              shape: BoxShape.rectangle,
                              border: Border.all(
                                color: FlutterFlowTheme.of(context).alternate,
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
                                    Expanded(
                                      flex: 1,
                                      child: Text(
                                        'Emergency contacts notified',
                                        style: FlutterFlowTheme.of(context)
                                            .bodyMedium
                                            .override(
                                              font: TextStyle(
                                                fontFamily: 'Inter',
                                                fontWeight:
                                                    FlutterFlowTheme.of(context)
                                                        .bodyMedium
                                                        .fontWeight,
                                                fontStyle:
                                                    FlutterFlowTheme.of(context)
                                                        .bodyMedium
                                                        .fontStyle,
                                              ),
                                              color:
                                                  FlutterFlowTheme.of(context)
                                                      .primaryText,
                                              letterSpacing: 0.0,
                                              fontWeight:
                                                  FlutterFlowTheme.of(context)
                                                      .bodyMedium
                                                      .fontWeight,
                                              fontStyle:
                                                  FlutterFlowTheme.of(context)
                                                      .bodyMedium
                                                      .fontStyle,
                                              lineHeight: 1.5,
                                            ),
                                      ),
                                    ),
                                    Icon(
                                      Icons.check_circle_rounded,
                                      color:
                                          FlutterFlowTheme.of(context).success,
                                      size: 20.0,
                                    ),
                                  ].divide(const SizedBox(width: 16.0)),
                                ),
                              ),
                            ),
                          ),
                          Row(
                            mainAxisSize: MainAxisSize.max,
                            mainAxisAlignment: MainAxisAlignment.start,
                            crossAxisAlignment: CrossAxisAlignment.center,
                            children: [
                              Expanded(
                                flex: 1,
                                child: GestureDetector(
                                  onTap: () => _triggerSosAlert(
                                    message: 'Police assistance requested',
                                  ),
                                  behavior: HitTestBehavior.opaque,
                                  child: wrapWithModel(
                                    model: _model.buttonModel1,
                                    updateCallback: () => safeSetState(() {}),
                                    child: ButtonWidget(
                                      content: 'Call Police',
                                      icon: Icon(
                                        Icons.local_police_rounded,
                                        color: FlutterFlowTheme.of(context)
                                            .onError,
                                        size: 16.0,
                                      ),
                                      iconPresent: true,
                                      iconEndPresent: false,
                                      variant: 'destructive',
                                      size: 'large',
                                      fullWidth: true,
                                      loading: false,
                                      disabled: false,
                                    ),
                                  ),
                                ),
                              ),
                              Expanded(
                                flex: 1,
                                child: GestureDetector(
                                  onTap: () => _triggerSosAlert(
                                    message: 'Safe anchor requested',
                                  ),
                                  behavior: HitTestBehavior.opaque,
                                  child: wrapWithModel(
                                    model: _model.buttonModel2,
                                    updateCallback: () => safeSetState(() {}),
                                    child: ButtonWidget(
                                      content: 'Safe Anchor',
                                      icon: Icon(
                                        Icons.security_rounded,
                                        color: FlutterFlowTheme.of(context)
                                            .primaryText,
                                        size: 16.0,
                                      ),
                                      iconPresent: true,
                                      iconEndPresent: false,
                                      variant: 'outline',
                                      size: 'large',
                                      fullWidth: true,
                                      loading: false,
                                      disabled: false,
                                    ),
                                  ),
                                ),
                              ),
                            ].divide(const SizedBox(width: 16.0)),
                          ),
                        ].divide(const SizedBox(height: 8.0)),
                      ),
                    ].divide(const SizedBox(height: 16.0)),
                  ),
                ),
                ClipRRect(
                  borderRadius: const BorderRadius.only(),
                  child: BackdropFilter(
                    filter: ImageFilter.blur(
                      sigmaX: 10.0,
                      sigmaY: 10.0,
                    ),
                    child: Container(
                      decoration: BoxDecoration(
                        color: FlutterFlowTheme.of(context).surface20,
                        shape: BoxShape.rectangle,
                      ),
                      child: Padding(
                        padding: const EdgeInsetsDirectional.fromSTEB(
                            24.0, 16.0, 24.0, 40.0),
                        child: Container(
                          child: Row(
                            mainAxisSize: MainAxisSize.max,
                            mainAxisAlignment: MainAxisAlignment.center,
                            crossAxisAlignment: CrossAxisAlignment.center,
                            children: [
                              CircularPercentIndicator(
                                percent: 0.9,
                                radius: 8.0,
                                lineWidth: 3.0,
                                animation: true,
                                animateFromLastPercent: true,
                                progressColor:
                                    FlutterFlowTheme.of(context).success,
                                backgroundColor:
                                    FlutterFlowTheme.of(context).alternate,
                              ),
                              Text(
                                'Encrypted Satellite Link Established',
                                style: FlutterFlowTheme.of(context)
                                    .labelSmall
                                    .override(
                                      font: TextStyle(
                                        fontFamily: 'Orbitron',
                                        fontWeight: FlutterFlowTheme.of(context)
                                            .labelSmall
                                            .fontWeight,
                                        fontStyle: FlutterFlowTheme.of(context)
                                            .labelSmall
                                            .fontStyle,
                                      ),
                                      color: FlutterFlowTheme.of(context)
                                          .secondaryText,
                                      letterSpacing: 0.0,
                                      fontWeight: FlutterFlowTheme.of(context)
                                          .labelSmall
                                          .fontWeight,
                                      fontStyle: FlutterFlowTheme.of(context)
                                          .labelSmall
                                          .fontStyle,
                                      lineHeight: 1.2,
                                    ),
                              ),
                            ].divide(const SizedBox(width: 8.0)),
                          ),
                        ),
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
