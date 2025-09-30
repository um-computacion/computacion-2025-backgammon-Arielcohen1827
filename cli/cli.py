from core.board import Tablero
from core.player import Player

def main():
    print("=== Backgammon ===")

    # Pedir nombres de los jugadores
    nombre_x = input("Nombre del jugador X (fichas negras): ") or "Jugador X"
    nombre_o = input("Nombre del jugador O (fichas blancas): ") or "Jugador O"

    # Crear instancias de Player
    jugador_x = Player(nombre_x, "X")
    jugador_o = Player(nombre_o, "O")

    # Mostrar confirmación
    print(f"\nJugadores creados:")
    print(f" - {jugador_x.get_name()} juega con fichas '{jugador_x.get_ficha()}'")
    print(f" - {jugador_o.get_name()} juega con fichas '{jugador_o.get_ficha()}'")

    # Crear tablero
    tablero = Tablero()
    print("\nEstado inicial del tablero:")
    print(tablero.mostrar())

    # Ejemplo de tirada
    tirada = jugador_x.roll_dice()
    print(f"\n{jugador_x.get_name()} tira los dados: {tirada}")
    if jugador_x.has_double():
        print("¡Sacó dobles!")

if __name__ == "__main__":
    main()
