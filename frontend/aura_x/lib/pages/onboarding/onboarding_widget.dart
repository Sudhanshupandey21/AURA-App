import '/components/button/button_widget.dart';
import '/components/onboarding_step/onboarding_step_widget.dart';
import '/components/step_indicator/step_indicator_widget.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/index.dart';
import 'package:flutter/material.dart';
import 'package:material_palette/material_palette.dart';
import 'onboarding_model.dart';
export 'onboarding_model.dart';

class OnboardingWidget extends StatefulWidget {
  const OnboardingWidget({super.key});

  static String routeName = 'Onboarding';
  static String routePath = '/onboarding';

  @override
  State<OnboardingWidget> createState() => _OnboardingWidgetState();
}

class _OnboardingWidgetState extends State<OnboardingWidget> {
  late OnboardingModel _model;

  final scaffoldKey = GlobalKey<ScaffoldState>();

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => OnboardingModel());
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
                return RadialTurbulenceGradientShaderFill(
                  width: constraints.maxWidth.isFinite
                      ? constraints.maxWidth
                      : 200.0,
                  height: 200.0,
                  params: ShaderParams(values: {
                    'gradientCenterX': 0.5,
                    'gradientCenterY': 0.2,
                    'gradientScale': 2.03,
                    'gradientOffset': -0.02,
                    'noiseIntensity': 0.51,
                    'ditherStrength': 0.0,
                    'ditherScale': 1.0,
                    'animSpeed': 0.75,
                    'octaves': 3.02,
                    'baseFrequency': 1.94,
                    'noiseScale': 3.9,
                    'colorCount': 3.0,
                    'softness': 1.0,
                    'exposure': 1.0,
                    'contrast': 1.0,
                    'bumpStrength': 1.68,
                    'lightDirX': 0.17,
                    'lightDirY': 0.5,
                    'lightDirZ': 1.0,
                    'lightIntensity': 1.62,
                    'ambient': 0.67,
                    'specular': 0.06,
                    'shininess': 35.72,
                    'metallic': 0.0,
                    'roughness': 1.0,
                    'edgeFade': 2.3,
                    'edgeFadeMode': 1.0
                  }, colors: {
                    'color0': const Color(0xFF0A0A0A),
                    'color1': const Color(0xFF121212),
                    'color2': FlutterFlowTheme.of(context).onPrimary,
                    'color3': const Color(0x00808080),
                    'color4': const Color(0x00808080),
                    'color5': const Color(0x00808080),
                    'color6': const Color(0x00808080),
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
                Padding(
                  padding: const EdgeInsets.all(24.0),
                  child: Row(
                    mainAxisSize: MainAxisSize.max,
                    mainAxisAlignment: MainAxisAlignment.end,
                    crossAxisAlignment: CrossAxisAlignment.center,
                    children: [
                      InkWell(
                        splashColor: Colors.transparent,
                        focusColor: Colors.transparent,
                        hoverColor: Colors.transparent,
                        highlightColor: Colors.transparent,
                        onTap: () {
                          context.goNamed(HomeMapWidget.routeName);
                        },
                        child: wrapWithModel(
                          model: _model.buttonModel1,
                          updateCallback: () => safeSetState(() {}),
                          child: const ButtonWidget(
                            content: 'Skip',
                            iconPresent: false,
                            iconEndPresent: false,
                            variant: 'ghost',
                            size: 'medium',
                            fullWidth: false,
                            loading: false,
                            disabled: false,
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
                Expanded(
                  flex: 1,
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    mainAxisAlignment: MainAxisAlignment.center,
                    crossAxisAlignment: CrossAxisAlignment.center,
                    children: [
                      wrapWithModel(
                        model: _model.onboardingStepModel,
                        updateCallback: () => safeSetState(() {}),
                        child: const OnboardingStepWidget(
                          animDesc: 'assets/lottie/scanning_city.json',
                          description:
                              'AURA X uses real-time urban intelligence to monitor your path and predict risks before they emerge.',
                          title: 'AI Safety Shield',
                        ),
                      ),
                    ],
                  ),
                ),
                Container(
                  child: Padding(
                    padding: const EdgeInsets.all(32.0),
                    child: Container(
                      child: Column(
                        mainAxisSize: MainAxisSize.min,
                        mainAxisAlignment: MainAxisAlignment.start,
                        crossAxisAlignment: CrossAxisAlignment.center,
                        children: [
                          wrapWithModel(
                            model: _model.stepIndicatorModel,
                            updateCallback: () => safeSetState(() {}),
                            child: const StepIndicatorWidget(
                              activeStep: 'option_2',
                            ),
                          ),
                          Column(
                            mainAxisSize: MainAxisSize.min,
                            mainAxisAlignment: MainAxisAlignment.start,
                            crossAxisAlignment: CrossAxisAlignment.stretch,
                            children: [
                              InkWell(
                                splashColor: Colors.transparent,
                                focusColor: Colors.transparent,
                                hoverColor: Colors.transparent,
                                highlightColor: Colors.transparent,
                                onTap: () {
                                  context
                                      .goNamed(LoginRegisterWidget.routeName);
                                },
                                child: wrapWithModel(
                                  model: _model.buttonModel2,
                                  updateCallback: () => safeSetState(() {}),
                                  child: const ButtonWidget(
                                    content: 'Already have an account? Sign In',
                                    iconPresent: false,
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
                  ),
                ),
              ],
            ),
            Align(
              alignment: const AlignmentDirectional(0.0, -1.0),
              child: Container(
                child: Padding(
                  padding: const EdgeInsets.all(24.0),
                  child: Container(
                    child: Row(
                      mainAxisSize: MainAxisSize.max,
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      crossAxisAlignment: CrossAxisAlignment.center,
                      children: [
                        Container(
                          width: 60.0,
                          height: 2.0,
                          decoration: BoxDecoration(
                            color: FlutterFlowTheme.of(context).primary40,
                            borderRadius: BorderRadius.circular(9999.0),
                            shape: BoxShape.rectangle,
                          ),
                        ),
                        Text(
                          'SYSTEM STATUS: ACTIVE',
                          style: FlutterFlowTheme.of(context)
                              .labelSmall
                              .override(
                                font: TextStyle(
                                  fontFamily: 'Orbitron',
                                  fontWeight: FontWeight.bold,
                                  fontStyle: FlutterFlowTheme.of(context)
                                      .labelSmall
                                      .fontStyle,
                                ),
                                color: FlutterFlowTheme.of(context).primary80,
                                letterSpacing: 0.0,
                                fontWeight: FontWeight.bold,
                                fontStyle: FlutterFlowTheme.of(context)
                                    .labelSmall
                                    .fontStyle,
                                lineHeight: 1.2,
                              ),
                        ),
                        Container(
                          width: 60.0,
                          height: 2.0,
                          decoration: BoxDecoration(
                            color: FlutterFlowTheme.of(context).primary40,
                            borderRadius: BorderRadius.circular(9999.0),
                            shape: BoxShape.rectangle,
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ),
            ),
            Align(
              alignment: const AlignmentDirectional(0.0, 1.0),
              child: Padding(
                padding:
                    const EdgeInsetsDirectional.fromSTEB(0.0, 0.0, 0.0, 16.0),
                child: Container(
                  alignment: const AlignmentDirectional(0.0, 1.0),
                  child: Container(
                    width: 120.0,
                    height: 4.0,
                    decoration: BoxDecoration(
                      color: FlutterFlowTheme.of(context).primary20,
                      borderRadius: BorderRadius.circular(9999.0),
                      shape: BoxShape.rectangle,
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
