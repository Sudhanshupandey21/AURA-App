import '/components/button/button_widget.dart';
import '/components/incident_type_card/incident_type_card_widget.dart';
import '/components/severity_chip/severity_chip_widget.dart';
import '/components/text_field/text_field_widget.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/index.dart';
import 'incident_reporting_widget.dart' show IncidentReportingWidget;
import 'package:flutter/material.dart';

class IncidentReportingModel extends FlutterFlowModel<IncidentReportingWidget> {
  ///  State fields for stateful widgets in this page.

  // Model for IncidentTypeCard.
  late IncidentTypeCardModel incidentTypeCardModel1;
  // Model for IncidentTypeCard.
  late IncidentTypeCardModel incidentTypeCardModel2;
  // Model for IncidentTypeCard.
  late IncidentTypeCardModel incidentTypeCardModel3;
  // Model for IncidentTypeCard.
  late IncidentTypeCardModel incidentTypeCardModel4;
  // Model for SeverityChip.
  late SeverityChipModel severityChipModel1;
  // Model for SeverityChip.
  late SeverityChipModel severityChipModel2;
  // Model for SeverityChip.
  late SeverityChipModel severityChipModel3;
  // Model for TextField.
  late TextFieldModel textFieldModel;
  // Model for Button.
  late ButtonModel buttonModel1;
  // Model for Button.
  late ButtonModel buttonModel2;

  @override
  void initState(BuildContext context) {
    incidentTypeCardModel1 =
        createModel(context, () => IncidentTypeCardModel());
    incidentTypeCardModel2 =
        createModel(context, () => IncidentTypeCardModel());
    incidentTypeCardModel3 =
        createModel(context, () => IncidentTypeCardModel());
    incidentTypeCardModel4 =
        createModel(context, () => IncidentTypeCardModel());
    severityChipModel1 = createModel(context, () => SeverityChipModel());
    severityChipModel2 = createModel(context, () => SeverityChipModel());
    severityChipModel3 = createModel(context, () => SeverityChipModel());
    textFieldModel = createModel(context, () => TextFieldModel());
    buttonModel1 = createModel(context, () => ButtonModel());
    buttonModel2 = createModel(context, () => ButtonModel());
  }

  @override
  void dispose() {
    incidentTypeCardModel1.dispose();
    incidentTypeCardModel2.dispose();
    incidentTypeCardModel3.dispose();
    incidentTypeCardModel4.dispose();
    severityChipModel1.dispose();
    severityChipModel2.dispose();
    severityChipModel3.dispose();
    textFieldModel.dispose();
    buttonModel1.dispose();
    buttonModel2.dispose();
  }
}
