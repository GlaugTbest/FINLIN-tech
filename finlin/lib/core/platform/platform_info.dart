import 'platform_stub.dart'
    if (dart.library.io) 'platform_io.dart'
    if (dart.library.html) 'platform_web.dart';

class PlatformInfo {
  static bool get isWeb => platformIsWeb;
  static bool get isAndroid => platformIsAndroid;
}
