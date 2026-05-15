import '/components/button/button_widget.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'package:flutter/material.dart';
import 'hud_card_child8_model.dart';
export 'hud_card_child8_model.dart';

class HudCardChild8Widget extends StatefulWidget {
  const HudCardChild8Widget({super.key});

  @override
  State<HudCardChild8Widget> createState() => _HudCardChild8WidgetState();
}

class _HudCardChild8WidgetState extends State<HudCardChild8Widget> {
  late HudCardChild8Model _model;

  @override
  void setState(VoidCallback callback) {
    super.setState(callback);
    _model.onUpdate();
  }

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => HudCardChild8Model());
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
        Row(
          mainAxisSize: MainAxisSize.max,
          mainAxisAlignment: MainAxisAlignment.spaceAround,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            Column(
              mainAxisSize: MainAxisSize.min,
              mainAxisAlignment: MainAxisAlignment.start,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Text(
                  'Remaining',
                  style: FlutterFlowTheme.of(context).labelSmall.override(
                        font: TextStyle(
                          fontFamily: 'Orbitron',
                          fontWeight: FlutterFlowTheme.of(context)
                              .labelSmall
                              .fontWeight,
                          fontStyle:
                              FlutterFlowTheme.of(context).labelSmall.fontStyle,
                        ),
                        color: FlutterFlowTheme.of(context).secondaryText,
                        letterSpacing: 0.0,
                        fontWeight:
                            FlutterFlowTheme.of(context).labelSmall.fontWeight,
                        fontStyle:
                            FlutterFlowTheme.of(context).labelSmall.fontStyle,
                        lineHeight: 1.2,
                      ),
                ),
                Row(
                  mainAxisSize: MainAxisSize.max,
                  mainAxisAlignment: MainAxisAlignment.start,
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    Text(
                      '12',
                      style:
                          FlutterFlowTheme.of(context).headlineMedium.override(
                                font: TextStyle(
                                  fontFamily: 'Orbitron',
                                  fontWeight: FontWeight.bold,
                                  fontStyle: FlutterFlowTheme.of(context)
                                      .headlineMedium
                                      .fontStyle,
                                ),
                                color: FlutterFlowTheme.of(context).primaryText,
                                letterSpacing: 0.0,
                                fontWeight: FontWeight.bold,
                                fontStyle: FlutterFlowTheme.of(context)
                                    .headlineMedium
                                    .fontStyle,
                                lineHeight: 1.25,
                              ),
                    ),
                    Text(
                      'min',
                      style: FlutterFlowTheme.of(context).bodyMedium.override(
                            font: TextStyle(
                              fontFamily: 'Inter',
                              fontWeight: FlutterFlowTheme.of(context)
                                  .bodyMedium
                                  .fontWeight,
                              fontStyle: FlutterFlowTheme.of(context)
                                  .bodyMedium
                                  .fontStyle,
                            ),
                            color: FlutterFlowTheme.of(context).secondaryText,
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
                  ].divide(const SizedBox(width: 4.0)),
                ),
              ],
            ),
            Container(
              width: 1.0,
              height: 40.0,
              decoration: BoxDecoration(
                color: FlutterFlowTheme.of(context).alternate,
              ),
            ),
            Column(
              mainAxisSize: MainAxisSize.min,
              mainAxisAlignment: MainAxisAlignment.start,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Text(
                  'Safety Score',
                  style: FlutterFlowTheme.of(context).labelSmall.override(
                        font: TextStyle(
                          fontFamily: 'Orbitron',
                          fontWeight: FlutterFlowTheme.of(context)
                              .labelSmall
                              .fontWeight,
                          fontStyle:
                              FlutterFlowTheme.of(context).labelSmall.fontStyle,
                        ),
                        color: FlutterFlowTheme.of(context).secondaryText,
                        letterSpacing: 0.0,
                        fontWeight:
                            FlutterFlowTheme.of(context).labelSmall.fontWeight,
                        fontStyle:
                            FlutterFlowTheme.of(context).labelSmall.fontStyle,
                        lineHeight: 1.2,
                      ),
                ),
                Row(
                  mainAxisSize: MainAxisSize.min,
                  mainAxisAlignment: MainAxisAlignment.start,
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    Text(
                      '9.8',
                      style:
                          FlutterFlowTheme.of(context).headlineMedium.override(
                                font: TextStyle(
                                  fontFamily: 'Orbitron',
                                  fontWeight: FontWeight.bold,
                                  fontStyle: FlutterFlowTheme.of(context)
                                      .headlineMedium
                                      .fontStyle,
                                ),
                                color: FlutterFlowTheme.of(context).success,
                                letterSpacing: 0.0,
                                fontWeight: FontWeight.bold,
                                fontStyle: FlutterFlowTheme.of(context)
                                    .headlineMedium
                                    .fontStyle,
                                lineHeight: 1.25,
                              ),
                    ),
                    Icon(
                      Icons.help,
                      color: FlutterFlowTheme.of(context).success,
                      size: 20.0,
                    ),
                  ].divide(const SizedBox(width: 4.0)),
                ),
              ],
            ),
          ],
        ),
        Row(
          mainAxisSize: MainAxisSize.max,
          mainAxisAlignment: MainAxisAlignment.start,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            Expanded(
              flex: 1,
              child: wrapWithModel(
                model: _model.buttonModel1,
                updateCallback: () => safeSetState(() {}),
                child: ButtonWidget(
                  content: 'End Trip',
                  icon: Icon(
                    Icons.close_rounded,
                    color: FlutterFlowTheme.of(context).primaryText,
                    size: 16.0,
                  ),
                  iconPresent: true,
                  iconEndPresent: false,
                  variant: 'outline',
                  size: 'medium',
                  fullWidth: false,
                  loading: false,
                  disabled: false,
                ),
              ),
            ),
            Expanded(
              flex: 1,
              child: wrapWithModel(
                model: _model.buttonModel2,
                updateCallback: () => safeSetState(() {}),
                child: ButtonWidget(
                  content: 'AI Insights',
                  icon: Icon(
                    Icons.auto_awesome_rounded,
                    color: FlutterFlowTheme.of(context).onSecondary,
                    size: 16.0,
                  ),
                  iconPresent: true,
                  iconEndPresent: false,
                  variant: 'secondary',
                  size: 'medium',
                  fullWidth: false,
                  loading: false,
                  disabled: false,
                ),
              ),
            ),
          ].divide(const SizedBox(width: 16.0)),
        ),
      ].divide(const SizedBox(height: 24.0)),
    );
  }
}
