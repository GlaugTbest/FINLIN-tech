import 'package:flutter/foundation.dart';

/// Constantes da aplicação
class AppConstants {
  // URLs da API
  // IMPORTANTE: 'dart:io' quebra o Flutter Web.
  // Para Android Emulator/Dispositivo: use IP da máquina na rede local
  // Para Web: se estiver na porta 8000, usa o próprio host; senão, usa IP fixo

  static String get apiBaseUrl {
    const lanBaseUrl = 'http://192.168.0.3:8000';

    if (kIsWeb) {
      if (Uri.base.port == 8000) {
        return Uri.base.origin;
      }
      return lanBaseUrl;
    }

    return lanBaseUrl;
  }

  // Endpoints
  static const String loginEndpoint = '/auth/login';
  static const String usuariosEndpoint = '/usuarios';
  static const String contasEndpoint = '/contas';
  static const String categoriasEndpoint = '/categorias';
  static const String transacoesEndpoint = '/transacoes';
  static const String seedEndpoint = '/seed';
  static const String limparDadosEndpoint = '/limpar-dados';

  // IDs de exemplo para dados mockados (ainda usados em fallback)
  static const String usuarioIdMock = 'user_001';
  static const String contaBancariaMockId = 'conta_001';
  static const String contaPoupancaMockId = 'conta_002';

  // Formatação de moeda
  static const String currencySymbol = 'R\$';
  static const String dateFormat = 'dd/MM/yyyy';
  static const String dateTimeFormat = 'dd/MM/yyyy HH:mm';
}
