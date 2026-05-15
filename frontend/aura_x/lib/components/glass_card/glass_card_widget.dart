import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'dart:ui';
import 'package:flutter/material.dart';
import 'glass_card_model.dart';
export 'glass_card_model.dart';

class GlassCardWidget extends StatefulWidget {
  const GlassCardWidget({
    super.key,
    double? margin,
    double? padding,
    this.child,
  })  : margin = margin ?? 0.0,
        padding = padding ?? 28.0;

  final double margin;
  final double padding;
  final Widget Function()? child;

  @override
  State<GlassCardWidget> createState() => _GlassCardWidgetState();
}

class _GlassCardWidgetState extends State<GlassCardWidget> {
  late GlassCardModel _model;

  @override
  void setState(VoidCallback callback) {
    super.setState(callback);
    _model.onUpdate();
  }

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => GlassCardModel());
  }

  @override
  void dispose() {
    _model.maybeDispose();

    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return ClipRRect(
      borderRadius: BorderRadius.circular(24.0),
      child: BackdropFilter(
        filter: ImageFilter.blur(
          sigmaX: 8.0,
          sigmaY: 8.0,
        ),
        child: Container(
          decoration: BoxDecoration(
            color: FlutterFlowTheme.of(context).surface40,
            boxShadow: [
              BoxShadow(
                blurRadius: 16.0,
                color: FlutterFlowTheme.of(context).onPrimary40,
                offset: const Offset(
                  0.0,
                  8.0,
                ),
                spreadRadius: 0.0,
              )
            ],
            borderRadius: BorderRadius.circular(24.0),
            shape: BoxShape.rectangle,
            border: Border.all(
              color: FlutterFlowTheme.of(context).surface30,
              width: 1.0,
            ),
          ),
          child: Builder(builder: (_) {
            return widget.child != null
                ? widget.child!()
                : const SizedBox.shrink();
          }),
        ),
      ),
    );
  }
}
