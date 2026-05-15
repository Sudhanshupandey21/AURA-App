import '/components/button/button_widget.dart';
import '/components/holographic_pulse/holographic_pulse_widget.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/pages/home_map/home_map_widget.dart';
import 'dart:ui';
import 'package:flutter/material.dart';
import 'package:material_palette/material_palette.dart';
import 'splash_screen_model.dart';
export 'splash_screen_model.dart';

class SplashScreenWidget extends StatefulWidget {
  const SplashScreenWidget({super.key});

  static String routeName = 'SplashScreen';
  static String routePath = '/splashScreen';

  @override
  State<SplashScreenWidget> createState() => _SplashScreenWidgetState();
}

class _SplashScreenWidgetState extends State<SplashScreenWidget> {
  late SplashScreenModel _model;
  final scaffoldKey = GlobalKey<ScaffoldState>();
  bool _hasNavigated = false;

  @override
  void initState() {
    super.initState();

    _model = createModel(context, () => SplashScreenModel());

    Future.delayed(const Duration(seconds: 3), () {
      _navigateToHome();
    });
  }

  void _navigateToHome() {
    if (!mounted || _hasNavigated) return;

    _hasNavigated = true;

    context.go(HomeMapWidget.routePath);
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
            RepaintBoundary(
              child: LayoutBuilder(
                builder: (context, constraints) {
                  return FbmGradientShaderFill(
                    width: constraints.maxWidth.isFinite
                        ? constraints.maxWidth
                        : 200.0,
                    height: 200.0,
                    params: ShaderParams(values: {
                      'gradientAngle': 135.0,
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
                      'color1': const Color(0xFF0A0A0A),
                      'color2': const Color(0xFF001524),
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
            ),
            Column(
              mainAxisSize: MainAxisSize.max,
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                const Spacer(flex: 2),
                Column(
                  mainAxisSize: MainAxisSize.min,
                  mainAxisAlignment: MainAxisAlignment.start,
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    Stack(
                      alignment: const AlignmentDirectional(0.0, 0.0),
                      children: [
                        ClipRect(
                          child: ImageFiltered(
                            imageFilter: ImageFilter.blur(
                              sigmaX: 8.0,
                              sigmaY: 8.0,
                            ),
                            child: Container(
                              width: 120.0,
                              height: 120.0,
                              decoration: BoxDecoration(
                                color: FlutterFlowTheme.of(context).primary10,
                                borderRadius: BorderRadius.circular(9999.0),
                                shape: BoxShape.rectangle,
                              ),
                            ),
                          ),
                        ),
                        Container(
                          width: 100.0,
                          height: 100.0,
                          alignment: const AlignmentDirectional(0.0, 0.0),
                          decoration: BoxDecoration(
                            borderRadius: BorderRadius.circular(9999.0),
                            color: FlutterFlowTheme.of(context).primary,
                          ),
                          child: Icon(
                            Icons.shield_rounded,
                            size: 50.0,
                            color:
                                FlutterFlowTheme.of(context).primaryBackground,
                          ),
                        ),
                      ],
                    ),
                    Column(
                      mainAxisSize: MainAxisSize.min,
                      mainAxisAlignment: MainAxisAlignment.start,
                      crossAxisAlignment: CrossAxisAlignment.center,
                      children: [
                        Text(
                          'AURA X',
                          style: FlutterFlowTheme.of(context)
                              .headlineLarge
                              .override(
                                fontFamily: 'Orbitron',
                                color: FlutterFlowTheme.of(context).primary,
                                letterSpacing: 0.0,
                                fontWeight: FontWeight.w900,
                                fontStyle: FlutterFlowTheme.of(context)
                                    .headlineLarge
                                    .fontStyle,
                                lineHeight: 1.2,
                              ),
                        ),
                        Text(
                          'AI URBAN SAFETY OS',
                          style: FlutterFlowTheme.of(context)
                              .labelMedium
                              .override(
                                fontFamily: 'Orbitron',
                                color:
                                    FlutterFlowTheme.of(context).secondaryText,
                                letterSpacing: 0.0,
                                fontWeight: FontWeight.w500,
                                fontStyle: FlutterFlowTheme.of(context)
                                    .labelMedium
                                    .fontStyle,
                                lineHeight: 1.3,
                              ),
                        ),
                      ].divide(const SizedBox(height: 4.0)),
                    ),
                  ].divide(const SizedBox(height: 16.0)),
                ),
                const Spacer(),
                wrapWithModel(
                  model: _model.holographicPulseModel,
                  updateCallback: () => safeSetState(() {}),
                  child: const HolographicPulseWidget(),
                ),
                const Spacer(flex: 2),
                Padding(
                  padding:
                      const EdgeInsetsDirectional.fromSTEB(0.0, 0.0, 0.0, 24.0),
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    mainAxisAlignment: MainAxisAlignment.start,
                    crossAxisAlignment: CrossAxisAlignment.center,
                    children: [
                      Text(
                        'INITIALIZING NEURAL GRID',
                        style: FlutterFlowTheme.of(context).labelSmall.override(
                              font: TextStyle(
                                fontFamily: 'Orbitron',
                                fontWeight: FontWeight.w600,
                                fontStyle: FlutterFlowTheme.of(context)
                                    .labelSmall
                                    .fontStyle,
                              ),
                              color: FlutterFlowTheme.of(context).primary60,
                              letterSpacing: 0.0,
                              fontWeight: FontWeight.w600,
                              fontStyle: FlutterFlowTheme.of(context)
                                  .labelSmall
                                  .fontStyle,
                              lineHeight: 1.2,
                            ),
                      ),
                      ClipRRect(
                        borderRadius: BorderRadius.circular(9999.0),
                        child: Container(
                          width: 200.0,
                          height: 2.0,
                          decoration: BoxDecoration(
                            color: FlutterFlowTheme.of(context).surfaceVariant,
                            borderRadius: BorderRadius.circular(9999.0),
                            shape: BoxShape.rectangle,
                          ),
                          child: Align(
                            alignment: const AlignmentDirectional(-1.0, 0.0),
                            child: Container(
                              width: 80.0,
                              height: 2.0,
                              decoration: BoxDecoration(
                                color: FlutterFlowTheme.of(context).primary,
                                boxShadow: [
                                  BoxShadow(
                                    blurRadius: 10.0,
                                    color: FlutterFlowTheme.of(context).primary,
                                    offset: const Offset(
                                      0.0,
                                      0.0,
                                    ),
                                    spreadRadius: 2.0,
                                  )
                                ],
                                shape: BoxShape.rectangle,
                              ),
                            ),
                          ),
                        ),
                      ),
                    ].divide(const SizedBox(height: 8.0)),
                  ),
                ),
              ].divide(const SizedBox(height: 32.0)),
            ),
            Align(
              alignment: const AlignmentDirectional(0.0, 1.0),
              child: Padding(
                padding: const EdgeInsets.all(24.0),
                child: GestureDetector(
                  onTap: _navigateToHome,
                  child: wrapWithModel(
                    model: _model.buttonModel,
                    updateCallback: () => safeSetState(() {}),
                    child: ButtonWidget(
                      content: 'ENTER SYSTEM',
                      icon: Icon(
                        Icons.arrow_forward_rounded,
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
              ),
            ),
          ],
        ),
      ),
    );
  }
}
