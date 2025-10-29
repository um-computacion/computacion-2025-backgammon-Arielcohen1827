from core.dice import Dice

class Player:
    """
    Representa a un jugador de Backgammon.
    """

    def __init__(self, name: str, ficha: str):
        self.__name__ = name
        self.__ficha__ = ficha
        self.__dice__ = Dice()

    def get_name(self) -> str:
        return self.__name__

    def get_ficha(self) -> str:
        return self.__ficha__

    def roll_dice(self) -> list[int]:
        return self.__dice__.roll()

    def get_last_roll(self) -> list[int]:
        return self.__dice__.get_last_rolls()

    def has_double(self) -> bool:
        return self.__dice__.is_double()

    def movimientos(self) -> list[int]:

        return self.__dice__.movimientos()

    def __str__(self):
        return f"Jugador {self.__name__} ({self.__ficha__})"
