import '/components/button/button_widget.dart';
import '/components/glass_card2/glass_card2_widget.dart';
import '/components/glass_card_child2/glass_card_child2_widget.dart';
import '/components/glass_card_child3/glass_card_child3_widget.dart';
import '/components/glass_card_child4/glass_card_child4_widget.dart';
import '/flutter_flow/flutter_flow_icon_button.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/index.dart';
import 'package:flutter/material.dart';
import 'package:material_palette/material_palette.dart';
import 'profile_safety_analytics_model.dart';
export 'profile_safety_analytics_model.dart';

class ProfileSafetyAnalyticsWidget extends StatefulWidget {
  const ProfileSafetyAnalyticsWidget({super.key});

  static String routeName = 'ProfileSafetyAnalytics';
  static String routePath = '/profileSafetyAnalytics';

  @override
  State<ProfileSafetyAnalyticsWidget> createState() =>
      _ProfileSafetyAnalyticsWidgetState();
}

class _ProfileSafetyAnalyticsWidgetState
    extends State<ProfileSafetyAnalyticsWidget> {
  late ProfileSafetyAnalyticsModel _model;

  final scaffoldKey = GlobalKey<ScaffoldState>();

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => ProfileSafetyAnalyticsModel());
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
                  height: constraints.maxHeight.isFinite
                      ? constraints.maxHeight
                      : 200.0,
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
                    'color0': FlutterFlowTheme.of(context).primaryBackground,
                    'color1': FlutterFlowTheme.of(context).primaryBackground,
                    'color2': const Color(0x1A00F0FF),
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
            SingleChildScrollView(
              primary: false,
              child: Column(
                mainAxisSize: MainAxisSize.min,
                mainAxisAlignment: MainAxisAlignment.start,
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Padding(
                    padding: const EdgeInsetsDirectional.fromSTEB(
                        0.0, 0.0, 0.0, 32.0),
                    child: Container(
                      child: Column(
                        mainAxisSize: MainAxisSize.min,
                        mainAxisAlignment: MainAxisAlignment.start,
                        crossAxisAlignment: CrossAxisAlignment.center,
                        children: [
                          Container(
                            decoration: BoxDecoration(
                              gradient: LinearGradient(
                                colors: [
                                  FlutterFlowTheme.of(context).surface80,
                                  Colors.transparent
                                ],
                                stops: const [0.0, 1.0],
                                begin: const AlignmentDirectional(0.0, -1.0),
                                end: const AlignmentDirectional(0, 1.0),
                              ),
                              shape: BoxShape.rectangle,
                            ),
                            child: Padding(
                              padding: const EdgeInsetsDirectional.fromSTEB(
                                  24.0, 60.0, 24.0, 32.0),
                              child: Container(
                                child: Column(
                                  mainAxisSize: MainAxisSize.min,
                                  mainAxisAlignment: MainAxisAlignment.start,
                                  crossAxisAlignment: CrossAxisAlignment.center,
                                  children: [
                                    Stack(
                                      alignment:
                                          const AlignmentDirectional(0.0, 0.0),
                                      children: [
                                        Container(
                                          width: 104.0,
                                          height: 104.0,
                                          decoration: BoxDecoration(
                                            borderRadius:
                                                BorderRadius.circular(9999.0),
                                            shape: BoxShape.rectangle,
                                            border: Border.all(
                                              color:
                                                  FlutterFlowTheme.of(context)
                                                      .primary,
                                              width: 2.0,
                                            ),
                                          ),
                                          child: Padding(
                                            padding: const EdgeInsets.all(4.0),
                                            child: Container(
                                              child: ClipRRect(
                                                borderRadius:
                                                    BorderRadius.circular(46.0),
                                                child: Container(
                                                  width: 92.0,
                                                  height: 92.0,
                                                  decoration: BoxDecoration(
                                                    color: FlutterFlowTheme.of(
                                                            context)
                                                        .primary,
                                                    borderRadius:
                                                        BorderRadius.circular(
                                                            46.0),
                                                  ),
                                                  alignment:
                                                      const Alignment(0.0, 0.0),
                                                  child: const Icon(
                                                    Icons.person,
                                                    color: Colors.white,
                                                    size: 40.0,
                                                  ),
                                                ),
                                              ),
                                            ),
                                          ),
                                        ),
                                        Align(
                                          alignment: const AlignmentDirectional(
                                              1.0, 1.0),
                                          child: Padding(
                                            padding: const EdgeInsetsDirectional
                                                .fromSTEB(0.0, 0.0, 6.0, 6.0),
                                            child: Container(
                                              alignment:
                                                  const AlignmentDirectional(
                                                      1.0, 1.0),
                                              child: Container(
                                                width: 24.0,
                                                height: 24.0,
                                                decoration: BoxDecoration(
                                                  color: FlutterFlowTheme.of(
                                                          context)
                                                      .success,
                                                  borderRadius:
                                                      BorderRadius.circular(
                                                          9999.0),
                                                  shape: BoxShape.rectangle,
                                                  border: Border.all(
                                                    color: FlutterFlowTheme.of(
                                                            context)
                                                        .primaryBackground,
                                                    width: 3.0,
                                                  ),
                                                ),
                                              ),
                                            ),
                                          ),
                                        ),
                                      ],
                                    ),
                                    Column(
                                      mainAxisSize: MainAxisSize.min,
                                      mainAxisAlignment:
                                          MainAxisAlignment.start,
                                      crossAxisAlignment:
                                          CrossAxisAlignment.center,
                                      children: [
                                        Text(
                                          'Aria Sterling',
                                          style: FlutterFlowTheme.of(context)
                                              .headlineMedium
                                              .override(
                                                font: TextStyle(
                                                  fontFamily: 'Orbitron',
                                                  fontWeight: FontWeight.bold,
                                                  fontStyle:
                                                      FlutterFlowTheme.of(
                                                              context)
                                                          .headlineMedium
                                                          .fontStyle,
                                                ),
                                                color:
                                                    FlutterFlowTheme.of(context)
                                                        .primaryText,
                                                letterSpacing: 0.0,
                                                fontWeight: FontWeight.bold,
                                                fontStyle:
                                                    FlutterFlowTheme.of(context)
                                                        .headlineMedium
                                                        .fontStyle,
                                                lineHeight: 1.25,
                                              ),
                                        ),
                                        Row(
                                          mainAxisSize: MainAxisSize.max,
                                          mainAxisAlignment:
                                              MainAxisAlignment.center,
                                          crossAxisAlignment:
                                              CrossAxisAlignment.center,
                                          children: [
                                            Icon(
                                              Icons.verified_user_rounded,
                                              color:
                                                  FlutterFlowTheme.of(context)
                                                      .primary,
                                              size: 16.0,
                                            ),
                                            Text(
                                              'AURA LEVEL 98 • ELITE PROTECTOR',
                                              style: FlutterFlowTheme.of(
                                                      context)
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
                                                    color: FlutterFlowTheme.of(
                                                            context)
                                                        .primary,
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
                                          ].divide(const SizedBox(width: 4.0)),
                                        ),
                                      ].divide(const SizedBox(height: 4.0)),
                                    ),
                                  ].divide(const SizedBox(height: 16.0)),
                                ),
                              ),
                            ),
                          ),
                          Padding(
                            padding: const EdgeInsetsDirectional.fromSTEB(
                                24.0, 0.0, 24.0, 0.0),
                            child: Column(
                              mainAxisSize: MainAxisSize.min,
                              mainAxisAlignment: MainAxisAlignment.start,
                              crossAxisAlignment: CrossAxisAlignment.stretch,
                              children: [
                                Padding(
                                  padding: const EdgeInsetsDirectional.fromSTEB(
                                      4.0, 0.0, 0.0, 8.0),
                                  child: Container(
                                    child: Text(
                                      'SAFETY ANALYTICS',
                                      style: FlutterFlowTheme.of(context)
                                          .labelMedium
                                          .override(
                                            font: TextStyle(
                                              fontFamily: 'Orbitron',
                                              fontWeight:
                                                  FlutterFlowTheme.of(context)
                                                      .labelMedium
                                                      .fontWeight,
                                              fontStyle:
                                                  FlutterFlowTheme.of(context)
                                                      .labelMedium
                                                      .fontStyle,
                                            ),
                                            color: FlutterFlowTheme.of(context)
                                                .secondaryText,
                                            letterSpacing: 0.0,
                                            fontWeight:
                                                FlutterFlowTheme.of(context)
                                                    .labelMedium
                                                    .fontWeight,
                                            fontStyle:
                                                FlutterFlowTheme.of(context)
                                                    .labelMedium
                                                    .fontStyle,
                                            lineHeight: 1.3,
                                          ),
                                    ),
                                  ),
                                ),
                                wrapWithModel(
                                  model: _model.glassCard2Model1,
                                  updateCallback: () => safeSetState(() {}),
                                  child: GlassCard2Widget(
                                    child: () => const GlassCardChild2Widget(),
                                  ),
                                ),
                              ],
                            ),
                          ),
                          Padding(
                            padding: const EdgeInsetsDirectional.fromSTEB(
                                0.0, 16.0, 0.0, 0.0),
                            child: Container(
                              child: Padding(
                                padding: const EdgeInsetsDirectional.fromSTEB(
                                    24.0, 0.0, 24.0, 0.0),
                                child: Column(
                                  mainAxisSize: MainAxisSize.min,
                                  mainAxisAlignment: MainAxisAlignment.start,
                                  crossAxisAlignment:
                                      CrossAxisAlignment.stretch,
                                  children: [
                                    Row(
                                      mainAxisSize: MainAxisSize.max,
                                      mainAxisAlignment:
                                          MainAxisAlignment.spaceBetween,
                                      crossAxisAlignment:
                                          CrossAxisAlignment.center,
                                      children: [
                                        Padding(
                                          padding: const EdgeInsetsDirectional
                                              .fromSTEB(4.0, 0.0, 0.0, 8.0),
                                          child: Container(
                                            child: Text(
                                              'EMERGENCY CONTACTS',
                                              style: FlutterFlowTheme.of(
                                                      context)
                                                  .labelMedium
                                                  .override(
                                                    font: TextStyle(
                                                      fontFamily: 'Orbitron',
                                                      fontWeight:
                                                          FlutterFlowTheme.of(
                                                                  context)
                                                              .labelMedium
                                                              .fontWeight,
                                                      fontStyle:
                                                          FlutterFlowTheme.of(
                                                                  context)
                                                              .labelMedium
                                                              .fontStyle,
                                                    ),
                                                    color: FlutterFlowTheme.of(
                                                            context)
                                                        .secondaryText,
                                                    letterSpacing: 0.0,
                                                    fontWeight:
                                                        FlutterFlowTheme.of(
                                                                context)
                                                            .labelMedium
                                                            .fontWeight,
                                                    fontStyle:
                                                        FlutterFlowTheme.of(
                                                                context)
                                                            .labelMedium
                                                            .fontStyle,
                                                    lineHeight: 1.3,
                                                  ),
                                            ),
                                          ),
                                        ),
                                        Text(
                                          'ADD NEW',
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
                                                        .primary,
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
                                      ],
                                    ),
                                    wrapWithModel(
                                      model: _model.glassCard2Model2,
                                      updateCallback: () => safeSetState(() {}),
                                      child: GlassCard2Widget(
                                        child: () =>
                                            const GlassCardChild3Widget(),
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                            ),
                          ),
                          Padding(
                            padding: const EdgeInsetsDirectional.fromSTEB(
                                0.0, 16.0, 0.0, 0.0),
                            child: Container(
                              child: Padding(
                                padding: const EdgeInsetsDirectional.fromSTEB(
                                    24.0, 0.0, 24.0, 0.0),
                                child: Column(
                                  mainAxisSize: MainAxisSize.min,
                                  mainAxisAlignment: MainAxisAlignment.start,
                                  crossAxisAlignment:
                                      CrossAxisAlignment.stretch,
                                  children: [
                                    Padding(
                                      padding:
                                          const EdgeInsetsDirectional.fromSTEB(
                                              4.0, 0.0, 0.0, 8.0),
                                      child: Container(
                                        child: Text(
                                          'AI SENSOR ENGINE',
                                          style: FlutterFlowTheme.of(context)
                                              .labelMedium
                                              .override(
                                                font: TextStyle(
                                                  fontFamily: 'Orbitron',
                                                  fontWeight:
                                                      FlutterFlowTheme.of(
                                                              context)
                                                          .labelMedium
                                                          .fontWeight,
                                                  fontStyle:
                                                      FlutterFlowTheme.of(
                                                              context)
                                                          .labelMedium
                                                          .fontStyle,
                                                ),
                                                color:
                                                    FlutterFlowTheme.of(context)
                                                        .secondaryText,
                                                letterSpacing: 0.0,
                                                fontWeight:
                                                    FlutterFlowTheme.of(context)
                                                        .labelMedium
                                                        .fontWeight,
                                                fontStyle:
                                                    FlutterFlowTheme.of(context)
                                                        .labelMedium
                                                        .fontStyle,
                                                lineHeight: 1.3,
                                              ),
                                        ),
                                      ),
                                    ),
                                    wrapWithModel(
                                      model: _model.glassCard2Model3,
                                      updateCallback: () => safeSetState(() {}),
                                      child: GlassCard2Widget(
                                        child: () =>
                                            const GlassCardChild4Widget(),
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                            ),
                          ),
                          Padding(
                            padding: const EdgeInsets.all(24.0),
                            child: Column(
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
                                            'Safety history log would be displayed here'),
                                        duration: Duration(seconds: 2),
                                      ),
                                    );
                                    // TODO: Implement safety history log view
                                  },
                                  child: wrapWithModel(
                                    model: _model.buttonModel1,
                                    updateCallback: () => safeSetState(() {}),
                                    child: ButtonWidget(
                                      content: 'View Safety History Log',
                                      icon: Icon(
                                        Icons.history_rounded,
                                        color: FlutterFlowTheme.of(context)
                                            .onSecondary,
                                        size: 16.0,
                                      ),
                                      iconPresent: true,
                                      iconEndPresent: false,
                                      variant: 'secondary',
                                      size: 'medium',
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
                                        content:
                                            Text('AURA session deactivated'),
                                        duration: Duration(seconds: 2),
                                      ),
                                    );
                                    // TODO: Implement session deactivation/logout
                                    context
                                        .goNamed(LoginRegisterWidget.routeName);
                                  },
                                  child: wrapWithModel(
                                    model: _model.buttonModel2,
                                    updateCallback: () => safeSetState(() {}),
                                    child: ButtonWidget(
                                      content: 'Deactivate AURA Session',
                                      icon: Icon(
                                        Icons.power_settings_new_rounded,
                                        color: FlutterFlowTheme.of(context)
                                            .primary,
                                        size: 16.0,
                                      ),
                                      iconPresent: true,
                                      iconEndPresent: false,
                                      variant: 'ghost',
                                      size: 'medium',
                                      fullWidth: true,
                                      loading: false,
                                      disabled: false,
                                    ),
                                  ),
                                ),
                              ].divide(const SizedBox(height: 16.0)),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                ],
              ),
            ),
            Align(
              alignment: const AlignmentDirectional(0.0, -1.0),
              child: SizedBox(
                height: 100.0,
                child: Padding(
                  padding: const EdgeInsetsDirectional.fromSTEB(
                      24.0, 40.0, 24.0, 0.0),
                  child: Container(
                    child: Container(
                      height: 60.0,
                      alignment: const AlignmentDirectional(0.0, 0.0),
                      child: Row(
                        mainAxisSize: MainAxisSize.max,
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        crossAxisAlignment: CrossAxisAlignment.center,
                        children: [
                          FlutterFlowIconButton(
                            borderRadius: 8.0,
                            buttonSize: 40.0,
                            fillColor: Colors.transparent,
                            icon: Icon(
                              Icons.arrow_back_ios_new_rounded,
                              color: FlutterFlowTheme.of(context).primaryText,
                              size: 24.0,
                            ),
                            onPressed: () async {
                              context.goNamed(HomeMapWidget.routeName);
                            },
                          ),
                          Text(
                            'AURA IDENTITY',
                            style: FlutterFlowTheme.of(context)
                                .titleMedium
                                .override(
                                  font: TextStyle(
                                    fontFamily: 'Inter',
                                    fontWeight: FontWeight.bold,
                                    fontStyle: FlutterFlowTheme.of(context)
                                        .titleMedium
                                        .fontStyle,
                                  ),
                                  letterSpacing: 0.0,
                                  fontWeight: FontWeight.bold,
                                  fontStyle: FlutterFlowTheme.of(context)
                                      .titleMedium
                                      .fontStyle,
                                  lineHeight: 1.4,
                                ),
                          ),
                          FlutterFlowIconButton(
                            borderRadius: 8.0,
                            buttonSize: 40.0,
                            fillColor: Colors.transparent,
                            icon: Icon(
                              Icons.tune_rounded,
                              color: FlutterFlowTheme.of(context).primaryText,
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
              ),
            ),
          ],
        ),
      ),
    );
  }
}
