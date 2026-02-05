import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'presentation/screens/login_screen_v2.dart';
import 'presentation/screens/home_screen_v2.dart';
import 'presentation/screens/transacoes_screen.dart';
import 'presentation/screens/relatorio_screen.dart';
import 'presentation/screens/conta_detalhes_screen.dart';
import 'presentation/screens/categorias_screen.dart';
import 'presentation/providers/login_provider.dart';

void main() {
  runApp(const ProviderScope(child: MyApp()));
}

/// Aplicativo principal FINLIN
///
/// Gerenciamento de estado com Riverpod
/// Arquitetura limpa com separação entre camadas
class MyApp extends ConsumerWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final loginState = ref.watch(loginProvider);
    final isAuthenticated = loginState.isAuthenticated;

    return MaterialApp(
      title: 'FINLIN - Controle Financeiro',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF2C6BEA),
          brightness: Brightness.dark,
        ),
        scaffoldBackgroundColor: const Color(0xFF0E1116),
        appBarTheme: const AppBarTheme(
          elevation: 0,
          centerTitle: false,
          backgroundColor: Color(0xFF0E1116),
          foregroundColor: Color(0xFFE6EAF2),
        ),
        cardTheme: CardThemeData(
          color: const Color(0xFF151A22),
          elevation: 0,
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
        ),
        listTileTheme: const ListTileThemeData(
          iconColor: Color(0xFF8EA6FF),
          textColor: Color(0xFFE6EAF2),
        ),
        bottomNavigationBarTheme: const BottomNavigationBarThemeData(
          backgroundColor: Color(0xFF0E1116),
          selectedItemColor: Color(0xFF8EA6FF),
          unselectedItemColor: Color(0xFF7B8797),
          type: BottomNavigationBarType.fixed,
        ),
        floatingActionButtonTheme: const FloatingActionButtonThemeData(
          backgroundColor: Color(0xFF2C6BEA),
          foregroundColor: Colors.white,
        ),
        snackBarTheme: const SnackBarThemeData(
          backgroundColor: Color(0xFF1B2230),
          contentTextStyle: TextStyle(color: Color(0xFFE6EAF2)),
        ),
        dialogTheme: DialogThemeData(
          backgroundColor: const Color(0xFF151A22),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
          titleTextStyle: const TextStyle(
            color: Color(0xFFE6EAF2),
            fontWeight: FontWeight.w600,
            fontSize: 18,
          ),
          contentTextStyle: const TextStyle(color: Color(0xFFC2C9D6)),
        ),
        dividerTheme: const DividerThemeData(
          color: Color(0xFF232A35),
          thickness: 1,
          space: 1,
        ),
        inputDecorationTheme: InputDecorationTheme(
          filled: true,
          fillColor: const Color(0xFF151A22),
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(14),
            borderSide: const BorderSide(color: Color(0xFF263040)),
          ),
          enabledBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(14),
            borderSide: const BorderSide(color: Color(0xFF263040)),
          ),
          focusedBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(14),
            borderSide: const BorderSide(color: Color(0xFF8EA6FF), width: 1.5),
          ),
          labelStyle: const TextStyle(color: Color(0xFF9AA4B2)),
          hintStyle: const TextStyle(color: Color(0xFF7B8797)),
        ),
        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
            backgroundColor: const Color(0xFF2C6BEA),
            foregroundColor: Colors.white,
            padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 14),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(14),
            ),
          ),
        ),
        outlinedButtonTheme: OutlinedButtonThemeData(
          style: OutlinedButton.styleFrom(
            foregroundColor: const Color(0xFFE6EAF2),
            side: const BorderSide(color: Color(0xFF2C6BEA)),
            padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 12),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(14),
            ),
          ),
        ),
        textButtonTheme: TextButtonThemeData(
          style: TextButton.styleFrom(
            foregroundColor: const Color(0xFF8EA6FF),
          ),
        ),
        textTheme: const TextTheme(
          displaySmall: TextStyle(
            color: Color(0xFFE6EAF2),
            fontWeight: FontWeight.w700,
            letterSpacing: 0.2,
          ),
          titleLarge: TextStyle(
            color: Color(0xFFE6EAF2),
            fontWeight: FontWeight.w700,
            letterSpacing: 0.1,
          ),
          titleMedium: TextStyle(
            color: Color(0xFFE6EAF2),
            fontWeight: FontWeight.w600,
          ),
          bodyLarge: TextStyle(
            color: Color(0xFFD6DBE6),
            height: 1.3,
          ),
          bodyMedium: TextStyle(
            color: Color(0xFFC2C9D6),
            height: 1.25,
          ),
          bodySmall: TextStyle(
            color: Color(0xFF9AA4B2),
            letterSpacing: 0.2,
          ),
        ),
      ),
      home: isAuthenticated ? const HomeScreenV2() : const LoginScreenV2(),
      routes: {
        '/relatorio': (context) => const RelatorioScreen(),
        '/categorias': (context) => const CategoriasScreen(),
        '/conta-detalhes': (context) {
          final contaId = ModalRoute.of(context)?.settings.arguments as String?;
          return ContaDetalhesScreen(contaId: contaId ?? '');
        },
      },
    );
  }
}
