import '/components/button/button_widget.dart';
import '/components/input_label/input_label_widget.dart';
import '/components/text_field/text_field_widget.dart';
import '/flutter_flow/flutter_flow_icon_button.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'package:flutter/material.dart';
import 'glass_card_child_model.dart';
export 'glass_card_child_model.dart';

class GlassCardChildWidget extends StatefulWidget {
  const GlassCardChildWidget({super.key});

  @override
  State<GlassCardChildWidget> createState() => _GlassCardChildWidgetState();
}

class _GlassCardChildWidgetState extends State<GlassCardChildWidget> {
  late GlassCardChildModel _model;

  @override
  void setState(VoidCallback callback) {
    super.setState(callback);
    _model.onUpdate();
  }

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => GlassCardChildModel());
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
        Container(
          decoration: BoxDecoration(
            color: FlutterFlowTheme.of(context).background60,
            borderRadius: BorderRadius.circular(24.0),
            shape: BoxShape.rectangle,
            border: Border.all(
              color: FlutterFlowTheme.of(context).alternate,
              width: 1.0,
            ),
          ),
          child: Padding(
            padding: const EdgeInsets.all(4.0),
            child: Container(
              child: Row(
                mainAxisSize: MainAxisSize.max,
                mainAxisAlignment: MainAxisAlignment.start,
                crossAxisAlignment: CrossAxisAlignment.center,
                children: [
                  Expanded(
                    flex: 1,
                    child: Container(
                      decoration: BoxDecoration(
                        color: FlutterFlowTheme.of(context).secondaryBackground,
                        borderRadius: BorderRadius.circular(24.0),
                        shape: BoxShape.rectangle,
                        border: Border.all(
                          color: FlutterFlowTheme.of(context).primary50,
                          width: 1.0,
                        ),
                      ),
                      child: Padding(
                        padding: const EdgeInsetsDirectional.fromSTEB(
                            0.0, 12.0, 0.0, 12.0),
                        child: Container(
                          child: Container(
                            alignment: const AlignmentDirectional(0.0, 0.0),
                            child: Text(
                              'SIGN IN',
                              style: FlutterFlowTheme.of(context)
                                  .labelLarge
                                  .override(
                                    font: TextStyle(
                                      fontFamily: 'Orbitron',
                                      fontWeight: FontWeight.bold,
                                      fontStyle: FlutterFlowTheme.of(context)
                                          .labelLarge
                                          .fontStyle,
                                    ),
                                    color: FlutterFlowTheme.of(context).primary,
                                    letterSpacing: 0.0,
                                    fontWeight: FontWeight.bold,
                                    fontStyle: FlutterFlowTheme.of(context)
                                        .labelLarge
                                        .fontStyle,
                                    lineHeight: 1.3,
                                  ),
                            ),
                          ),
                        ),
                      ),
                    ),
                  ),
                  Expanded(
                    flex: 1,
                    child: Container(
                      child: Padding(
                        padding: const EdgeInsetsDirectional.fromSTEB(
                            0.0, 12.0, 0.0, 12.0),
                        child: Container(
                          child: Container(
                            alignment: const AlignmentDirectional(0.0, 0.0),
                            child: Text(
                              'REGISTER',
                              style: FlutterFlowTheme.of(context)
                                  .labelLarge
                                  .override(
                                    font: TextStyle(
                                      fontFamily: 'Orbitron',
                                      fontWeight: FlutterFlowTheme.of(context)
                                          .labelLarge
                                          .fontWeight,
                                      fontStyle: FlutterFlowTheme.of(context)
                                          .labelLarge
                                          .fontStyle,
                                    ),
                                    color: FlutterFlowTheme.of(context)
                                        .secondaryText,
                                    letterSpacing: 0.0,
                                    fontWeight: FlutterFlowTheme.of(context)
                                        .labelLarge
                                        .fontWeight,
                                    fontStyle: FlutterFlowTheme.of(context)
                                        .labelLarge
                                        .fontStyle,
                                    lineHeight: 1.3,
                                  ),
                            ),
                          ),
                        ),
                      ),
                    ),
                  ),
                ].divide(const SizedBox(width: 0.0)),
              ),
            ),
          ),
        ),
        Column(
          mainAxisSize: MainAxisSize.min,
          mainAxisAlignment: MainAxisAlignment.start,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            Column(
              mainAxisSize: MainAxisSize.min,
              mainAxisAlignment: MainAxisAlignment.start,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                wrapWithModel(
                  model: _model.inputLabelModel1,
                  updateCallback: () => safeSetState(() {}),
                  child: InputLabelWidget(
                    color: FlutterFlowTheme.of(context).primary,
                    label: 'SECURE IDENTITY',
                  ),
                ),
                wrapWithModel(
                  model: _model.textFieldModel1,
                  updateCallback: () => safeSetState(() {}),
                  child: TextFieldWidget(
                    label: '',
                    labelPresent: false,
                    helper: '',
                    helperPresent: false,
                    hint: 'Neural ID or Email',
                    value: '',
                    onChange: '',
                    onSubmit: '',
                    leadingIcon: Icon(
                      Icons.fingerprint_rounded,
                      color: FlutterFlowTheme.of(context).primaryText,
                      size: 16.0,
                    ),
                    leadingIconPresent: true,
                    trailingIconPresent: false,
                    variant: 'ghost',
                    error: false,
                  ),
                ),
              ],
            ),
            Column(
              mainAxisSize: MainAxisSize.min,
              mainAxisAlignment: MainAxisAlignment.start,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                wrapWithModel(
                  model: _model.inputLabelModel2,
                  updateCallback: () => safeSetState(() {}),
                  child: InputLabelWidget(
                    color: FlutterFlowTheme.of(context).primary,
                    label: 'ENCRYPTION KEY',
                  ),
                ),
                wrapWithModel(
                  model: _model.textFieldModel2,
                  updateCallback: () => safeSetState(() {}),
                  child: TextFieldWidget(
                    label: '',
                    labelPresent: false,
                    helper: '',
                    helperPresent: false,
                    hint: 'Enter Passcode',
                    value: '',
                    onChange: '',
                    onSubmit: '',
                    leadingIcon: Icon(
                      Icons.lock_rounded,
                      color: FlutterFlowTheme.of(context).primaryText,
                      size: 16.0,
                    ),
                    leadingIconPresent: true,
                    trailingIcon: Icon(
                      Icons.visibility_off_rounded,
                      color: FlutterFlowTheme.of(context).primaryText,
                      size: 16.0,
                    ),
                    trailingIconPresent: true,
                    variant: 'ghost',
                    error: false,
                  ),
                ),
              ],
            ),
          ].divide(const SizedBox(height: 16.0)),
        ),
        Column(
          mainAxisSize: MainAxisSize.min,
          mainAxisAlignment: MainAxisAlignment.start,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            wrapWithModel(
              model: _model.buttonModel,
              updateCallback: () => safeSetState(() {}),
              child: ButtonWidget(
                content: 'INITIALIZE INTERFACE',
                icon: Icon(
                  Icons.bolt_rounded,
                  color: FlutterFlowTheme.of(context).onPrimary,
                  size: 16.0,
                ),
                iconPresent: true,
                iconEndPresent: false,
                variant: 'primary',
                size: 'large',
                fullWidth: true,
                loading: false,
                disabled: false,
              ),
            ),
            Row(
              mainAxisSize: MainAxisSize.max,
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Text(
                  'FORGOT ACCESS KEY?',
                  style: FlutterFlowTheme.of(context).labelSmall.override(
                        font: TextStyle(
                          fontFamily: 'Orbitron',
                          fontWeight: FlutterFlowTheme.of(context)
                              .labelSmall
                              .fontWeight,
                          fontStyle:
                              FlutterFlowTheme.of(context).labelSmall.fontStyle,
                        ),
                        color: FlutterFlowTheme.of(context).secondaryText,
                        letterSpacing: 0.0,
                        fontWeight:
                            FlutterFlowTheme.of(context).labelSmall.fontWeight,
                        fontStyle:
                            FlutterFlowTheme.of(context).labelSmall.fontStyle,
                        decoration: TextDecoration.underline,
                        lineHeight: 1.2,
                      ),
                ),
              ],
            ),
          ].divide(const SizedBox(height: 16.0)),
        ),
        Column(
          mainAxisSize: MainAxisSize.min,
          mainAxisAlignment: MainAxisAlignment.start,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            Divider(
              height: 16.0,
              thickness: 1.0,
              indent: 0.0,
              endIndent: 0.0,
              color: FlutterFlowTheme.of(context).divider30,
            ),
            Align(
              alignment: const AlignmentDirectional(0.0, 0.0),
              child: Text(
                'OR QUICK ACCESS VIA',
                textAlign: TextAlign.center,
                style: FlutterFlowTheme.of(context).labelSmall.override(
                      font: TextStyle(
                        fontFamily: 'Orbitron',
                        fontWeight:
                            FlutterFlowTheme.of(context).labelSmall.fontWeight,
                        fontStyle:
                            FlutterFlowTheme.of(context).labelSmall.fontStyle,
                      ),
                      color: FlutterFlowTheme.of(context).onSecondary,
                      letterSpacing: 0.0,
                      fontWeight:
                          FlutterFlowTheme.of(context).labelSmall.fontWeight,
                      fontStyle:
                          FlutterFlowTheme.of(context).labelSmall.fontStyle,
                      lineHeight: 1.2,
                    ),
              ),
            ),
            Row(
              mainAxisSize: MainAxisSize.min,
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                FlutterFlowIconButton(
                  borderRadius: 9999.0,
                  borderWidth: 1.0,
                  buttonSize: 40.0,
                  fillColor: FlutterFlowTheme.of(context).surface60,
                  icon: Icon(
                    Icons.face_retouching_natural_rounded,
                    color: FlutterFlowTheme.of(context).primary,
                    size: 24.0,
                  ),
                  onPressed: () {
                    print('IconButton pressed ...');
                  },
                ),
                FlutterFlowIconButton(
                  borderRadius: 9999.0,
                  borderWidth: 1.0,
                  buttonSize: 40.0,
                  fillColor: FlutterFlowTheme.of(context).surface60,
                  icon: Icon(
                    Icons.fingerprint_rounded,
                    color: FlutterFlowTheme.of(context).primary,
                    size: 24.0,
                  ),
                  onPressed: () {
                    print('IconButton pressed ...');
                  },
                ),
              ].divide(const SizedBox(width: 24.0)),
            ),
          ].divide(const SizedBox(height: 8.0)),
        ),
      ].divide(const SizedBox(height: 24.0)),
    );
  }
}
