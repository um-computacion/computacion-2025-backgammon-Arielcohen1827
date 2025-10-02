# tests/test_cli.py
import unittest
from core.player import Player
from cli.cli import Interfaz


class TestSorteoInicial(unittest.TestCase):
    def test_gana_x_a_la_primera(self):
        x = Player("Ana", "X")
        o = Player("Beto", "O")

        # Sobreescribo el método roll_dice directamente
        x.roll_dice = lambda: [6, 5]   # suma 11
        o.roll_dice = lambda: [3, 3]   # suma 6

        ganador = Interfaz().sorteo_inicial(x, o)
        self.assertEqual(ganador, "Ana")

    def test_gana_o_a_la_primera(self):
        x = Player("Ana", "X")
        o = Player("Beto", "O")

        x.roll_dice = lambda: [2, 2]   # suma 4
        o.roll_dice = lambda: [4, 5]   # suma 9

        ganador = Interfaz().sorteo_inicial(x, o)
        self.assertEqual(ganador, "Beto")

    def test_empate_y_luego_gana_o(self):
        x = Player("Ana", "X")
        o = Player("Beto", "O")

        # En este caso necesitamos dos tiradas: usamos un iterador
        tiradas_x = iter([[3, 3], [1, 1]])   # 6 → 2
        tiradas_o = iter([[4, 2], [6, 1]])   # 6 → 7
        x.roll_dice = lambda: next(tiradas_x)
        o.roll_dice = lambda: next(tiradas_o)

        ganador = Interfaz().sorteo_inicial(x, o)
        self.assertEqual(ganador, "Beto")

    def test_empate_y_luego_gana_x(self):
        x = Player("Ana", "X")
        o = Player("Beto", "O")

        # En este caso necesitamos dos tiradas: usamos un iterador
        tiradas_x = iter([[4, 5], [2, 6]])   # 9 → 8
        tiradas_o = iter([[3, 6], [4, 1]])   # 9 → 5
        x.roll_dice = lambda: next(tiradas_x)
        o.roll_dice = lambda: next(tiradas_o)

        ganador = Interfaz().sorteo_inicial(x, o)
        self.assertEqual(ganador, "Ana")



if __name__ == "__main__":
    unittest.main()
