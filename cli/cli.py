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

    # Sorteo inicial: ambos tiran dados hasta que uno saque mayor suma
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
            break
        elif suma_o > suma_x:
            print(f"\n{jugador_o.get_name()} comienza la partida.")
            break
        else:
            print("Empate, se repite la tirada...")

if __name__ == "__main__":
    main()
