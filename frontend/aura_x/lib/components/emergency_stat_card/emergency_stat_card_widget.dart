import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'dart:ui';
import 'package:flutter/material.dart';
import 'emergency_stat_card_model.dart';
export 'emergency_stat_card_model.dart';

class EmergencyStatCardWidget extends StatefulWidget {
  const EmergencyStatCardWidget({
    super.key,
    Color? color,
    this.icon,
    String? label,
    String? value,
  })  : color = color ?? const Color(0x00000000),
        label = label ?? 'ACCURACY',
        value = value ?? '2.4m';

  final Color color;
  final Widget? icon;
  final String label;
  final String value;

  @override
  State<EmergencyStatCardWidget> createState() =>
      _EmergencyStatCardWidgetState();
}

class _EmergencyStatCardWidgetState extends State<EmergencyStatCardWidget> {
  late EmergencyStatCardModel _model;

  @override
  void setState(VoidCallback callback) {
    super.setState(callback);
    _model.onUpdate();
  }

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => EmergencyStatCardModel());
  }

  @override
  void dispose() {
    _model.maybeDispose();

    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return ClipRRect(
      borderRadius: BorderRadius.circular(16.0),
      child: BackdropFilter(
        filter: ImageFilter.blur(
          sigmaX: 8.0,
          sigmaY: 8.0,
        ),
        child: Container(
          decoration: BoxDecoration(
            color: FlutterFlowTheme.of(context).surface40,
            borderRadius: BorderRadius.circular(16.0),
            shape: BoxShape.rectangle,
            border: Border.all(
              color: Colors.transparent,
              width: 1.0,
            ),
          ),
          child: Padding(
            padding: const EdgeInsets.all(16.0),
            child: Container(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                mainAxisAlignment: MainAxisAlignment.start,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    mainAxisSize: MainAxisSize.min,
                    mainAxisAlignment: MainAxisAlignment.start,
                    crossAxisAlignment: CrossAxisAlignment.center,
                    children: [
                      widget.icon!,
                      Text(
                        valueOrDefault<String>(
                          widget.label,
                          'ACCURACY',
                        ),
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
                              fontStyle: FlutterFlowTheme.of(context)
                                  .labelSmall
                                  .fontStyle,
                              lineHeight: 1.2,
                            ),
                      ),
                    ].divide(const SizedBox(width: 4.0)),
                  ),
                  Text(
                    valueOrDefault<String>(
                      widget.value,
                      '2.4m',
                    ),
                    style: FlutterFlowTheme.of(context).titleMedium.override(
                          font: TextStyle(
                            fontFamily: 'Inter',
                            fontWeight: FontWeight.bold,
                            fontStyle: FlutterFlowTheme.of(context)
                                .titleMedium
                                .fontStyle,
                          ),
                          color: FlutterFlowTheme.of(context).primaryText,
                          letterSpacing: 0.0,
                          fontWeight: FontWeight.bold,
                          fontStyle: FlutterFlowTheme.of(context)
                              .titleMedium
                              .fontStyle,
                          lineHeight: 1.4,
                        ),
                  ),
                ].divide(const SizedBox(height: 4.0)),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
