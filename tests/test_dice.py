import unittest
from core.dice import Dice

class TestDice(unittest.TestCase):
    def setUp(self):
        """Configura un nuevo dado antes de cada prueba."""
        self.dice = Dice()

    def test_roll_returns_valid_numbers(self):
        """Verifica que el método roll devuelva números entre 1 y 6."""
        rolls = self.dice.roll()
        self.assertTrue(all(1 <= roll <= 6 for roll in rolls))

    def test_get_last_rolls(self):
        """Verifica que get_last_rolls devuelva los últimos resultados de ambos dados."""
        self.dice.roll()
        last_rolls = self.dice.get_last_rolls()
        self.assertEqual(last_rolls, self.dice.last_rolls)

    def test_is_double(self):
        """Verifica que is_double funcione correctamente."""
        self.dice.last_rolls = [6, 6]  # Simulamos un doble
        self.assertTrue(self.dice.is_double())
        self.dice.last_rolls = [5, 6]  # Simulamos no un doble
        self.assertFalse(self.dice.is_double())

if __name__ == '__main__':
    unittest.main()
