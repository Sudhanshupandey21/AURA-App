// ignore_for_file: overridden_fields, annotate_overrides

import 'package:flutter/material.dart';

import 'package:shared_preferences/shared_preferences.dart';

const kThemeModeKey = '__theme_mode__';

SharedPreferences? _prefs;

abstract class FlutterFlowTheme {
  static Future initialize() async =>
      _prefs = await SharedPreferences.getInstance();

  static ThemeMode get themeMode {
    final darkMode = _prefs?.getBool(kThemeModeKey);
    return darkMode == null
        ? ThemeMode.system
        : darkMode
            ? ThemeMode.dark
            : ThemeMode.light;
  }

  static void saveThemeMode(ThemeMode mode) => mode == ThemeMode.system
      ? _prefs?.remove(kThemeModeKey)
      : _prefs?.setBool(kThemeModeKey, mode == ThemeMode.dark);

  static FlutterFlowTheme of(BuildContext context) {
    return Theme.of(context).brightness == Brightness.dark
        ? DarkModeTheme()
        : LightModeTheme();
  }

  @Deprecated('Use primary instead')
  Color get primaryColor => primary;
  @Deprecated('Use secondary instead')
  Color get secondaryColor => secondary;
  @Deprecated('Use tertiary instead')
  Color get tertiaryColor => tertiary;

  late Color primary;
  late Color secondary;
  late Color tertiary;
  late Color alternate;
  late Color primaryText;
  late Color secondaryText;
  late Color primaryBackground;
  late Color secondaryBackground;
  late Color accent1;
  late Color accent2;
  late Color accent3;
  late Color accent4;
  late Color success;
  late Color warning;
  late Color error;
  late Color info;

  late Color onPrimary;
  late Color primaryContainer;
  late Color onPrimaryContainer;
  late Color onSecondary;
  late Color secondaryContainer;
  late Color onSecondaryContainer;
  late Color onAccent;
  late Color accentContainer;
  late Color onAccentContainer;
  late Color onBackground;
  late Color onSurface;
  late Color surfaceVariant;
  late Color onSurfaceVariant;
  late Color onSuccess;
  late Color onWarning;
  late Color onError;
  late Color onInfo;
  late Color transparent;
  late Color fullContrast;
  late Color primary10;
  late Color primary20;
  late Color primary40;
  late Color primary80;
  late Color primary60;
  late Color primary30;
  late Color accent20;
  late Color primary70;
  late Color surface40;
  late Color surface30;
  late Color onPrimary40;
  late Color primary50;
  late Color background60;
  late Color divider30;
  late Color surface60;
  late Color secondaryText60;
  late Color outline20;
  late Color success20;
  late Color outline30;
  late Color primary5;
  late Color onPrimary67;
  late Color success50;
  late Color info30;
  late Color error20;
  late Color onSurface10;
  late Color error50;
  late Color onSurface60;
  late Color surface20;
  late Color error10;
  late Color error30;
  late Color surface80;
  late Color divider20;

  FFDesignTokens get designToken => FFDesignTokens(this);

  @Deprecated('Use displaySmallFamily instead')
  String get title1Family => displaySmallFamily;
  @Deprecated('Use displaySmall instead')
  TextStyle get title1 => typography.displaySmall;
  @Deprecated('Use headlineMediumFamily instead')
  String get title2Family => typography.headlineMediumFamily;
  @Deprecated('Use headlineMedium instead')
  TextStyle get title2 => typography.headlineMedium;
  @Deprecated('Use headlineSmallFamily instead')
  String get title3Family => typography.headlineSmallFamily;
  @Deprecated('Use headlineSmall instead')
  TextStyle get title3 => typography.headlineSmall;
  @Deprecated('Use titleMediumFamily instead')
  String get subtitle1Family => typography.titleMediumFamily;
  @Deprecated('Use titleMedium instead')
  TextStyle get subtitle1 => typography.titleMedium;
  @Deprecated('Use titleSmallFamily instead')
  String get subtitle2Family => typography.titleSmallFamily;
  @Deprecated('Use titleSmall instead')
  TextStyle get subtitle2 => typography.titleSmall;
  @Deprecated('Use bodyMediumFamily instead')
  String get bodyText1Family => typography.bodyMediumFamily;
  @Deprecated('Use bodyMedium instead')
  TextStyle get bodyText1 => typography.bodyMedium;
  @Deprecated('Use bodySmallFamily instead')
  String get bodyText2Family => typography.bodySmallFamily;
  @Deprecated('Use bodySmall instead')
  TextStyle get bodyText2 => typography.bodySmall;

  String get displayLargeFamily => typography.displayLargeFamily;
  bool get displayLargeIsCustom => typography.displayLargeIsCustom;
  TextStyle get displayLarge => typography.displayLarge;
  String get displayMediumFamily => typography.displayMediumFamily;
  bool get displayMediumIsCustom => typography.displayMediumIsCustom;
  TextStyle get displayMedium => typography.displayMedium;
  String get displaySmallFamily => typography.displaySmallFamily;
  bool get displaySmallIsCustom => typography.displaySmallIsCustom;
  TextStyle get displaySmall => typography.displaySmall;
  String get headlineLargeFamily => typography.headlineLargeFamily;
  bool get headlineLargeIsCustom => typography.headlineLargeIsCustom;
  TextStyle get headlineLarge => typography.headlineLarge;
  String get headlineMediumFamily => typography.headlineMediumFamily;
  bool get headlineMediumIsCustom => typography.headlineMediumIsCustom;
  TextStyle get headlineMedium => typography.headlineMedium;
  String get headlineSmallFamily => typography.headlineSmallFamily;
  bool get headlineSmallIsCustom => typography.headlineSmallIsCustom;
  TextStyle get headlineSmall => typography.headlineSmall;
  String get titleLargeFamily => typography.titleLargeFamily;
  bool get titleLargeIsCustom => typography.titleLargeIsCustom;
  TextStyle get titleLarge => typography.titleLarge;
  String get titleMediumFamily => typography.titleMediumFamily;
  bool get titleMediumIsCustom => typography.titleMediumIsCustom;
  TextStyle get titleMedium => typography.titleMedium;
  String get titleSmallFamily => typography.titleSmallFamily;
  bool get titleSmallIsCustom => typography.titleSmallIsCustom;
  TextStyle get titleSmall => typography.titleSmall;
  String get labelLargeFamily => typography.labelLargeFamily;
  bool get labelLargeIsCustom => typography.labelLargeIsCustom;
  TextStyle get labelLarge => typography.labelLarge;
  String get labelMediumFamily => typography.labelMediumFamily;
  bool get labelMediumIsCustom => typography.labelMediumIsCustom;
  TextStyle get labelMedium => typography.labelMedium;
  String get labelSmallFamily => typography.labelSmallFamily;
  bool get labelSmallIsCustom => typography.labelSmallIsCustom;
  TextStyle get labelSmall => typography.labelSmall;
  String get bodyLargeFamily => typography.bodyLargeFamily;
  bool get bodyLargeIsCustom => typography.bodyLargeIsCustom;
  TextStyle get bodyLarge => typography.bodyLarge;
  String get bodyMediumFamily => typography.bodyMediumFamily;
  bool get bodyMediumIsCustom => typography.bodyMediumIsCustom;
  TextStyle get bodyMedium => typography.bodyMedium;
  String get bodySmallFamily => typography.bodySmallFamily;
  bool get bodySmallIsCustom => typography.bodySmallIsCustom;
  TextStyle get bodySmall => typography.bodySmall;

  Typography get typography => ThemeTypography(this);
}

class LightModeTheme extends FlutterFlowTheme {
  @Deprecated('Use primary instead')
  Color get primaryColor => primary;
  @Deprecated('Use secondary instead')
  Color get secondaryColor => secondary;
  @Deprecated('Use tertiary instead')
  Color get tertiaryColor => tertiary;

  late Color primary = const Color(0xFF00F0FF);
  late Color secondary = const Color(0xFF7000FF);
  late Color tertiary = const Color(0xFFFF003C);
  late Color alternate = const Color(0xFF26262C);
  late Color primaryText = const Color(0xFFFFFFFF);
  late Color secondaryText = const Color(0xFFA0A0AB);
  late Color primaryBackground = const Color(0xFF0A0A0C);
  late Color accent1 = const Color(0x4C4B39EF);
  late Color accent2 = const Color(0x4D39D2C0);
  late Color accent3 = const Color(0xFF4E4E59);
  late Color accent4 = const Color(0xCCFFFFFF);
  late Color success = const Color(0xFF00FFA3);
  late Color warning = const Color(0xFFFFD600);
  late Color error = const Color(0xFFFF003C);
  late Color info = const Color(0xFF00F0FF);

  late Color onPrimary = const Color(0xFF000000);
  late Color primaryContainer = const Color(0x1A00F0FF);
  late Color onPrimaryContainer = const Color(0xFFFFFFFF);
  late Color onSecondary = const Color(0xFFFFFFFF);
  late Color secondaryContainer = const Color(0x1A7000FF);
  late Color onSecondaryContainer = const Color(0xFFFFFFFF);
  late Color onAccent = const Color(0xFFFFFFFF);
  late Color accentContainer = const Color(0x1AFF003C);
  late Color onAccentContainer = const Color(0xFFFFFFFF);
  late Color onBackground = const Color(0xFFFFFFFF);
  late Color secondaryBackground = const Color(0xFF141417);
  late Color onSurface = const Color(0xFFFFFFFF);
  late Color surfaceVariant = const Color(0xFF2A2A30);
  late Color onSurfaceVariant = const Color(0xFFA0A0AB);
  late Color onSuccess = const Color(0xFF000000);
  late Color onWarning = const Color(0xFF000000);
  late Color onError = const Color(0xFFFFFFFF);
  late Color onInfo = const Color(0xFF000000);
  late Color transparent = const Color(0x00000000);
  late Color fullContrast = const Color(0xFF000000);
  late Color primary10 = const Color(0x1A00F0FF);
  late Color primary20 = const Color(0x3300F0FF);
  late Color primary40 = const Color(0x6600F0FF);
  late Color primary80 = const Color(0xCC00F0FF);
  late Color primary60 = const Color(0x9900F0FF);
  late Color primary30 = const Color(0x4D00F0FF);
  late Color accent20 = const Color(0x33FF003C);
  late Color primary70 = const Color(0xB300F0FF);
  late Color surface40 = const Color(0x661E1E22);
  late Color surface30 = const Color(0x4D1E1E22);
  late Color onPrimary40 = const Color(0x66000000);
  late Color primary50 = const Color(0x8000F0FF);
  late Color background60 = const Color(0x990A0A0C);
  late Color divider30 = const Color(0x4D26262C);
  late Color surface60 = const Color(0x991E1E22);
  late Color secondaryText60 = const Color(0x99A0A0AB);
  late Color outline20 = const Color(0x3333333B);
  late Color success20 = const Color(0x3300FFA3);
  late Color outline30 = const Color(0x4D33333B);
  late Color primary5 = const Color(0x0D00F0FF);
  late Color onPrimary67 = const Color(0xAB000000);
  late Color success50 = const Color(0x8000FFA3);
  late Color info30 = const Color(0x4D00F0FF);
  late Color error20 = const Color(0x33FF003C);
  late Color onSurface10 = const Color(0x1AFFFFFF);
  late Color error50 = const Color(0x80FF003C);
  late Color onSurface60 = const Color(0x99FFFFFF);
  late Color surface20 = const Color(0x331E1E22);
  late Color error10 = const Color(0x1AFF003C);
  late Color error30 = const Color(0x4DFF003C);
  late Color surface80 = const Color(0xCC1E1E22);
  late Color divider20 = const Color(0x3326262C);
}

abstract class Typography {
  String get displayLargeFamily;
  bool get displayLargeIsCustom;
  TextStyle get displayLarge;
  String get displayMediumFamily;
  bool get displayMediumIsCustom;
  TextStyle get displayMedium;
  String get displaySmallFamily;
  bool get displaySmallIsCustom;
  TextStyle get displaySmall;
  String get headlineLargeFamily;
  bool get headlineLargeIsCustom;
  TextStyle get headlineLarge;
  String get headlineMediumFamily;
  bool get headlineMediumIsCustom;
  TextStyle get headlineMedium;
  String get headlineSmallFamily;
  bool get headlineSmallIsCustom;
  TextStyle get headlineSmall;
  String get titleLargeFamily;
  bool get titleLargeIsCustom;
  TextStyle get titleLarge;
  String get titleMediumFamily;
  bool get titleMediumIsCustom;
  TextStyle get titleMedium;
  String get titleSmallFamily;
  bool get titleSmallIsCustom;
  TextStyle get titleSmall;
  String get labelLargeFamily;
  bool get labelLargeIsCustom;
  TextStyle get labelLarge;
  String get labelMediumFamily;
  bool get labelMediumIsCustom;
  TextStyle get labelMedium;
  String get labelSmallFamily;
  bool get labelSmallIsCustom;
  TextStyle get labelSmall;
  String get bodyLargeFamily;
  bool get bodyLargeIsCustom;
  TextStyle get bodyLarge;
  String get bodyMediumFamily;
  bool get bodyMediumIsCustom;
  TextStyle get bodyMedium;
  String get bodySmallFamily;
  bool get bodySmallIsCustom;
  TextStyle get bodySmall;
}

class ThemeTypography extends Typography {
  ThemeTypography(this.theme);

  final FlutterFlowTheme theme;

  String get displayLargeFamily => 'Orbitron';
  bool get displayLargeIsCustom => false;
  TextStyle get displayLarge => TextStyle(
        fontFamily: 'Orbitron',
        color: theme.primaryText,
        fontWeight: FontWeight.bold,
        fontSize: 58.0,
        height: 1.1,
      );
  String get displayMediumFamily => 'Orbitron';
  bool get displayMediumIsCustom => false;
  TextStyle get displayMedium => TextStyle(
        fontFamily: 'Orbitron',
        color: theme.primaryText,
        fontWeight: FontWeight.bold,
        fontSize: 46.0,
        height: 1.15,
      );
  String get displaySmallFamily => 'Orbitron';
  bool get displaySmallIsCustom => false;
  TextStyle get displaySmall => TextStyle(
        fontFamily: 'Orbitron',
        color: theme.primaryText,
        fontWeight: FontWeight.bold,
        fontSize: 38.0,
        height: 1.2,
      );
  String get headlineLargeFamily => 'Orbitron';
  bool get headlineLargeIsCustom => false;
  TextStyle get headlineLarge => TextStyle(
        fontFamily: 'Orbitron',
        color: theme.primaryText,
        fontWeight: FontWeight.bold,
        fontSize: 32.0,
        height: 1.2,
      );
  String get headlineMediumFamily => 'Orbitron';
  bool get headlineMediumIsCustom => false;
  TextStyle get headlineMedium => TextStyle(
        fontFamily: 'Orbitron',
        color: theme.primaryText,
        fontWeight: FontWeight.w600,
        fontSize: 26.0,
        height: 1.25,
      );
  String get headlineSmallFamily => 'Orbitron';
  bool get headlineSmallIsCustom => false;
  TextStyle get headlineSmall => TextStyle(
        fontFamily: 'Orbitron',
        color: theme.primaryText,
        fontWeight: FontWeight.w600,
        fontSize: 24.0,
        height: 1.3,
      );
  String get titleLargeFamily => 'Orbitron';
  bool get titleLargeIsCustom => false;
  TextStyle get titleLarge => TextStyle(
        fontFamily: 'Orbitron',
        color: theme.primaryText,
        fontWeight: FontWeight.w600,
        fontSize: 20.0,
        height: 1.3,
      );
  String get titleMediumFamily => 'Inter';
  bool get titleMediumIsCustom => false;
  TextStyle get titleMedium => TextStyle(
        fontFamily: 'Inter',
        color: theme.primaryText,
        fontWeight: FontWeight.w600,
        fontSize: 16.0,
        height: 1.4,
      );
  String get titleSmallFamily => 'Inter';
  bool get titleSmallIsCustom => false;
  TextStyle get titleSmall => TextStyle(
        fontFamily: 'Inter',
        color: theme.primaryText,
        fontWeight: FontWeight.w600,
        fontSize: 14.0,
        height: 1.4,
      );
  String get labelLargeFamily => 'Orbitron';
  bool get labelLargeIsCustom => false;
  TextStyle get labelLarge => TextStyle(
        fontFamily: 'Orbitron',
        color: theme.secondaryText,
        fontWeight: FontWeight.w600,
        fontSize: 14.0,
        height: 1.3,
      );
  String get labelMediumFamily => 'Orbitron';
  bool get labelMediumIsCustom => false;
  TextStyle get labelMedium => TextStyle(
        fontFamily: 'Orbitron',
        color: theme.secondaryText,
        fontWeight: FontWeight.w600,
        fontSize: 12.0,
        height: 1.3,
      );
  String get labelSmallFamily => 'Orbitron';
  bool get labelSmallIsCustom => false;
  TextStyle get labelSmall => TextStyle(
        fontFamily: 'Orbitron',
        color: theme.secondaryText,
        fontWeight: FontWeight.w600,
        fontSize: 10.0,
        height: 1.2,
      );
  String get bodyLargeFamily => 'Inter';
  bool get bodyLargeIsCustom => false;
  TextStyle get bodyLarge => TextStyle(
        fontFamily: 'Inter',
        color: theme.primaryText,
        fontWeight: FontWeight.normal,
        fontSize: 16.0,
        height: 1.6,
      );
  String get bodyMediumFamily => 'Inter';
  bool get bodyMediumIsCustom => false;
  TextStyle get bodyMedium => TextStyle(
        fontFamily: 'Inter',
        color: theme.primaryText,
        fontWeight: FontWeight.normal,
        fontSize: 14.0,
        height: 1.5,
      );
  String get bodySmallFamily => 'Inter';
  bool get bodySmallIsCustom => false;
  TextStyle get bodySmall => TextStyle(
        fontFamily: 'Inter',
        color: theme.primaryText,
        fontWeight: FontWeight.normal,
        fontSize: 12.0,
        height: 1.5,
      );
}

class DarkModeTheme extends FlutterFlowTheme {
  @Deprecated('Use primary instead')
  Color get primaryColor => primary;
  @Deprecated('Use secondary instead')
  Color get secondaryColor => secondary;
  @Deprecated('Use tertiary instead')
  Color get tertiaryColor => tertiary;

  late Color primary = const Color(0xFF00F0FF);
  late Color secondary = const Color(0xFF7000FF);
  late Color tertiary = const Color(0xFFFF003C);
  late Color alternate = const Color(0xFF1E1E24);
  late Color primaryText = const Color(0xFFFFFFFF);
  late Color secondaryText = const Color(0xFF94A3B8);
  late Color primaryBackground = const Color(0xFF050505);
  late Color accent1 = const Color(0x4C4B39EF);
  late Color accent2 = const Color(0x4D39D2C0);
  late Color accent3 = const Color(0xFF475569);
  late Color accent4 = const Color(0xB2262D34);
  late Color success = const Color(0xFF00FFA3);
  late Color warning = const Color(0xFFFFD600);
  late Color error = const Color(0xFFFF003C);
  late Color info = const Color(0xFF00F0FF);

  late Color onPrimary = const Color(0xFF000000);
  late Color primaryContainer = const Color(0x2400F0FF);
  late Color onPrimaryContainer = const Color(0xFFFFFFFF);
  late Color onSecondary = const Color(0xFFFFFFFF);
  late Color secondaryContainer = const Color(0x247000FF);
  late Color onSecondaryContainer = const Color(0xFFFFFFFF);
  late Color onAccent = const Color(0xFFFFFFFF);
  late Color accentContainer = const Color(0x24FF003C);
  late Color onAccentContainer = const Color(0xFFFFFFFF);
  late Color onBackground = const Color(0xFFFFFFFF);
  late Color secondaryBackground = const Color(0xFF0D0D0F);
  late Color onSurface = const Color(0xFFFFFFFF);
  late Color surfaceVariant = const Color(0xFF1C1C21);
  late Color onSurfaceVariant = const Color(0xFF94A3B8);
  late Color onSuccess = const Color(0xFF000000);
  late Color onWarning = const Color(0xFF000000);
  late Color onError = const Color(0xFFFFFFFF);
  late Color onInfo = const Color(0xFF000000);
  late Color transparent = const Color(0x00000000);
  late Color fullContrast = const Color(0xFFFFFFFF);
  late Color primary10 = const Color(0x1A00F0FF);
  late Color primary20 = const Color(0x3300F0FF);
  late Color primary40 = const Color(0x6600F0FF);
  late Color primary80 = const Color(0xCC00F0FF);
  late Color primary60 = const Color(0x9900F0FF);
  late Color primary30 = const Color(0x4D00F0FF);
  late Color accent20 = const Color(0x33FF003C);
  late Color primary70 = const Color(0xB300F0FF);
  late Color surface40 = const Color(0x66121214);
  late Color surface30 = const Color(0x4D121214);
  late Color onPrimary40 = const Color(0x66000000);
  late Color primary50 = const Color(0x8000F0FF);
  late Color background60 = const Color(0x99050505);
  late Color divider30 = const Color(0x4D1E1E24);
  late Color surface60 = const Color(0x99121214);
  late Color secondaryText60 = const Color(0x9994A3B8);
  late Color outline20 = const Color(0x332D2D35);
  late Color success20 = const Color(0x3300FFA3);
  late Color outline30 = const Color(0x4D2D2D35);
  late Color primary5 = const Color(0x0D00F0FF);
  late Color onPrimary67 = const Color(0xAB000000);
  late Color success50 = const Color(0x8000FFA3);
  late Color info30 = const Color(0x4D00F0FF);
  late Color error20 = const Color(0x33FF003C);
  late Color onSurface10 = const Color(0x1AFFFFFF);
  late Color error50 = const Color(0x80FF003C);
  late Color onSurface60 = const Color(0x99FFFFFF);
  late Color surface20 = const Color(0x33121214);
  late Color error10 = const Color(0x1AFF003C);
  late Color error30 = const Color(0x4DFF003C);
  late Color surface80 = const Color(0xCC121214);
  late Color divider20 = const Color(0x331E1E24);
}

class FFDesignTokens {
  const FFDesignTokens(this.theme);
  final FlutterFlowTheme theme;
  FFSpacing get spacing => const FFSpacing();
  FFRadius get radius => const FFRadius();
  FFShadows get shadow => FFShadows(theme);
}

class FFSpacing {
  const FFSpacing();
  double get none => 0.0;
  double get xs => 4.0;
  double get sm => 8.0;
  double get md => 16.0;
  double get lg => 24.0;
  double get xl => 32.0;
  double get xxl => 48.0;
  double get xxxl => 64.0;
}

class FFRadius {
  const FFRadius();
  double get none => 0.0;
  double get xs => 4.0;
  double get sm => 8.0;
  double get md => 12.0;
  double get lg => 16.0;
  double get xl => 24.0;
  double get xxl => 40.0;
  double get full => 9999.0;
}

class FFShadows {
  const FFShadows(this.theme);
  final FlutterFlowTheme theme;
  BoxShadow get none => const BoxShadow(
      blurRadius: 0.0,
      color: Color(0x00000000),
      offset: Offset(0.0, 0.0),
      spreadRadius: 0.0);
  BoxShadow get xs => const BoxShadow(
      blurRadius: 4.0,
      color: Color(0x3300F0FF),
      offset: Offset(0.0, 2.0),
      spreadRadius: 0.0);
  BoxShadow get sm => const BoxShadow(
      blurRadius: 8.0,
      color: Color(0x4D00F0FF),
      offset: Offset(0.0, 4.0),
      spreadRadius: 0.0);
  BoxShadow get md => const BoxShadow(
      blurRadius: 12.0,
      color: Color(0x6600F0FF),
      offset: Offset(0.0, 0.0),
      spreadRadius: 2.0);
  BoxShadow get lg => const BoxShadow(
      blurRadius: 20.0,
      color: Color(0x66FF003C),
      offset: Offset(0.0, 0.0),
      spreadRadius: 2.0);
  BoxShadow get xl => const BoxShadow(
      blurRadius: 40.0,
      color: Color(0x80000000),
      offset: Offset(0.0, 20.0),
      spreadRadius: -10.0);
  BoxShadow get xxl => const BoxShadow(
      blurRadius: 60.0,
      color: Color(0x3300F0FF),
      offset: Offset(0.0, 0.0),
      spreadRadius: 10.0);
}

extension TextStyleHelper on TextStyle {
  TextStyle override({
    TextStyle? font,
    String? fontFamily,
    Color? color,
    double? fontSize,
    FontWeight? fontWeight,
    double? letterSpacing,
    FontStyle? fontStyle,
    TextDecoration? decoration,
    double? lineHeight,
    List<Shadow>? shadows,
    String? package,
  }) {
    return font != null
        ? font.copyWith(
            color: color ?? this.color,
            fontSize: fontSize ?? this.fontSize,
            letterSpacing: letterSpacing ?? this.letterSpacing,
            fontWeight: fontWeight ?? this.fontWeight,
            fontStyle: fontStyle ?? this.fontStyle,
            decoration: decoration,
            height: lineHeight,
            shadows: shadows,
          )
        : copyWith(
            fontFamily: fontFamily,
            package: package,
            color: color,
            fontSize: fontSize,
            letterSpacing: letterSpacing,
            fontWeight: fontWeight,
            fontStyle: fontStyle,
            decoration: decoration,
            height: lineHeight,
            shadows: shadows,
          );
  }
}
