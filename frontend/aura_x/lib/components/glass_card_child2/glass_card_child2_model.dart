import '/components/metric_item/metric_item_widget.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'glass_card_child2_widget.dart' show GlassCardChild2Widget;
import 'package:flutter/material.dart';

class GlassCardChild2Model extends FlutterFlowModel<GlassCardChild2Widget> {
  ///  State fields for stateful widgets in this component.

  // Model for MetricItem.
  late MetricItemModel metricItemModel1;
  // Model for MetricItem.
  late MetricItemModel metricItemModel2;
  // Model for MetricItem.
  late MetricItemModel metricItemModel3;

  @override
  void initState(BuildContext context) {
    metricItemModel1 = createModel(context, () => MetricItemModel());
    metricItemModel2 = createModel(context, () => MetricItemModel());
    metricItemModel3 = createModel(context, () => MetricItemModel());
  }

  @override
  void dispose() {
    metricItemModel1.dispose();
    metricItemModel2.dispose();
    metricItemModel3.dispose();
  }
}
