# dice.py

import random

class Dice:
    def __init__(self):
        """Inicializa los dados."""
        self.last_rolls = [None, None]  # Almacena los resultados de los dos dados

    def roll(self):
        """Lanza dos dados y devuelve los resultados."""
        self.last_rolls[0] = random.randint(1, 6)
        self.last_rolls[1] = random.randint(1, 6)
        return self.last_rolls

    def is_double(self):
        """Verifica si ambos dados son dobles (iguales)."""
        return self.last_rolls[0] == self.last_rolls[1]

    def get_last_rolls(self):
        """Devuelve los últimos resultados de los dos dados."""
        return self.last_rolls
    

if __name__ == '__main__':
    dice = Dice()
    rolls = dice.roll()
    print(f"Tiradas: {rolls[0]} y {rolls[1]}")
    
    if dice.is_double():
        print("¡Es un doble!")
    else:
        print("No es un doble.")