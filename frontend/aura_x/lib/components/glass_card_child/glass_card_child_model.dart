import '/components/button/button_widget.dart';
import '/components/input_label/input_label_widget.dart';
import '/components/text_field/text_field_widget.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'glass_card_child_widget.dart' show GlassCardChildWidget;
import 'package:flutter/material.dart';

class GlassCardChildModel extends FlutterFlowModel<GlassCardChildWidget> {
  ///  State fields for stateful widgets in this component.

  // Model for InputLabel.
  late InputLabelModel inputLabelModel1;
  // Model for TextField.
  late TextFieldModel textFieldModel1;
  // Model for InputLabel.
  late InputLabelModel inputLabelModel2;
  // Model for TextField.
  late TextFieldModel textFieldModel2;
  // Model for Button.
  late ButtonModel buttonModel;

  @override
  void initState(BuildContext context) {
    inputLabelModel1 = createModel(context, () => InputLabelModel());
    textFieldModel1 = createModel(context, () => TextFieldModel());
    inputLabelModel2 = createModel(context, () => InputLabelModel());
    textFieldModel2 = createModel(context, () => TextFieldModel());
    buttonModel = createModel(context, () => ButtonModel());
  }

  @override
  void dispose() {
    inputLabelModel1.dispose();
    textFieldModel1.dispose();
    inputLabelModel2.dispose();
    textFieldModel2.dispose();
    buttonModel.dispose();
  }
}
