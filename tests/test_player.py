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


if __name__ == "__main__":
    unittest.main()
