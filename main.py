from core.board import Tablero

def main():
    juego = Tablero()
    print("🎲 Estado inicial del tablero:\n")
    print(juego.mostrar())

    # Ejemplo 1: mover ficha O correctamente
    print("\n🔹 Movimiento válido: ficha O de 13 a 11")
    juego.mover_ficha(13, 11)
    print(juego.mostrar())

    # Ejemplo 2: mover ficha X correctamente
    print("\n🔹 Movimiento válido: ficha X de 1 a 3")
    juego.mover_ficha(1, 3)
    print(juego.mostrar())

    # Ejemplo 3: intento inválido (O no puede subir de 11 a 13)
    print("\n🔹 Movimiento inválido: ficha O intentando subir de 11 a 13")
    juego.mover_ficha(11, 13)
    print(juego.mostrar())

    # Ejemplo 4: intento inválido (X no puede bajar de 3 a 2)
    print("\n🔹 Movimiento inválido: ficha X intentando bajar de 3 a 2")
    juego.mover_ficha(3, 2)
    print(juego.mostrar())

    # Ejemplo 5: movimiento bloqueado (O de 11 a 19, ocupado por 5 X)
    print("\n🔹 Movimiento bloqueado: O intentando entrar en punto 19 con 5 X")
    juego.mover_ficha(11, 19)
    print(juego.mostrar())

    # Ejemplo 6: comer ficha (preparamos punto 5 con 1 X, O baja de 6 a 5)
    print("\n🔹 Movimiento con captura: O de 6 a 5 (come a X)")
    juego.tablero[5] = ["X"]
    juego.mover_ficha(6, 5)
    print(juego.mostrar())
    print("📦 Barra actual:", juego.bar)

    # Ejemplo 7: mover varias veces (O de 13→7 en 2 pasos)
    print("\n🔹 Movimiento en dos pasos: O de 13 a 7 (13→11→7)")
    juego.mover_ficha(13, 11)
    juego.mover_ficha(11, 7)
    print(juego.mostrar())

    # Ejemplo 8: intentar mover cuando hay fichas en la barra
    print("\n🔹 Movimiento inválido: O intenta mover otra ficha mientras tiene piezas en la barra")
    # Forzamos a que O tenga una ficha en la barra
    juego.bar["O"].append("O")
    # Intentamos mover otra ficha O desde 13 a 11
    juego.mover_ficha(13, 11)
    print(juego.mostrar())
    print("📦 Barra actual:", juego.bar)

if __name__ == "__main__":
    main()