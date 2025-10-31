# cli.py
from typing import List, Optional, Tuple
from core.board import Tablero
from core.player import Player


class Interfaz:
    """Interfaz de consola (CLI) para jugar Backgammon.

    Coordina la interacción por terminal:
      - carga de nombres,
      - sorteo inicial,
      - tiradas y consumo de movimientos,
      - entrada 'origen-destino',
      - consulta al `Tablero` para validar y efectuar jugadas.

    La lógica de reglas permanece encapsulada en `Tablero`.
    """

    def __init__(self) -> None:
        """Crea una interfaz sin estado de juego aún inicializado."""
        self.tablero: Optional[Tablero] = None
        self.jugador_x: Optional[Player] = None
        self.jugador_o: Optional[Player] = None

    # Paso 1: crear jugadores y tablero
    def pedir_nombres(self) -> None:
        """Solicita y registra los nombres de los jugadores."""
        nombre_x = input("Nombre del jugador X (fichas negras): ") or "Jugador X"
        nombre_o = input("Nombre del jugador O (fichas blancas): ") or "Jugador O"
        self.jugador_x = Player(nombre_x, "X")
        self.jugador_o = Player(nombre_o, "O")

    def mostrar_jugadores(self) -> None:
        """Imprime la información de los jugadores actuales en pantalla."""
        print("\nJugadores creados:")
        print(f" - {self.jugador_x.get_name()} juega con fichas '{self.jugador_x.get_ficha()}'")
        print(f" - {self.jugador_o.get_name()} juega con fichas '{self.jugador_o.get_ficha()}'")

    def crear_y_mostrar_tablero(self) -> None:
        """Crea el tablero inicial y lo muestra por pantalla."""
        self.tablero = Tablero()
        print("\nEstado inicial del tablero:")
        print(self.tablero.mostrar())

    # Paso 2: sorteo inicial
    def sorteo_inicial(self, jugador_x: Player, jugador_o: Player) -> Player:
        """Realiza el sorteo inicial para decidir quién comienza.

        Cada jugador tira dos dados; comienza quien obtenga mayor suma.
        En caso de empate, se repite la tirada hasta desempatar.

        Args:
            jugador_x (Player): Jugador con ficha 'X'.
            jugador_o (Player): Jugador con ficha 'O'.

        Returns:
            Player: Jugador que comenzará la partida.
        """
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
            if suma_o > suma_x:
                print(f"\n{jugador_o.get_name()} comienza la partida.")
                return jugador_o
            print("Empate, se repite la tirada...")

    # Paso 3: tirar dados y mostrar movimientos
    def tirar_dados_y_mostrar(self, jugador: Player) -> List[int]:
        """Tira los dados para un jugador y muestra sus movimientos derivados.

        Args:
            jugador (Player): Jugador activo.

        Returns:
            List[int]: Lista de movimientos disponibles (2 valores o 4 si doble).
        """
        tirada = jugador.roll_dice()
        movimientos = jugador.movimientos()
        print(f"\n{jugador.get_name()} tiró los dados: {tirada} -> movimientos: {movimientos}")
        return movimientos

    # Paso 4: pedir y ejecutar un movimiento
    def pedir_movimiento(self) -> Optional[Tuple[int, int]]:
        """Pide una jugada en formato 'origen-destino'.

        Returns:
            Optional[Tuple[int, int]]: Par (origen, destino) si el formato es válido,
            `None` si la entrada es incorrecta.
        """
        mov = input("Movimiento (formato origen-destino, ej. 13-11): ").strip()
        try:
            origen, destino = map(int, mov.split("-"))
            return origen, destino
        except Exception:
            print("❌ Formato incorrecto.")
            return None

    def ejecutar_movimiento(self, jugador: Player, origen: int, destino: int) -> bool:
        """Solicita al tablero ejecutar un movimiento y reporta el resultado.

        Args:
            jugador (Player): Jugador que intenta mover.
            origen (int): Punto de origen.
            destino (int): Punto de destino.

        Returns:
            bool: `True` si el movimiento fue realizado; `False` si fue inválido.
        """
        ok = self.tablero.mover_ficha(origen, destino)  # type: ignore[union-attr]
        if ok:
            print(f"✅ Movimiento realizado por {jugador.get_name()}: {origen} → {destino}")
            return True
        print("❌ Movimiento inválido.")
        return False

    def _consumir_movimiento(self, movimientos: List[int], distancia: int) -> bool:
        """Consume una única ocurrencia de `distancia` de la lista de movimientos.

        Args:
            movimientos (List[int]): Movimientos disponibles (se muta si consume).
            distancia (int): Distancia legal a consumir (coincidente con dados).

        Returns:
            bool: `True` si se quitó una ocurrencia, `False` si no existía.
        """
        if distancia in movimientos:
            movimientos.remove(distancia)
            return True
        return False

    def jugar_turno(self, jugador: Player) -> None:
        """Ejecuta un turno completo de un jugador en la CLI.

        Secuencia:
            - Tira dados y obtiene movimientos.
            - Muestra tablero y pide 'origen-destino' para cada movimiento.
            - Valida dirección con `Tablero.distancia_legal`.
            - Ejecuta movimiento; si falla, devuelve el valor a la lista.
            - El usuario puede presionar ENTER para saltar el resto del turno.

        Args:
            jugador (Player): Jugador que realiza el turno.
        """
        print("\n" + "=" * 40)
        print(f"👉 Turno de {jugador.get_name()} ({jugador.get_ficha()})")
        movimientos = self.tirar_dados_y_mostrar(jugador)[:]  # copia para consumir

        while movimientos:
            print("\nTablero actual:")
            print(self.tablero.mostrar())  # type: ignore[union-attr]
            print(f"Movimientos disponibles: {movimientos}")
            entrada = input("Origen-Destino (ENTER para pasar el resto del turno): ").strip()
            if not entrada:
                print("⏭️  El jugador decide no usar los movimientos restantes.")
                break

            try:
                origen, destino = map(int, entrada.split("-"))
            except Exception:
                print("❌ Formato incorrecto. Usa 'origen-destino', ej. 13-11.")
                continue

            # 1) Validar dirección/distancia con las reglas del tablero
            distancia = self.tablero.distancia_legal(jugador.get_ficha(), origen, destino)  # type: ignore[union-attr]
            if distancia is None:
                print("❌ Dirección inválida para tus fichas.")
                continue

            # 2) Verificar que exista ese valor en los movimientos disponibles (NO consumir todavía)
            if distancia not in movimientos:
                print(f"❌ No tienes un movimiento de {distancia} disponible.")
                continue

            # 3) Vista previa + confirmación
            print(f"👀 Vista previa: mover {jugador.get_ficha()} de {origen} a {destino} (usa {distancia}).")
            confirmar = input("¿Confirmar? (s/N): ").strip().lower()
            if confirmar != "s":
                print("↩️  Movimiento cancelado por el jugador. No se consume el dado.")
                continue

            # 4) Ejecutar en el tablero; si funciona recién ahí CONSUMIR el movimiento
            if self.ejecutar_movimiento(jugador, origen, destino):
                # éxito → consumir ese valor exacto
                self._consumir_movimiento(movimientos, distancia)
            else:
                # fallo → no consumir (lista queda igual)
                print("🔁 No se consumió el dado porque el movimiento fue inválido.")
                continue


        print("\nFin del turno.")
        print(self.tablero.mostrar())  # type: ignore[union-attr]

    # Demo principal (pasos 1 a 4) + turnos
    def main(self) -> None:
        """Ejecuta el flujo de juego por consola (demo/partida manual)."""
        print("=== Backgammon ===")
        self.pedir_nombres()
        self.mostrar_jugadores()
        self.crear_y_mostrar_tablero()

        # Sorteo: quién empieza
        actual = self.sorteo_inicial(self.jugador_x, self.jugador_o)  # type: ignore[arg-type]
        rival = self.jugador_o if actual is self.jugador_x else self.jugador_x  # type: ignore[assignment]

        # Bucle de turnos
        while True:
            self.jugar_turno(actual)  # type: ignore[arg-type]

            # ¿Hay ganador?
            ganador = self.tablero.ganador()  # type: ignore[union-attr]
            if ganador:
                nombre = self.jugador_x.get_name() if ganador == "X" else self.jugador_o.get_name()  # type: ignore[union-attr]
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
