import '/components/route_card/route_card_widget.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/index.dart';
import 'route_comparison_widget.dart' show RouteComparisonWidget;
import 'package:flutter/material.dart';

class RouteComparisonModel extends FlutterFlowModel<RouteComparisonWidget> {
  ///  State fields for stateful widgets in this page.

  // Model for RouteCard.
  late RouteCardModel routeCardModel1;
  // Model for RouteCard.
  late RouteCardModel routeCardModel2;

  @override
  void initState(BuildContext context) {
    routeCardModel1 = createModel(context, () => RouteCardModel());
    routeCardModel2 = createModel(context, () => RouteCardModel());
  }

  @override
  void dispose() {
    routeCardModel1.dispose();
    routeCardModel2.dispose();
  }
}
