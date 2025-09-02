import random

class Dice:
    def __init__(self):
        """Inicializa el dado."""
        self.last_roll = None

    def roll(self):
        """Lanza el dado y devuelve el resultado."""
        self.last_roll = random.randint(1, 6)
        return self.last_roll
