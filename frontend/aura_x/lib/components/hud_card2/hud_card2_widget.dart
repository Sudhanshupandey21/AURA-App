import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'dart:ui';
import 'package:flutter/material.dart';
import 'hud_card2_model.dart';
export 'hud_card2_model.dart';

class HudCard2Widget extends StatefulWidget {
  const HudCard2Widget({
    super.key,
    String? margin,
    String? padding,
    String? crossAlign,
    this.child,
  })  : margin = margin ?? 'lg',
        padding = padding ?? 'lg',
        crossAlign = crossAlign ?? '';

  final String margin;
  final String padding;
  final String crossAlign;
  final Widget Function()? child;

  @override
  State<HudCard2Widget> createState() => _HudCard2WidgetState();
}

class _HudCard2WidgetState extends State<HudCard2Widget> {
  late HudCard2Model _model;

  @override
  void setState(VoidCallback callback) {
    super.setState(callback);
    _model.onUpdate();
  }

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => HudCard2Model());
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
              color: FlutterFlowTheme.of(context).onSurface10,
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
