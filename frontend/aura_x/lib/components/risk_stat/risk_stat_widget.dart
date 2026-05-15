import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'package:flutter/material.dart';
import 'risk_stat_model.dart';
export 'risk_stat_model.dart';

class RiskStatWidget extends StatefulWidget {
  const RiskStatWidget({
    super.key,
    Color? color,
    String? label,
    String? value,
  })  : color = color ?? const Color(0x00000000),
        label = label ?? 'LIGHTING',
        value = value ?? '12%';

  final Color color;
  final String label;
  final String value;

  @override
  State<RiskStatWidget> createState() => _RiskStatWidgetState();
}

class _RiskStatWidgetState extends State<RiskStatWidget> {
  late RiskStatModel _model;

  @override
  void setState(VoidCallback callback) {
    super.setState(callback);
    _model.onUpdate();
  }

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => RiskStatModel());
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
        Text(
          valueOrDefault<String>(
            widget.value,
            '12%',
          ),
          style: FlutterFlowTheme.of(context).titleMedium.override(
                font: TextStyle(
                  fontFamily: 'Inter',
                  fontWeight: FontWeight.bold,
                  fontStyle: FlutterFlowTheme.of(context).titleMedium.fontStyle,
                ),
                color: valueOrDefault<Color>(
                  widget.color,
                  FlutterFlowTheme.of(context).error,
                ),
                letterSpacing: 0.0,
                fontWeight: FontWeight.bold,
                fontStyle: FlutterFlowTheme.of(context).titleMedium.fontStyle,
                lineHeight: 1.4,
              ),
        ),
        Text(
          valueOrDefault<String>(
            widget.label,
            'LIGHTING',
          ),
          style: FlutterFlowTheme.of(context).labelSmall.override(
                font: TextStyle(
                  fontFamily: 'Orbitron',
                  fontWeight:
                      FlutterFlowTheme.of(context).labelSmall.fontWeight,
                  fontStyle: FlutterFlowTheme.of(context).labelSmall.fontStyle,
                ),
                color: FlutterFlowTheme.of(context).onSurface60,
                letterSpacing: 0.0,
                fontWeight: FlutterFlowTheme.of(context).labelSmall.fontWeight,
                fontStyle: FlutterFlowTheme.of(context).labelSmall.fontStyle,
                lineHeight: 1.2,
              ),
        ),
      ].divide(const SizedBox(height: 4.0)),
    );
  }
}
