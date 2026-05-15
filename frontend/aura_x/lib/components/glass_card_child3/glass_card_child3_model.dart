import '/components/contact_tile/contact_tile_widget.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'glass_card_child3_widget.dart' show GlassCardChild3Widget;
import 'package:flutter/material.dart';

class GlassCardChild3Model extends FlutterFlowModel<GlassCardChild3Widget> {
  ///  State fields for stateful widgets in this component.

  // Model for ContactTile.
  late ContactTileModel contactTileModel1;
  // Model for ContactTile.
  late ContactTileModel contactTileModel2;

  @override
  void initState(BuildContext context) {
    contactTileModel1 = createModel(context, () => ContactTileModel());
    contactTileModel2 = createModel(context, () => ContactTileModel());
  }

  @override
  void dispose() {
    contactTileModel1.dispose();
    contactTileModel2.dispose();
  }
}
