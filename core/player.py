# player.py
from typing import List
from core.dice import Dice


class Player:
    """Representa a un jugador de Backgammon.

    Cada jugador tiene:
      - un nombre,
      - un identificador de ficha: 'X' o 'O',
      - un par de dados para sus tiradas.

    La clase expone métodos de conveniencia para acceder a la tirada
    actual y para traducirla a movimientos válidos según las reglas.
    """

    def __init__(self, name: str, ficha: str) -> None:
        """Crea un nuevo jugador.

        Args:
            name (str): Nombre a mostrar durante la partida.
            ficha (str): Identificador de ficha ('X' o 'O').
        """
        self.__name__ = name
        self.__ficha__ = ficha
        self.__dice__ = Dice()

    def get_name(self) -> str:
        """Devuelve el nombre del jugador.

        Returns:
            str: Nombre del jugador.
        """
        return self.__name__

    def get_ficha(self) -> str:
        """Devuelve el identificador de ficha del jugador.

        Returns:
            str: 'X' o 'O' según corresponda.
        """
        return self.__ficha__

    def roll_dice(self) -> List[int]:
        """Realiza una tirada de dados para el jugador.

        Returns:
            List[int]: Dos enteros entre 1 y 6 (inclusive).
        """
        return self.__dice__.roll()

    def get_last_roll(self) -> List[int]:
        """Devuelve la última tirada del jugador.

        Returns:
            List[int]: Última tirada de dos valores.
        """
        # `Dice.get_last_rolls` tipa Optional, pero en práctica se usa tras tirar.
        return self.__dice__.get_last_rolls()  # type: ignore[return-value]

    def has_double(self) -> bool:
        """Indica si la última tirada fue doble.

        Returns:
            bool: `True` si ambos dados muestran el mismo valor.
        """
        return self.__dice__.is_double()

    def movimientos(self) -> List[int]:
        """Devuelve la lista de movimientos disponibles para consumir.

        Returns:
            List[int]: Movimientos (dos valores o cuatro si fue doble).
        """
        return self.__dice__.movimientos()

    def __str__(self) -> str:
        """Representación legible del jugador.

        Returns:
            str: Cadena con el nombre y la ficha, por ejemplo 'Jugador Ana (X)'.
        """
        return f"Jugador {self.__name__} ({self.__ficha__})"
