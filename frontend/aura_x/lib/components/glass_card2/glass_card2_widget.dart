import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'dart:ui';
import 'package:flutter/material.dart';
import 'glass_card2_model.dart';
export 'glass_card2_model.dart';

class GlassCard2Widget extends StatefulWidget {
  const GlassCard2Widget({
    super.key,
    this.child,
  });

  final Widget Function()? child;

  @override
  State<GlassCard2Widget> createState() => _GlassCard2WidgetState();
}

class _GlassCard2WidgetState extends State<GlassCard2Widget> {
  late GlassCard2Model _model;

  @override
  void setState(VoidCallback callback) {
    super.setState(callback);
    _model.onUpdate();
  }

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => GlassCard2Model());
  }

  @override
  void dispose() {
    _model.maybeDispose();

    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsetsDirectional.fromSTEB(0.0, 0.0, 0.0, 16.0),
      child: Container(
        child: ClipRRect(
          borderRadius: BorderRadius.circular(24.0),
          child: BackdropFilter(
            filter: ImageFilter.blur(
              sigmaX: 8.0,
              sigmaY: 8.0,
            ),
            child: Container(
              decoration: BoxDecoration(
                color: FlutterFlowTheme.of(context).surface40,
                borderRadius: BorderRadius.circular(24.0),
                shape: BoxShape.rectangle,
                border: Border.all(
                  color: FlutterFlowTheme.of(context).outline20,
                  width: 1.0,
                ),
              ),
              child: Padding(
                padding: const EdgeInsets.all(24.0),
                child: Container(
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    mainAxisAlignment: MainAxisAlignment.start,
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                      Builder(builder: (_) {
                        return widget.child != null
                            ? widget.child!()
                            : const SizedBox.shrink();
                      }),
                    ].divide(const SizedBox(height: 16.0)),
                  ),
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
