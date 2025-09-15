from core.checker import Checker

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

    def mover_ficha(self, origen, destino):
        """Mueve una ficha si el Checker lo permite."""
        if origen not in self.tablero or len(self.tablero[origen]) == 0:
            print(f"No hay fichas en el punto {origen}")
            return False

        ficha = self.tablero[origen][-1]
        fichas_destino = self.tablero.get(destino, [])
        # 🔹 Validar dirección de movimiento
        if ficha == "O" and destino >= origen:
            print(f"❌ Ficha 'O' solo puede bajar (de {origen} a menor número).")
            return False
        if ficha == "X" and destino <= origen:
            print(f"❌ Ficha 'X' solo puede subir (de {origen} a mayor número).")
            return False


        # Usamos Checker para validar
        if not Checker.movimiento_valido(ficha, fichas_destino):
            print(f"❌ No puedes mover al punto {destino}: bloqueado por el rival.")
            return False

        # Movimiento válido
        self.tablero[origen].pop()
        self.tablero.setdefault(destino, []).append(ficha)
        return True


if __name__ == "__main__":
    juego = Tablero()
    print(juego.mostrar())

    print("\n🔹 Intentando mover ficha de 13 a 8 (ocupado por 3 'O')...\n")
    juego.mover_ficha(13, 8)  # debería bloquearse
    print(juego.mostrar())

    print("\n🔹 Moviendo ficha de 13 a 11...\n")
    juego.mover_ficha(13, 11)  # debería funcionar
    print(juego.mostrar())