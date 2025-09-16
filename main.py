from core.board import Tablero

def main():
    juego = Tablero()
    print("🎲 Estado inicial del tablero:")
    print(juego.mostrar())

    # 🔹 Intento inválido: mover a un punto bloqueado
    print("\n🔹 Intentando mover ficha de 13 a 8 (ocupado por 3 'O')...\n")
    juego.mover_ficha(13, 8)
    print(juego.mostrar())

    # 🔹 Movimiento válido
    print("\n🔹 Moviendo ficha de 13 a 11...\n")
    juego.mover_ficha(13, 11)
    print(juego.mostrar())

    # 🔹 Comer ficha rival (si hay 1 sola del otro color en destino)
    print("\n🔹 Simulando comer ficha en punto 12...\n")
    juego.tablero[12] = ["X"]  # dejamos solo una X
    juego.tablero[11] = ["O"]  # movemos O desde 11
    juego.mover_ficha(11, 12)
    print(juego.mostrar())
    print("Barra:", juego.bar)

    # 🔹 Intentar mover cuando hay fichas en la barra
    print("\n🔹 Intentando mover otra ficha 'X' mientras tiene piezas en la barra...\n")
    juego.mover_ficha(12, 13)  # debería bloquearse porque 'X' tiene piezas en barra
    print(juego.mostrar())

    # 🔹 Retirar fichas (bearing off)
    print("\n🔹 Probando retiro de fichas 'O'...\n")
    # Forzamos que todas las O estén en el cuadrante final
    juego.tablero = {p: [] for p in range(1, 25)}
    juego.tablero[1] = ["O", "O", "O"]
    juego.mover_ficha(1, 0)  # retirar una ficha
    print(juego.mostrar())
    print("Fichas retiradas (off):", juego.off)

if __name__ == "__main__":
    main()
