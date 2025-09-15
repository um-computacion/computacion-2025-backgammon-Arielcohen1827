import unittest
from core.board import Tablero   # usamos Tablero con Checker integrado


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

    def test_no_mover_a_bloqueado(self):
        # Punto 19 arranca con 5 fichas "X"
        # Una "O" desde 13 no debería poder moverse allí
        self.assertFalse(self.juego.mover_ficha(13, 19))

class TestMovimientoDireccion(unittest.TestCase):

    def setUp(self):
        self.juego = Tablero()

    def test_o_no_puede_subir(self):
        # Ficha "O" en 13 intenta ir a 15 (subir → inválido)
        self.assertFalse(self.juego.mover_ficha(13, 15))
        # Debe seguir habiendo 5 fichas en 13
        self.assertEqual(len(self.juego.tablero[13]), 5)
        self.assertNotIn(15, self.juego.tablero)

    def test_o_puede_bajar(self):
        # Ficha "O" en 13 baja a 11 (válido)
        self.assertTrue(self.juego.mover_ficha(13, 11))
        self.assertEqual(len(self.juego.tablero[13]), 4)
        self.assertEqual(len(self.juego.tablero[11]), 1)

    def test_x_no_puede_bajar(self):
        # Ficha "X" en 1 intenta ir a 0 (bajar → inválido)
        self.assertFalse(self.juego.mover_ficha(1, 0))
        self.assertEqual(len(self.juego.tablero[1]), 2)
        self.assertNotIn(0, self.juego.tablero)

    def test_x_puede_subir(self):
        # Ficha "X" en 1 sube a 3 (válido)
        self.assertTrue(self.juego.mover_ficha(1, 3))
        self.assertEqual(len(self.juego.tablero[1]), 1)
        self.assertEqual(len(self.juego.tablero[3]), 1)



if __name__ == "__main__":
    unittest.main()
