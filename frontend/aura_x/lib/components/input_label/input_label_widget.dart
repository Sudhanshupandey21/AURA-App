import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'package:flutter/material.dart';
import 'input_label_model.dart';
export 'input_label_model.dart';

class InputLabelWidget extends StatefulWidget {
  const InputLabelWidget({
    super.key,
    Color? color,
    String? label,
  })  : color = color ?? const Color(0x00000000),
        label = label ?? 'SECURE IDENTITY';

  final Color color;
  final String label;

  @override
  State<InputLabelWidget> createState() => _InputLabelWidgetState();
}

class _InputLabelWidgetState extends State<InputLabelWidget> {
  late InputLabelModel _model;

  @override
  void setState(VoidCallback callback) {
    super.setState(callback);
    _model.onUpdate();
  }

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => InputLabelModel());
  }

  @override
  void dispose() {
    _model.maybeDispose();

    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsetsDirectional.fromSTEB(0.0, 0.0, 0.0, 8.0),
      child: Container(
        child: Row(
          mainAxisSize: MainAxisSize.min,
          mainAxisAlignment: MainAxisAlignment.start,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            Container(
              width: 6.0,
              height: 6.0,
              decoration: BoxDecoration(
                color: valueOrDefault<Color>(
                  widget.color,
                  FlutterFlowTheme.of(context).primary,
                ),
                borderRadius: BorderRadius.circular(9999.0),
                shape: BoxShape.rectangle,
              ),
            ),
            Text(
              valueOrDefault<String>(
                widget.label,
                'SECURE IDENTITY',
              ),
              style: FlutterFlowTheme.of(context).labelMedium.override(
                    font: TextStyle(
                      fontFamily: 'Orbitron',
                      fontWeight: FontWeight.bold,
                      fontStyle:
                          FlutterFlowTheme.of(context).labelMedium.fontStyle,
                    ),
                    color: valueOrDefault<Color>(
                      widget.color,
                      FlutterFlowTheme.of(context).primary,
                    ),
                    letterSpacing: 0.0,
                    fontWeight: FontWeight.bold,
                    fontStyle:
                        FlutterFlowTheme.of(context).labelMedium.fontStyle,
                    lineHeight: 1.3,
                  ),
            ),
          ].divide(const SizedBox(width: 4.0)),
        ),
      ),
    );
  }
}
