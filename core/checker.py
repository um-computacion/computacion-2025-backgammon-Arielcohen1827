class Checker:
    """Clase que valida las condiciones de movimiento en el tablero de backgammon."""

    @staticmethod
    def movimiento_valido(ficha, fichas_destino):
        """
        Retorna True si el movimiento es válido según las reglas básicas:
        - Si el destino tiene 2 o más fichas rivales → movimiento inválido.
        - En otro caso → válido (vacío, fichas propias, o 1 ficha rival).
        """
        if len(fichas_destino) >= 2 and all(f != ficha for f in fichas_destino):
            return False
        return True