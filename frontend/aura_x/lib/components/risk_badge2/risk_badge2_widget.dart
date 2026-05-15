import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'package:flutter/material.dart';
import 'risk_badge2_model.dart';
export 'risk_badge2_model.dart';

class RiskBadge2Widget extends StatefulWidget {
  const RiskBadge2Widget({
    super.key,
    Color? color,
    this.icon,
    String? label,
  })  : color = color ?? const Color(0x00000000),
        label = label ?? 'DANGER ZONE AHEAD';

  final Color color;
  final Widget? icon;
  final String label;

  @override
  State<RiskBadge2Widget> createState() => _RiskBadge2WidgetState();
}

class _RiskBadge2WidgetState extends State<RiskBadge2Widget> {
  late RiskBadge2Model _model;

  @override
  void setState(VoidCallback callback) {
    super.setState(callback);
    _model.onUpdate();
  }

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => RiskBadge2Model());
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
        color: valueOrDefault<Color>(
          widget.color,
          FlutterFlowTheme.of(context).error,
        ),
        shape: BoxShape.rectangle,
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        mainAxisAlignment: MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          widget.icon!,
          Text(
            valueOrDefault<String>(
              widget.label,
              'DANGER ZONE AHEAD',
            ),
            style: FlutterFlowTheme.of(context).labelSmall.override(
                  font: TextStyle(
                    fontFamily: 'Orbitron',
                    fontWeight: FontWeight.bold,
                    fontStyle:
                        FlutterFlowTheme.of(context).labelSmall.fontStyle,
                  ),
                  color: valueOrDefault<Color>(
                    widget.color,
                    FlutterFlowTheme.of(context).error,
                  ),
                  letterSpacing: 0.0,
                  fontWeight: FontWeight.bold,
                  fontStyle: FlutterFlowTheme.of(context).labelSmall.fontStyle,
                  lineHeight: 1.2,
                ),
          ),
        ].divide(const SizedBox(width: 4.0)),
      ),
    );
  }
}
