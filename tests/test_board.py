import unittest
from core.board import mostrar_tablero
class TestMostrarTablero(unittest.TestCase):

    def test_contiene_numeros(self):
        tablero = mostrar_tablero()
        self.assertIn("13", tablero)
        self.assertIn("24", tablero)
        self.assertIn("12", tablero)
        self.assertIn(" 1 ", tablero)

    def test_contiene_fichas(self):
        tablero = mostrar_tablero()
        self.assertIn("O", tablero)
        self.assertIn("X", tablero)

    def test_cantidad_lineas(self):
        tablero = mostrar_tablero().split("\n")
        self.assertEqual(len(tablero), 19)

if __name__ == "__main__":
    unittest.main()