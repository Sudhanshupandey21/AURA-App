import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'package:flutter/material.dart';
import 'hud_card_child6_model.dart';
export 'hud_card_child6_model.dart';

class HudCardChild6Widget extends StatefulWidget {
  const HudCardChild6Widget({super.key});

  @override
  State<HudCardChild6Widget> createState() => _HudCardChild6WidgetState();
}

class _HudCardChild6WidgetState extends State<HudCardChild6Widget> {
  late HudCardChild6Model _model;

  @override
  void setState(VoidCallback callback) {
    super.setState(callback);
    _model.onUpdate();
  }

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => HudCardChild6Model());
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
        Icon(
          Icons.group_rounded,
          color: FlutterFlowTheme.of(context).info,
          size: 20.0,
        ),
        Text(
          'High',
          style: FlutterFlowTheme.of(context).labelSmall.override(
                font: TextStyle(
                  fontFamily: 'Orbitron',
                  fontWeight:
                      FlutterFlowTheme.of(context).labelSmall.fontWeight,
                  fontStyle: FlutterFlowTheme.of(context).labelSmall.fontStyle,
                ),
                color: FlutterFlowTheme.of(context).primaryText,
                letterSpacing: 0.0,
                fontWeight: FlutterFlowTheme.of(context).labelSmall.fontWeight,
                fontStyle: FlutterFlowTheme.of(context).labelSmall.fontStyle,
                lineHeight: 1.2,
              ),
        ),
        Text(
          'CROWD',
          style: FlutterFlowTheme.of(context).bodyMedium.override(
                font: TextStyle(
                  fontFamily: 'Inter',
                  fontWeight:
                      FlutterFlowTheme.of(context).bodyMedium.fontWeight,
                  fontStyle: FlutterFlowTheme.of(context).bodyMedium.fontStyle,
                ),
                color: FlutterFlowTheme.of(context).secondaryText,
                fontSize: 10.0,
                letterSpacing: 0.0,
                fontWeight: FlutterFlowTheme.of(context).bodyMedium.fontWeight,
                fontStyle: FlutterFlowTheme.of(context).bodyMedium.fontStyle,
                lineHeight: 1.5,
              ),
        ),
      ].divide(const SizedBox(height: 4.0)),
    );
  }
}
