import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'package:flutter/material.dart';
import 'hud_card_child_model.dart';
export 'hud_card_child_model.dart';

class HudCardChildWidget extends StatefulWidget {
  const HudCardChildWidget({super.key});

  @override
  State<HudCardChildWidget> createState() => _HudCardChildWidgetState();
}

class _HudCardChildWidgetState extends State<HudCardChildWidget> {
  late HudCardChildModel _model;

  @override
  void setState(VoidCallback callback) {
    super.setState(callback);
    _model.onUpdate();
  }

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => HudCardChildModel());
  }

  @override
  void dispose() {
    _model.maybeDispose();

    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      mainAxisAlignment: MainAxisAlignment.start,
      crossAxisAlignment: CrossAxisAlignment.center,
      children: [
        Container(
          width: 36.0,
          height: 36.0,
          decoration: BoxDecoration(
            color: FlutterFlowTheme.of(context).primary,
            shape: BoxShape.circle,
          ),
          alignment: const AlignmentDirectional(0.0, 0.0),
          child: Text(
            'AX',
            textAlign: TextAlign.center,
            maxLines: 1,
            style: FlutterFlowTheme.of(context).labelMedium.override(
                  font: TextStyle(
                    fontFamily: 'Orbitron',
                    fontWeight: FontWeight.w600,
                    fontStyle:
                        FlutterFlowTheme.of(context).labelMedium.fontStyle,
                  ),
                  color: FlutterFlowTheme.of(context).onPrimary,
                  fontSize: 13.68,
                  letterSpacing: 0.0,
                  fontWeight: FontWeight.w600,
                  fontStyle: FlutterFlowTheme.of(context).labelMedium.fontStyle,
                  lineHeight: 1.3,
                ),
            overflow: TextOverflow.clip,
          ),
        ),
        Column(
          mainAxisSize: MainAxisSize.min,
          mainAxisAlignment: MainAxisAlignment.start,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'AURA X ACTIVE',
              style: FlutterFlowTheme.of(context).labelSmall.override(
                    font: TextStyle(
                      fontFamily: 'Orbitron',
                      fontWeight: FontWeight.bold,
                      fontStyle:
                          FlutterFlowTheme.of(context).labelSmall.fontStyle,
                    ),
                    color: FlutterFlowTheme.of(context).primary,
                    letterSpacing: 0.0,
                    fontWeight: FontWeight.bold,
                    fontStyle:
                        FlutterFlowTheme.of(context).labelSmall.fontStyle,
                    lineHeight: 1.2,
                  ),
            ),
            Text(
              'Scanning Environment...',
              style: FlutterFlowTheme.of(context).labelSmall.override(
                    font: TextStyle(
                      fontFamily: 'Orbitron',
                      fontWeight:
                          FlutterFlowTheme.of(context).labelSmall.fontWeight,
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
          ],
        ),
      ].divide(const SizedBox(width: 8.0)),
    );
  }
}
