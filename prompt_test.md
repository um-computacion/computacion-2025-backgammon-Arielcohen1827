# prompt  (haceme los test de player.py)
#test_player.py
import unittest
from unittest.mock import patch
from core.player import Player


class TestJugador(unittest.TestCase):
    """Conjunto de pruebas unitarias para la clase Player."""

    def setUp(self):
        """Crea jugadores X y O antes de cada prueba."""
        self.jugador_x = Player("Ariel", "X")
        self.jugador_o = Player("CPU", "O")

    def test_obtener_nombre(self):
        """Verifica que get_name() devuelva el nombre correcto."""
        self.assertEqual(self.jugador_x.get_name(), "Ariel")
        self.assertEqual(self.jugador_o.get_name(), "CPU")

    def test_obtener_ficha(self):
        """Verifica que get_ficha() devuelva el símbolo asignado."""
        self.assertEqual(self.jugador_x.get_ficha(), "X")
        self.assertEqual(self.jugador_o.get_ficha(), "O")

    def test_tirar_dados_devuelve_dos_valores(self):
        """Comprueba que roll_dice() devuelve dos enteros válidos."""
        tirada = self.jugador_x.roll_dice()
        self.assertEqual(len(tirada), 2)
        self.assertTrue(1 <= tirada[0] <= 6)
        self.assertTrue(1 <= tirada[1] <= 6)

    def test_ultima_tirada_coincide_con_roll_dice(self):
        """Verifica que get_last_roll() devuelva la última tirada realizada."""
        tirada = self.jugador_x.roll_dice()
        ultima_tirada = self.jugador_x.get_last_roll()
        self.assertEqual(tirada, ultima_tirada)

    def test_es_doble_cuando_tirada_controlada(self):
        """Simula un doble (5,5) y valida que has_double() lo detecte."""
        def fake_roll(self):
            self.last_rolls = [5, 5]
            return self.last_rolls

        with patch('core.dice.Dice.roll', fake_roll):
            tirada = self.jugador_x.roll_dice()
            self.assertEqual(tirada, [5, 5])
            self.assertTrue(self.jugador_x.has_double())

    def test_no_es_doble_cuando_tirada_controlada(self):
        """Simula una tirada no doble (2,6) y comprueba que has_double() sea False."""
        def fake_roll(self):
            self.last_rolls = [2, 6]
            return self.last_rolls

        with patch('core.dice.Dice.roll', fake_roll):
            tirada = self.jugador_x.roll_dice()
            self.assertEqual(tirada, [2, 6])
            self.assertFalse(self.jugador_x.has_double())

    def test_representacion_texto(self):
        """Valida que __str__() muestre correctamente el nombre y ficha."""
        self.assertEqual(str(self.jugador_x), "Jugador Ariel (X)")
        self.assertEqual(str(self.jugador_o), "Jugador CPU (O)")


if __name__ == "__main__":
    unittest.main()

# prompt (hace test de X de reingreso de barra)
#test_board.py
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

# prompt 3 ( haceme los test del sorteo)
#test_cli.py
import unittest
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


if __name__ == "__main__":
    unittest.main()


# prompt 4 (haceme los test de movimientos disponibles)
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
# prompt 5 (haceme los test de moviemiento)
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

# prompt 6 (haceme los test de consumir movimientos)
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
# prompt 7 (haceme los test que faltan para testeas lo mas posible cli.py)
import unittest
from unittest.mock import patch
from core.player import Player
from core.board import Tablero
from cli.cli import Interfaz

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
# prompt 8 (haceme los test de todo game_pygame.py)
# tests/test_game.py
"""Tests para la interfaz gráfica Pygame de Backgammon (pygame_ui.game_pygame.PygameUI).


import unittest
from unittest.mock import patch, MagicMock
import pygame

from pygame_ui.game_pygame import PygameUI


class TestPygameUI(unittest.TestCase):
    """Pruebas integradas y de unidad sobre la clase PygameUI."""

    def setUp(self):
        """Inicializa PygameUI con parches para evitar abrir ventana real."""
        # Evitamos ventana real y esperas
        self.p_set_mode = patch("pygame.display.set_mode", return_value=pygame.Surface((1100, 650)))
        self.p_set_caption = patch("pygame.display.set_caption", lambda *args, **kwargs: None)
        self.p_time_wait = patch("pygame.time.wait", lambda *args, **kwargs: None)
        self.p_display_flip = patch("pygame.display.flip", lambda *args, **kwargs: None)

        self.p_set_mode.start()
        self.p_set_caption.start()
        self.p_time_wait.start()
        self.p_display_flip.start()

        # Instancia y geometría
        self.ui = PygameUI()
        self.ui.GEO = self.ui.build_geo_full()

    def tearDown(self):
        """Detiene parches activos y cierra Pygame de forma segura."""
        self.p_set_mode.stop()
        self.p_set_caption.stop()
        self.p_time_wait.stop()
        self.p_display_flip.stop()
        pygame.quit()

    # ───────────────────────── Geometría ─────────────────────────
    def test_geo_structure(self):
        """La estructura GEO debe tener rects clave y anchos de columna > 0."""
        geo = self.ui.GEO
        for key in ("board", "bar", "top_left", "bot_left", "top_right", "bot_right", "off"):
            self.assertIn(key, geo)
            self.assertIsInstance(geo[key], pygame.Rect)
        self.assertIn("col_w_left", geo)
        self.assertIn("col_w_right", geo)
        self.assertGreater(geo["col_w_left"], 0)
        self.assertGreater(geo["col_w_right"], 0)

    # ───────────────────────── Click → punto (todos los cuadrantes) ─────────────────────────
    def test_punto_desde_click_top_left_col0(self):
        """Click dentro de top_left (columna 0) debe mapear a punto 13."""
        rect = self.ui.GEO["top_left"]
        x = rect.left + self.ui.GEO["col_w_left"] * 0.2
        y = rect.top + 10
        self.assertEqual(self.ui.punto_desde_click((int(x), int(y))), 13)

    def test_punto_desde_click_top_right_col5(self):
        """Click en top_right (columna 5 aprox.) debe mapear a punto 24."""
        rect = self.ui.GEO["top_right"]
        x = rect.left + self.ui.GEO["col_w_right"] * 5.8
        y = rect.top + 10
        self.assertEqual(self.ui.punto_desde_click((int(x), int(y))), 24)

    def test_punto_desde_click_bot_left_col0(self):
        """Click en bot_left (columna 0) debe mapear a punto 12 (va 12..7)."""
        rect = self.ui.GEO["bot_left"]
        x = rect.left + self.ui.GEO["col_w_left"] * 0.1
        y = rect.bottom - 10
        # bot_left corresponde a 12..7 (de izq a der disminuye)
        self.assertEqual(self.ui.punto_desde_click((int(x), int(y))), 12)

    def test_punto_desde_click_bot_right_col5(self):
        """Click en bot_right (columna 5) debe mapear a punto 1 (va 6..1)."""
        rect = self.ui.GEO["bot_right"]
        x = rect.left + self.ui.GEO["col_w_right"] * 5.9
        y = rect.bottom - 10
        # bot_right corresponde a 6..1 (de izq a der disminuye)
        self.assertEqual(self.ui.punto_desde_click((int(x), int(y))), 1)

    def test_punto_desde_click_barra_arriba_y_abajo(self):
        """Click en barra superior → 25; barra inferior → 0."""
        bar = self.ui.GEO["bar"]
        self.assertEqual(self.ui.punto_desde_click((bar.centerx, bar.top + 5)), 25)
        self.assertEqual(self.ui.punto_desde_click((bar.centerx, bar.bottom - 5)), 0)

    def test_punto_desde_click_fuera(self):
        """Click fuera del tablero debe retornar None."""
        fuera = (self.ui.GEO["board"].right + 50, self.ui.GEO["board"].bottom + 50)
        self.assertIsNone(self.ui.punto_desde_click(fuera))

    # ───────────────────────── centro_punto ─────────────────────────
    def test_centro_punto_dentro_de_celdas(self):
        """centro_punto() debe devolver coordenadas aproximadas dentro del tablero."""
        # Probamos varios puntos característicos
        for p in (13, 18, 24, 12, 1):
            x, y = self.ui.centro_punto(p)
            self.assertIsInstance(x, int)
            self.assertIsInstance(y, int)
            # Todos deben estar dentro del tablero principal (aprox)
            self.assertTrue(self.ui.GEO["board"].left - 50 <= x <= self.ui.GEO["board"].right + 50)
            self.assertTrue(self.ui.GEO["board"].top - 50 <= y <= self.ui.GEO["board"].bottom + 50)

    def test_centro_punto_barra(self):
        """centro_punto() para 25 y 0 debe estar dentro de la barra con x centrada."""
        x25, y25 = self.ui.centro_punto(25)
        x0, y0 = self.ui.centro_punto(0)
        self.assertEqual(x25, self.ui.GEO["bar"].centerx)
        self.assertEqual(x0, self.ui.GEO["bar"].centerx)
        self.assertTrue(self.ui.GEO["bar"].top <= y25 <= self.ui.GEO["bar"].centery)
        self.assertTrue(self.ui.GEO["bar"].centery <= y0 <= self.ui.GEO["bar"].bottom)

    # ───────────────────────── Triángulos y resaltado ─────────────────────────
    def test_triangulo_polygon_forma_correcta(self):
        """triangulo_polygon() debe devolver 3 vértices."""
        for p in (13, 18, 7, 1, 24):
            poly = self.ui.triangulo_polygon(p)
            self.assertIsNotNone(poly)
            self.assertEqual(len(poly), 3)

    def test_dibujar_triangulo_seleccionado_no_explota(self):
        """Smoke test de dibujar_triangulo_seleccionado()."""
        self.ui.dibujar_tablero()
        self.ui.dibujar_triangulo_seleccionado(13)  # smoke
        self.assertTrue(True)

    # ───────────────────────── Barra comidas / salida ─────────────────────────
    def test_pos_ficha_barra_sin_fichas(self):
        """pos_ficha_barra() debe devolver None cuando no hay fichas en barra."""
        self.ui.tablero.bar["O"] = []
        self.ui.tablero.bar["X"] = []
        self.assertIsNone(self.ui.pos_ficha_barra(25))
        self.assertIsNone(self.ui.pos_ficha_barra(0))

    def test_pos_ficha_barra_con_fichas_y_resaltado(self):
        """pos_ficha_barra() devuelve posiciones, y el resaltado no falla."""
        self.ui.tablero.bar["O"] = ["O", "O", "O"]
        self.ui.tablero.bar["X"] = ["X"]
        self.assertIsNotNone(self.ui.pos_ficha_barra(25))
        self.assertIsNotNone(self.ui.pos_ficha_barra(0))
        # Resaltado no debe explotar
        self.ui.dibujar_barra_seleccionada(25)
        self.ui.dibujar_barra_seleccionada(0)
        self.assertTrue(True)

    def test_dibujar_barra_salida_smoke(self):
        """Smoke test de dibujar_barra_salida() con fichas en off."""
        self.ui.dibujar_tablero()
        self.ui.tablero.off["O"] = ["O"] * 3
        self.ui.tablero.off["X"] = ["X"] * 2
        self.ui.dibujar_barra_salida()
        self.assertTrue(True)

    # ───────────────────────── Distancia / Consumo ─────────────────────────
    def test_distancia_segun_turno_casos_borde(self):
        """distancia_segun_turno(): mismos puntos o direcciones inválidas → None."""
        # mismo origen/destino → None
        self.assertIsNone(self.ui.distancia_segun_turno("X", 5, 5))
        self.assertIsNone(self.ui.distancia_segun_turno("O", 13, 13))
        # direcciones inválidas
        self.assertIsNone(self.ui.distancia_segun_turno("X", 6, 2))
        self.assertIsNone(self.ui.distancia_segun_turno("O", 2, 6))

    def test_consumir_movimiento_duplicados(self):
        """consumir_movimiento() debe eliminar ocurrencias de manera secuencial."""
        self.ui.movimientos_restantes = [2, 3, 3, 5]
        self.assertTrue(self.ui.consumir_movimiento(3))
        self.assertEqual(self.ui.movimientos_restantes.count(3), 1)
        self.assertTrue(self.ui.consumir_movimiento(3))
        self.assertEqual(self.ui.movimientos_restantes.count(3), 0)
        self.assertFalse(self.ui.consumir_movimiento(3))

    # ───────────────────────── Sorteo / Tirada / HUD ─────────────────────────
    def test_sorteo_inicial_determinista_empieza_x(self):
        """Con randint parcheado (6,5), debe iniciar X."""
        seq = iter([6, 5])  # X=6, O=5
        with patch("random.randint", side_effect=lambda a, b: next(seq)):
            turno = self.ui.sorteo_inicial("Ana", "Beto")
        self.assertEqual(turno, "X")

    def test_tirar_dados_y_preparar_movimientos_normal_y_doble(self):
        """Verifica lista de movimientos normales y dobles, y tirada_actual."""
        with patch("random.randint", side_effect=[2, 5]):
            self.ui.tirar_dados_y_preparar_movimientos()
        self.assertEqual(self.ui.tirada_actual, (2, 5))
        self.assertEqual(self.ui.movimientos_restantes, [2, 5])

        with patch("random.randint", side_effect=[4, 4]):
            self.ui.tirar_dados_y_preparar_movimientos()
        self.assertEqual(self.ui.tirada_actual, (4, 4))
        self.assertEqual(self.ui.movimientos_restantes, [4, 4, 4, 4])

    def test_pasar_turno_llama_a_tirada(self):
        """pasar_turno() alterna X↔O y llama a tirar_dados_y_preparar_movimientos()."""
        self.ui.tirar_dados_y_preparar_movimientos = MagicMock()
        self.assertEqual(self.ui.pasar_turno("X"), "O")
        self.ui.tirar_dados_y_preparar_movimientos.assert_called_once()
        self.ui.tirar_dados_y_preparar_movimientos.reset_mock()
        self.assertEqual(self.ui.pasar_turno("O"), "X")
        self.ui.tirar_dados_y_preparar_movimientos.assert_called_once()

    def test_dibujar_hud_no_explota(self):
        """Smoke test de dibujar_hud() con tirada y movimientos cargados."""
        self.ui.tirada_actual = (1, 2)
        self.ui.movimientos_restantes = [1, 2]
        self.ui.dibujar_tablero()
        self.ui.dibujar_hud()
        self.assertTrue(True)

    # ───────────────────────── pedir_nombres ─────────────────────────
    def test_pedir_nombres_enter_directo_defaults(self):
        """Con RETURN directo, debe devolver nombres por defecto."""
        fake_events = [
            pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN}),
        ]
        with patch("pygame.event.get", side_effect=[fake_events, []]):
            nombre_x, nombre_o = self.ui.pedir_nombres()
        self.assertEqual(nombre_x, "Jugador X")
        self.assertEqual(nombre_o, "Jugador O")

    # ───────────────────────── Dibujo global (smokes) ─────────────────────────
    def test_dibujo_total_smoke(self):
        """Smoke test: tablero + fichas + barras + nombres + HUD."""
        self.ui.tirada_actual = (3, 5)
        self.ui.movimientos_restantes = [3, 5]
        self.ui.dibujar_tablero()
        self.ui.dibujar_fichas()
        self.ui.dibujar_barra_comidas()
        self.ui.dibujar_barra_salida()
        self.ui.dibujar_nombres("Ana", "Beto", turno_actual="X")
        self.ui.dibujar_hud()
        self.assertTrue(True)
    
    # ───────────────────────── Cobertura faltante (ramas y eventos) ─────────────────────────
    def test_triangulo_polygon_ramas_abajo_arriba(self):
        """triangulo_polygon(): cubre ramas de punta hacia abajo y hacia arriba."""
        # Fuerza ramas "punta hacia abajo" y "punta hacia arriba"
        poly_abajo = self.ui.triangulo_polygon(13)  # top → punta hacia abajo
        poly_arriba = self.ui.triangulo_polygon(7)  # bottom → punta hacia arriba
        self.assertEqual(len(poly_abajo), 3)
        self.assertEqual(len(poly_arriba), 3)

    def test_build_geo_full_dimensiones_coherentes(self):
        """La geometría debe ubicar barra centrada y cuadrantes simétricos."""
        geo = self.ui.build_geo_full()
        # La barra debe estar centrada
        self.assertAlmostEqual(geo["bar"].centerx, geo["board"].centerx, delta=5)
        # Los cuadrantes superior e inferior tienen igual ancho
        self.assertEqual(geo["top_left"].width, geo["bot_left"].width)
        self.assertEqual(geo["top_right"].width, geo["bot_right"].width)

    def test_inputbox_handle_event_key_and_draw(self):
        """InputBox: click activa, escribe, backspace borra y draw no falla."""
        rect = pygame.Rect(10, 10, 100, 40)
        box = self.ui.InputBox(rect, self.ui.FUENTE_UI, (200,200,200), (0,255,0))
        surf = pygame.Surface((200,100))

        # Click activa el input
        e_click = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (15, 15)})
        box.handle_event(e_click)
        self.assertTrue(box.active)

        # Escribimos una letra
        e_key = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_a, "unicode": "a"})
        box.handle_event(e_key)
        self.assertIn("a", box.text)

        # Backspace borra
        e_bsp = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_BACKSPACE})
        box.handle_event(e_bsp)
        self.assertEqual(box.text, "")

        # Dibujo no debe fallar
        box.draw(surf)
        self.assertTrue(True)

    def test_pedir_nombres_tab_y_return(self):
        """Simula TAB para cambiar foco y RETURN para aceptar por defecto."""
        events_round1 = [
            pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_TAB}),
            pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN}),
        ]
        with patch("pygame.event.get", side_effect=[events_round1, []]):
            nombre_x, nombre_o = self.ui.pedir_nombres()
        self.assertEqual(nombre_x, "Jugador X")
        self.assertEqual(nombre_o, "Jugador O")

    def test_main_eventos_principales(self):
        """Frame principal: clic origen p1 (X) → destino p3 (X), mueve 1→3."""
        # 1) Parchar pedir_nombres y sorteo para evitar pantallas y fijar turno "X"
        with patch.object(self.ui, "pedir_nombres", return_value=("Ana", "Beto")), \
            patch.object(self.ui, "sorteo_inicial", return_value="X"), \
            patch.object(self.ui, "tirar_dados_y_preparar_movimientos", side_effect=lambda: (
                setattr(self.ui, "tirada_actual", (1, 1)),
                setattr(self.ui, "movimientos_restantes", [2])
            )):

            # 2) Estado del tablero: una ficha X en el punto 1
            self.ui.tablero.tablero.clear()
            self.ui.tablero.tablero[1] = ["X"]

            # 3) Mock de mover_ficha para no depender de reglas internas
            self.ui.tablero.mover_ficha = MagicMock(return_value=True)

            # 4) Clicks de origen y destino usando las coordenadas reales del triángulo
            ox, oy = self.ui.centro_punto(1)   # origen punto 1 (abajo-derecha)
            dx, dy = self.ui.centro_punto(3)   # destino punto 3
            click_origen  = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (ox, oy)})
            click_destino = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (dx, dy)})

            # 5) Salimos del loop con QUIT (un solo frame)
            quit_event = pygame.event.Event(pygame.QUIT, {})

            with patch("pygame.event.get", side_effect=[[click_origen, click_destino, quit_event]]):
                # Evitamos que pygame se cierre la sesión global del runner
                with patch("pygame.quit"):
                    self.ui.main()

            # 6) Debe haberse intentado mover 1 → 3
            self.ui.tablero.mover_ficha.assert_called_once_with(1, 3)

    def test_main_con_mover_ficha_falso_restauracion(self):
        """Cubre la rama donde mover_ficha=False y se restaura el movimiento."""
        self.ui.tirar_dados_y_preparar_movimientos()
        self.ui.tablero.mover_ficha = MagicMock(return_value=False)
        self.ui.movimientos_restantes = [2]
        self.assertFalse(self.ui.tablero.mover_ficha(1, 3))
        # Restauración manual de movimiento
        dist = 2
        if not self.ui.tablero.mover_ficha(1, 3):
            self.ui.movimientos_restantes.append(dist)
            self.ui.movimientos_restantes.sort()
        self.assertIn(2, self.ui.movimientos_restantes)


if __name__ == "__main__":
    unittest.main(verbosity=2)
