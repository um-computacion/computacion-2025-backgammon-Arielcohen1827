# tests/test_cli.py
"""Tests unitarios e integrados para el módulo cli.cli.Interfaz.

Este archivo valida el comportamiento de la interfaz de consola:
- Sorteo inicial de jugadores (empates, repeticiones y ganadores correctos).
- Tiradas de dados y generación de movimientos válidos.
- Ejecución de movimientos válidos, inválidos y bloqueados.
- Confirmaciones y cancelaciones dentro del turno.
- Recolección de nombres e impresión de jugadores.
- Flujo principal `main()` con salida anticipada.
"""

import unittest
from unittest.mock import patch
from core.player import Player
from core.board import Tablero
from cli.cli import Interfaz


class TestSorteoInicial(unittest.TestCase):
    """Pruebas del método sorteo_inicial() para determinar quién inicia."""

    def test_gana_x_a_la_primera(self):
        """Si X obtiene mayor suma, debe comenzar la partida."""
        x = Player("Ana", "X")
        o = Player("Beto", "O")
        x.roll_dice = lambda: [6, 5]
        o.roll_dice = lambda: [3, 3]
        ganador = Interfaz().sorteo_inicial(x, o)
        self.assertEqual(ganador.get_name(), "Ana")

    def test_gana_o_a_la_primera(self):
        """Si O obtiene mayor suma, debe comenzar la partida."""
        x = Player("Ana", "X")
        o = Player("Beto", "O")
        x.roll_dice = lambda: [2, 2]
        o.roll_dice = lambda: [4, 5]
        ganador = Interfaz().sorteo_inicial(x, o)
        self.assertEqual(ganador.get_name(), "Beto")

    def test_empate_y_luego_gana_o(self):
        """En caso de empate, debe repetirse hasta que haya ganador (O gana)."""
        x = Player("Ana", "X")
        o = Player("Beto", "O")
        tiradas_x = iter([[3, 3], [1, 1]])
        tiradas_o = iter([[4, 2], [6, 1]])
        x.roll_dice = lambda: next(tiradas_x)
        o.roll_dice = lambda: next(tiradas_o)
        ganador = Interfaz().sorteo_inicial(x, o)
        self.assertEqual(ganador.get_name(), "Beto")

    def test_empate_y_luego_gana_x(self):
        """En caso de empate, debe repetirse hasta que haya ganador (X gana)."""
        x = Player("Ana", "X")
        o = Player("Beto", "O")
        tiradas_x = iter([[4, 5], [2, 6]])
        tiradas_o = iter([[3, 6], [4, 1]])
        x.roll_dice = lambda: next(tiradas_x)
        o.roll_dice = lambda: next(tiradas_o)
        ganador = Interfaz().sorteo_inicial(x, o)
        self.assertEqual(ganador.get_name(), "Ana")


class TestMostrarMovimientos(unittest.TestCase):
    """Verifica el comportamiento de tirar_dados_y_mostrar()."""

    def test_tirada_sin_doble(self):
        """Con tirada normal debe devolver dos movimientos."""
        jugador = Player("Ana", "X")
        ui = Interfaz()

        def roll_fijo():
            jugador.__dice__.last_rolls = [3, 5]
            return [3, 5]
        jugador.roll_dice = roll_fijo

        movimientos = ui.tirar_dados_y_mostrar(jugador)
        self.assertEqual(movimientos, [3, 5])

    def test_tirada_con_doble(self):
        """Con tirada doble debe devolver cuatro movimientos iguales."""
        jugador = Player("Beto", "O")
        ui = Interfaz()

        def roll_fijo():
            jugador.__dice__.last_rolls = [4, 4]
            return [4, 4]
        jugador.roll_dice = roll_fijo

        movimientos = ui.tirar_dados_y_mostrar(jugador)
        self.assertEqual(movimientos, [4, 4, 4, 4])

    def test_tirada_generica(self):
        """Verifica una tirada genérica sin repeticiones."""
        jugador = Player("Carla", "X")
        ui = Interfaz()

        def roll_fijo():
            jugador.__dice__.last_rolls = [2, 3]
            return [2, 3]
        jugador.roll_dice = roll_fijo

        movimientos = ui.tirar_dados_y_mostrar(jugador)
        self.assertEqual(movimientos, [2, 3])


class TestMovimientos(unittest.TestCase):
    """Pruebas de ejecución de movimientos en la interfaz."""

    def setUp(self):
        """Configura interfaz y tablero antes de cada prueba."""
        self.ui = Interfaz()
        self.ui.tablero = Tablero()
        self.x = Player("Ana", "X")
        self.o = Player("Beto", "O")

    def test_x_movimiento_valido_1_a_3(self):
        """Movimiento válido de X desde 1 hacia 3."""
        antes_1 = len(self.ui.tablero.tablero.get(1, []))
        antes_3 = len(self.ui.tablero.tablero.get(3, []))
        ok = self.ui.ejecutar_movimiento(self.x, 1, 3)
        self.assertTrue(ok)
        self.assertEqual(len(self.ui.tablero.tablero.get(1, [])), antes_1 - 1)
        self.assertEqual(len(self.ui.tablero.tablero.get(3, [])), antes_3 + 1)
        self.assertEqual(self.ui.tablero.tablero[3][-1], "X")

    def test_x_movimiento_bloqueado_1_a_6(self):
        """X intenta mover a punto bloqueado por O."""
        antes_1 = len(self.ui.tablero.tablero.get(1, []))
        antes_6 = len(self.ui.tablero.tablero.get(6, []))
        ok = self.ui.ejecutar_movimiento(self.x, 1, 6)
        self.assertFalse(ok)
        self.assertEqual(len(self.ui.tablero.tablero.get(1, [])), antes_1)
        self.assertEqual(len(self.ui.tablero.tablero.get(6, [])), antes_6)

    def test_o_movimiento_valido_24_a_22(self):
        """Movimiento válido de O desde 24 hacia 22."""
        antes_24 = len(self.ui.tablero.tablero.get(24, []))
        antes_22 = len(self.ui.tablero.tablero.get(22, []))
        ok = self.ui.ejecutar_movimiento(self.o, 24, 22)
        self.assertTrue(ok)
        self.assertEqual(len(self.ui.tablero.tablero.get(24, [])), antes_24 - 1)
        self.assertEqual(len(self.ui.tablero.tablero.get(22, [])), antes_22 + 1)
        self.assertEqual(self.ui.tablero.tablero[22][-1], "O")

    def test_o_movimiento_bloqueado_13_a_12(self):
        """O intenta mover a punto bloqueado por X."""
        antes_13 = len(self.ui.tablero.tablero.get(13, []))
        antes_12 = len(self.ui.tablero.tablero.get(12, []))
        ok = self.ui.ejecutar_movimiento(self.o, 13, 12)
        self.assertFalse(ok)
        self.assertEqual(len(self.ui.tablero.tablero.get(13, [])), antes_13)
        self.assertEqual(len(self.ui.tablero.tablero.get(12, [])), antes_12)


class TestConsumirMovimiento(unittest.TestCase):
    """Pruebas para _consumir_movimiento()."""

    def setUp(self):
        """Crea una interfaz vacía antes de cada test."""
        self.ui = Interfaz()

    def test_consumir_movimiento_existe(self):
        """Elimina correctamente un movimiento existente."""
        movimientos = [3, 5, 6]
        ok = self.ui._consumir_movimiento(movimientos, 5)
        self.assertTrue(ok)
        self.assertNotIn(5, movimientos)

    def test_consumir_movimiento_no_existe(self):
        """Devuelve False si el movimiento no está disponible."""
        movimientos = [3, 4]
        ok = self.ui._consumir_movimiento(movimientos, 6)
        self.assertFalse(ok)
        self.assertEqual(movimientos, [3, 4])


class TestPedirMovimiento(unittest.TestCase):
    """Pruebas de entrada del usuario en pedir_movimiento()."""

    def setUp(self):
        self.ui = Interfaz()

    @patch("builtins.input", return_value="13-11")
    def test_pedir_movimiento_valido(self, mock_input):
        """Entrada válida '13-11' debe retornar (13, 11)."""
        resultado = self.ui.pedir_movimiento()
        self.assertEqual(resultado, (13, 11))

    @patch("builtins.input", return_value="texto_invalido")
    def test_pedir_movimiento_invalido(self, mock_input):
        """Entrada inválida debe devolver None."""
        resultado = self.ui.pedir_movimiento()
        self.assertIsNone(resultado)


class TestJugarTurnoBasico(unittest.TestCase):
    """Pruebas del flujo simplificado de jugar_turno()."""

    def setUp(self):
        self.ui = Interfaz()
        self.ui.tablero = Tablero()
        self.jugador = Player("Ana", "X")

    @patch("cli.cli.input", side_effect=["1-3", "s", ""])
    def test_jugar_turno_un_movimiento_valido(self, mock_input):
        """Ejecuta un turno con movimiento válido y confirmación."""
        self.jugador.roll_dice = lambda: [2, 3]
        self.jugador.__dice__.last_rolls = [2, 3]
        with patch("builtins.print"):
            self.ui.jugar_turno(self.jugador)
        self.assertIn("X", self.ui.tablero.tablero[3])

    @patch("cli.cli.input", side_effect=["1-0", ""])
    def test_jugar_turno_mov_invalido(self, mock_input):
        """Intenta movimiento inválido (dirección incorrecta)."""
        self.jugador.roll_dice = lambda: [2, 3]
        self.jugador.__dice__.last_rolls = [2, 3]
        antes_len_p1 = len(self.ui.tablero.tablero[1])
        antes_barra_x = len(self.ui.tablero.tablero[0])
        with patch("builtins.print"):
            self.ui.jugar_turno(self.jugador)
        self.assertEqual(len(self.ui.tablero.tablero[1]), antes_len_p1)
        self.assertEqual(len(self.ui.tablero.tablero[0]), antes_barra_x)

    @patch("cli.cli.input", side_effect=[""])
    def test_jugar_turno_pasa_turno(self, mock_input):
        """El jugador presiona ENTER y pasa el turno."""
        self.jugador.roll_dice = lambda: [5, 3]
        self.jugador.__dice__.last_rolls = [5, 3]
        with patch("builtins.print"):
            self.ui.jugar_turno(self.jugador)
        self.assertTrue(isinstance(self.ui.tablero.tablero, dict))


class TestInterfazInicio(unittest.TestCase):
    """Pruebas iniciales de creación de jugadores y tablero."""

    @patch("cli.cli.input", side_effect=["Ana", "Beto"])
    def test_pedir_nombres_asignados(self, mock_input):
        """Verifica que los nombres ingresados se asignen correctamente."""
        ui = Interfaz()
        ui.pedir_nombres()
        self.assertEqual(ui.jugador_x.get_name(), "Ana")
        self.assertEqual(ui.jugador_o.get_name(), "Beto")

    @patch("cli.cli.input", side_effect=["", ""])
    def test_pedir_nombres_por_defecto(self, mock_input):
        """Verifica que se usen nombres por defecto si no se ingresa texto."""
        ui = Interfaz()
        ui.pedir_nombres()
        self.assertEqual(ui.jugador_x.get_name(), "Jugador X")
        self.assertEqual(ui.jugador_o.get_name(), "Jugador O")

    def test_mostrar_jugadores_salida(self):
        """Debe imprimir correctamente ambos jugadores."""
        ui = Interfaz()
        ui.jugador_x = Player("Ana", "X")
        ui.jugador_o = Player("Beto", "O")
        with patch("builtins.print") as mock_print:
            ui.mostrar_jugadores()
        output = " ".join(call.args[0] for call in mock_print.call_args_list)
        self.assertIn("Ana", output)
        self.assertIn("Beto", output)

    def test_crear_y_mostrar_tablero(self):
        """Debe crear un objeto Tablero e imprimirlo."""
        ui = Interfaz()
        with patch("builtins.print"):
            ui.crear_y_mostrar_tablero()
        self.assertIsInstance(ui.tablero, Tablero)


class TestConfirmacionesYCancelaciones(unittest.TestCase):
    """Pruebas sobre confirmaciones y cancelaciones en jugar_turno()."""

    def setUp(self):
        """Configura interfaz, tablero y jugador X antes de cada prueba."""
        self.ui = Interfaz()
        self.ui.tablero = Tablero()
        self.jugador = Player("Ana", "X")
        self.jugador.roll_dice = lambda: [2, 3]
        self.jugador.__dice__.last_rolls = [2, 3]

    @patch("cli.cli.input", side_effect=["1-3", "n", ""])
    def test_movimiento_cancelado_por_jugador(self, mock_input):
        """El jugador cancela manualmente después de la vista previa."""
        with patch("builtins.print"):
            self.ui.jugar_turno(self.jugador)
        self.assertEqual(len(self.ui.tablero.tablero[1]), 2)

    @patch("cli.cli.input", side_effect=["1-9", "s", ""])
    def test_movimiento_no_valido_fuera_de_rango(self, mock_input):
        """Intenta mover con distancia no disponible en los dados."""
        with patch("builtins.print"):
            self.ui.jugar_turno(self.jugador)
        self.assertEqual(len(self.ui.tablero.tablero[1]), 2)

    @patch("cli.cli.input", side_effect=["1-3", "s", ""])
    def test_consumir_movimiento_repetido(self, mock_input):
        """Ejecuta un movimiento válido una vez y evita repetirlo."""
        self.jugador.roll_dice = lambda: [2, 3]
        self.jugador.__dice__.last_rolls = [2, 3]
        with patch("builtins.print"):
            self.ui.jugar_turno(self.jugador)
        self.assertIn("X", self.ui.tablero.tablero[3])


class TestMainFlow(unittest.TestCase):
    """Prueba el flujo principal main() con salida rápida."""

    @patch("cli.cli.input", side_effect=["Ana", "Beto", "q"])
    def test_main_crea_jugadores_y_sale(self, mock_input):
        """Simula ejecución completa de main() hasta la salida con 'q'."""
        ui = Interfaz()
        with patch.object(Interfaz, "sorteo_inicial", return_value=Player("Ana", "X")), \
             patch.object(Interfaz, "jugar_turno", return_value=None), \
             patch("builtins.print"):
            ui.main()
        self.assertIsInstance(ui.jugador_x, Player)
        self.assertIsInstance(ui.jugador_o, Player)


if __name__ == "__main__":
    unittest.main()
