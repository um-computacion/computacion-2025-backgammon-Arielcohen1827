# tests/test_player.py
"""Tests unitarios para el módulo core.player.

Evalúa la clase Player:
- Accesores de nombre y ficha.
- Integración con la clase Dice.
- Detección de tiradas dobles.
- Representación de texto legible.
"""

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
