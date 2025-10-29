# tests/test_cli.py
import unittest
from core.player import Player
from core.board import Tablero
from cli.cli import Interfaz   


class TestSorteoInicial(unittest.TestCase):
    def test_gana_x_a_la_primera(self):
        x = Player("Ana", "X")
        o = Player("Beto", "O")

        # Forzamos tiradas
        x.roll_dice = lambda: [6, 5]   # suma 11
        o.roll_dice = lambda: [3, 3]   # suma 6

        ganador = Interfaz().sorteo_inicial(x, o)
        self.assertEqual(ganador.get_name(), "Ana")

    def test_gana_o_a_la_primera(self):
        x = Player("Ana", "X")
        o = Player("Beto", "O")

        x.roll_dice = lambda: [2, 2]   # suma 4
        o.roll_dice = lambda: [4, 5]   # suma 9

        ganador = Interfaz().sorteo_inicial(x, o)
        self.assertEqual(ganador.get_name(), "Beto")

    def test_empate_y_luego_gana_o(self):
        x = Player("Ana", "X")
        o = Player("Beto", "O")

        # 1ª: empate (6 vs 6) | 2ª: gana O (2 vs 7)
        tiradas_x = iter([[3, 3], [1, 1]])   # 6 -> 2
        tiradas_o = iter([[4, 2], [6, 1]])   # 6 -> 7
        x.roll_dice = lambda: next(tiradas_x)
        o.roll_dice = lambda: next(tiradas_o)

        ganador = Interfaz().sorteo_inicial(x, o)
        self.assertEqual(ganador.get_name(), "Beto")

    def test_empate_y_luego_gana_x(self):
        x = Player("Ana", "X")
        o = Player("Beto", "O")

        # 1ª: empate (9 vs 9) | 2ª: gana X (8 vs 5)
        tiradas_x = iter([[4, 5], [2, 6]])   # 9 -> 8
        tiradas_o = iter([[3, 6], [4, 1]])   # 9 -> 5
        x.roll_dice = lambda: next(tiradas_x)
        o.roll_dice = lambda: next(tiradas_o)

        ganador = Interfaz().sorteo_inicial(x, o)
        self.assertEqual(ganador.get_name(), "Ana")

class Testmostrarmovimientos(unittest.TestCase):
    def test_tirada_sin_doble(self):
        jugador = Player("Ana", "X")
        ui = Interfaz()

        def roll_fijo():
            jugador.__dice__.last_rolls = [3, 5]
            return [3, 5]
        jugador.roll_dice = roll_fijo

        movimientos = ui.tirar_dados_y_mostrar(jugador)
        self.assertEqual(movimientos, [3, 5])

    def test_tirada_con_doble(self):
        jugador = Player("Beto", "O")
        ui = Interfaz()

        def roll_fijo():
            jugador.__dice__.last_rolls = [4, 4]
            return [4, 4]
        jugador.roll_dice = roll_fijo

        movimientos = ui.tirar_dados_y_mostrar(jugador)
        self.assertEqual(movimientos, [4, 4, 4, 4])

    def test_tirada_generica(self):
        jugador = Player("Carla", "X")
        ui = Interfaz()

        def roll_fijo():
            jugador.__dice__.last_rolls = [2, 3]
            return [2, 3]
        jugador.roll_dice = roll_fijo

        movimientos = ui.tirar_dados_y_mostrar(jugador)
        self.assertEqual(movimientos, [2, 3])

class TestMovimientos(unittest.TestCase):
    def setUp(self):
        # Interfaz con tablero real, sin prints de setup
        self.ui = Interfaz()
        self.ui.tablero = Tablero()
        self.x = Player("Ana", "X")
        self.o = Player("Beto", "O")

    def test_x_movimiento_valido_1_a_3(self):
        # Antes: X tiene 2 en el punto 1; 3 está vacío
        antes_1 = len(self.ui.tablero.tablero.get(1, []))
        antes_3 = len(self.ui.tablero.tablero.get(3, []))
        ok = self.ui.ejecutar_movimiento(self.x, 1, 3)
        self.assertTrue(ok)
        self.assertEqual(len(self.ui.tablero.tablero.get(1, [])), antes_1 - 1)
        self.assertEqual(len(self.ui.tablero.tablero.get(3, [])), antes_3 + 1)
        self.assertEqual(self.ui.tablero.tablero[3][-1], "X")

    def test_x_movimiento_bloqueado_1_a_6(self):
        # 6 está ocupado por O con 5 fichas al inicio -> bloqueado para X
        antes_1 = len(self.ui.tablero.tablero.get(1, []))
        antes_6 = len(self.ui.tablero.tablero.get(6, []))
        ok = self.ui.ejecutar_movimiento(self.x, 1, 6)
        self.assertFalse(ok)
        self.assertEqual(len(self.ui.tablero.tablero.get(1, [])), antes_1)  # sin cambios
        self.assertEqual(len(self.ui.tablero.tablero.get(6, [])), antes_6)

    def test_o_movimiento_valido_24_a_22(self):
        # Antes: O tiene 2 en el 24; 22 está vacío
        antes_24 = len(self.ui.tablero.tablero.get(24, []))
        antes_22 = len(self.ui.tablero.tablero.get(22, []))
        ok = self.ui.ejecutar_movimiento(self.o, 24, 22)
        self.assertTrue(ok)
        self.assertEqual(len(self.ui.tablero.tablero.get(24, [])), antes_24 - 1)
        self.assertEqual(len(self.ui.tablero.tablero.get(22, [])), antes_22 + 1)
        self.assertEqual(self.ui.tablero.tablero[22][-1], "O")

    def test_o_movimiento_bloqueado_13_a_12(self):
        # 12 está ocupado por X con 5 fichas al inicio -> bloqueado para O
        antes_13 = len(self.ui.tablero.tablero.get(13, []))
        antes_12 = len(self.ui.tablero.tablero.get(12, []))
        ok = self.ui.ejecutar_movimiento(self.o, 13, 12)
        self.assertFalse(ok)
        self.assertEqual(len(self.ui.tablero.tablero.get(13, [])), antes_13)
        self.assertEqual(len(self.ui.tablero.tablero.get(12, [])), antes_12)

if __name__ == "__main__":
    unittest.main()
