import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'dart:ui';
import 'package:flutter/material.dart';
import 'reroute_option_model.dart';
export 'reroute_option_model.dart';

class RerouteOptionWidget extends StatefulWidget {
  const RerouteOptionWidget({
    super.key,
    String? desc,
    this.icon,
    String? risk,
    String? time,
    String? title,
    bool? isSafe,
  })  : desc = desc ?? 'Via well-lit main boulevard',
        risk = risk ?? 'LOW RISK',
        time = time ?? '+4 min',
        title = title ?? 'AURA Safe Path',
        isSafe = isSafe ?? true;

  final String desc;
  final Widget? icon;
  final String risk;
  final String time;
  final String title;
  final bool isSafe;

  @override
  State<RerouteOptionWidget> createState() => _RerouteOptionWidgetState();
}

class _RerouteOptionWidgetState extends State<RerouteOptionWidget> {
  late RerouteOptionModel _model;

  @override
  void setState(VoidCallback callback) {
    super.setState(callback);
    _model.onUpdate();
  }

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => RerouteOptionModel());
  }

  @override
  void dispose() {
    _model.maybeDispose();

    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return ClipRRect(
      borderRadius: BorderRadius.circular(16.0),
      child: BackdropFilter(
        filter: ImageFilter.blur(
          sigmaX: 8.0,
          sigmaY: 8.0,
        ),
        child: Container(
          decoration: BoxDecoration(
            color: FlutterFlowTheme.of(context).surface40,
            borderRadius: BorderRadius.circular(16.0),
            shape: BoxShape.rectangle,
            border: Border.all(
              color: widget.isSafe
                  ? FlutterFlowTheme.of(context).success50
                  : const Color(0x00000000),
              width: widget.isSafe ? 1.0 : 1.0,
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
                  Container(
                    width: 48.0,
                    height: 48.0,
                    decoration: BoxDecoration(
                      color: widget.isSafe
                          ? FlutterFlowTheme.of(context).success20
                          : FlutterFlowTheme.of(context).secondaryBackground,
                      borderRadius: BorderRadius.circular(12.0),
                      shape: BoxShape.rectangle,
                    ),
                    alignment: const AlignmentDirectional(0.0, 0.0),
                    child: widget.icon!,
                  ),
                  Expanded(
                    flex: 1,
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      mainAxisAlignment: MainAxisAlignment.start,
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          mainAxisSize: MainAxisSize.max,
                          mainAxisAlignment: MainAxisAlignment.start,
                          crossAxisAlignment: CrossAxisAlignment.center,
                          children: [
                            Expanded(
                              child: Text(
                                valueOrDefault<String>(
                                  widget.title,
                                  'AURA Safe Path',
                                ),
                                maxLines: 1,
                                style: FlutterFlowTheme.of(context)
                                    .bodyLarge
                                    .override(
                                      font: TextStyle(
                                        fontFamily: 'Inter',
                                        fontWeight: FontWeight.bold,
                                        fontStyle: FlutterFlowTheme.of(context)
                                            .bodyLarge
                                            .fontStyle,
                                      ),
                                      color: FlutterFlowTheme.of(context)
                                          .onSurface,
                                      letterSpacing: 0.0,
                                      fontWeight: FontWeight.bold,
                                      fontStyle: FlutterFlowTheme.of(context)
                                          .bodyLarge
                                          .fontStyle,
                                      lineHeight: 1.6,
                                    ),
                                overflow: TextOverflow.ellipsis,
                              ),
                            ),
                            if (valueOrDefault<bool>(
                              widget.isSafe,
                              true,
                            ))
                              Container(
                                decoration: BoxDecoration(
                                  color: widget.isSafe
                                      ? FlutterFlowTheme.of(context).success
                                      : FlutterFlowTheme.of(context).info,
                                  borderRadius: BorderRadius.circular(8.0),
                                  shape: BoxShape.rectangle,
                                ),
                                child: Padding(
                                  padding: const EdgeInsetsDirectional.fromSTEB(
                                      2.0, 4.0, 2.0, 4.0),
                                  child: Container(
                                    child: Text(
                                      'RECOMMENDED',
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
                                                .onSuccess,
                                            fontSize: 10.0,
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
                                  ),
                                ),
                              ),
                          ].divide(const SizedBox(width: 8.0)),
                        ),
                        Text(
                          valueOrDefault<String>(
                            widget.desc,
                            'Via well-lit main boulevard',
                          ),
                          maxLines: 1,
                          style: FlutterFlowTheme.of(context)
                              .bodySmall
                              .override(
                                font: TextStyle(
                                  fontFamily: 'Inter',
                                  fontWeight: FlutterFlowTheme.of(context)
                                      .bodySmall
                                      .fontWeight,
                                  fontStyle: FlutterFlowTheme.of(context)
                                      .bodySmall
                                      .fontStyle,
                                ),
                                color:
                                    FlutterFlowTheme.of(context).secondaryText,
                                letterSpacing: 0.0,
                                fontWeight: FlutterFlowTheme.of(context)
                                    .bodySmall
                                    .fontWeight,
                                fontStyle: FlutterFlowTheme.of(context)
                                    .bodySmall
                                    .fontStyle,
                                lineHeight: 1.5,
                              ),
                          overflow: TextOverflow.ellipsis,
                        ),
                      ].divide(const SizedBox(height: 4.0)),
                    ),
                  ),
                  Column(
                    mainAxisSize: MainAxisSize.min,
                    mainAxisAlignment: MainAxisAlignment.start,
                    crossAxisAlignment: CrossAxisAlignment.end,
                    children: [
                      Text(
                        valueOrDefault<String>(
                          widget.time,
                          '+4 min',
                        ),
                        style:
                            FlutterFlowTheme.of(context).labelMedium.override(
                                  font: TextStyle(
                                    fontFamily: 'Orbitron',
                                    fontWeight: FontWeight.bold,
                                    fontStyle: FlutterFlowTheme.of(context)
                                        .labelMedium
                                        .fontStyle,
                                  ),
                                  color: FlutterFlowTheme.of(context).onSurface,
                                  letterSpacing: 0.0,
                                  fontWeight: FontWeight.bold,
                                  fontStyle: FlutterFlowTheme.of(context)
                                      .labelMedium
                                      .fontStyle,
                                  lineHeight: 1.3,
                                ),
                      ),
                      Text(
                        valueOrDefault<String>(
                          widget.risk,
                          'LOW RISK',
                        ),
                        style: FlutterFlowTheme.of(context).labelSmall.override(
                              font: TextStyle(
                                fontFamily: 'Orbitron',
                                fontWeight: FlutterFlowTheme.of(context)
                                    .labelSmall
                                    .fontWeight,
                                fontStyle: FlutterFlowTheme.of(context)
                                    .labelSmall
                                    .fontStyle,
                              ),
                              color: widget.isSafe
                                  ? FlutterFlowTheme.of(context).success
                                  : FlutterFlowTheme.of(context).warning,
                              letterSpacing: 0.0,
                              fontWeight: FlutterFlowTheme.of(context)
                                  .labelSmall
                                  .fontWeight,
                              fontStyle: FlutterFlowTheme.of(context)
                                  .labelSmall
                                  .fontStyle,
                              lineHeight: 1.2,
                            ),
                      ),
                    ].divide(const SizedBox(height: 4.0)),
                  ),
                ].divide(const SizedBox(width: 16.0)),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
