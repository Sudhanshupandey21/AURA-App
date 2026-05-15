import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'package:flutter/material.dart';
import 'risk_badge_model.dart';
export 'risk_badge_model.dart';

class RiskBadgeWidget extends StatefulWidget {
  const RiskBadgeWidget({
    super.key,
    String? label,
    String? level,
  })  : label = label ?? 'SAFE ZONE',
        level = level ?? 'low';

  final String label;
  final String level;

  @override
  State<RiskBadgeWidget> createState() => _RiskBadgeWidgetState();
}

class _RiskBadgeWidgetState extends State<RiskBadgeWidget> {
  late RiskBadgeModel _model;

  @override
  void setState(VoidCallback callback) {
    super.setState(callback);
    _model.onUpdate();
  }

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => RiskBadgeModel());
  }

  @override
  void dispose() {
    _model.maybeDispose();

    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        color: widget.level == 'med'
            ? const Color(0x00000000)
            : FlutterFlowTheme.of(context).success20,
        borderRadius: BorderRadius.circular(16.0),
        shape: BoxShape.rectangle,
        border: Border.all(
          color: FlutterFlowTheme.of(context).alternate,
          width: 1.0,
        ),
      ),
      child: Padding(
        padding: const EdgeInsetsDirectional.fromSTEB(16.0, 8.0, 16.0, 8.0),
        child: Container(
          child: Row(
            mainAxisSize: MainAxisSize.min,
            mainAxisAlignment: MainAxisAlignment.start,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Container(
                width: 8.0,
                height: 8.0,
                decoration: BoxDecoration(
                  color: widget.level == 'med'
                      ? const Color(0x00000000)
                      : FlutterFlowTheme.of(context).success,
                  borderRadius: BorderRadius.circular(9999.0),
                  shape: BoxShape.rectangle,
                ),
              ),
              Text(
                valueOrDefault<String>(
                  widget.label,
                  'SAFE ZONE',
                ),
                style: FlutterFlowTheme.of(context).labelLarge.override(
                      font: TextStyle(
                        fontFamily: 'Orbitron',
                        fontWeight: FontWeight.bold,
                        fontStyle:
                            FlutterFlowTheme.of(context).labelLarge.fontStyle,
                      ),
                      color: widget.level == 'med'
                          ? const Color(0x00000000)
                          : FlutterFlowTheme.of(context).success,
                      letterSpacing: 0.0,
                      fontWeight: FontWeight.bold,
                      fontStyle:
                          FlutterFlowTheme.of(context).labelLarge.fontStyle,
                      lineHeight: 1.3,
                    ),
              ),
            ].divide(const SizedBox(width: 4.0)),
          ),
        ),
      ),
    );
  }
}
