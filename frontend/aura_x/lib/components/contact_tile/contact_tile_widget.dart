import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'package:flutter/material.dart';
import 'contact_tile_model.dart';
export 'contact_tile_model.dart';

class ContactTileWidget extends StatefulWidget {
  const ContactTileWidget({
    super.key,
    String? initials,
    String? name,
    String? relation,
  })  : initials = initials ?? 'MS',
        name = name ?? 'Marcus Sterling',
        relation = relation ?? 'Husband • Primary';

  final String initials;
  final String name;
  final String relation;

  @override
  State<ContactTileWidget> createState() => _ContactTileWidgetState();
}

class _ContactTileWidgetState extends State<ContactTileWidget> {
  late ContactTileModel _model;

  @override
  void setState(VoidCallback callback) {
    super.setState(callback);
    _model.onUpdate();
  }

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => ContactTileModel());
  }

  @override
  void dispose() {
    _model.maybeDispose();

    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsetsDirectional.fromSTEB(0.0, 8.0, 0.0, 8.0),
      child: Row(
        mainAxisSize: MainAxisSize.max,
        mainAxisAlignment: MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          Container(
            width: 48.0,
            height: 48.0,
            decoration: BoxDecoration(
              color: FlutterFlowTheme.of(context).primary20,
              shape: BoxShape.circle,
            ),
            alignment: const AlignmentDirectional(0.0, 0.0),
            child: Text(
              valueOrDefault<String>(
                widget.initials,
                'MS',
              ),
              textAlign: TextAlign.center,
              maxLines: 1,
              style: FlutterFlowTheme.of(context).labelMedium.override(
                    font: TextStyle(
                      fontFamily: 'Orbitron',
                      fontWeight: FontWeight.w600,
                      fontStyle:
                          FlutterFlowTheme.of(context).labelMedium.fontStyle,
                    ),
                    color: FlutterFlowTheme.of(context).primary,
                    fontSize: 18.24,
                    letterSpacing: 0.0,
                    fontWeight: FontWeight.w600,
                    fontStyle:
                        FlutterFlowTheme.of(context).labelMedium.fontStyle,
                    lineHeight: 1.3,
                  ),
              overflow: TextOverflow.clip,
            ),
          ),
          Expanded(
            flex: 1,
            child: Column(
              mainAxisSize: MainAxisSize.min,
              mainAxisAlignment: MainAxisAlignment.start,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  valueOrDefault<String>(
                    widget.name,
                    'Marcus Sterling',
                  ),
                  style: FlutterFlowTheme.of(context).bodyLarge.override(
                        font: TextStyle(
                          fontFamily: 'Inter',
                          fontWeight: FontWeight.w600,
                          fontStyle:
                              FlutterFlowTheme.of(context).bodyLarge.fontStyle,
                        ),
                        color: FlutterFlowTheme.of(context).primaryText,
                        letterSpacing: 0.0,
                        fontWeight: FontWeight.w600,
                        fontStyle:
                            FlutterFlowTheme.of(context).bodyLarge.fontStyle,
                        lineHeight: 1.6,
                      ),
                ),
                Text(
                  valueOrDefault<String>(
                    widget.relation,
                    'Husband • Primary',
                  ),
                  style: FlutterFlowTheme.of(context).bodySmall.override(
                        font: TextStyle(
                          fontFamily: 'Inter',
                          fontWeight:
                              FlutterFlowTheme.of(context).bodySmall.fontWeight,
                          fontStyle:
                              FlutterFlowTheme.of(context).bodySmall.fontStyle,
                        ),
                        color: FlutterFlowTheme.of(context).secondaryText,
                        letterSpacing: 0.0,
                        fontWeight:
                            FlutterFlowTheme.of(context).bodySmall.fontWeight,
                        fontStyle:
                            FlutterFlowTheme.of(context).bodySmall.fontStyle,
                        lineHeight: 1.5,
                      ),
                ),
              ].divide(const SizedBox(height: 2.0)),
            ),
          ),
          Icon(
            Icons.phone_in_talk_rounded,
            color: FlutterFlowTheme.of(context).primary,
            size: 20.0,
          ),
        ].divide(const SizedBox(width: 16.0)),
      ),
    );
  }
}
