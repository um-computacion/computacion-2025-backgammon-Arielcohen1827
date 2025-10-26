import unittest
from core.board import Tablero   # usamos Tablero con Checker integrado


class TestMostrarTablero(unittest.TestCase):

    def setUp(self):
        self.juego = Tablero()

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
        tablero = self.juego.mostrar().splitlines()

        # Detecto si imprime barra/off
        muestra_barra = any("Barra X" in ln or "Barra O" in ln for ln in tablero) or \
                        any("Off X" in ln or "Off O" in ln for ln in tablero)

        if muestra_barra:
            # Layout nuevo (19 base + 3 extras: línea en blanco + 2 barras + 2 off = 22)
            self.assertEqual(len(tablero), 22)
        else:
            # Layout clásico (sin barra/off)
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
        self.assertFalse(self.juego.mover_ficha(12, 9))
        self.assertEqual(len(self.juego.tablero[12]), 5)
        self.assertNotIn(9, self.juego.tablero)

    def test_x_puede_subir(self):
        # Ficha "X" en 1 sube a 3 (válido)
        self.assertTrue(self.juego.mover_ficha(1, 3))
        self.assertEqual(len(self.juego.tablero[1]), 1)
        self.assertEqual(len(self.juego.tablero[3]), 1)

class TestComerFicha(unittest.TestCase):

    def setUp(self):
        self.juego = Tablero()

    def test_o_come_a_x(self):
        # Preparamos un destino con una sola "X"
        self.juego.tablero[5] = ["X"]
        # Movemos "O" desde 6 a 5 (O baja → válido y debería comer a X)
        resultado = self.juego.mover_ficha(6, 5)
        self.assertTrue(resultado)
        # El punto 5 ahora debe tener solo una "O"
        self.assertEqual(self.juego.tablero[5], ["O"])
        # La "X" debe estar en la barra
        self.assertEqual(self.juego.bar["X"], ["X"])

    def test_x_come_a_o(self):
        # Preparamos un destino con una sola "O"
        self.juego.tablero[14] = ["O"]
        # Movemos "X" desde 12 a 14 (X sube → válido y debería comer a O)
        resultado = self.juego.mover_ficha(12, 14)
        self.assertTrue(resultado)
        # El punto 14 ahora debe tener solo una "X"
        self.assertEqual(self.juego.tablero[14], ["X"])
        # La "O" debe estar en la barra
        self.assertEqual(self.juego.bar["O"], ["O"])

    def test_no_comer_si_hay_mas_de_una(self):
        # Preparamos un destino con 2 "X" (bloqueado para O)
        self.juego.tablero[5] = ["X", "X"]
        resultado = self.juego.mover_ficha(6, 5)
        # Movimiento inválido (bloqueado), no se mueve ni se come
        self.assertFalse(resultado)
        self.assertEqual(self.juego.tablero[5], ["X", "X"])
        self.assertEqual(self.juego.bar["X"], [])

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
        
class TestMovimientoConBarra(unittest.TestCase):

    def setUp(self):
        self.juego = Tablero()

    def test_o_no_puede_mover_si_tiene_en_barra(self):
        # Forzamos a que O tenga una ficha en la barra
        self.juego.bar["O"].append("O")
        # Intentamos mover otra ficha O desde 13 a 11
        resultado = self.juego.mover_ficha(13, 11)
        self.assertFalse(resultado)
        # El tablero no debería cambiar
        self.assertEqual(len(self.juego.tablero[13]), 5)
        self.assertNotIn(11, self.juego.tablero)

    def test_x_no_puede_mover_si_tiene_en_barra(self):
        # Forzamos a que X tenga una ficha en la barra
        self.juego.bar["X"].append("X")
        # Intentamos mover otra ficha X desde 1 a 3
        resultado = self.juego.mover_ficha(1, 3)
        self.assertFalse(resultado)
        # El tablero no debería cambiar
        self.assertEqual(len(self.juego.tablero[1]), 2)
        self.assertNotIn(3, self.juego.tablero)

class TestBearingOff(unittest.TestCase):

    def setUp(self):
        self.juego = Tablero()

    def test_o_no_puede_retirar_si_no_todas_en_cuadrante(self):
        # Intentamos retirar una "O" desde el punto 13 → no debería poder
        resultado = self.juego.mover_ficha(13, 0)
        self.assertFalse(resultado)
        self.assertEqual(self.juego.off["O"], [])

    def test_x_no_puede_retirar_si_no_todas_en_cuadrante(self):
        # Intentamos retirar una "X" desde el punto 12 → no debería poder
        resultado = self.juego.mover_ficha(12, 25)
        self.assertFalse(resultado)
        self.assertEqual(self.juego.off["X"], [])

    def test_o_puede_retirar_cuando_todas_en_cuadrante(self):
        # Preparamos el tablero con todas las fichas O en [1–6]
        self.juego.tablero = {
            1: ["O"] * 2,
            2: ["O"] * 3,
            3: ["O"] * 5,
            6: ["O"] * 5,
            19: ["X"] * 5,
            24: ["X"] * 10,
        }
        # Retiramos una ficha O desde el punto 6
        resultado = self.juego.mover_ficha(6, 0)
        self.assertTrue(resultado)
        self.assertEqual(self.juego.off["O"], ["O"])
        self.assertEqual(len(self.juego.tablero[6]), 4)

    def test_x_puede_retirar_cuando_todas_en_cuadrante(self):
        # Preparamos el tablero con todas las fichas X en [19–24]
        self.juego.tablero = {
            19: ["X"] * 5,
            20: ["X"] * 3,
            24: ["X"] * 7,
            6: ["O"] * 10,
        }
        # Retiramos una ficha X desde el punto 24
        resultado = self.juego.mover_ficha(24, 25)
        self.assertTrue(resultado)
        self.assertEqual(self.juego.off["X"], ["X"])
        self.assertEqual(len(self.juego.tablero[24]), 6)

    def test_varias_fichas_retiradas(self):
        # Preparamos todas las fichas O en [1–6]
        self.juego.tablero = {
            1: ["O"] * 15,
            19: ["X"] * 15,
        }
        # Retiramos 3 fichas
        self.juego.mover_ficha(1, 0)
        self.juego.mover_ficha(1, 0)
        self.juego.mover_ficha(1, 0)
        self.assertEqual(len(self.juego.off["O"]), 3)
        self.assertEqual(len(self.juego.tablero[1]), 12)

class TestFichasRestantes(unittest.TestCase):
    def setUp(self):
        self.t = Tablero()
        # Partimos de un estado controlado
        self.t.tablero.clear()
        self.t.bar = {"X": [], "O": []}
        self.t.off = {"X": [], "O": []}

    def test_cuenta_en_tablero(self):
        # 3 X en punto 6, 2 O en punto 12
        self.t.tablero[6] = ["X", "X", "X"]
        self.t.tablero[12] = ["O", "O"]
        self.assertEqual(self.t.fichas_restantes("X"), 3)
        self.assertEqual(self.t.fichas_restantes("O"), 2)

    def test_incluye_barra_pero_no_off(self):
        # 2 X en tablero + 1 X en barra + 5 X en off
        self.t.tablero[5] = ["X", "X"]
        self.t.bar["X"] = ["X"]
        self.t.off["X"] = ["X"] * 5
        # 1 O en tablero + 2 O en barra
        self.t.tablero[10] = ["O"]
        self.t.bar["O"] = ["O", "O"]
        self.assertEqual(self.t.fichas_restantes("X"), 3)  # 2 tablero + 1 barra
        self.assertEqual(self.t.fichas_restantes("O"), 3)  # 1 tablero + 2 barra

class TestGanador(unittest.TestCase):
    def setUp(self):
        self.t = Tablero()
        # Estado controlado
        self.t.tablero.clear()
        self.t.bar = {"X": [], "O": []}
        self.t.off = {"X": [], "O": []}

    def test_sin_ganador(self):
        # Aún con fichas en tablero y/o barra, off < 15
        self.t.tablero[24] = ["X"] * 10
        self.t.bar["X"] = ["X"] * 2
        self.t.off["X"] = ["X"] * 3  # total 15 repartidas, pero off != 15 → no gana
        self.assertIsNone(self.t.ganador())

    def test_gana_x_cuando_off_15(self):
        self.t.off["X"] = ["X"] * 15
        # Aunque quede algo en tablero (no debería pasar en juego real), gana por definición de la función
        self.t.tablero[1] = ["X"]
        self.assertEqual(self.t.ganador(), "X")

    def test_gana_o_cuando_off_15(self):
        self.t.off["O"] = ["O"] * 15
        self.t.bar["O"] = []  # irrelevante
        self.assertEqual(self.t.ganador(), "O")

    def test_prioridad_x_sobre_o_si_ambos_15(self):
        # Caso límite: ambos tienen 15 off. Según implementación, retorna X primero.
        self.t.off["X"] = ["X"] * 15
        self.t.off["O"] = ["O"] * 15
        self.assertEqual(self.t.ganador(), "X")
class TestReingresoDesdeBarraX(unittest.TestCase):
    def setUp(self):
        self.t = Tablero()
        # Estado limpio y controlado para estos tests
        self.t.bar["X"].clear()
        self.t.bar["O"].clear()
        # Vaciar destinos que vamos a usar
        for p in [5, 6, 7, 8]:
            self.t.tablero[p] = []

    def test_no_puede_entrar_si_bloqueado_por_2_o_mas_O(self):
        # Barra X con 1 ficha
        self.t.bar["X"].append("X")
        # Destino con 2 O => bloqueado
        self.t.tablero[6] = ["O", "O"]
        ok = self.t.mover_ficha(0, 6)
        self.assertFalse(ok)
        self.assertIn("X", self.t.bar["X"])             # no salió de la barra
        self.assertEqual(self.t.tablero[6], ["O","O"])  # destino intacto

    def test_entrar_en_destino_libre(self):
        self.t.bar["X"].append("X")
        self.t.tablero[6] = []                          # libre
        ok = self.t.mover_ficha(0, 6)
        self.assertTrue(ok)
        self.assertEqual(self.t.bar["X"], [])           # salió de barra
        self.assertEqual(self.t.tablero[6], ["X"])      # entró 1 X

    def test_entrar_en_destino_propio(self):
        self.t.bar["X"].append("X")
        self.t.tablero[6] = ["X","X"]                   # propio
        ok = self.t.mover_ficha(0, 6)
        self.assertTrue(ok)
        self.assertEqual(self.t.bar["X"], [])
        self.assertEqual(self.t.tablero[6], ["X","X","X"])

    def test_comer_si_hay_una_sola_O(self):
        self.t.bar["X"].append("X")
        self.t.tablero[6] = ["O"]                       # un blot rival
        ok = self.t.mover_ficha(0, 6)
        self.assertTrue(ok)
        # La O fue enviada a su barra
        self.assertEqual(self.t.bar["O"], ["O"])
        # Quedó la X en el punto
        self.assertEqual(self.t.tablero[6], ["X"])




if __name__ == "__main__":
    unittest.main()

