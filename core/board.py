def mostrar_tablero():
    tablero = {
        24: ["O"] * 2,
        13: ["O"] * 5,
        8:  ["O"] * 3,
        6:  ["O"] * 5,
        1:  ["X"] * 2,
        12: ["X"] * 5,
        17: ["X"] * 3,
        19: ["X"] * 5,
    }

    max_altura = 8  # altura visible

    def celda(contenido):
        """Devuelve el contenido centrado en un ancho fijo de 3."""
        return f"{contenido:^3}"

    # Parte superior (13–24)
    for fila in range(max_altura, 0, -1):
        linea = " "
        for punto in range(13, 19):
            fichas = tablero.get(punto, [])
            linea += celda(fichas[fila-1] if len(fichas) >= fila else " ")
        linea += "|"
        for punto in range(19, 25):
            fichas = tablero.get(punto, [])
            linea += celda(fichas[fila-1] if len(fichas) >= fila else " ")
        print(linea)

    # Numeración superior
    linea = " "
    for punto in range(13, 19):
        linea += celda(punto)
    linea += "|"
    for punto in range(19, 25):
        linea += celda(punto)
    print(linea)

    print(" " + "-" * (3*12 + 1))

    # Numeración inferior
    linea = " "
    for punto in range(12, 6, -1):
        linea += celda(punto)
    linea += "|"
    for punto in range(6, 0, -1):
        linea += celda(punto)
    print(linea)

    # Parte inferior (12–1)
    for fila in range(1, max_altura + 1):
        linea = " "
        for punto in range(12, 6, -1):
            fichas = tablero.get(punto, [])
            linea += celda(fichas[fila-1] if len(fichas) >= fila else " ")
        linea += "|"
        for punto in range(6, 0, -1):
            fichas = tablero.get(punto, [])
            linea += celda(fichas[fila-1] if len(fichas) >= fila else " ")
        print(linea)


if __name__ == "__main__":
    mostrar_tablero()