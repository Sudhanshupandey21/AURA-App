import '/components/button/button_widget.dart';
import '/components/aura_live_map.dart';
import '/components/incident_type_card/incident_type_card_widget.dart';
import '/components/severity_chip/severity_chip_widget.dart';
import '/components/text_field/text_field_widget.dart';
import '/flutter_flow/flutter_flow_icon_button.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/index.dart';
import 'package:flutter/material.dart';
import 'package:lottie/lottie.dart';
import 'incident_reporting_model.dart';
export 'incident_reporting_model.dart';

class IncidentReportingWidget extends StatefulWidget {
  const IncidentReportingWidget({super.key});

  static String routeName = 'IncidentReporting';
  static String routePath = '/incidentReporting';

  @override
  State<IncidentReportingWidget> createState() =>
      _IncidentReportingWidgetState();
}

class _IncidentReportingWidgetState extends State<IncidentReportingWidget> {
  late IncidentReportingModel _model;

  final scaffoldKey = GlobalKey<ScaffoldState>();

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => IncidentReportingModel());
  }

  @override
  void dispose() {
    _model.dispose();

    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () {
        FocusScope.of(context).unfocus();
        FocusManager.instance.primaryFocus?.unfocus();
      },
      child: Scaffold(
        key: scaffoldKey,
        resizeToAvoidBottomInset: false,
        backgroundColor: FlutterFlowTheme.of(context).primaryBackground,
        body: SingleChildScrollView(
          primary: false,
          child: Column(
            mainAxisSize: MainAxisSize.min,
            mainAxisAlignment: MainAxisAlignment.start,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Padding(
                padding: const EdgeInsets.all(24.0),
                child: Container(
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    mainAxisAlignment: MainAxisAlignment.start,
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                      Row(
                        mainAxisSize: MainAxisSize.max,
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        crossAxisAlignment: CrossAxisAlignment.center,
                        children: [
                          FlutterFlowIconButton(
                            borderRadius: 8.0,
                            buttonSize: 40.0,
                            fillColor: Colors.transparent,
                            icon: Icon(
                              Icons.arrow_back_rounded,
                              color: FlutterFlowTheme.of(context).primaryText,
                              size: 24.0,
                            ),
                            onPressed: () async {
                              context.goNamed(HomeMapWidget.routeName);
                            },
                          ),
                          Text(
                            'REPORT INCIDENT',
                            style: FlutterFlowTheme.of(context)
                                .titleLarge
                                .override(
                                  font: TextStyle(
                                    fontFamily: 'Orbitron',
                                    fontWeight: FontWeight.bold,
                                    fontStyle: FlutterFlowTheme.of(context)
                                        .titleLarge
                                        .fontStyle,
                                  ),
                                  color: FlutterFlowTheme.of(context).error,
                                  letterSpacing: 0.0,
                                  fontWeight: FontWeight.bold,
                                  fontStyle: FlutterFlowTheme.of(context)
                                      .titleLarge
                                      .fontStyle,
                                  lineHeight: 1.3,
                                ),
                          ),
                          FlutterFlowIconButton(
                            borderRadius: 8.0,
                            buttonSize: 40.0,
                            fillColor: Colors.transparent,
                            icon: Icon(
                              Icons.info_outlined,
                              color: FlutterFlowTheme.of(context).secondaryText,
                              size: 24.0,
                            ),
                            onPressed: () {
                              print('IconButton pressed ...');
                            },
                          ),
                        ],
                      ),
                      Container(
                        decoration: BoxDecoration(
                          color: FlutterFlowTheme.of(context).error10,
                          borderRadius: BorderRadius.circular(16.0),
                          shape: BoxShape.rectangle,
                          border: Border.all(
                            color: FlutterFlowTheme.of(context).error30,
                            width: 1.0,
                          ),
                        ),
                        child: Padding(
                          padding: const EdgeInsets.all(16.0),
                          child: Container(
                            child: Row(
                              mainAxisSize: MainAxisSize.max,
                              mainAxisAlignment: MainAxisAlignment.start,
                              crossAxisAlignment: CrossAxisAlignment.center,
                              children: [
                                Lottie.asset(
                                  'assets/lottie/glowing_pulse.json',
                                  width: 40.0,
                                  height: 40.0,
                                  fit: BoxFit.contain,
                                  animate: true,
                                ),
                                Expanded(
                                  flex: 1,
                                  child: Column(
                                    mainAxisSize: MainAxisSize.min,
                                    mainAxisAlignment: MainAxisAlignment.start,
                                    crossAxisAlignment:
                                        CrossAxisAlignment.start,
                                    children: [
                                      Text(
                                        'AI ASSISTANT ACTIVE',
                                        style: FlutterFlowTheme.of(context)
                                            .labelSmall
                                            .override(
                                              font: TextStyle(
                                                fontFamily: 'Orbitron',
                                                fontWeight: FontWeight.bold,
                                                fontStyle:
                                                    FlutterFlowTheme.of(context)
                                                        .labelSmall
                                                        .fontStyle,
                                              ),
                                              color:
                                                  FlutterFlowTheme.of(context)
                                                      .onError,
                                              letterSpacing: 0.0,
                                              fontWeight: FontWeight.bold,
                                              fontStyle:
                                                  FlutterFlowTheme.of(context)
                                                      .labelSmall
                                                      .fontStyle,
                                              lineHeight: 1.2,
                                            ),
                                      ),
                                      Text(
                                        'Your report will immediately update safe routes for 42 nearby users.',
                                        maxLines: 2,
                                        style: FlutterFlowTheme.of(context)
                                            .bodySmall
                                            .override(
                                              font: TextStyle(
                                                fontFamily: 'Inter',
                                                fontWeight:
                                                    FlutterFlowTheme.of(context)
                                                        .bodySmall
                                                        .fontWeight,
                                                fontStyle:
                                                    FlutterFlowTheme.of(context)
                                                        .bodySmall
                                                        .fontStyle,
                                              ),
                                              color:
                                                  FlutterFlowTheme.of(context)
                                                      .onError,
                                              letterSpacing: 0.0,
                                              fontWeight:
                                                  FlutterFlowTheme.of(context)
                                                      .bodySmall
                                                      .fontWeight,
                                              fontStyle:
                                                  FlutterFlowTheme.of(context)
                                                      .bodySmall
                                                      .fontStyle,
                                              lineHeight: 1.5,
                                            ),
                                        overflow: TextOverflow.ellipsis,
                                      ),
                                    ].divide(const SizedBox(height: 4.0)),
                                  ),
                                ),
                              ].divide(const SizedBox(width: 16.0)),
                            ),
                          ),
                        ),
                      ),
                      Column(
                        mainAxisSize: MainAxisSize.min,
                        mainAxisAlignment: MainAxisAlignment.start,
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'WHAT\'S HAPPENING?',
                            style: FlutterFlowTheme.of(context)
                                .titleMedium
                                .override(
                                  font: TextStyle(
                                    fontFamily: 'Inter',
                                    fontWeight: FlutterFlowTheme.of(context)
                                        .titleMedium
                                        .fontWeight,
                                    fontStyle: FlutterFlowTheme.of(context)
                                        .titleMedium
                                        .fontStyle,
                                  ),
                                  color:
                                      FlutterFlowTheme.of(context).primaryText,
                                  letterSpacing: 0.0,
                                  fontWeight: FlutterFlowTheme.of(context)
                                      .titleMedium
                                      .fontWeight,
                                  fontStyle: FlutterFlowTheme.of(context)
                                      .titleMedium
                                      .fontStyle,
                                  lineHeight: 1.4,
                                ),
                          ),
                          Column(
                            mainAxisSize: MainAxisSize.min,
                            mainAxisAlignment: MainAxisAlignment.start,
                            crossAxisAlignment: CrossAxisAlignment.center,
                            children: [
                              Row(
                                mainAxisSize: MainAxisSize.max,
                                mainAxisAlignment: MainAxisAlignment.start,
                                crossAxisAlignment: CrossAxisAlignment.center,
                                children: [
                                  Expanded(
                                    flex: 1,
                                    child: wrapWithModel(
                                      model: _model.incidentTypeCardModel1,
                                      updateCallback: () => safeSetState(() {}),
                                      child: IncidentTypeCardWidget(
                                        icon: Icon(
                                          Icons.gpp_maybe_rounded,
                                          color: FlutterFlowTheme.of(context)
                                              .error,
                                          size: 28.0,
                                        ),
                                        label: 'Harassment',
                                        onTap: 'On Tap',
                                        selected: true,
                                      ),
                                    ),
                                  ),
                                  Expanded(
                                    flex: 1,
                                    child: wrapWithModel(
                                      model: _model.incidentTypeCardModel2,
                                      updateCallback: () => safeSetState(() {}),
                                      child: IncidentTypeCardWidget(
                                        icon: Icon(
                                          Icons.lightbulb_outline_rounded,
                                          color: FlutterFlowTheme.of(context)
                                              .secondaryText,
                                          size: 28.0,
                                        ),
                                        label: 'Poor Lighting',
                                        onTap: 'On Tap',
                                        selected: false,
                                      ),
                                    ),
                                  ),
                                ].divide(const SizedBox(width: 16.0)),
                              ),
                              Row(
                                mainAxisSize: MainAxisSize.max,
                                mainAxisAlignment: MainAxisAlignment.start,
                                crossAxisAlignment: CrossAxisAlignment.center,
                                children: [
                                  Expanded(
                                    flex: 1,
                                    child: wrapWithModel(
                                      model: _model.incidentTypeCardModel3,
                                      updateCallback: () => safeSetState(() {}),
                                      child: IncidentTypeCardWidget(
                                        icon: Icon(
                                          Icons.groups_rounded,
                                          color: FlutterFlowTheme.of(context)
                                              .secondaryText,
                                          size: 28.0,
                                        ),
                                        label: 'Suspicious Crowd',
                                        onTap: 'On Tap',
                                        selected: false,
                                      ),
                                    ),
                                  ),
                                  Expanded(
                                    flex: 1,
                                    child: wrapWithModel(
                                      model: _model.incidentTypeCardModel4,
                                      updateCallback: () => safeSetState(() {}),
                                      child: IncidentTypeCardWidget(
                                        icon: Icon(
                                          Icons.warning_amber_rounded,
                                          color: FlutterFlowTheme.of(context)
                                              .secondaryText,
                                          size: 28.0,
                                        ),
                                        label: 'Other Threat',
                                        onTap: 'On Tap',
                                        selected: false,
                                      ),
                                    ),
                                  ),
                                ].divide(const SizedBox(width: 16.0)),
                              ),
                            ].divide(const SizedBox(height: 16.0)),
                          ),
                        ].divide(const SizedBox(height: 16.0)),
                      ),
                      Column(
                        mainAxisSize: MainAxisSize.min,
                        mainAxisAlignment: MainAxisAlignment.start,
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'SEVERITY LEVEL',
                            style: FlutterFlowTheme.of(context)
                                .titleMedium
                                .override(
                                  font: TextStyle(
                                    fontFamily: 'Inter',
                                    fontWeight: FlutterFlowTheme.of(context)
                                        .titleMedium
                                        .fontWeight,
                                    fontStyle: FlutterFlowTheme.of(context)
                                        .titleMedium
                                        .fontStyle,
                                  ),
                                  color:
                                      FlutterFlowTheme.of(context).primaryText,
                                  letterSpacing: 0.0,
                                  fontWeight: FlutterFlowTheme.of(context)
                                      .titleMedium
                                      .fontWeight,
                                  fontStyle: FlutterFlowTheme.of(context)
                                      .titleMedium
                                      .fontStyle,
                                  lineHeight: 1.4,
                                ),
                          ),
                          Row(
                            mainAxisSize: MainAxisSize.max,
                            mainAxisAlignment: MainAxisAlignment.start,
                            crossAxisAlignment: CrossAxisAlignment.center,
                            children: [
                              Expanded(
                                flex: 1,
                                child: wrapWithModel(
                                  model: _model.severityChipModel1,
                                  updateCallback: () => safeSetState(() {}),
                                  child: const SeverityChipWidget(
                                    color: 'success',
                                    label: 'LOW',
                                    onTap: 'On Tap',
                                    active: false,
                                  ),
                                ),
                              ),
                              Expanded(
                                flex: 1,
                                child: wrapWithModel(
                                  model: _model.severityChipModel2,
                                  updateCallback: () => safeSetState(() {}),
                                  child: const SeverityChipWidget(
                                    color: 'warning',
                                    label: 'MEDIUM',
                                    onTap: 'On Tap',
                                    active: false,
                                  ),
                                ),
                              ),
                              Expanded(
                                flex: 1,
                                child: wrapWithModel(
                                  model: _model.severityChipModel3,
                                  updateCallback: () => safeSetState(() {}),
                                  child: const SeverityChipWidget(
                                    color: 'error',
                                    label: 'CRITICAL',
                                    onTap: 'On Tap',
                                    active: true,
                                  ),
                                ),
                              ),
                            ].divide(const SizedBox(width: 16.0)),
                          ),
                        ].divide(const SizedBox(height: 16.0)),
                      ),
                      Column(
                        mainAxisSize: MainAxisSize.min,
                        mainAxisAlignment: MainAxisAlignment.start,
                        crossAxisAlignment: CrossAxisAlignment.stretch,
                        children: [
                          Text(
                            'INCIDENT LOCATION',
                            style: FlutterFlowTheme.of(context)
                                .titleMedium
                                .override(
                                  font: TextStyle(
                                    fontFamily: 'Inter',
                                    fontWeight: FlutterFlowTheme.of(context)
                                        .titleMedium
                                        .fontWeight,
                                    fontStyle: FlutterFlowTheme.of(context)
                                        .titleMedium
                                        .fontStyle,
                                  ),
                                  color:
                                      FlutterFlowTheme.of(context).primaryText,
                                  letterSpacing: 0.0,
                                  fontWeight: FlutterFlowTheme.of(context)
                                      .titleMedium
                                      .fontWeight,
                                  fontStyle: FlutterFlowTheme.of(context)
                                      .titleMedium
                                      .fontStyle,
                                  lineHeight: 1.4,
                                ),
                          ),
                          ClipRRect(
                            borderRadius: BorderRadius.circular(16.0),
                            child: Container(
                              height: 160.0,
                              decoration: BoxDecoration(
                                borderRadius: BorderRadius.circular(16.0),
                                shape: BoxShape.rectangle,
                                border: Border.all(
                                  color: FlutterFlowTheme.of(context).alternate,
                                  width: 1.0,
                                ),
                              ),
                              child: Stack(
                                alignment:
                                    const AlignmentDirectional(-1.0, -1.0),
                                children: [
                                  const SizedBox(
                                    height: 160.0,
                                    child: AuraLiveMap(
                                      initialZoom: 15,
                                      followCurrentLocation: true,
                                      showLoadingFallback: false,
                                    ),
                                  ),
                                  Container(
                                    decoration: const BoxDecoration(
                                      color: Color(0x66081018),
                                      shape: BoxShape.rectangle,
                                    ),
                                    alignment:
                                        const AlignmentDirectional(0.0, 0.0),
                                    child: Row(
                                      mainAxisSize: MainAxisSize.min,
                                      mainAxisAlignment:
                                          MainAxisAlignment.start,
                                      crossAxisAlignment:
                                          CrossAxisAlignment.center,
                                      children: [
                                        Icon(
                                          Icons.location_on_rounded,
                                          color: FlutterFlowTheme.of(context)
                                              .error,
                                          size: 24.0,
                                        ),
                                        Text(
                                          'Current Location',
                                          style: FlutterFlowTheme.of(context)
                                              .labelLarge
                                              .override(
                                                font: TextStyle(
                                                  fontFamily: 'Orbitron',
                                                  fontWeight: FontWeight.bold,
                                                  fontStyle:
                                                      FlutterFlowTheme.of(
                                                              context)
                                                          .labelLarge
                                                          .fontStyle,
                                                ),
                                                color:
                                                    FlutterFlowTheme.of(context)
                                                        .onError,
                                                letterSpacing: 0.0,
                                                fontWeight: FontWeight.bold,
                                                fontStyle:
                                                    FlutterFlowTheme.of(context)
                                                        .labelLarge
                                                        .fontStyle,
                                                lineHeight: 1.3,
                                              ),
                                        ),
                                      ].divide(const SizedBox(width: 4.0)),
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          ),
                          wrapWithModel(
                            model: _model.textFieldModel,
                            updateCallback: () => safeSetState(() {}),
                            child: const TextFieldWidget(
                              label: 'ADDITIONAL DETAILS (OPTIONAL)',
                              labelPresent: true,
                              helper: '',
                              helperPresent: false,
                              hint: 'Describe the situation...',
                              value: '',
                              onChange: '',
                              onSubmit: '',
                              leadingIconPresent: false,
                              trailingIconPresent: false,
                              variant: 'filled',
                              error: false,
                            ),
                          ),
                        ].divide(const SizedBox(height: 16.0)),
                      ),
                      Padding(
                        padding: const EdgeInsetsDirectional.fromSTEB(
                            0.0, 0.0, 0.0, 32.0),
                        child: Column(
                          mainAxisSize: MainAxisSize.min,
                          mainAxisAlignment: MainAxisAlignment.start,
                          crossAxisAlignment: CrossAxisAlignment.center,
                          children: [
                            InkWell(
                              splashColor: Colors.transparent,
                              focusColor: Colors.transparent,
                              hoverColor: Colors.transparent,
                              highlightColor: Colors.transparent,
                              onTap: () {
                                ScaffoldMessenger.of(context).showSnackBar(
                                  const SnackBar(
                                    content: Text(
                                        'Incident report transmitted successfully!'),
                                    duration: Duration(seconds: 2),
                                  ),
                                );
                                // TODO: Implement incident report submission
                                context.goNamed(HomeMapWidget.routeName);
                              },
                              child: wrapWithModel(
                                model: _model.buttonModel1,
                                updateCallback: () => safeSetState(() {}),
                                child: ButtonWidget(
                                  content: 'TRANSMIT REPORT',
                                  icon: Icon(
                                    Icons.sensors_rounded,
                                    color: FlutterFlowTheme.of(context).onError,
                                    size: 16.0,
                                  ),
                                  iconPresent: true,
                                  iconEndPresent: false,
                                  variant: 'destructive',
                                  size: 'large',
                                  fullWidth: true,
                                  loading: false,
                                  disabled: false,
                                ),
                              ),
                            ),
                            InkWell(
                              splashColor: Colors.transparent,
                              focusColor: Colors.transparent,
                              hoverColor: Colors.transparent,
                              highlightColor: Colors.transparent,
                              onTap: () {
                                context.goNamed(HomeMapWidget.routeName);
                              },
                              child: wrapWithModel(
                                model: _model.buttonModel2,
                                updateCallback: () => safeSetState(() {}),
                                child: const ButtonWidget(
                                  content: 'DISCARD',
                                  iconPresent: false,
                                  iconEndPresent: false,
                                  variant: 'ghost',
                                  size: 'medium',
                                  fullWidth: true,
                                  loading: false,
                                  disabled: false,
                                ),
                              ),
                            ),
                          ].divide(const SizedBox(height: 16.0)),
                        ),
                      ),
                      Container(
                        child: Padding(
                          padding: const EdgeInsets.all(24.0),
                          child: Container(
                            child: Container(
                              alignment: const AlignmentDirectional(0.0, 0.0),
                              child: Row(
                                mainAxisSize: MainAxisSize.min,
                                mainAxisAlignment: MainAxisAlignment.start,
                                crossAxisAlignment: CrossAxisAlignment.center,
                                children: [
                                  Icon(
                                    Icons.emergency_rounded,
                                    color: FlutterFlowTheme.of(context).error50,
                                    size: 16.0,
                                  ),
                                  Text(
                                    'TAP AND HOLD FOR 3S FOR DIRECT POLICE SOS',
                                    style: FlutterFlowTheme.of(context)
                                        .labelSmall
                                        .override(
                                          font: TextStyle(
                                            fontFamily: 'Orbitron',
                                            fontWeight:
                                                FlutterFlowTheme.of(context)
                                                    .labelSmall
                                                    .fontWeight,
                                            fontStyle:
                                                FlutterFlowTheme.of(context)
                                                    .labelSmall
                                                    .fontStyle,
                                          ),
                                          color: FlutterFlowTheme.of(context)
                                              .secondaryText,
                                          letterSpacing: 0.0,
                                          fontWeight:
                                              FlutterFlowTheme.of(context)
                                                  .labelSmall
                                                  .fontWeight,
                                          fontStyle:
                                              FlutterFlowTheme.of(context)
                                                  .labelSmall
                                                  .fontStyle,
                                          lineHeight: 1.2,
                                        ),
                                  ),
                                ].divide(const SizedBox(width: 8.0)),
                              ),
                            ),
                          ),
                        ),
                      ),
                    ].divide(const SizedBox(height: 32.0)),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
