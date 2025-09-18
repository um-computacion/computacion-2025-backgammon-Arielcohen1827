# tests/test_player.py

import unittest
from core.player import Player

class TestPlayer(unittest.TestCase):

    def setUp(self):
        """Se ejecuta antes de cada test."""
        self.player_x = Player("Ariel", "X")
        self.player_o = Player("CPU", "O")

    def test_get_name(self):
        self.assertEqual(self.player_x.get_name(), "Ariel")
        self.assertEqual(self.player_o.get_name(), "CPU")

    def test_get_ficha(self):
        self.assertEqual(self.player_x.get_ficha(), "X")
        self.assertEqual(self.player_o.get_ficha(), "O")

    def test_roll_dice_returns_two_values(self):
        rolls = self.player_x.roll_dice()
        self.assertEqual(len(rolls), 2)
        self.assertTrue(1 <= rolls[0] <= 6)
        self.assertTrue(1 <= rolls[1] <= 6)

    def test_get_last_roll_matches_roll_dice(self):
        rolls = self.player_x.roll_dice()
        last_rolls = self.player_x.get_last_roll()
        self.assertEqual(rolls, last_rolls)

    def test_has_double_true_when_both_dice_same(self):
        # Forzamos los valores manualmente para simular un doble
        self.player_x._Player__dice__.last_rolls = [3, 3]
        self.assertTrue(self.player_x.has_double())

    def test_has_double_false_when_dice_different(self):
        self.player_x._Player__dice__.last_rolls = [2, 5]
        self.assertFalse(self.player_x.has_double())

    def test_str_representation(self):
        self.assertEqual(str(self.player_x), "Jugador Ariel (X)")
        self.assertEqual(str(self.player_o), "Jugador CPU (O)")


if __name__ == "__main__":
    unittest.main()
