class Tablero:
    def __init__(self):
        self.tablero = {
            24: ["O"] * 2,
            13: ["O"] * 5,
            8:  ["O"] * 3,
            6:  ["O"] * 5,
            1:  ["X"] * 2,
            12: ["X"] * 5,
            17: ["X"] * 3,
            19: ["X"] * 5,
        }
        self.max_altura = 8
        # 🔹 Agregamos la barra para fichas comidas
        self.bar = {"O": [], "X": []}

        # 🔹 Fichas retiradas (bearing off)
        self.off = {"O": [], "X": []}

    def celda(self, contenido):
        return f"{contenido:^3}"

    def mostrar(self):
        output = []

        # Parte superior (13–24)
        for fila in range(self.max_altura, 0, -1):
            linea = " "
            for punto in range(13, 19):
                fichas = self.tablero.get(punto, [])
                linea += self.celda(fichas[fila-1] if len(fichas) >= fila else " ")
            linea += "|"
            for punto in range(19, 25):
                fichas = self.tablero.get(punto, [])
                linea += self.celda(fichas[fila-1] if len(fichas) >= fila else " ")
            output.append(linea)

        # Numeración superior
        linea = " "
        for punto in range(13, 19):
            linea += self.celda(punto)
        linea += "|"
        for punto in range(19, 25):
            linea += self.celda(punto)
        output.append(linea)

        output.append(" " + "-" * (3*12 + 1))

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
                linea += self.celda(fichas[fila-1] if len(fichas) >= fila else " ")
            linea += "|"
            for punto in range(6, 0, -1):
                fichas = self.tablero.get(punto, [])
                linea += self.celda(fichas[fila-1] if len(fichas) >= fila else " ")
            output.append(linea)

        return "\n".join(output)

    def todas_en_cuadrante_final(self, ficha):
        """Devuelve True si todas las fichas del jugador están en su cuadrante final."""
        if ficha == "O":
            # fichas O deben estar en puntos 1–6
            for punto, fichas in self.tablero.items():
                if "O" in fichas and punto > 6:
                    return False
        else:  # ficha == "X"
            # fichas X deben estar en puntos 19–24
            for punto, fichas in self.tablero.items():
                if "X" in fichas and punto < 19:
                    return False
        return True
    
    def movimiento_valido(self, ficha, fichas_destino):
        """
        Regla básica:
        - Si el destino tiene 2 o más fichas rivales → movimiento inválido.
        - En otro caso → válido.
        """
        if len(fichas_destino) >= 2 and all(f != ficha for f in fichas_destino):
            return False
        return True

    def mover_ficha(self, origen, destino):
        """Mueve una ficha aplicando reglas de backgammon."""
        if origen not in self.tablero or len(self.tablero[origen]) == 0:
            print(f"No hay fichas en el punto {origen}")
            return False

        ficha = self.tablero[origen][-1]
        fichas_destino = self.tablero.get(destino, [])

        # 🔹 Validación: si hay fichas capturadas, deben reintegrarse primero
        if self.bar[ficha]:
            print(f"❌ No puedes mover otras fichas '{ficha}' mientras tengas piezas en la barra.")
            return False

        # 🔹 Caso especial: retirar fichas 
        if ficha == "O" and destino == 0:
            if self.todas_en_cuadrante_final("O"):
                self.tablero[origen].pop()
                self.off["O"].append("O")
                print(f"✅ Ficha 'O' retirada del tablero.")
                return True
            else:
                print("❌ No puedes retirar fichas 'O' todavía (no todas están en el cuadrante final).")
                return False

        if ficha == "X" and destino == 25:
            if self.todas_en_cuadrante_final("X"):
                self.tablero[origen].pop()
                self.off["X"].append("X")
                print(f"✅ Ficha 'X' retirada del tablero.")
                return True
            else:
                print("❌ No puedes retirar fichas 'X' todavía (no todas están en el cuadrante final).")
                return False

        # 🔹 Validar dirección de movimiento
        if ficha == "O" and destino >= origen:
            print(f"❌ Ficha 'O' solo puede bajar (de {origen} a menor número).")
            return False
        if ficha == "X" and destino <= origen:
            print(f"❌ Ficha 'X' solo puede subir (de {origen} a mayor número).")
            return False

        # 🔹 Validar con las reglas 
        if not self.movimiento_valido(ficha, fichas_destino):
            print(f"❌ No puedes mover al punto {destino}: bloqueado por el rival.")
            return False

        # 🔹 Si hay una sola ficha rival → se come
        if len(fichas_destino) == 1 and fichas_destino[0] != ficha:
            rival = fichas_destino.pop()      # quitar ficha rival
            self.bar[rival].append(rival)     # enviar a la barra
            print(f"🍴 Ficha '{rival}' comida en el punto {destino} y enviada a la barra.")

        # 🔹 Movimiento válido
        self.tablero[origen].pop()
        self.tablero.setdefault(destino, []).append(ficha)
        return True


