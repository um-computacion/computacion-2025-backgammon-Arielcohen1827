import unittest
from core.board import Tablero   # ✅ ahora usamos Tablero

class TestMostrarTablero(unittest.TestCase):

    def test_contiene_numeros(self):
        tablero = Tablero().mostrar()
        self.assertIn("13", tablero)
        self.assertIn("24", tablero)
        self.assertIn("12", tablero)
        self.assertIn(" 1 ", tablero)

    def test_contiene_fichas(self):
        tablero = Tablero().mostrar()
        self.assertIn("O", tablero)
        self.assertIn("X", tablero)

    def test_cantidad_lineas(self):
        tablero = Tablero().mostrar().split("\n")
        self.assertEqual(len(tablero), 19)


class TestMovimientoFichas(unittest.TestCase):

    def setUp(self):
        self.juego = Tablero()

    def test_mover_ficha_valida(self):
        # Punto 13 tiene 5 fichas "O" al inicio
        self.assertEqual(len(self.juego.tablero[13]), 5)
        self.juego.mover_ficha(13, 11)
        # Ahora 13 debería tener 4 y 11 debería tener 1
        self.assertEqual(len(self.juego.tablero[13]), 4)
        self.assertEqual(len(self.juego.tablero[11]), 1)

    def test_mover_ficha_origen_vacio(self):
        # El punto 2 arranca vacío
        self.assertFalse(self.juego.mover_ficha(2, 5))
        # Nada cambia
        self.assertNotIn(2, self.juego.tablero)

    def test_mover_varias_fichas(self):
        self.juego.mover_ficha(24, 10)
        self.juego.mover_ficha(24, 10)
        # 24 empieza con 2 fichas, después de mover 2 queda vacío
        self.assertEqual(len(self.juego.tablero[24]), 0)
        self.assertEqual(len(self.juego.tablero[10]), 2)

    def test_mover_preserva_tipo(self):
        # Mover ficha de jugador O desde 13 a 7
        ficha = self.juego.tablero[13][-1]
        self.juego.mover_ficha(13, 7)
        self.assertIn(ficha, self.juego.tablero[7])


if __name__ == "__main__":
    unittest.main()
