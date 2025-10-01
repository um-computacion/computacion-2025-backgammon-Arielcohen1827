# cli.py
from core.board import Tablero
from core.player import Player


class Interfaz:
    def __init__(self):
        self.tablero = None
        self.jugador_x = None
        self.jugador_o = None

    def pedir_nombres(self):
        nombre_x = input("Nombre del jugador X (fichas negras): ") or "Jugador X"
        nombre_o = input("Nombre del jugador O (fichas blancas): ") or "Jugador O"
        self.jugador_x = Player(nombre_x, "X")
        self.jugador_o = Player(nombre_o, "O")

    def mostrar_jugadores(self):
        print(f"\nJugadores creados:")
        print(f" - {self.jugador_x.get_name()} juega con fichas '{self.jugador_x.get_ficha()}'")
        print(f" - {self.jugador_o.get_name()} juega con fichas '{self.jugador_o.get_ficha()}'")

    def crear_y_mostrar_tablero(self):
        self.tablero = Tablero()
        print("\nEstado inicial del tablero:")
        print(self.tablero.mostrar())

    def sorteo_inicial(self, jugador_x: Player, jugador_o: Player) -> str:
        """Decide quién comienza; devuelve el nombre del ganador del sorteo."""
        
        while True:
            tirada_x = jugador_x.roll_dice()
            tirada_o = jugador_o.roll_dice()
            suma_x = sum(tirada_x)
            suma_o = sum(tirada_o)

            print("\nTirada inicial:")
            print(f" - {jugador_x.get_name()} ({jugador_x.get_ficha()}): {tirada_x} -> suma {suma_x}")
            print(f" - {jugador_o.get_name()} ({jugador_o.get_ficha()}): {tirada_o} -> suma {suma_o}")

            if suma_x > suma_o:
                print(f"\n{jugador_x.get_name()} comienza la partida.")
                return jugador_x.get_name()
            elif suma_o > suma_x:
                print(f"\n{jugador_o.get_name()} comienza la partida.")
                return jugador_o.get_name()
            else:
                print("Empate, se repite la tirada...")

    def main(self):
        print("=== Backgammon ===")
        self.pedir_nombres()
        self.mostrar_jugadores()
        self.crear_y_mostrar_tablero()
        self.sorteo_inicial(self.jugador_x, self.jugador_o)





if __name__ == "__main__":
    Interfaz().main()
