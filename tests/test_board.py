# tests/test_board.py
"""Tests unitarios para el módulo core.board.Tablero.

Este archivo valida:
- Renderizado textual del tablero (`mostrar`) con chequeo dinámico de líneas.
- Movimientos básicos (válidos/ inválidos) y direcciones por ficha.
- Reglas de captura ("comer") y bloqueo.
- Reingreso desde la barra (X en 0, O en 25), incluyendo bloqueo y captura.
- Retiro de fichas (bearing off).
- Conteo de fichas restantes y detección de ganador.
"""

import unittest
from core.board import Tablero


class TestMostrarTablero(unittest.TestCase):
    """Pruebas de visualización (render) del tablero."""

    def setUp(self):
        """Crea un tablero para las pruebas de render."""
        self.juego = Tablero()

    def test_contiene_numeros(self):
        """El render debe incluir números de puntos representativos."""
        tablero = Tablero().mostrar()
        self.assertIn("13", tablero)
        self.assertIn("24", tablero)
        self.assertIn("12", tablero)
        self.assertIn(" 1 ", tablero)

    def test_contiene_fichas(self):
        """El tablero inicial debe mostrar fichas 'X' y 'O'."""
        tablero = Tablero().mostrar()
        self.assertIn("O", tablero)
        self.assertIn("X", tablero)

    def test_cantidad_lineas(self):
        """El render puede incluir o no secciones de barra/off (layout dinámico)."""
        tablero = self.juego.mostrar().splitlines()

        # Si el render imprime barra/off, esperamos líneas extra.
        muestra_barra = any("Barra X" in ln or "Barra O" in ln for ln in tablero) or \
                        any("Off X" in ln or "Off O" in ln for ln in tablero)

        if muestra_barra:
            # 19 base + extras (según implementación). Ajuste conservador de 22.
            self.assertEqual(len(tablero), 22)
        else:
            # Layout clásico (sin barra/off)
            self.assertEqual(len(tablero), 19)


class TestMovimientoFichas(unittest.TestCase):
    """Pruebas de movimiento básico de fichas sobre el tablero."""

    def setUp(self):
        """Crea un tablero inicial antes de cada prueba."""
        self.juego = Tablero()

    def test_mover_ficha_valida(self):
        """Mover desde un punto válido actualiza origen y destino."""
        self.assertEqual(len(self.juego.tablero[13]), 5)  # O en 13
        self.juego.mover_ficha(13, 11)
        self.assertEqual(len(self.juego.tablero[13]), 4)
        self.assertEqual(len(self.juego.tablero[11]), 1)

    def test_mover_ficha_origen_vacio(self):
        """Intentar mover desde un punto vacío debe fallar."""
        self.assertFalse(self.juego.mover_ficha(2, 5))
        self.assertNotIn(2, self.juego.tablero)

    def test_mover_varias_fichas(self):
        """Mover dos fichas desde un mismo origen actualiza correctamente."""
        self.juego.mover_ficha(24, 10)
        self.juego.mover_ficha(24, 10)
        self.assertEqual(len(self.juego.tablero[24]), 0)
        self.assertEqual(len(self.juego.tablero[10]), 2)

    def test_mover_preserva_tipo(self):
        """La ficha movida mantiene su tipo en el destino."""
        ficha = self.juego.tablero[13][-1]
        self.juego.mover_ficha(13, 7)
        self.assertIn(ficha, self.juego.tablero[7])

    def test_no_mover_a_bloqueado(self):
        """No debe poder moverse a un punto bloqueado por 2+ rivales."""
        # 19 tiene 5 X al inicio → bloqueado para O
        self.assertFalse(self.juego.mover_ficha(13, 19))


class TestMovimientoDireccion(unittest.TestCase):
    """Direcciones válidas por tipo de ficha ('X' sube, 'O' baja)."""

    def setUp(self):
        """Crea un tablero inicial antes de cada prueba."""
        self.juego = Tablero()

    def test_o_no_puede_subir(self):
        """Una 'O' no puede ir a un número mayor (subir)."""
        self.assertFalse(self.juego.mover_ficha(13, 15))
        self.assertEqual(len(self.juego.tablero[13]), 5)
        self.assertNotIn(15, self.juego.tablero)

    def test_o_puede_bajar(self):
        """Una 'O' puede bajar (ir a número menor)."""
        self.assertTrue(self.juego.mover_ficha(13, 11))
        self.assertEqual(len(self.juego.tablero[13]), 4)
        self.assertEqual(len(self.juego.tablero[11]), 1)

    def test_x_no_puede_bajar(self):
        """Una 'X' no puede ir a un número menor (bajar)."""
        # En tu setup, X está en 12 con 5 fichas (inicio clásico)
        self.assertFalse(self.juego.mover_ficha(12, 9))
        self.assertEqual(len(self.juego.tablero[12]), 5)
        self.assertNotIn(9, self.juego.tablero)

    def test_x_puede_subir(self):
        """Una 'X' puede subir (ir a número mayor)."""
        self.assertTrue(self.juego.mover_ficha(1, 3))
        self.assertEqual(len(self.juego.tablero[1]), 1)
        self.assertEqual(len(self.juego.tablero[3]), 1)


class TestComerFicha(unittest.TestCase):
    """Validación de regla de captura (comer una sola ficha rival)."""

    def setUp(self):
        """Crea un tablero inicial antes de cada prueba."""
        self.juego = Tablero()

    def test_o_come_a_x(self):
        """'O' come a 'X' si hay exactamente una 'X' en destino."""
        self.juego.tablero[5] = ["X"]
        resultado = self.juego.mover_ficha(6, 5)
        self.assertTrue(resultado)
        self.assertEqual(self.juego.tablero[5], ["O"])
        self.assertEqual(self.juego.bar["X"], ["X"])

    def test_x_come_a_o(self):
        """'X' come a 'O' si hay exactamente una 'O' en destino."""
        self.juego.tablero[14] = ["O"]
        resultado = self.juego.mover_ficha(12, 14)
        self.assertTrue(resultado)
        self.assertEqual(self.juego.tablero[14], ["X"])
        self.assertEqual(self.juego.bar["O"], ["O"])

    def test_no_comer_si_hay_mas_de_una(self):
        """No se puede capturar si el destino tiene 2 o más fichas rivales."""
        self.juego.tablero[5] = ["X", "X"]
        resultado = self.juego.mover_ficha(6, 5)
        self.assertFalse(resultado)
        self.assertEqual(self.juego.tablero[5], ["X", "X"])
        self.assertEqual(self.juego.bar["X"], [])


class TestMovimientoConBarra(unittest.TestCase):
    """Restricción: si hay fichas en la barra, deben reingresar primero."""

    def setUp(self):
        """Crea un tablero inicial antes de cada prueba."""
        self.juego = Tablero()

    def test_o_no_puede_mover_si_tiene_en_barra(self):
        """Si 'O' tiene fichas en barra, no puede mover otras fichas."""
        self.juego.bar["O"].append("O")
        resultado = self.juego.mover_ficha(13, 11)
        self.assertFalse(resultado)
        self.assertEqual(len(self.juego.tablero[13]), 5)
        self.assertNotIn(11, self.juego.tablero)

    def test_x_no_puede_mover_si_tiene_en_barra(self):
        """Si 'X' tiene fichas en barra, no puede mover otras fichas."""
        self.juego.bar["X"].append("X")
        resultado = self.juego.mover_ficha(1, 3)
        self.assertFalse(resultado)
        self.assertEqual(len(self.juego.tablero[1]), 2)
        self.assertNotIn(3, self.juego.tablero)


class TestBearingOff(unittest.TestCase):
    """Pruebas de retiro de fichas (bearing off)."""

    def setUp(self):
        """Crea un tablero inicial antes de cada prueba."""
        self.juego = Tablero()

    def test_o_no_puede_retirar_si_no_todas_en_cuadrante(self):
        """'O' no puede retirar si no están todas en [1–6]."""
        resultado = self.juego.mover_ficha(13, 0)
        self.assertFalse(resultado)
        self.assertEqual(self.juego.off["O"], [])

    def test_x_no_puede_retirar_si_no_todas_en_cuadrante(self):
        """'X' no puede retirar si no están todas en [19–24]."""
        resultado = self.juego.mover_ficha(12, 25)
        self.assertFalse(resultado)
        self.assertEqual(self.juego.off["X"], [])

    def test_o_puede_retirar_cuando_todas_en_cuadrante(self):
        """'O' puede retirar fichas cuando todas están en [1–6]."""
        self.juego.tablero = {
            1: ["O"] * 2,
            2: ["O"] * 3,
            3: ["O"] * 5,
            6: ["O"] * 5,
            19: ["X"] * 5,
            24: ["X"] * 10,
        }
        resultado = self.juego.mover_ficha(6, 0)
        self.assertTrue(resultado)
        self.assertEqual(self.juego.off["O"], ["O"])
        self.assertEqual(len(self.juego.tablero[6]), 4)

    def test_x_puede_retirar_cuando_todas_en_cuadrante(self):
        """'X' puede retirar fichas cuando todas están en [19–24]."""
        self.juego.tablero = {
            19: ["X"] * 5,
            20: ["X"] * 3,
            24: ["X"] * 7,
            6: ["O"] * 10,
        }
        resultado = self.juego.mover_ficha(24, 25)
        self.assertTrue(resultado)
        self.assertEqual(self.juego.off["X"], ["X"])
        self.assertEqual(len(self.juego.tablero[24]), 6)

    def test_varias_fichas_retiradas(self):
        """Retirar múltiples fichas debe acumularse en `off`."""
        self.juego.tablero = {
            1: ["O"] * 15,
            19: ["X"] * 15,
        }
        self.juego.mover_ficha(1, 0)
        self.juego.mover_ficha(1, 0)
        self.juego.mover_ficha(1, 0)
        self.assertEqual(len(self.juego.off["O"]), 3)
        self.assertEqual(len(self.juego.tablero[1]), 12)


class TestFichasRestantes(unittest.TestCase):
    """Conteo de fichas restantes (tablero + barra; excluye off)."""

    def setUp(self):
        """Inicializa un estado controlado para conteos."""
        self.t = Tablero()
        self.t.tablero.clear()
        self.t.bar = {"X": [], "O": []}
        self.t.off = {"X": [], "O": []}

    def test_cuenta_en_tablero(self):
        """Cuenta fichas de cada jugador en el tablero."""
        self.t.tablero[6] = ["X", "X", "X"]
        self.t.tablero[12] = ["O", "O"]
        self.assertEqual(self.t.fichas_restantes("X"), 3)
        self.assertEqual(self.t.fichas_restantes("O"), 2)

    def test_incluye_barra_pero_no_off(self):
        """Incluye barra en el conteo, excluye fichas ya retiradas."""
        self.t.tablero[5] = ["X", "X"]
        self.t.bar["X"] = ["X"]
        self.t.off["X"] = ["X"] * 5
        self.t.tablero[10] = ["O"]
        self.t.bar["O"] = ["O", "O"]
        self.assertEqual(self.t.fichas_restantes("X"), 3)  # 2 tablero + 1 barra
        self.assertEqual(self.t.fichas_restantes("O"), 3)  # 1 tablero + 2 barra


class TestGanador(unittest.TestCase):
    """Detección de ganador cuando `off` alcanza 15 fichas."""

    def setUp(self):
        """Inicializa un estado controlado para ganador."""
        self.t = Tablero()
        self.t.tablero.clear()
        self.t.bar = {"X": [], "O": []}
        self.t.off = {"X": [], "O": []}

    def test_sin_ganador(self):
        """Con menos de 15 fichas en off, no hay ganador."""
        self.t.tablero[24] = ["X"] * 10
        self.t.bar["X"] = ["X"] * 2
        self.t.off["X"] = ["X"] * 3
        self.assertIsNone(self.t.ganador())

    def test_gana_x_cuando_off_15(self):
        """'X' gana al alcanzar 15 fichas retiradas."""
        self.t.off["X"] = ["X"] * 15
        self.t.tablero[1] = ["X"]  # irrelevante para la función actual
        self.assertEqual(self.t.ganador(), "X")

    def test_gana_o_cuando_off_15(self):
        """'O' gana al alcanzar 15 fichas retiradas."""
        self.t.off["O"] = ["O"] * 15
        self.assertEqual(self.t.ganador(), "O")

    def test_prioridad_x_sobre_o_si_ambos_15(self):
        """Caso límite: si ambos llegan a 15, la función retorna 'X' primero."""
        self.t.off["X"] = ["X"] * 15
        self.t.off["O"] = ["O"] * 15
        self.assertEqual(self.t.ganador(), "X")


# =========================
# 8 TESTS DE REINGRESO (BARRA)
# =========================

class TestReingresoDesdeBarraX(unittest.TestCase):
    """Reingreso desde barra para X (origen = 0)."""

    def setUp(self):
        """Prepara barra X y destinos controlados para reingresos."""
        self.t = Tablero()
        self.t.bar["X"].clear()
        self.t.bar["O"].clear()
        for p in [5, 6, 7, 8]:
            self.t.tablero[p] = []

    def test_no_puede_entrar_si_bloqueado_por_2_o_mas_O(self):
        """X no puede reingresar a un punto bloqueado por 2+ 'O'."""
        self.t.bar["X"].append("X")
        self.t.tablero[6] = ["O", "O"]  # bloqueado
        ok = self.t.mover_ficha(0, 6)
        self.assertFalse(ok)
        self.assertIn("X", self.t.bar["X"])
        self.assertEqual(self.t.tablero[6], ["O", "O"])

    def test_entrar_en_destino_libre(self):
        """X reingresa a un punto vacío."""
        self.t.bar["X"].append("X")
        self.t.tablero[6] = []
        ok = self.t.mover_ficha(0, 6)
        self.assertTrue(ok)
        self.assertEqual(self.t.bar["X"], [])
        self.assertEqual(self.t.tablero[6], ["X"])

    def test_entrar_en_destino_propio(self):
        """X reingresa a un punto con fichas propias (apila)."""
        self.t.bar["X"].append("X")
        self.t.tablero[6] = ["X", "X"]
        ok = self.t.mover_ficha(0, 6)
        self.assertTrue(ok)
        self.assertEqual(self.t.bar["X"], [])
        self.assertEqual(self.t.tablero[6], ["X", "X", "X"])

    def test_comer_si_hay_una_sola_O(self):
        """X reingresa y come si hay exactamente una 'O' en destino."""
        self.t.bar["X"].append("X")
        self.t.tablero[6] = ["O"]  # blot rival
        ok = self.t.mover_ficha(0, 6)
        self.assertTrue(ok)
        self.assertEqual(self.t.bar["O"], ["O"])
        self.assertEqual(self.t.tablero[6], ["X"])


class TestReingresoDesdeBarraO(unittest.TestCase):
    """Reingreso desde barra para O (origen = 25)."""

    def setUp(self):
        """Prepara barra O y destinos controlados para reingresos."""
        self.t = Tablero()
        self.t.bar["X"].clear()
        self.t.bar["O"].clear()
        for p in [18, 19, 20, 21]:
            self.t.tablero[p] = []

    def test_no_puede_entrar_si_bloqueado_por_2_o_mas_X(self):
        """O no puede reingresar a un punto bloqueado por 2+ 'X'."""
        self.t.bar["O"].append("O")
        self.t.tablero[19] = ["X", "X"]
        ok = self.t.mover_ficha(25, 19)
        self.assertFalse(ok)
        self.assertIn("O", self.t.bar["O"])
        self.assertEqual(self.t.tablero[19], ["X", "X"])

    def test_entrar_en_destino_libre(self):
        """O reingresa a un punto vacío."""
        self.t.bar["O"].append("O")
        self.t.tablero[19] = []
        ok = self.t.mover_ficha(25, 19)
        self.assertTrue(ok)
        we = self.t.tablero[19]
        self.assertEqual(self.t.bar["O"], [])
        self.assertEqual(we, ["O"])

    def test_entrar_en_destino_propio(self):
        """O reingresa a un punto con fichas propias (apila)."""
        self.t.bar["O"].append("O")
        self.t.tablero[19] = ["O", "O"]
        ok = self.t.mover_ficha(25, 19)
        self.assertTrue(ok)
        self.assertEqual(self.t.bar["O"], [])
        self.assertEqual(self.t.tablero[19], ["O", "O", "O"])

    def test_comer_si_hay_una_sola_X(self):
        """O reingresa y come si hay exactamente una 'X' en destino."""
        self.t.bar["O"].append("O")
        self.t.tablero[19] = ["X"]
        ok = self.t.mover_ficha(25, 19)
        self.assertTrue(ok)
        self.assertEqual(self.t.bar["X"], ["X"])
        self.assertEqual(self.t.tablero[19], ["O"])


if __name__ == "__main__":
    unittest.main()
