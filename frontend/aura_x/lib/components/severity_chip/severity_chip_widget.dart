import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'package:flutter/material.dart';
import 'severity_chip_model.dart';
export 'severity_chip_model.dart';

class SeverityChipWidget extends StatefulWidget {
  const SeverityChipWidget({
    super.key,
    String? color,
    String? label,
    String? onTap,
    bool? active,
  })  : color = color ?? 'success',
        label = label ?? 'LOW',
        onTap = onTap ?? 'On Tap',
        active = active ?? false;

  final String color;
  final String label;
  final String onTap;
  final bool active;

  @override
  State<SeverityChipWidget> createState() => _SeverityChipWidgetState();
}

class _SeverityChipWidgetState extends State<SeverityChipWidget> {
  late SeverityChipModel _model;

  @override
  void setState(VoidCallback callback) {
    super.setState(callback);
    _model.onUpdate();
  }

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => SeverityChipModel());
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
        color: widget.active
            ? const Color(0x00000000)
            : FlutterFlowTheme.of(context).secondaryBackground,
        borderRadius: BorderRadius.circular(12.0),
        shape: BoxShape.rectangle,
        border: Border.all(
          color: FlutterFlowTheme.of(context).alternate,
          width: 1.0,
        ),
      ),
      child: Padding(
        padding: const EdgeInsets.all(8.0),
        child: Container(
          child: Text(
            valueOrDefault<String>(
              widget.label,
              'LOW',
            ),
            textAlign: TextAlign.center,
            style: FlutterFlowTheme.of(context).labelLarge.override(
                  font: TextStyle(
                    fontFamily: 'Orbitron',
                    fontWeight:
                        FlutterFlowTheme.of(context).labelLarge.fontWeight,
                    fontStyle:
                        FlutterFlowTheme.of(context).labelLarge.fontStyle,
                  ),
                  color: widget.active
                      ? FlutterFlowTheme.of(context).onError
                      : FlutterFlowTheme.of(context).secondaryText,
                  letterSpacing: 0.0,
                  fontWeight:
                      FlutterFlowTheme.of(context).labelLarge.fontWeight,
                  fontStyle: FlutterFlowTheme.of(context).labelLarge.fontStyle,
                  lineHeight: 1.3,
                ),
          ),
        ),
      ),
    );
  }
}
