# board.py
from typing import Dict, List, Optional


class Tablero:
    """Representa el tablero y toda la lógica de estado de Backgammon.

    Esta clase mantiene:
      - la distribución de fichas por punto (1–24),
      - las barras de fichas comidas,
      - las pilas de fichas retiradas (bearing off),
      - validaciones básicas de dirección, bloqueo y captura.

    Notas de diseño:
      * La clase NO conoce de turnos, entradas de usuario ni de CLI/GUI.
        Solo aplica reglas sobre el estado del tablero.
      * La validación de distancias legales (`distancia_legal`) se expone
        para que la capa de interfaz pueda cotejar movimientos con dados.
    """

    def __init__(self) -> None:
        """Inicializa el estado con la disposición clásica de Backgammon."""
        self.tablero: Dict[int, List[str]] = {
            24: ["O"] * 2,
            13: ["O"] * 5,
            8:  ["O"] * 3,
            6:  ["O"] * 5,
            1:  ["X"] * 2,
            12: ["X"] * 5,
            17: ["X"] * 3,
            19: ["X"] * 5,
            0:  [],   # barra de X (para compatibilidad con algún flujo)
            25: [],   # barra de O (para compatibilidad con algún flujo)
        }
        self.max_altura = 8  # Alto máximo para renderizar columnas
        # Barras de fichas comidas (fuente de verdad para reingresos)
        self.bar: Dict[str, List[str]] = {"O": [], "X": []}
        # Fichas retiradas (bearing off)
        self.off: Dict[str, List[str]] = {"O": [], "X": []}

    def celda(self, contenido: object) -> str:
        """Formatea una celda de ancho fijo para el render del tablero.

        Args:
            contenido (object): Contenido a centrar en 3 caracteres.

        Returns:
            str: Cadena con el contenido centrado.
        """
        return f"{contenido:^3}"

    def mostrar(self) -> str:
        """Devuelve una representación en texto del estado actual del tablero.

        Returns:
            str: Multilínea con la cuadrícula superior e inferior, numeraciones,
            y la información de barras al final.
        """
        output: List[str] = []

        # Parte superior (13–24)
        for fila in range(self.max_altura, 0, -1):
            linea = " "
            for punto in range(13, 19):
                fichas = self.tablero.get(punto, [])
                linea += self.celda(fichas[fila - 1] if len(fichas) >= fila else " ")
            linea += "|"
            for punto in range(19, 25):
                fichas = self.tablero.get(punto, [])
                linea += self.celda(fichas[fila - 1] if len(fichas) >= fila else " ")
            output.append(linea)

        # Numeración superior
        linea = " "
        for punto in range(13, 19):
            linea += self.celda(punto)
        linea += "|"
        for punto in range(19, 25):
            linea += self.celda(punto)
        output.append(linea)

        output.append(" " + "-" * (3 * 12 + 1))

        # Numeración inferior
        linea = " "
        for punto in range(12, 6, -1):
            linea += self.celda(punto)
        linea += "|"
        for punto in range(6, 0, -1):
            linea += self.celda(punto)
        output.append(linea)

        # Parte inferior (12–1)
        for fila in range(1, self.max_altura + 1):
            linea = " "
            for punto in range(12, 6, -1):
                fichas = self.tablero.get(punto, [])
                linea += self.celda(fichas[fila - 1] if len(fichas) >= fila else " ")
            linea += "|"
            for punto in range(6, 0, -1):
                fichas = self.tablero.get(punto, [])
                linea += self.celda(fichas[fila - 1] if len(fichas) >= fila else " ")
            output.append(linea)

        # Mostrar barras (se concatena con posibles estructuras 0/25 por compatibilidad)
        barra_o = self.tablero.get(25, []) + self.bar["O"]
        barra_x = self.tablero.get(0, []) + self.bar["X"]
        output.append("\nBarra O (0): " + str(barra_o))
        output.append("Barra X (25): " + str(barra_x))

        return "\n".join(output)

    def todas_en_cuadrante_final(self, ficha: str) -> bool:
        """Indica si todas las fichas de un jugador están en su cuadrante final.

        Args:
            ficha (str): 'X' o 'O'.

        Returns:
            bool: `True` si todas están en el cuadrante final, `False` de lo contrario.
        """
        if ficha == "O":
            # Para O, todas entre 1–6
            for punto, fichas in self.tablero.items():
                if "O" in fichas and punto > 6:
                    return False
        else:  # ficha == "X"
            # Para X, todas entre 19–24
            for punto, fichas in self.tablero.items():
                if "X" in fichas and punto < 19:
                    return False
        return True

    def movimiento_valido(self, ficha: str, fichas_destino: List[str]) -> bool:
        """Valida si el destino está bloqueado por el rival.

        Reglas:
            - Si el destino tiene 2 o más fichas rivales → movimiento inválido.
            - En otro caso → válido.

        Args:
            ficha (str): 'X' o 'O' que intenta moverse.
            fichas_destino (List[str]): Pila en el punto destino (puede estar vacía).

        Returns:
            bool: `True` si el destino NO está bloqueado para `ficha`.
        """
        if len(fichas_destino) >= 2 and all(f != ficha for f in fichas_destino):
            return False
        return True

    def distancia_legal(self, ficha: str, origen: int, destino: int) -> Optional[int]:
        """Calcula la distancia positiva si la dirección es legal para la ficha.

        Reglas:
            - X avanza hacia números MAYORES (destino > origen).
            - O avanza hacia números MENORES (destino < origen).

        Args:
            ficha (str): 'X' o 'O'.
            origen (int): Punto de origen (1–24).
            destino (int): Punto de destino.

        Returns:
            Optional[int]: Distancia positiva a consumir con los dados si es legal,
            `None` si la dirección es inválida.
        """
        if ficha == "X":
            if destino <= origen:
                return None
            return destino - origen
        # ficha == 'O'
        if destino >= origen:
            return None
        return origen - destino

    def fichas_restantes(self, ficha: str) -> int:
        """Cuenta cuántas fichas de un jugador quedan en tablero + barra.

        Args:
            ficha (str): 'X' o 'O'.

        Returns:
            int: Cantidad total en tablero y barra (excluye retiradas en `off`).
        """
        total = 0
        for _, pila in self.tablero.items():
            total += sum(1 for x in pila if x == ficha)
        return total + len(self.bar[ficha])

    def ganador(self) -> Optional[str]:
        """Determina si existe un ganador por retiro de todas sus fichas.

        Returns:
            Optional[str]: 'X' o 'O' si alguno completó 15 fichas en `off`.
            `None` si aún no hay ganador.
        """
        if len(self.off["X"]) == 15:
            return "X"
        if len(self.off["O"]) == 15:
            return "O"
        return None

    def mover_ficha(self, origen: int, destino: int) -> bool:
        """Mueve una ficha aplicando reglas básicas de Backgammon.

        Validaciones realizadas (en este orden):
            1) Reingreso desde barras especiales `0` (X) o `25` (O) si aplica.
            2) Existencia de ficha en `origen`.
            3) Si el jugador tiene fichas en su `bar`, no puede mover otras.
            4) Retiro (bearing off) si todas las fichas están en el cuadrante final.
            5) Dirección legal (X sube; O baja).
            6) Bloqueo por dos o más fichas rivales en `destino`.
            7) Captura si hay exactamente una ficha rival en `destino`.

        Args:
            origen (int): Punto de origen (1–24) o barras especiales (0/25).
            destino (int): Punto de destino. Para retiro: 0 (O) o 25 (X).

        Returns:
            bool: `True` si el movimiento se ejecutó, `False` si fue inválido.
        """
        """Mueve una ficha aplicando reglas de backgammon (incluye reingreso y captura)."""

        # --- Reingreso desde barra X (origen 0) ---
        if origen == 0:
            ficha = "X"
            if not self.bar[ficha]:
                print("No hay fichas 'X' en la barra (0).")
                return False

            fichas_destino = self.tablero.get(destino, [])
            # Bloqueo: 2 o más rivales
            if not self.movimiento_valido(ficha, fichas_destino):
                print(f"❌ No puedes reingresar a {destino}: bloqueado por el rival.")
                return False

            # Captura: exactamente una rival
            if len(fichas_destino) == 1 and fichas_destino[0] != ficha:
                rival = fichas_destino.pop()
                self.bar[rival].append(rival)
                print(f"🍴 Ficha '{rival}' comida en el punto {destino} y enviada a la barra.")

            # Efectuar reingreso
            self.bar[ficha].pop()
            self.tablero.setdefault(destino, []).append(ficha)
            print(f"✅ Ficha 'X' reingresó desde barra al punto {destino}.")
            return True

        # --- Reingreso desde barra O (origen 25) ---
        if origen == 25:
            ficha = "O"
            if not self.bar[ficha]:
                print("No hay fichas 'O' en la barra (25).")
                return False

            fichas_destino = self.tablero.get(destino, [])
            if not self.movimiento_valido(ficha, fichas_destino):
                print(f"❌ No puedes reingresar a {destino}: bloqueado por el rival.")
                return False

            if len(fichas_destino) == 1 and fichas_destino[0] != ficha:
                rival = fichas_destino.pop()
                self.bar[rival].append(rival)
                print(f"🍴 Ficha '{rival}' comida en el punto {destino} y enviada a la barra.")

            self.bar[ficha].pop()
            self.tablero.setdefault(destino, []).append(ficha)
            print(f"✅ Ficha 'O' reingresó desde barra al punto {destino}.")
            return True

        # Origen debe contener fichas
        if origen not in self.tablero or len(self.tablero[origen]) == 0:
            print(f"No hay fichas en el punto {origen}")
            return False

        ficha = self.tablero[origen][-1]
        fichas_destino = self.tablero.get(destino, [])

        # Si hay fichas capturadas del jugador, deben reingresar primero
        if self.bar[ficha]:
            print(f"❌ No puedes mover otras fichas '{ficha}' mientras tengas piezas en la barra.")
            return False

        # Retiro (bearing off)
        if ficha == "O" and destino == 0:
            if self.todas_en_cuadrante_final("O"):
                self.tablero[origen].pop()
                self.off["O"].append("O")
                print("✅ Ficha 'O' retirada del tablero.")
                return True
            print("❌ No puedes retirar fichas 'O' todavía (no todas están en el cuadrante final).")
            return False

        if ficha == "X" and destino == 25:
            if self.todas_en_cuadrante_final("X"):
                self.tablero[origen].pop()
                self.off["X"].append("X")
                print("✅ Ficha 'X' retirada del tablero.")
                return True
            print("❌ No puedes retirar fichas 'X' todavía (no todas están en el cuadrante final).")
            return False

        # Dirección legal
        if ficha == "O" and destino >= origen:
            print(f"❌ Ficha 'O' solo puede bajar (de {origen} a menor número).")
            return False
        if ficha == "X" and destino <= origen:
            print(f"❌ Ficha 'X' solo puede subir (de {origen} a mayor número).")
            return False

        # Bloqueo
        if not self.movimiento_valido(ficha, fichas_destino):
            print(f"❌ No puedes mover al punto {destino}: bloqueado por el rival.")
            return False

        # Captura (una sola ficha rival en destino)
        if len(fichas_destino) == 1 and fichas_destino[0] != ficha:
            rival = fichas_destino.pop()
            self.bar[rival].append(rival)
            print(f"🍴 Ficha '{rival}' comida en el punto {destino} y enviada a la barra.")

        # Movimiento válido
        self.tablero[origen].pop()
        self.tablero.setdefault(destino, []).append(ficha)
        return True
