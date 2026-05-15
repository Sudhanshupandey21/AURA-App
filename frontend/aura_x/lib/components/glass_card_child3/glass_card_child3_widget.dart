import '/components/contact_tile/contact_tile_widget.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'package:flutter/material.dart';
import 'glass_card_child3_model.dart';
export 'glass_card_child3_model.dart';

class GlassCardChild3Widget extends StatefulWidget {
  const GlassCardChild3Widget({super.key});

  @override
  State<GlassCardChild3Widget> createState() => _GlassCardChild3WidgetState();
}

class _GlassCardChild3WidgetState extends State<GlassCardChild3Widget> {
  late GlassCardChild3Model _model;

  @override
  void setState(VoidCallback callback) {
    super.setState(callback);
    _model.onUpdate();
  }

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => GlassCardChild3Model());
  }

  @override
  void dispose() {
    _model.maybeDispose();

    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisSize: MainAxisSize.min,
      mainAxisAlignment: MainAxisAlignment.start,
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        wrapWithModel(
          model: _model.contactTileModel1,
          updateCallback: () => safeSetState(() {}),
          child: const ContactTileWidget(
            initials: 'MS',
            name: 'Marcus Sterling',
            relation: 'Husband • Primary',
          ),
        ),
        Divider(
          height: 16.0,
          thickness: 1.0,
          indent: 0.0,
          endIndent: 0.0,
          color: FlutterFlowTheme.of(context).divider20,
        ),
        wrapWithModel(
          model: _model.contactTileModel2,
          updateCallback: () => safeSetState(() {}),
          child: const ContactTileWidget(
            initials: 'JL',
            name: 'Janet Lawson',
            relation: 'Sister • Secondary',
          ),
        ),
      ],
    );
  }
}
