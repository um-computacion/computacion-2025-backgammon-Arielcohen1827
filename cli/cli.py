# cli.py
from core.board import Tablero
from core.player import Player
import copy
import io
import contextlib


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
    def jugar_turno(self, jugador: Player):
        """
        Turno con PREVIEW + confirmación:
        - Calcula distancia legal.
        - Muestra una vista previa del tablero si el movimiento es posible.
        - Pide confirmación; solo entonces consume el dado y mueve.
        - ENTER pasa el resto del turno.
        """
        print("\n" + "=" * 40)
        print(f"👉 Turno de {jugador.get_name()} ({jugador.get_ficha()})")
        movimientos = self.tirar_dados_y_mostrar(jugador)[:]  # copia para consumir

        while movimientos:
            print("\nTablero actual:")
            print(self.tablero.mostrar())
            print(f"Movimientos disponibles: {movimientos}")
            entrada = input("Origen-Destino (ENTER para pasar el resto del turno): ").strip()
            if not entrada:
                print("⏭️  El jugador decide no usar los movimientos restantes.")
                break

            # Parseo
            try:
                origen, destino = map(int, entrada.split("-"))
            except Exception:
                print("❌ Formato incorrecto. Usa 'origen-destino', ej. 13-11.")
                continue

            # Distancia según reglas del tablero (no consumimos aún)
            distancia = self.tablero.distancia_legal(jugador.get_ficha(), origen, destino)
            if distancia is None:
                print("❌ Dirección inválida para tus fichas.")
                continue

            # Simular en una COPIA del tablero, silenciando prints internos
            tablero_preview = copy.deepcopy(self.tablero)
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                ok_preview = tablero_preview.mover_ficha(origen, destino)

            if not ok_preview:
                # Movimiento no es posible (bloqueos, barra, bearing off inválido, etc.)
                print("❌ Movimiento inválido (según reglas).")
                continue

            # Mostrar cómo quedaría
            print("\n🧪 Vista previa del tablero si confirmás este movimiento:")
            print(tablero_preview.mostrar())

            # Confirmación
            confirmar = input(f"¿Confirmás mover de {origen} a {destino}? (s/n): ").strip().lower()
            if confirmar not in ("s", "si", "y", "yes"):
                print("⏪ Movimiento cancelado por el jugador.")
                continue

            # Consumir la distancia ahora que confirmaste
            if not self._consumir_movimiento(movimientos, distancia):
                print(f"⚠️ Ya no tenés un movimiento de {distancia} disponible.")
                continue

            # Ejecutar de verdad en el tablero real
            if not self.ejecutar_movimiento(jugador, origen, destino):
                movimientos.append(distancia)
                movimientos.sort()
                continue

        print("\nFin del turno.")
        print(self.tablero.mostrar())


    

    # Demo principal (pasos 1 a 4) + turnos
    def main(self):
        print("=== Backgammon ===")
        self.pedir_nombres()
        self.mostrar_jugadores()
        self.crear_y_mostrar_tablero()

        # Sorteo: quién empieza
        actual = self.sorteo_inicial(self.jugador_x, self.jugador_o)
        rival = self.jugador_o if actual is self.jugador_x else self.jugador_x

        # Bucle de turnos
        while True:
            self.jugar_turno(actual)
            
            # ¿Hay ganador?
            ganador = self.tablero.ganador()
            if ganador:
                nombre = self.jugador_x.get_name() if ganador == "X" else self.jugador_o.get_name()
                print(f"\n🏆 ¡{nombre} ha ganado la partida!")
                break
            
            # Alternar
            actual, rival = rival, actual

            # Opción simple para salir
            seguir = input("\n¿Continuar? (ENTER sí / 'q' para salir): ").strip().lower()
            if seguir == "q":
                print("👋 Fin de la partida (salida manual).")
                break



if __name__ == "__main__":
    Interfaz().main()
