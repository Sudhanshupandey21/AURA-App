import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'dart:ui';
import 'package:flutter/material.dart';
import 'map_action_model.dart';
export 'map_action_model.dart';

class MapActionWidget extends StatefulWidget {
  const MapActionWidget({
    super.key,
    this.icon,
  });

  final Widget? icon;

  @override
  State<MapActionWidget> createState() => _MapActionWidgetState();
}

class _MapActionWidgetState extends State<MapActionWidget> {
  late MapActionModel _model;

  @override
  void setState(VoidCallback callback) {
    super.setState(callback);
    _model.onUpdate();
  }

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => MapActionModel());
  }

  @override
  void dispose() {
    _model.maybeDispose();

    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return ClipRRect(
      borderRadius: BorderRadius.circular(9999.0),
      child: BackdropFilter(
        filter: ImageFilter.blur(
          sigmaX: 10.0,
          sigmaY: 10.0,
        ),
        child: Container(
          width: 48.0,
          height: 48.0,
          decoration: BoxDecoration(
            color: FlutterFlowTheme.of(context).surface60,
            borderRadius: BorderRadius.circular(9999.0),
            shape: BoxShape.rectangle,
            border: Border.all(
              color: FlutterFlowTheme.of(context).outline30,
              width: 1.0,
            ),
          ),
          alignment: const AlignmentDirectional(0.0, 0.0),
          child: widget.icon!,
        ),
      ),
    );
  }
}
