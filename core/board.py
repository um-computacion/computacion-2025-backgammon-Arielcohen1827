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
        return f"{contenido:^3}"

    output = []

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
        output.append(linea)

    # Numeración superior
    linea = " "
    for punto in range(13, 19):
        linea += celda(punto)
    linea += "|"
    for punto in range(19, 25):
        linea += celda(punto)
    output.append(linea)

    output.append(" " + "-" * (3*12 + 1))

    # Numeración inferior
    linea = " "
    for punto in range(12, 6, -1):
        linea += celda(punto)
    linea += "|"
    for punto in range(6, 0, -1):
        linea += celda(punto)
    output.append(linea)

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
        output.append(linea)

    # ✅ Devuelve el tablero como string
    return "\n".join(output)


if __name__ == "__main__":
    # ✅ Si corrés este archivo directamente, imprime el tablero
    print(mostrar_tablero())
