# cli.py
from core.board import Tablero
from core.player import Player


class Interfaz:
    def __init__(self):
        self.tablero = None
        self.jugador_x = None
        self.jugador_o = None

    # Paso 1: crear jugadores y tablero
    def pedir_nombres(self):
        nombre_x = input("Nombre del jugador X (fichas negras): ") or "Jugador X"
        nombre_o = input("Nombre del jugador O (fichas blancas): ") or "Jugador O"
        self.jugador_x = Player(nombre_x, "X")
        self.jugador_o = Player(nombre_o, "O")

    def mostrar_jugadores(self):
        print("\nJugadores creados:")
        print(f" - {self.jugador_x.get_name()} juega con fichas '{self.jugador_x.get_ficha()}'")
        print(f" - {self.jugador_o.get_name()} juega con fichas '{self.jugador_o.get_ficha()}'")

    def crear_y_mostrar_tablero(self):
        self.tablero = Tablero()
        print("\nEstado inicial del tablero:")
        print(self.tablero.mostrar())

    # Paso 2: sorteo inicial
    def sorteo_inicial(self, jugador_x: Player, jugador_o: Player) -> Player:
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
                return jugador_x
            elif suma_o > suma_x:
                print(f"\n{jugador_o.get_name()} comienza la partida.")
                return jugador_o
            else:
                print("Empate, se repite la tirada...")

    # Paso 3: tirar dados y mostrar movimientos (usa Player.movimientos -> Dice.movimientos)
    def tirar_dados_y_mostrar(self, jugador: Player):
        tirada = jugador.roll_dice()
        movimientos = jugador.movimientos()
        print(f"\n{jugador.get_name()} tiró los dados: {tirada} -> movimientos: {movimientos}")
        return movimientos

    # Paso 4: pedir y ejecutar un movimiento
    def pedir_movimiento(self):
        mov = input("Movimiento (formato origen-destino, ej. 13-11): ").strip()
        try:
            origen, destino = map(int, mov.split("-"))
            return origen, destino
        except Exception:
            print("❌ Formato incorrecto.")
            return None

    def ejecutar_movimiento(self, jugador: Player, origen: int, destino: int) -> bool:
        ok = self.tablero.mover_ficha(origen, destino)
        if ok:
            print(f"✅ Movimiento realizado por {jugador.get_name()}: {origen} → {destino}")
            return True
        else:
            print("❌ Movimiento inválido.")
            return False
    # Paso 5 

    def _consumir_movimiento(self, movimientos: list[int], distancia: int) -> bool:
        """Quita una única ocurrencia de 'distancia' de la lista de movimientos."""
        if distancia in movimientos:
            movimientos.remove(distancia)
            return True
        return False

    # Demo principal (pasos 1 a 4)
    def main(self):
        print("=== Backgammon ===")
        self.pedir_nombres()
        self.mostrar_jugadores()
        self.crear_y_mostrar_tablero()

        # Sorteo: quién empieza
        primero = self.sorteo_inicial(self.jugador_x, self.jugador_o)

        # Ese jugador tira y se muestran sus movimientos posibles
        self.tirar_dados_y_mostrar(primero)

        # Un solo movimiento de demostración
        print("\nTablero actual:")
        print(self.tablero.mostrar())
        entrada = self.pedir_movimiento()
        if entrada:
            origen, destino = entrada
            self.ejecutar_movimiento(primero, origen, destino)

        print("\nTablero tras el movimiento:")
        print(self.tablero.mostrar())



if __name__ == "__main__":
    Interfaz().main()
