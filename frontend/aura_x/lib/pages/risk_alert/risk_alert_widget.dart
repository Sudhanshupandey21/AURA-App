import '/components/button/button_widget.dart';
import '/components/reroute_option/reroute_option_widget.dart';
import '/components/risk_stat/risk_stat_widget.dart';
import '/flutter_flow/flutter_flow_icon_button.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'dart:ui';
import '/index.dart';
import 'package:flutter/material.dart';
import 'package:lottie/lottie.dart';
import 'package:material_palette/material_palette.dart';
import 'risk_alert_model.dart';
export 'risk_alert_model.dart';

class RiskAlertWidget extends StatefulWidget {
  const RiskAlertWidget({super.key});

  static String routeName = 'RiskAlert';
  static String routePath = '/riskAlert';

  @override
  State<RiskAlertWidget> createState() => _RiskAlertWidgetState();
}

class _RiskAlertWidgetState extends State<RiskAlertWidget> {
  late RiskAlertModel _model;

  final scaffoldKey = GlobalKey<ScaffoldState>();

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => RiskAlertModel());
  }

  @override
  void dispose() {
    _model.dispose();

    super.dispose();
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
        backgroundColor: FlutterFlowTheme.of(context).primaryBackground,
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
                    'gradientAngle': 90.0,
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
                    'color0': FlutterFlowTheme.of(context).error,
                    'color1': FlutterFlowTheme.of(context).primaryBackground,
                    'color2': const Color(0x4DFF003C),
                    'color3': FlutterFlowTheme.of(context).primaryBackground,
                    'color4': FlutterFlowTheme.of(context).primaryBackground,
                    'color5': FlutterFlowTheme.of(context).primaryBackground,
                    'color6': FlutterFlowTheme.of(context).primaryBackground,
                    'color7': const Color(0x00808080),
                    'color8': const Color(0x00808080),
                    'color9': const Color(0x00808080)
                  }),
                  animationMode: ShaderAnimationMode.continuous,
                  cache: false,
                );
              },
            ),
            Padding(
              padding: const EdgeInsets.all(32.0),
              child: Column(
                mainAxisSize: MainAxisSize.max,
                mainAxisAlignment: MainAxisAlignment.start,
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Container(
                    height: 24.0,
                  ),
                  Column(
                    mainAxisSize: MainAxisSize.min,
                    mainAxisAlignment: MainAxisAlignment.start,
                    crossAxisAlignment: CrossAxisAlignment.center,
                    children: [
                      Lottie.asset(
                        'assets/lottie/radar_pulse.json',
                        width: 120.0,
                        height: 120.0,
                        fit: BoxFit.contain,
                        animate: true,
                      ),
                      Text(
                        'RISK DETECTED',
                        style:
                            FlutterFlowTheme.of(context).headlineLarge.override(
                                  font: TextStyle(
                                    fontFamily: 'Orbitron',
                                    fontWeight: FontWeight.w900,
                                    fontStyle: FlutterFlowTheme.of(context)
                                        .headlineLarge
                                        .fontStyle,
                                  ),
                                  color: FlutterFlowTheme.of(context).error,
                                  letterSpacing: 0.0,
                                  fontWeight: FontWeight.w900,
                                  fontStyle: FlutterFlowTheme.of(context)
                                      .headlineLarge
                                      .fontStyle,
                                  lineHeight: 1.2,
                                ),
                      ),
                      Container(
                        decoration: BoxDecoration(
                          color: FlutterFlowTheme.of(context).error20,
                          borderRadius: BorderRadius.circular(9999.0),
                          shape: BoxShape.rectangle,
                          border: Border.all(
                            color: FlutterFlowTheme.of(context).error50,
                            width: 1.0,
                          ),
                        ),
                        child: Padding(
                          padding: const EdgeInsetsDirectional.fromSTEB(
                              8.0, 16.0, 8.0, 16.0),
                          child: Container(
                            child: Row(
                              mainAxisSize: MainAxisSize.min,
                              mainAxisAlignment: MainAxisAlignment.start,
                              crossAxisAlignment: CrossAxisAlignment.center,
                              children: [
                                Icon(
                                  Icons.report_problem_rounded,
                                  color: FlutterFlowTheme.of(context).onError,
                                  size: 16.0,
                                ),
                                Text(
                                  'CRITICAL THREAT LEVEL',
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
                                            .onError,
                                        letterSpacing: 0.0,
                                        fontWeight: FontWeight.bold,
                                        fontStyle: FlutterFlowTheme.of(context)
                                            .labelLarge
                                            .fontStyle,
                                        lineHeight: 1.3,
                                      ),
                                ),
                              ].divide(const SizedBox(width: 4.0)),
                            ),
                          ),
                        ),
                      ),
                    ].divide(const SizedBox(height: 16.0)),
                  ),
                  ClipRRect(
                    borderRadius: BorderRadius.circular(24.0),
                    child: BackdropFilter(
                      filter: ImageFilter.blur(
                        sigmaX: 8.0,
                        sigmaY: 8.0,
                      ),
                      child: Container(
                        decoration: BoxDecoration(
                          color: FlutterFlowTheme.of(context).surface30,
                          borderRadius: BorderRadius.circular(24.0),
                          shape: BoxShape.rectangle,
                          border: Border.all(
                            color: Colors.transparent,
                            width: 1.0,
                          ),
                        ),
                        child: Padding(
                          padding: const EdgeInsets.all(24.0),
                          child: Container(
                            child: Column(
                              mainAxisSize: MainAxisSize.min,
                              mainAxisAlignment: MainAxisAlignment.start,
                              crossAxisAlignment: CrossAxisAlignment.center,
                              children: [
                                Text(
                                  'Unusual crowd activity and low lighting detected 200m ahead on 5th Avenue. Incident reported 2 mins ago.',
                                  textAlign: TextAlign.center,
                                  style: FlutterFlowTheme.of(context)
                                      .bodyLarge
                                      .override(
                                        font: TextStyle(
                                          fontFamily: 'Inter',
                                          fontWeight:
                                              FlutterFlowTheme.of(context)
                                                  .bodyLarge
                                                  .fontWeight,
                                          fontStyle:
                                              FlutterFlowTheme.of(context)
                                                  .bodyLarge
                                                  .fontStyle,
                                        ),
                                        color: FlutterFlowTheme.of(context)
                                            .onSurface,
                                        letterSpacing: 0.0,
                                        fontWeight: FlutterFlowTheme.of(context)
                                            .bodyLarge
                                            .fontWeight,
                                        fontStyle: FlutterFlowTheme.of(context)
                                            .bodyLarge
                                            .fontStyle,
                                        lineHeight: 1.6,
                                      ),
                                ),
                                Divider(
                                  height: 16.0,
                                  thickness: 1.0,
                                  indent: 0.0,
                                  endIndent: 0.0,
                                  color: FlutterFlowTheme.of(context).alternate,
                                ),
                                Row(
                                  mainAxisSize: MainAxisSize.max,
                                  mainAxisAlignment:
                                      MainAxisAlignment.spaceAround,
                                  crossAxisAlignment: CrossAxisAlignment.center,
                                  children: [
                                    wrapWithModel(
                                      model: _model.riskStatModel1,
                                      updateCallback: () => safeSetState(() {}),
                                      child: RiskStatWidget(
                                        color:
                                            FlutterFlowTheme.of(context).error,
                                        label: 'LIGHTING',
                                        value: '12%',
                                      ),
                                    ),
                                    wrapWithModel(
                                      model: _model.riskStatModel2,
                                      updateCallback: () => safeSetState(() {}),
                                      child: RiskStatWidget(
                                        color: FlutterFlowTheme.of(context)
                                            .warning,
                                        label: 'CROWD',
                                        value: 'HIGH',
                                      ),
                                    ),
                                    wrapWithModel(
                                      model: _model.riskStatModel3,
                                      updateCallback: () => safeSetState(() {}),
                                      child: RiskStatWidget(
                                        color:
                                            FlutterFlowTheme.of(context).info,
                                        label: 'POLICE',
                                        value: '1.2km',
                                      ),
                                    ),
                                  ],
                                ),
                              ].divide(const SizedBox(height: 24.0)),
                            ),
                          ),
                        ),
                      ),
                    ),
                  ),
                  Column(
                    mainAxisSize: MainAxisSize.min,
                    mainAxisAlignment: MainAxisAlignment.start,
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'AI REROUTE SUGGESTIONS',
                        style: FlutterFlowTheme.of(context).labelLarge.override(
                              font: TextStyle(
                                fontFamily: 'Orbitron',
                                fontWeight: FontWeight.bold,
                                fontStyle: FlutterFlowTheme.of(context)
                                    .labelLarge
                                    .fontStyle,
                              ),
                              color: FlutterFlowTheme.of(context).secondaryText,
                              letterSpacing: 0.0,
                              fontWeight: FontWeight.bold,
                              fontStyle: FlutterFlowTheme.of(context)
                                  .labelLarge
                                  .fontStyle,
                              lineHeight: 1.3,
                            ),
                      ),
                      wrapWithModel(
                        model: _model.rerouteOptionModel1,
                        updateCallback: () => safeSetState(() {}),
                        child: RerouteOptionWidget(
                          desc: 'Via well-lit main boulevard',
                          icon: Icon(
                            Icons.shield_rounded,
                            color: FlutterFlowTheme.of(context).success,
                            size: 24.0,
                          ),
                          risk: 'LOW RISK',
                          time: '+4 min',
                          title: 'AURA Safe Path',
                          isSafe: true,
                        ),
                      ),
                      wrapWithModel(
                        model: _model.rerouteOptionModel2,
                        updateCallback: () => safeSetState(() {}),
                        child: RerouteOptionWidget(
                          desc: 'Current path (Not advised)',
                          icon: Icon(
                            Icons.directions_walk_rounded,
                            color: FlutterFlowTheme.of(context).onSurface,
                            size: 24.0,
                          ),
                          risk: 'CRITICAL',
                          time: '0 min',
                          title: 'Fastest Route',
                          isSafe: false,
                        ),
                      ),
                    ].divide(const SizedBox(height: 16.0)),
                  ),
                  const Spacer(),
                  Column(
                    mainAxisSize: MainAxisSize.min,
                    mainAxisAlignment: MainAxisAlignment.start,
                    crossAxisAlignment: CrossAxisAlignment.center,
                    children: [
                      InkWell(
                        splashColor: Colors.transparent,
                        focusColor: Colors.transparent,
                        hoverColor: Colors.transparent,
                        highlightColor: Colors.transparent,
                        onTap: () {
                          ScaffoldMessenger.of(context).showSnackBar(
                            const SnackBar(
                              content: Text(
                                  'Safe reroute accepted! Navigating to safer route...'),
                              duration: Duration(seconds: 2),
                            ),
                          );
                          // TODO: Implement safe reroute navigation
                          context.goNamed(HomeMapWidget.routeName);
                        },
                        child: wrapWithModel(
                          model: _model.buttonModel1,
                          updateCallback: () => safeSetState(() {}),
                          child: ButtonWidget(
                            content: 'ACCEPT SAFE REROUTE',
                            icon: Icon(
                              Icons.alt_route_rounded,
                              color: FlutterFlowTheme.of(context).onPrimary,
                              size: 16.0,
                            ),
                            iconPresent: true,
                            iconEndPresent: false,
                            variant: 'primary',
                            size: 'large',
                            fullWidth: true,
                            loading: false,
                            disabled: false,
                          ),
                        ),
                      ),
                      InkWell(
                        splashColor: Colors.transparent,
                        focusColor: Colors.transparent,
                        hoverColor: Colors.transparent,
                        highlightColor: Colors.transparent,
                        onTap: () {
                          context.goNamed(SOSEmergencyWidget.routeName);
                        },
                        child: wrapWithModel(
                          model: _model.buttonModel2,
                          updateCallback: () => safeSetState(() {}),
                          child: ButtonWidget(
                            content: 'EMERGENCY SOS',
                            icon: Icon(
                              Icons.sos_rounded,
                              color: FlutterFlowTheme.of(context).onError,
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
                      InkWell(
                        splashColor: Colors.transparent,
                        focusColor: Colors.transparent,
                        hoverColor: Colors.transparent,
                        highlightColor: Colors.transparent,
                        onTap: () {
                          ScaffoldMessenger.of(context).showSnackBar(
                            const SnackBar(
                              content: Text('Alert dismissed'),
                              duration: Duration(seconds: 2),
                            ),
                          );
                          context.goNamed(HomeMapWidget.routeName);
                        },
                        child: wrapWithModel(
                          model: _model.buttonModel3,
                          updateCallback: () => safeSetState(() {}),
                          child: ButtonWidget(
                            content: 'I am safe, ignore alert',
                            icon: Icon(
                              Icons.close_rounded,
                              color: FlutterFlowTheme.of(context).primary,
                              size: 16.0,
                            ),
                            iconPresent: true,
                            iconEndPresent: false,
                            variant: 'ghost',
                            size: 'medium',
                            fullWidth: false,
                            loading: false,
                            disabled: false,
                          ),
                        ),
                      ),
                    ].divide(const SizedBox(height: 16.0)),
                  ),
                ].divide(const SizedBox(height: 32.0)),
              ),
            ),
            Align(
              alignment: const AlignmentDirectional(0.0, -1.0),
              child: SizedBox(
                height: 100.0,
                child: Padding(
                  padding: const EdgeInsetsDirectional.fromSTEB(
                      24.0, 32.0, 24.0, 0.0),
                  child: Container(
                    child: Container(
                      height: 68.0,
                      alignment: const AlignmentDirectional(0.0, 0.0),
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
                              color: FlutterFlowTheme.of(context).onSurface,
                              size: 24.0,
                            ),
                            onPressed: () async {
                              context.goNamed(HomeMapWidget.routeName);
                            },
                          ),
                          ClipRRect(
                            borderRadius: BorderRadius.circular(9999.0),
                            child: BackdropFilter(
                              filter: ImageFilter.blur(
                                sigmaX: 10.0,
                                sigmaY: 10.0,
                              ),
                              child: Container(
                                decoration: BoxDecoration(
                                  color: FlutterFlowTheme.of(context).surface40,
                                  borderRadius: BorderRadius.circular(9999.0),
                                  shape: BoxShape.rectangle,
                                  border: Border.all(
                                    color: Colors.transparent,
                                    width: 1.0,
                                  ),
                                ),
                                child: Padding(
                                  padding: const EdgeInsetsDirectional.fromSTEB(
                                      8.0, 16.0, 8.0, 16.0),
                                  child: Container(
                                    child: Row(
                                      mainAxisSize: MainAxisSize.min,
                                      mainAxisAlignment:
                                          MainAxisAlignment.start,
                                      crossAxisAlignment:
                                          CrossAxisAlignment.center,
                                      children: [
                                        Lottie.asset(
                                          'assets/lottie/orb_pulse.json',
                                          width: 20.0,
                                          height: 20.0,
                                          fit: BoxFit.contain,
                                          animate: true,
                                        ),
                                        Text(
                                          'AURA X ACTIVE',
                                          style: FlutterFlowTheme.of(context)
                                              .labelSmall
                                              .override(
                                                font: TextStyle(
                                                  fontFamily: 'Orbitron',
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
                                                color:
                                                    FlutterFlowTheme.of(context)
                                                        .onSurface,
                                                letterSpacing: 0.0,
                                                fontWeight:
                                                    FlutterFlowTheme.of(context)
                                                        .labelSmall
                                                        .fontWeight,
                                                fontStyle:
                                                    FlutterFlowTheme.of(context)
                                                        .labelSmall
                                                        .fontStyle,
                                                lineHeight: 1.2,
                                              ),
                                        ),
                                      ].divide(const SizedBox(width: 4.0)),
                                    ),
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
            ),
          ],
        ),
      ),
    );
  }
}
