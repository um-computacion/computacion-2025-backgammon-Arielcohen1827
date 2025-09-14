class Tablero:
    def __init__(self):
        # Representa el tablero como dict: clave = punto, valor = lista de fichas
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
        """Mueve una ficha de un punto a otro (si existe)."""
        if origen not in self.tablero or len(self.tablero[origen]) == 0:
            print(f"No hay fichas en el punto {origen}")
            return False

        ficha = self.tablero[origen].pop()  # saca una ficha
        self.tablero.setdefault(destino, []).append(ficha)  # la pone en destino
        return True


if __name__ == "__main__":
    juego = Tablero()
    print(juego.mostrar())

    print("\n🔹 Moviendo ficha de 13 a 11...\n")
    juego.mover_ficha(13, 11)

    print(juego.mostrar())
