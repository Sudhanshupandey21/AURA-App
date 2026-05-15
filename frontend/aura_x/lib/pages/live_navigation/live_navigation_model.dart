import '/components/hud_card2/hud_card2_widget.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'live_navigation_widget.dart' show LiveNavigationWidget;
import 'package:flutter/material.dart';

class LiveNavigationModel extends FlutterFlowModel<LiveNavigationWidget> {
  ///  State fields for stateful widgets in this page.

  // Model for HudCard2.
  late HudCard2Model hudCard2Model1;
  // Model for HudCard2.
  late HudCard2Model hudCard2Model2;
  // Model for HudCard2.
  late HudCard2Model hudCard2Model3;
  // Model for HudCard2.
  late HudCard2Model hudCard2Model4;
  // Model for HudCard2.
  late HudCard2Model hudCard2Model5;

  @override
  void initState(BuildContext context) {
    hudCard2Model1 = createModel(context, () => HudCard2Model());
    hudCard2Model2 = createModel(context, () => HudCard2Model());
    hudCard2Model3 = createModel(context, () => HudCard2Model());
    hudCard2Model4 = createModel(context, () => HudCard2Model());
    hudCard2Model5 = createModel(context, () => HudCard2Model());
  }

  @override
  void dispose() {
    hudCard2Model1.dispose();
    hudCard2Model2.dispose();
    hudCard2Model3.dispose();
    hudCard2Model4.dispose();
    hudCard2Model5.dispose();
  }
}
