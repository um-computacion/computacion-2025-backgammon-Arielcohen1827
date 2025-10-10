import unittest
from core.dice import Dice

class TestDados(unittest.TestCase):
    def setUp(self):
        """Configura un nuevo dado antes de cada prueba."""
        self.dado = Dice()

    def test_tirada_devuelve_valores_validos(self):
        """Verifica que el método roll devuelva números entre 1 y 6."""
        tirada = self.dado.roll()
        self.assertTrue(all(1 <= valor <= 6 for valor in tirada))

    def test_obtener_ultima_tirada(self):
        """Verifica que get_last_rolls devuelva los últimos resultados de ambos dados."""
        self.dado.roll()
        ultima = self.dado.get_last_rolls()
        self.assertEqual(ultima, self.dado.last_rolls)

    def test_es_doble(self):
        """Verifica que is_double funcione correctamente."""
        self.dado.last_rolls = [6, 6]  # Simulamos un doble
        self.assertTrue(self.dado.is_double())
        self.dado.last_rolls = [5, 6]  # Simulamos no un doble
        self.assertFalse(self.dado.is_double())

    def test_inicializacion_valores_none(self):
        """Al inicializar, los valores deben ser [None, None]."""
        self.assertEqual(self.dado.last_rolls, [None, None])

    def test_movimientos_con_doble(self):
        """Si es doble, debe devolver 4 movimientos iguales."""
        self.dado.last_rolls = [4, 4]
        self.assertEqual(self.dado.movimientos(), [4, 4, 4, 4])

    def test_movimientos_sin_doble(self):
        """Si no es doble, debe devolver la misma tirada."""
        self.dado.last_rolls = [3, 5]
        self.assertEqual(self.dado.movimientos(), [3, 5])

    def test_roll_actualiza_last_rolls(self):
        """Cada tirada debe actualizar el valor almacenado en last_rolls."""
        anterior = self.dado.last_rolls[:]
        nueva = self.dado.roll()
        self.assertNotEqual(anterior, nueva)
        self.assertEqual(self.dado.get_last_rolls(), nueva)

    def test_movimientos_despues_de_tirada(self):
        """movimientos() debe reflejar la tirada actual."""
        self.dado.last_rolls = [3, 6]
        self.assertEqual(self.dado.movimientos(), [3, 6])



if __name__ == '__main__':
    unittest.main(verbosity=2)
