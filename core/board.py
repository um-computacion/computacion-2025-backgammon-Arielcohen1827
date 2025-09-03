def mostrar_tablero():
    def celda(contenido):
        return f"{contenido:^3}"  # ancho fijo

    # Parte superior (13–24)
    print(" " + "".join(celda(p) for p in range(13, 19)) + "|" +
               "".join(celda(p) for p in range(19, 25)))

    print(" " + "-" * (3*12 + 1))

    # Parte inferior (12–1)
    print(" " + "".join(celda(p) for p in range(12, 6, -1)) + "|" +
               "".join(celda(p) for p in range(6, 0, -1)))


if __name__ == "__main__":
    mostrar_tablero()
