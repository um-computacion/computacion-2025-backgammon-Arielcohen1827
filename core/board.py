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
            0:  [],   # barra de X
            25: [],   # barra de O
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
        # 🔹 Mostrar barra al final
        barra_o = self.tablero.get(25, []) + self.bar["O"]
        barra_x = self.tablero.get(0, []) + self.bar["X"]
        output.append("\nBarra O (25): " + str(barra_o))
        output.append("Barra X (0): " + str(barra_x))

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

    def distancia_legal(self, ficha: str, origen: int, destino: int) -> int | None:
        """
        Regla de dirección/distancia:
        - X avanza hacia números MAYORES (destino > origen)
        - O avanza hacia números MENORES (destino < origen)
        Devuelve la distancia positiva a consumir si es legal; si no, None.
        """
        if ficha == "X":
            if destino <= origen:
                return None
            return destino - origen
        else:  # 'O'
            if destino >= origen:
                return None
            return origen - destino
        
        
    def fichas_restantes(self, ficha: str) -> int:
        """Cuenta cuántas fichas de `ficha` quedan en el tablero (sin incluir bar/off)."""
        total = 0
        for p, pila in self.tablero.items():
            total += sum(1 for x in pila if x == ficha)
        return total + len(self.bar[ficha])

    def ganador(self):
        """
        Devuelve 'X' o 'O' si alguno retiró las 15 fichas (off).
        Si nadie ganó, devuelve None.
        """
        if len(self.off["X"]) == 15:
            return "X"
        if len(self.off["O"]) == 15:
            return "O"
        # Alternativa equivalente: no quedan fichas ni en tablero ni en barra
        # if self.fichas_restantes('X') == 0: return 'X'
        # if self.fichas_restantes('O') == 0: return 'O'
        return None
    
    

    def mover_ficha(self, origen, destino):
        
        """Mueve una ficha aplicando reglas de backgammon."""
        # --- Reingreso desde barra (simple) ---
        if origen == 0:   # barra de X
                # Reingreso desde barra: usa self.bar["X"] como fuente de verdad
                if not self.bar["X"] and not self.tablero[0]:
                    print("No hay fichas 'X' en la barra (0).")
                    return False

                fichas_destino = self.tablero.get(destino, [])

                # Bloqueo: no puede entrar si hay 2+ del rival
                if not self.movimiento_valido("X", fichas_destino):
                    print(f"❌ No puedes reingresar a {destino}: bloqueado por el rival.")
                    return False

                # Comer si hay 1 rival
                if len(fichas_destino) == 1 and fichas_destino[0] == "O":
                    fichas_destino.pop()
                    self.bar["O"].append("O")

                # Sacar de la barra (preferimos self.bar sobre tablero[0] por compatibilidad)
                if self.bar["X"]:
                    self.bar["X"].pop()
                else:
                    self.tablero[0].pop()

                self.tablero.setdefault(destino, []).append("X")
                print(f"✅ Ficha 'X' reingresó desde 0 al punto {destino}.")
                return True

        if origen == 25:  # barra de O
            # Reingreso desde barra: usa self.bar["O"]
            if not self.bar["O"] and not self.tablero[25]:
                print("No hay fichas 'O' en la barra (25).")
                return False

            fichas_destino = self.tablero.get(destino, [])

            # Bloqueo: no puede entrar si hay 2+ del rival
            if not self.movimiento_valido("O", fichas_destino):
                print(f"❌ No puedes reingresar a {destino}: bloqueado por el rival.")
                return False

            # Comer si hay 1 rival
            if len(fichas_destino) == 1 and fichas_destino[0] == "X":
                fichas_destino.pop()
                self.bar["X"].append("X")

            # Sacar de la barra (preferimos self.bar sobre tablero[25] por compatibilidad)
            if self.bar["O"]:
                self.bar["O"].pop()
            else:
                self.tablero[25].pop()

            self.tablero.setdefault(destino, []).append("O")
            print(f"✅ Ficha 'O' reingresó desde 25 al punto {destino}.")
            return True
        # --- fin reingreso desde barra ---
        
        
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

    

