from core.dice import Dice

class Player:
    """
    Representa a un jugador de Backgammon.
    
    """

    def __init__(self, name: str, ficha: str):
        """
        Inicializa un jugador.

        """
        self.__name__ = name
        self.__ficha__ = ficha
        self.__dice__ = Dice()

    def get_name(self) -> str:
        """Devuelve el nombre del jugador."""
        return self.__name__

    def get_ficha(self) -> str:
        """Devuelve la ficha asociada al jugador ("X" o "O")."""
        return self.__ficha__

    def roll_dice(self) -> list[int]:
        """Tira los dados y devuelve los valores obtenidos."""
        return self.__dice__.roll()

    def get_last_roll(self) -> list[int]:
        """Devuelve la última tirada de dados."""
        return self.__dice__.get_last_rolls()

    def has_double(self) -> bool:
        """Indica si la última tirada fue un doble."""
        return self.__dice__.is_double()

    def __str__(self):
        return f"Jugador {self.__name__} ({self.__ficha__})"
