# dice.py
import random

class Dice:
    def __init__(self):
        self.last_rolls = [None, None]

    def roll(self):
        self.last_rolls = [random.randint(1, 6), random.randint(1, 6)]
        return self.last_rolls

    def get_last_rolls(self):
        return self.last_rolls

    def is_double(self):
        return self.last_rolls[0] == self.last_rolls[1]

    def movimientos(self):
        """
        Devuelve la lista de movimientos según la última tirada.
        - Si es doble → 4 movimientos iguales.
        - Si no → dos movimientos distintos.
        """
        if self.is_double():
            return [self.last_rolls[0]] * 4
        return self.last_rolls[:]
