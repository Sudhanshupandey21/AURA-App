import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'package:flutter/material.dart';
import 'package:lottie/lottie.dart';
import 'package:material_palette/material_palette.dart';
import 'onboarding_step_model.dart';
export 'onboarding_step_model.dart';

class OnboardingStepWidget extends StatefulWidget {
  const OnboardingStepWidget({
    super.key,
    String? animDesc,
    String? description,
    String? title,
  })  : animDesc = animDesc ?? 'assets/lottie/scanning_city.json',
        description = description ??
            'AURA X uses real-time urban intelligence to monitor your path and predict risks before they emerge.',
        title = title ?? 'AI Safety Shield';

  final String animDesc;
  final String description;
  final String title;

  @override
  State<OnboardingStepWidget> createState() => _OnboardingStepWidgetState();
}

class _OnboardingStepWidgetState extends State<OnboardingStepWidget> {
  late OnboardingStepModel _model;

  @override
  void setState(VoidCallback callback) {
    super.setState(callback);
    _model.onUpdate();
  }

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => OnboardingStepModel());
  }

  @override
  void dispose() {
    _model.maybeDispose();

    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisSize: MainAxisSize.min,
      mainAxisAlignment: MainAxisAlignment.start,
      crossAxisAlignment: CrossAxisAlignment.center,
      children: [
        SizedBox(
          width: 380.0,
          height: 380.0,
          child: Stack(
            alignment: const AlignmentDirectional(0.0, 0.0),
            children: [
              LayoutBuilder(
                builder: (context, constraints) {
                  return SimplexGradientShaderFill(
                    width: constraints.maxWidth.isFinite
                        ? constraints.maxWidth
                        : 200.0,
                    height: 200.0,
                    params: ShaderParams(values: {
                      'gradientAngle': 45.0,
                      'gradientScale': 0.89,
                      'gradientOffset': 0.0,
                      'noiseIntensity': 0.32,
                      'ditherStrength': 2.51,
                      'ditherScale': 0.29,
                      'animSpeed': 1.46,
                      'noiseScale': 6.36,
                      'sharpness': 2.2,
                      'colorCount': 6.76,
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
                      'edgeFadeMode': 0.0
                    }, colors: {
                      'color0': FlutterFlowTheme.of(context).primary30,
                      'color1': FlutterFlowTheme.of(context).primaryBackground,
                      'color2': FlutterFlowTheme.of(context).accent20,
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
              Lottie.asset(
                valueOrDefault<String>(
                  widget.animDesc,
                  'assets/lottie/scanning_city.json',
                ),
                width: 300.0,
                height: 300.0,
                fit: BoxFit.contain,
                animate: true,
              ),
            ],
          ),
        ),
        Padding(
          padding: const EdgeInsetsDirectional.fromSTEB(32.0, 0.0, 32.0, 0.0),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            mainAxisAlignment: MainAxisAlignment.start,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Text(
                valueOrDefault<String>(
                  widget.title,
                  'AI Safety Shield',
                ),
                textAlign: TextAlign.center,
                style: FlutterFlowTheme.of(context).headlineLarge.override(
                      font: TextStyle(
                        fontFamily: 'Orbitron',
                        fontWeight: FontWeight.bold,
                        fontStyle: FlutterFlowTheme.of(context)
                            .headlineLarge
                            .fontStyle,
                      ),
                      color: FlutterFlowTheme.of(context).primaryText,
                      letterSpacing: 0.0,
                      fontWeight: FontWeight.bold,
                      fontStyle:
                          FlutterFlowTheme.of(context).headlineLarge.fontStyle,
                      lineHeight: 1.2,
                    ),
              ),
              Text(
                valueOrDefault<String>(
                  widget.description,
                  'AURA X uses real-time urban intelligence to monitor your path and predict risks before they emerge.',
                ),
                textAlign: TextAlign.center,
                style: FlutterFlowTheme.of(context).bodyLarge.override(
                      font: TextStyle(
                        fontFamily: 'Inter',
                        fontWeight:
                            FlutterFlowTheme.of(context).bodyLarge.fontWeight,
                        fontStyle:
                            FlutterFlowTheme.of(context).bodyLarge.fontStyle,
                      ),
                      color: FlutterFlowTheme.of(context).secondaryText,
                      letterSpacing: 0.0,
                      fontWeight:
                          FlutterFlowTheme.of(context).bodyLarge.fontWeight,
                      fontStyle:
                          FlutterFlowTheme.of(context).bodyLarge.fontStyle,
                      lineHeight: 1.5,
                    ),
              ),
            ].divide(const SizedBox(height: 16.0)),
          ),
        ),
      ].divide(const SizedBox(height: 32.0)),
    );
  }
}
