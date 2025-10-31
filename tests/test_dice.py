# tests/test_dice.py
"""Tests unitarios para el módulo core.dice.

Este archivo valida el comportamiento de la clase Dice:
- Generación de tiradas válidas entre 1 y 6.
- Detección correcta de tiradas dobles.
- Persistencia de la última tirada.
- Generación de movimientos según las reglas del Backgammon.
"""

import unittest
from core.dice import Dice


class TestDados(unittest.TestCase):
    """Pruebas unitarias para la clase Dice."""

    def setUp(self):
        """Crea una nueva instancia de Dice antes de cada prueba."""
        self.dado = Dice()

    def test_tirada_devuelve_valores_validos(self):
        """Verifica que cada tirada contenga valores entre 1 y 6."""
        tirada = self.dado.roll()
        self.assertTrue(all(1 <= valor <= 6 for valor in tirada))

    def test_obtener_ultima_tirada(self):
        """Comprueba que get_last_rolls() refleje la última tirada realizada."""
        self.dado.roll()
        ultima = self.dado.get_last_rolls()
        self.assertEqual(ultima, self.dado.last_rolls)

    def test_es_doble(self):
        """Confirma que is_double() detecta correctamente una tirada doble."""
        self.dado.last_rolls = [6, 6]
        self.assertTrue(self.dado.is_double())
        self.dado.last_rolls = [5, 6]
        self.assertFalse(self.dado.is_double())

    def test_inicializacion_valores_none(self):
        """Verifica que los valores iniciales sean [None, None]."""
        self.assertEqual(self.dado.last_rolls, [None, None])

    def test_movimientos_con_doble(self):
        """Si es doble, movimientos() debe devolver 4 valores iguales."""
        self.dado.last_rolls = [4, 4]
        self.assertEqual(self.dado.movimientos(), [4, 4, 4, 4])

    def test_movimientos_sin_doble(self):
        """Si no es doble, movimientos() debe devolver los dos valores originales."""
        self.dado.last_rolls = [3, 5]
        self.assertEqual(self.dado.movimientos(), [3, 5])

    def test_roll_actualiza_last_rolls(self):
        """Cada tirada debe actualizar el atributo last_rolls."""
        anterior = self.dado.last_rolls[:]
        nueva = self.dado.roll()
        self.assertNotEqual(anterior, nueva)
        self.assertEqual(self.dado.get_last_rolls(), nueva)

    def test_movimientos_despues_de_tirada(self):
        """Verifica que movimientos() devuelva los valores de la última tirada."""
        self.dado.last_rolls = [3, 6]
        self.assertEqual(self.dado.movimientos(), [3, 6])


if __name__ == '__main__':
    unittest.main(verbosity=2)
