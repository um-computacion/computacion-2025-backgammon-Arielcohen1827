# dice.py
import random
from typing import List, Optional


class Dice:
    """Manejo de tiradas de dados para Backgammon.

    Esta clase modela dos dados de seis caras. Conserva la última tirada y
    ofrece utilidades para saber si fue doble y para derivar los movimientos
    disponibles de acuerdo a las reglas del juego (doble => 4 movimientos).
    """

    def __init__(self) -> None:
        """Inicializa el estado de los dados.

        Atributos:
            last_rolls (List[Optional[int]]): Última tirada (dos valores).
                Inicia como [None, None] hasta que se llame a `roll()`.
        """
        self.last_rolls: List[Optional[int]] = [None, None]

    def roll(self) -> List[int]:
        """Realiza una tirada de dos dados.

        Returns:
            List[int]: Lista de dos enteros entre 1 y 6 (inclusive) que
            representan la tirada actual en orden.
        """
        self.last_rolls = [random.randint(1, 6), random.randint(1, 6)]
        return self.last_rolls  # type: ignore[return-value]

    def get_last_rolls(self) -> List[Optional[int]]:
        """Devuelve la última tirada registrada.

        Returns:
            List[Optional[int]]: Dos valores con la última tirada. Pueden ser
            `None` si aún no se llamó a `roll()`.
        """
        return self.last_rolls

    def is_double(self) -> bool:
        """Indica si la última tirada fue doble.

        Returns:
            bool: `True` si ambos dados muestran el mismo valor y no son `None`,
            `False` en caso contrario.
        """
        return self.last_rolls[0] == self.last_rolls[1]

    def movimientos(self) -> List[int]:
        """Devuelve los movimientos disponibles derivados de la tirada.

        Reglas:
            - Si la tirada es doble → 4 movimientos con ese mismo valor.
            - Si no es doble → 2 movimientos con los valores de cada dado.

        Returns:
            List[int]: Lista de longitudes de movimiento a consumir.
        """
        # Nota: `is_double()` es seguro aquí porque compara posiciones 0 y 1.
        if self.is_double():
            return [self.last_rolls[0]] * 4  # type: ignore[list-item]
        return self.last_rolls[:]  # type: ignore[return-value]
