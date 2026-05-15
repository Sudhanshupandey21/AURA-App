import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'package:flutter/material.dart';
import 'package:lottie/lottie.dart';
import 'package:percent_indicator/percent_indicator.dart';
import 'hud_card_child2_model.dart';
export 'hud_card_child2_model.dart';

class HudCardChild2Widget extends StatefulWidget {
  const HudCardChild2Widget({super.key});

  @override
  State<HudCardChild2Widget> createState() => _HudCardChild2WidgetState();
}

class _HudCardChild2WidgetState extends State<HudCardChild2Widget> {
  late HudCardChild2Model _model;

  @override
  void setState(VoidCallback callback) {
    super.setState(callback);
    _model.onUpdate();
  }

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => HudCardChild2Model());
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
          mainAxisAlignment: MainAxisAlignment.start,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            Lottie.asset(
              'assets/lottie/circular_pulse.json',
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
                    'AI ASSISTANT',
                    style: FlutterFlowTheme.of(context).labelMedium.override(
                          font: TextStyle(
                            fontFamily: 'Orbitron',
                            fontWeight: FontWeight.bold,
                            fontStyle: FlutterFlowTheme.of(context)
                                .labelMedium
                                .fontStyle,
                          ),
                          color: FlutterFlowTheme.of(context).primary,
                          letterSpacing: 0.0,
                          fontWeight: FontWeight.bold,
                          fontStyle: FlutterFlowTheme.of(context)
                              .labelMedium
                              .fontStyle,
                          lineHeight: 1.3,
                        ),
                  ),
                  Text(
                    'Safest route to \'Home\' identified. Well-lit streets with 84% crowd density.',
                    maxLines: 2,
                    style: FlutterFlowTheme.of(context).bodySmall.override(
                          font: TextStyle(
                            fontFamily: 'Inter',
                            fontWeight: FlutterFlowTheme.of(context)
                                .bodySmall
                                .fontWeight,
                            fontStyle: FlutterFlowTheme.of(context)
                                .bodySmall
                                .fontStyle,
                          ),
                          color: FlutterFlowTheme.of(context).primaryText,
                          letterSpacing: 0.0,
                          fontWeight:
                              FlutterFlowTheme.of(context).bodySmall.fontWeight,
                          fontStyle:
                              FlutterFlowTheme.of(context).bodySmall.fontStyle,
                          lineHeight: 1.5,
                        ),
                    overflow: TextOverflow.ellipsis,
                  ),
                ],
              ),
            ),
          ].divide(const SizedBox(width: 16.0)),
        ),
        Row(
          mainAxisSize: MainAxisSize.max,
          mainAxisAlignment: MainAxisAlignment.start,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            Expanded(
              flex: 1,
              child: Column(
                mainAxisSize: MainAxisSize.min,
                mainAxisAlignment: MainAxisAlignment.start,
                crossAxisAlignment: CrossAxisAlignment.center,
                children: [
                  Text(
                    'LIGHTING',
                    style: FlutterFlowTheme.of(context).labelSmall.override(
                          font: TextStyle(
                            fontFamily: 'Orbitron',
                            fontWeight: FlutterFlowTheme.of(context)
                                .labelSmall
                                .fontWeight,
                            fontStyle: FlutterFlowTheme.of(context)
                                .labelSmall
                                .fontStyle,
                          ),
                          color: FlutterFlowTheme.of(context).secondaryText,
                          letterSpacing: 0.0,
                          fontWeight: FlutterFlowTheme.of(context)
                              .labelSmall
                              .fontWeight,
                          fontStyle:
                              FlutterFlowTheme.of(context).labelSmall.fontStyle,
                          lineHeight: 1.2,
                        ),
                  ),
                  LinearPercentIndicator(
                    percent: 0.9,
                    lineHeight: 4.0,
                    animation: true,
                    animateFromLastPercent: true,
                    progressColor: FlutterFlowTheme.of(context).success,
                    backgroundColor: FlutterFlowTheme.of(context).alternate,
                    barRadius: const Radius.circular(2.0),
                    padding: EdgeInsets.zero,
                  ),
                ].divide(const SizedBox(height: 4.0)),
              ),
            ),
            Expanded(
              flex: 1,
              child: Column(
                mainAxisSize: MainAxisSize.min,
                mainAxisAlignment: MainAxisAlignment.start,
                crossAxisAlignment: CrossAxisAlignment.center,
                children: [
                  Text(
                    'CROWD',
                    style: FlutterFlowTheme.of(context).labelSmall.override(
                          font: TextStyle(
                            fontFamily: 'Orbitron',
                            fontWeight: FlutterFlowTheme.of(context)
                                .labelSmall
                                .fontWeight,
                            fontStyle: FlutterFlowTheme.of(context)
                                .labelSmall
                                .fontStyle,
                          ),
                          color: FlutterFlowTheme.of(context).secondaryText,
                          letterSpacing: 0.0,
                          fontWeight: FlutterFlowTheme.of(context)
                              .labelSmall
                              .fontWeight,
                          fontStyle:
                              FlutterFlowTheme.of(context).labelSmall.fontStyle,
                          lineHeight: 1.2,
                        ),
                  ),
                  LinearPercentIndicator(
                    percent: 0.6,
                    lineHeight: 4.0,
                    animation: true,
                    animateFromLastPercent: true,
                    progressColor: FlutterFlowTheme.of(context).primary,
                    backgroundColor: FlutterFlowTheme.of(context).alternate,
                    barRadius: const Radius.circular(2.0),
                    padding: EdgeInsets.zero,
                  ),
                ].divide(const SizedBox(height: 4.0)),
              ),
            ),
          ].divide(const SizedBox(width: 16.0)),
        ),
      ].divide(const SizedBox(height: 16.0)),
    );
  }
}
