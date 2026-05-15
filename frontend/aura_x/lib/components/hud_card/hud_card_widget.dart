import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'dart:ui';
import 'package:flutter/material.dart';
import 'hud_card_model.dart';
export 'hud_card_model.dart';

class HudCardWidget extends StatefulWidget {
  const HudCardWidget({
    super.key,
    double? margin,
    String? padding,
    this.child,
  })  : margin = margin ?? 16.0,
        padding = padding ?? 'xs';

  final double margin;
  final String padding;
  final Widget Function()? child;

  @override
  State<HudCardWidget> createState() => _HudCardWidgetState();
}

class _HudCardWidgetState extends State<HudCardWidget> {
  late HudCardModel _model;

  @override
  void setState(VoidCallback callback) {
    super.setState(callback);
    _model.onUpdate();
  }

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => HudCardModel());
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
              color: FlutterFlowTheme.of(context).outline20,
              width: 1.0,
            ),
          ),
          child: Padding(
            padding: const EdgeInsets.all(16.0),
            child: Container(
              child: Builder(builder: (_) {
                return widget.child != null
                    ? widget.child!()
                    : const SizedBox.shrink();
              }),
            ),
          ),
        ),
      ),
    );
  }
}
