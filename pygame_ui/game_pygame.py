# pygame_ui/game_pygame.py
"""Interfaz gráfica de Backgammon usando Pygame.

Provee la clase `PygameUI` con:
- Construcción de geometría del tablero y áreas (barra, off).
- Dibujo del tablero, fichas, barra de comidas y barra de salida.
- Mapeo click ↔ punto de tablero; cálculo de centros y triángulos.
- HUD con tirada y movimientos restantes.
- Entrada de nombres mediante cuadros de texto.
- Lógica de turnos (sorteo, tirada de dados, consumo de movimientos).
- Bucle principal `main()` que orquesta el juego.

Este módulo no modifica las reglas core del juego; delega reglas y estado en
`core.board.Tablero`. Solo se encarga de visualización e interacción.
"""

import pygame, random
from core.board import Tablero


class PygameUI:
    """Interfaz de usuario para Backgammon basada en Pygame.

    Crea la ventana, calcula la geometría, dibuja el tablero y gestiona el
    bucle de eventos. El estado del juego (fichas, barra, off) se mantiene en
    una instancia de `core.board.Tablero`.

    Atributos:
        ANCHO (int): Ancho de la ventana.
        ALTO (int): Alto de la ventana.
        VENTANA (pygame.Surface): Superficie principal del display.
        FUENTE, FUENTE_UI, FUENTE_TIT, FUENTE_MINI: Fuentes tipográficas.
        tablero (Tablero): Estado core del tablero y fichas.
        tirada_actual (tuple[int, int]): Dados actuales (d1, d2).
        movimientos_restantes (list[int]): Valores de movimiento aún por usar.
        GEO (dict|None): Geometría calculada (rects, anchos de columna, etc.).
    """

    # ─────────────────────────────────────────────────────────────────────────────
    # Constructor e inicialización
    # ─────────────────────────────────────────────────────────────────────────────
    def __init__(self):
        """Inicializa Pygame, la ventana, colores, fuentes y estado base."""
        pygame.init()

        # Dimensiones
        self.ANCHO, self.ALTO = 1100, 650
        self.VENTANA = pygame.display.set_mode((self.ANCHO, self.ALTO))
        pygame.display.set_caption("Backgammon - Pygame")

        # 🎨 Colores
        self.MADERA_CLARA = (222, 206, 180)
        self.ARENA        = (243, 228, 211)
        self.BORDO        = (128, 0, 32)
        self.BARRA_GRIS   = (60, 60, 60)
        self.CONTORNO     = (40, 30, 20)
        self.NEGRO = (0, 0, 0)
        self.BLANCO = (255, 255, 255)
        self.FONDO_EXTERIOR = (26, 36, 48)
        self.CELESTE = (90, 170, 255)
        self.LIMA = (150, 255, 150)
        self.HIGHLIGHT = (80, 180, 250)
        self.HIGHLIGHT_TRI_FILL   = (80, 180, 250, 90)   # celeste con transparencia
        self.HIGHLIGHT_TRI_BORDER = (80, 180, 250)       # borde del triángulo seleccionado

        # Geometría base
        self.MARGEN_X = 50
        self.MARGEN_Y = 50
        self.BARRA_W = 80
        self.BAR_PILA_RADIO = 14
        self.BAR_PILA_SEP = 6

        # Fuentes
        pygame.font.init()
        self.FUENTE = pygame.font.SysFont("arial", 22, bold=True)
        self.FUENTE_UI = pygame.font.SysFont("arial", 24)
        self.FUENTE_TIT = pygame.font.SysFont("arial", 28, bold=True)
        self.FUENTE_MINI = pygame.font.SysFont("arial", 16)

        # Lógica
        self.tablero = Tablero()

        # Estado de juego
        self.tirada_actual = (0, 0)
        self.movimientos_restantes: list[int] = []

        # Geometría calculada (se setea en main)
        self.GEO = None

    # ─────────────────────────────────────────────────────────────────────────────
    # Construcción de geometría
    # ─────────────────────────────────────────────────────────────────────────────
    def build_geo_full(self):
        """Calcula rectángulos y anchos de columnas para todo el layout.

        Returns:
            dict: Diccionario con Rects clave:
                - "board": área del tablero
                - "bar": barra central
                - "top_left"/"bot_left"/"top_right"/"bot_right": cuadrantes
                - "off": barra de salida
                - "col_w_left"/"col_w_right": ancho de columna para 6 triángulos
        """
        OFF_W   = 90
        OFF_GAP = 16

        avail_w = self.ANCHO - 2 * self.MARGEN_X
        avail_h = self.ALTO  - 2 * self.MARGEN_Y

        board_w = avail_w - (OFF_W + OFF_GAP)
        board_h = avail_h

        board = pygame.Rect(self.MARGEN_X, self.MARGEN_Y, board_w, board_h)
        bar = pygame.Rect(board.centerx - self.BARRA_W // 2, board.top, self.BARRA_W, board.height)

        left  = pygame.Rect(board.left, board.top, (board.width - self.BARRA_W)//2, board.height)
        right = pygame.Rect(bar.right,  board.top, (board.width - self.BARRA_W)//2, board.height)

        top_left  = pygame.Rect(left.left,  left.top,  left.width,   left.height//2)
        bot_left  = pygame.Rect(left.left,  left.centery, left.width, left.height//2)
        top_right = pygame.Rect(right.left, right.top, right.width,  right.height//2)
        bot_right = pygame.Rect(right.left, right.centery, right.width, right.height//2)

        off_rect = pygame.Rect(board.right + OFF_GAP, board.top, OFF_W, board.height)

        return {
            "board": board, "bar": bar,
            "top_left": top_left, "bot_left": bot_left,
            "top_right": top_right, "bot_right": bot_right,
            "col_w_left":  top_left.width  / 6,
            "col_w_right": top_right.width / 6,
            "off": off_rect,
        }

    # ─────────────────────────────────────────────────────────────────────────────
    # Dibujo del tablero, fichas, barra y HUD
    # ─────────────────────────────────────────────────────────────────────────────
    def dibujar_tablero(self):
        """Pinta el tablero completo: fondo, triángulos, barra central."""
        self.VENTANA.fill(self.FONDO_EXTERIOR)
        pygame.draw.rect(self.VENTANA, self.MADERA_CLARA, self.GEO["board"], border_radius=10)

        def draw_region(rect: pygame.Rect, up: bool, left_side: bool):
            """Dibuja una fila de 6 triángulos en una región.

            Args:
                rect (pygame.Rect): Rectángulo de la región.
                up (bool): True si punta hacia arriba; False si hacia abajo.
                left_side (bool): Si pertenece al lado izquierdo (ancho de columna).
            """
            col_w = self.GEO["col_w_left"] if left_side else self.GEO["col_w_right"]
            for i in range(6):
                x0 = rect.left + i * col_w
                x1 = x0 + col_w
                xm = x0 + col_w/2
                color = self.ARENA if i % 2 == 0 else self.BORDO
                if up:
                    pts = [(x0, rect.bottom), (x1, rect.bottom), (xm, rect.top)]
                else:
                    pts = [(x0, rect.top), (x1, rect.top), (xm, rect.bottom)]
                pygame.draw.polygon(self.VENTANA, color, pts)
                pygame.draw.polygon(self.VENTANA, self.CONTORNO, pts, 1)

        # arriba
        draw_region(self.GEO["top_left"],  up=False, left_side=True)
        draw_region(self.GEO["top_right"], up=False, left_side=False)
        # abajo
        draw_region(self.GEO["bot_left"],  up=True,  left_side=True)
        draw_region(self.GEO["bot_right"], up=True,  left_side=False)

        # barra
        pygame.draw.rect(self.VENTANA, (120, 80, 40), self.GEO["bar"], border_radius=6)
        pygame.draw.rect(self.VENTANA, (40, 20, 10), self.GEO["bar"], 4, border_radius=6)

    def dibujar_fichas(self):
        """Dibuja todas las fichas del tablero en sus posiciones actuales."""
        radio = 15
        for punto, fichas in self.tablero.tablero.items():
            for idx, ficha in enumerate(fichas):
                if 13 <= punto <= 18:
                    col_w = self.GEO["col_w_left"]; rect = self.GEO["top_left"]
                    x = rect.left + (punto - 13 + 0.5) * col_w
                    y = self.MARGEN_Y + idx * 2 * radio + radio
                elif 19 <= punto <= 24:
                    col_w = self.GEO["col_w_right"]; rect = self.GEO["top_right"]
                    x = rect.left + (punto - 19 + 0.5) * col_w
                    y = self.MARGEN_Y + idx * 2 * radio + radio
                elif 7 <= punto <= 12:
                    col_w = self.GEO["col_w_left"]; rect = self.GEO["bot_left"]
                    x = rect.left + (12 - punto + 0.5) * col_w
                    y = self.ALTO - self.MARGEN_Y - idx * 2 * radio - radio
                elif 1 <= punto <= 6:
                    col_w = self.GEO["col_w_right"]; rect = self.GEO["bot_right"]
                    x = rect.left + (6 - punto + 0.5) * col_w
                    y = self.ALTO - self.MARGEN_Y - idx * 2 * radio - radio
                else:
                    continue

                color = self.NEGRO if ficha == "X" else self.BLANCO
                pygame.draw.circle(self.VENTANA, color, (int(x), int(y)), radio)
                pygame.draw.circle(self.VENTANA, self.CONTORNO, (int(x), int(y)), radio, 1)

    def dibujar_barra_comidas(self):
        """Representa visualmente la barra con fichas comidas (X abajo, O arriba)."""
        barra = self.GEO["bar"]
        inner = barra.inflate(-10, -10)
        pygame.draw.rect(self.VENTANA, (180, 140, 100), inner, border_radius=8)
        pygame.draw.rect(self.VENTANA, (50, 30, 20), inner, 2, border_radius=8)

        cx = barra.centerx

        # O (arriba)
        n_o = len(self.tablero.bar.get("O", []))
        y_top = inner.top + 14
        for i in range(n_o):
            y = y_top + i * (2*self.BAR_PILA_RADIO + self.BAR_PILA_SEP)
            if y + self.BAR_PILA_RADIO > inner.centery - 12: break
            pygame.draw.circle(self.VENTANA, self.BLANCO, (cx, y), self.BAR_PILA_RADIO)
            pygame.draw.circle(self.VENTANA, self.CONTORNO, (cx, y), self.BAR_PILA_RADIO, 1)
        if n_o:
            text = self.FUENTE_MINI.render(f"O:{n_o}", True, self.BLANCO)
            self.VENTANA.blit(text, text.get_rect(center=(cx, inner.top + 8)))

        # X (abajo)
        n_x = len(self.tablero.bar.get("X", []))
        y_bottom = inner.bottom - 14
        for i in range(n_x):
            y = y_bottom - i * (2*self.BAR_PILA_RADIO + self.BAR_PILA_SEP)
            if y - self.BAR_PILA_RADIO < inner.centery + 12: break
            pygame.draw.circle(self.VENTANA, self.NEGRO, (cx, y), self.BAR_PILA_RADIO)
            pygame.draw.circle(self.VENTANA, self.CONTORNO, (cx, y), self.BAR_PILA_RADIO, 1)
        if n_x:
            text = self.FUENTE_MINI.render(f"X:{n_x}", True, self.BLANCO)
            self.VENTANA.blit(text, text.get_rect(center=(cx, inner.bottom - 8)))

    def dibujar_nombres(self, jugador_x, jugador_o, turno_actual=None):
        """Imprime los nombres de jugadores y destaca el que tiene el turno.

        Args:
            jugador_x (str): Nombre del jugador con fichas negras (X).
            jugador_o (str): Nombre del jugador con fichas blancas (O).
            turno_actual (str|None): 'X' o 'O' para resaltar, o None sin resaltar.
        """
        offset_x = 12
        offset_y = 28

        color_o = self.CELESTE if turno_actual == "O" else self.BLANCO
        color_x = self.CELESTE if turno_actual == "X" else self.BLANCO

        texto_o = self.FUENTE.render(f"{jugador_o} (Blancas)", True, color_o)
        texto_x = self.FUENTE.render(f"{jugador_x} (Negras)",  True, color_x)

        rect_o = texto_o.get_rect(topleft=(self.GEO["board"].left - offset_x, self.GEO["board"].top - offset_y))
        rect_x = texto_x.get_rect(bottomleft=(self.GEO["board"].left - offset_x, self.GEO["board"].bottom + offset_y))

        self.VENTANA.blit(texto_o, rect_o)
        self.VENTANA.blit(texto_x, rect_x)

    def dibujar_hud(self):
        """Muestra tirada actual, movimientos restantes y un hint de teclado."""
        d1, d2 = self.tirada_actual
        hud1 = self.FUENTE.render(f"Tirada: {d1}-{d2}" if d1 else "Tirada: —", True, self.BLANCO)
        hud2 = self.FUENTE.render(f"Movimientos: {self.movimientos_restantes if self.movimientos_restantes else '—'}", True, self.BLANCO)
        hint = self.FUENTE_MINI.render("ENTER: pasar turno", True, self.BLANCO)
        self.VENTANA.blit(hud1, (self.ANCHO//2 - 120, 8))
        self.VENTANA.blit(hud2, (self.ANCHO//2 + 40, 8))
        self.VENTANA.blit(hint, (self.ANCHO//2 + 300, 12))

    # ─────────────────────────────────────────────────────────────────────────────
    # Mapeos (click ↔ punto) y utilidades de dibujo/selección
    # ─────────────────────────────────────────────────────────────────────────────
    def pasar_turno(self, turno_actual):
        """Alterna el turno, tira dados y prepara movimientos.

        Args:
            turno_actual (str): Turno actual ('X' o 'O').

        Returns:
            str: Nuevo turno ('O' si era 'X', y viceversa).
        """
        nuevo_turno = "O" if turno_actual == "X" else "X"
        self.tirar_dados_y_preparar_movimientos()
        return nuevo_turno

    def punto_desde_click(self, pos):
        """Convierte coordenadas de click a un punto del tablero o barra.

        Args:
            pos (tuple[int, int]): Posición (x, y) del click.

        Returns:
            int|None: Punto 1..24, 0 (barra X), 25 (barra O) o None si está fuera.
        """
        x, y = pos
        if not self.GEO["board"].collidepoint(x, y):
            return None

        if self.GEO["bar"].collidepoint(x, y):
            return 25 if y < self.GEO["board"].centery else 0

        if self.GEO["top_left"].collidepoint(x, y):
            i = int((x - self.GEO["top_left"].left) // self.GEO["col_w_left"])
            return 13 + max(0, min(5, i))
        if self.GEO["top_right"].collidepoint(x, y):
            i = int((x - self.GEO["top_right"].left) // self.GEO["col_w_right"])
            return 19 + max(0, min(5, i))
        if self.GEO["bot_left"].collidepoint(x, y):
            i = int((x - self.GEO["bot_left"].left) // self.GEO["col_w_left"])
            return 12 - max(0, min(5, i))
        if self.GEO["bot_right"].collidepoint(x, y):
            i = int((x - self.GEO["bot_right"].left) // self.GEO["col_w_right"])
            return 6 - max(0, min(5, i))

        return None

    def centro_punto(self, p):
        """Devuelve el centro (aprox.) donde dibujar para un punto del tablero.

        Args:
            p (int): Punto 1..24, 0 o 25.

        Returns:
            tuple[int, int]: Coordenadas (x, y) enteras para ese punto.
        """
        if 13 <= p <= 18:
            col_w = self.GEO["col_w_left"]; rect = self.GEO["top_left"]
            x = rect.left + (p - 13 + 0.5) * col_w; y = rect.bottom - 18
        elif 19 <= p <= 24:
            col_w = self.GEO["col_w_right"]; rect = self.GEO["top_right"]
            x = rect.left + (p - 19 + 0.5) * col_w; y = rect.bottom - 18
        elif 7 <= p <= 12:
            col_w = self.GEO["col_w_left"]; rect = self.GEO["bot_left"]
            x = rect.left + (12 - p + 0.5) * col_w; y = rect.top + 18
        elif 1 <= p <= 6:
            col_w = self.GEO["col_w_right"]; rect = self.GEO["bot_right"]
            x = rect.left + (6 - p + 0.5) * col_w; y = rect.top + 18
        elif p == 25:
            x, y = self.GEO["bar"].centerx, self.GEO["bar"].top + 20
        elif p == 0:
            x, y = self.GEO["bar"].centerx, self.GEO["bar"].bottom - 20
        else:
            x, y = self.ANCHO//2, self.ALTO//2
        return int(x), int(y)

    def triangulo_polygon(self, punto):
        """Calcula el polígono (3 vértices) del triángulo de un punto.

        Args:
            punto (int): Punto 1..24.

        Returns:
            list[tuple[int, int]]|None: Tres vértices del triángulo o None si inválido.
        """
        if 13 <= punto <= 18:
            rect = self.GEO["top_left"];  col_w = self.GEO["col_w_left"];  i = punto - 13
            x0 = rect.left + i * col_w;  x1 = x0 + col_w;  xm = x0 + col_w/2
            pts = [(x0, rect.top), (x1, rect.top), (xm, rect.bottom)]
        elif 19 <= punto <= 24:
            rect = self.GEO["top_right"]; col_w = self.GEO["col_w_right"]; i = punto - 19
            x0 = rect.left + i * col_w;  x1 = x0 + col_w;  xm = x0 + col_w/2
            pts = [(x0, rect.top), (x1, rect.top), (xm, rect.bottom)]
        elif 7 <= punto <= 12:
            rect = self.GEO["bot_left"];  col_w = self.GEO["col_w_left"];  i = 12 - punto
            x0 = rect.left + i * col_w;  x1 = x0 + col_w;  xm = x0 + col_w/2
            pts = [(x0, rect.bottom), (x1, rect.bottom), (xm, rect.top)]
        elif 1 <= punto <= 6:
            rect = self.GEO["bot_right"]; col_w = self.GEO["col_w_right"]; i = 6 - punto
            x0 = rect.left + i * col_w;  x1 = x0 + col_w;  xm = x0 + col_w/2
            pts = [(x0, rect.bottom), (x1, rect.bottom), (xm, rect.top)]
        else:
            return None

        inset = 2
        if pts[2][1] > pts[0][1]:  # punta hacia abajo
            return [(pts[0][0]+inset, pts[0][1]+inset),
                    (pts[1][0]-inset, pts[1][1]+inset),
                    (pts[2][0],       pts[2][1]-inset)]
        else:                      # punta hacia arriba
            return [(pts[0][0]+inset, pts[0][1]-inset),
                    (pts[1][0]-inset, pts[1][1]-inset),
                    (pts[2][0],       pts[2][1]+inset)]

    def dibujar_triangulo_seleccionado(self, punto):
        """Pinta un overlay translúcido resaltando el triángulo `punto`.

        Args:
            punto (int): Punto 1..24 a resaltar. Si no es válido, no hace nada.
        """
        poly = self.triangulo_polygon(punto)
        if not poly:
            return
        s = pygame.Surface((self.ANCHO, self.ALTO), pygame.SRCALPHA)
        pygame.draw.polygon(s, self.HIGHLIGHT_TRI_FILL, poly)
        self.VENTANA.blit(s, (0, 0))
        pygame.draw.polygon(self.VENTANA, self.HIGHLIGHT_TRI_BORDER, poly, 3)

    def pos_ficha_barra(self, punto):
        """Devuelve la posición donde dibujar la ficha superior de la barra.

        Args:
            punto (int): 25 para O (arriba) o 0 para X (abajo).

        Returns:
            tuple[int, int] | None: Centro (x, y) para dibujar, o None si vacío.
        """
        barra = self.GEO["bar"]
        inner = barra.inflate(-10, -10)
        cx = barra.centerx

        if punto == 25:  # O
            n = len(self.tablero.bar.get("O", []))
            if n <= 0:
                return None
            y_top = inner.top + 14
            y = y_top + (n - 1) * (2*self.BAR_PILA_RADIO + self.BAR_PILA_SEP)
            y = min(y, inner.centery - 12)
            return (cx, int(y))

        if punto == 0:   # X
            n = len(self.tablero.bar.get("X", []))
            if n <= 0:
                return None
            y_bottom = inner.bottom - 14
            y = y_bottom - (n - 1) * (2*self.BAR_PILA_RADIO + self.BAR_PILA_SEP)
            y = max(y, inner.centery + 12)
            return (cx, int(y))

        return None

    def dibujar_barra_seleccionada(self, punto):
        """Resalta visualmente la mitad de la barra (arriba O / abajo X).

        Args:
            punto (int): 25 para mitad superior (O) o 0 para inferior (X).
        """
        barra = self.GEO["bar"]
        s = pygame.Surface((self.ANCHO, self.ALTO), pygame.SRCALPHA)

        if punto == 25:
            half = pygame.Rect(barra.left, barra.top, barra.width, barra.height//2)
        elif punto == 0:
            half = pygame.Rect(barra.left, barra.centery, barra.width, barra.height//2)
        else:
            return

        pygame.draw.rect(s, (80, 180, 250, 90), half, border_radius=6)
        self.VENTANA.blit(s, (0, 0))
        pygame.draw.rect(self.VENTANA, (80, 180, 250), half, 3, border_radius=6)

        pos = self.pos_ficha_barra(punto)
        if pos:
            cx, cy = pos
            pygame.draw.circle(self.VENTANA, (80, 180, 250), (cx, cy), self.BAR_PILA_RADIO + 4, 3)

    def dibujar_barra_salida(self):
        """Dibuja el panel lateral de salida (off) con contadores X/O."""
        rect = self.GEO["off"]
        pygame.draw.rect(self.VENTANA, (200, 180, 130), rect, border_radius=8)
        pygame.draw.rect(self.VENTANA, (80, 60, 30), rect, 3, border_radius=8)

        txt = self.FUENTE.render("SALIDA", True, (40, 30, 20))
        self.VENTANA.blit(txt, txt.get_rect(center=(rect.centerx, rect.top + 20)))

        off_o = self.tablero.off.get("O", [])
        off_x = self.tablero.off.get("X", [])

        cx = rect.centerx
        y_top = rect.top + 50
        for i, _ in enumerate(off_o):
            y = y_top + i * (2 * self.BAR_PILA_RADIO + self.BAR_PILA_SEP)
            pygame.draw.circle(self.VENTANA, self.BLANCO, (cx, y), self.BAR_PILA_RADIO)
            pygame.draw.circle(self.VENTANA, self.CONTORNO, (cx, y), self.BAR_PILA_RADIO, 1)

        y_bottom = rect.bottom - 30
        for i, _ in enumerate(off_x):
            y = y_bottom - i * (2 * self.BAR_PILA_RADIO + self.BAR_PILA_SEP)
            pygame.draw.circle(self.VENTANA, self.NEGRO, (cx, y), self.BAR_PILA_RADIO)
            pygame.draw.circle(self.VENTANA, self.CONTORNO, (cx, y), self.BAR_PILA_RADIO, 1)

        if off_o:
            txt = self.FUENTE_MINI.render(f"O:{len(off_o)}", True, self.BLANCO)
            self.VENTANA.blit(txt, txt.get_rect(center=(cx, rect.top + 35)))
        if off_x:
            txt = self.FUENTE_MINI.render(f"X:{len(off_x)}", True, self.BLANCO)
            self.VENTANA.blit(txt, txt.get_rect(center=(cx, rect.bottom - 15)))

    # ─────────────────────────────────────────────────────────────────────────────
    # Entrada de nombres
    # ─────────────────────────────────────────────────────────────────────────────
    class InputBox:
        """Cuadro de texto simple para ingresar nombres con click/teclado.

        Permite activar con click, tipear caracteres, borrar con backspace y
        dibujar el texto o el *placeholder*.

        Args:
            rect (pygame.Rect): Área del input en pantalla.
            fuente (pygame.font.Font): Fuente para renderizar texto.
            color_idle (tuple[int,int,int]): Color del borde inactivo.
            color_active (tuple[int,int,int]): Color del borde activo.
            placeholder (str): Texto gris de ayuda cuando no hay contenido.
        """

        def __init__(self, rect: pygame.Rect, fuente, color_idle, color_active, placeholder=""):
            self.rect = rect
            self.fuente = fuente
            self.color_idle = color_idle
            self.color_active = color_active
            self.color = self.color_idle
            self.text = ""
            self.txt_surf = fuente.render("", True, (20,20,20))
            self.active = False
            self.placeholder = placeholder
            self.placeholder_surf = fuente.render(placeholder, True, (130,130,130))

        def handle_event(self, e):
            """Procesa eventos de mouse/teclado para editar o activar el input.

            Args:
                e (pygame.event.Event): Evento de Pygame.
            """
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                self.active = self.rect.collidepoint(e.pos)
                self.color = self.color_active if self.active else self.color_idle
            if e.type == pygame.KEYDOWN and self.active:
                if e.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif e.key not in (pygame.K_RETURN, pygame.K_TAB):
                    if len(self.text) < 24:
                        self.text += e.unicode
                self.txt_surf = self.fuente.render(self.text, True, (20,20,20))

        def draw(self, surf):
            """Dibuja el rectángulo del input y su contenido o placeholder.

            Args:
                surf (pygame.Surface): Superficie de destino.
            """
            pygame.draw.rect(surf, (250,250,250), self.rect, border_radius=6)
            pygame.draw.rect(surf, self.color, self.rect, 2, border_radius=6)
            if self.text:
                surf.blit(self.txt_surf, (self.rect.x+10, self.rect.y+8))
            else:
                surf.blit(self.placeholder_surf, (self.rect.x+10, self.rect.y+8))

        def get_value(self, default):
            """Devuelve el texto actual o un valor por defecto si está vacío.

            Args:
                default (str): Texto a usar si no se ingresó nada.

            Returns:
                str: Contenido ingresado o `default` si no hay texto.
            """
            return self.text.strip() or default

    def pedir_nombres(self):
        """Muestra un panel modal para ingresar nombres de X y O.

        Usa dos `InputBox` con TAB para cambiar foco y ENTER para confirmar.

        Returns:
            tuple[str, str]: `(nombre_x, nombre_o)` con valores por defecto
            si el usuario confirma sin escribir nada.
        """
        clock = pygame.time.Clock()
        running = True
        panel = pygame.Rect(self.ANCHO//2-320, self.ALTO//2-140, 640, 280)
        box_x = self.InputBox(
            pygame.Rect(panel.x+40, panel.y+90, 560, 40),
            self.FUENTE_UI, (200,200,200), self.CELESTE,
            "Nombre del Jugador X (Negras)"
        )
        box_o = self.InputBox(
            pygame.Rect(panel.x+40, panel.y+170, 560, 40),
            self.FUENTE_UI, (200,200,200), self.CELESTE,
            "Nombre del Jugador O (Blancas)"
        )
        boxes = [box_x, box_o]; focus = 0
        boxes[focus].active = True; boxes[focus].color = boxes[focus].color_active

        while running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit(); raise SystemExit
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_TAB:
                        boxes[focus].active=False; boxes[focus].color=boxes[focus].color_idle
                        focus=(focus+1)%2; boxes[focus].active=True; boxes[focus].color=boxes[focus].color_active
                    elif e.key == pygame.K_RETURN:
                        running=False
                for b in boxes:
                    b.handle_event(e)

            self.VENTANA.fill(self.FONDO_EXTERIOR)
            pygame.draw.rect(self.VENTANA, (245,245,245), panel, border_radius=12)
            pygame.draw.rect(self.VENTANA, (210,210,210), panel,2,border_radius=12)
            titulo = self.FUENTE_TIT.render("Ingresá los nombres de los jugadores", True, (30,30,30))
            subt = self.FUENTE_UI.render("TAB cambia de campo · ENTER para comenzar", True, (60,60,60))
            self.VENTANA.blit(titulo, titulo.get_rect(center=(panel.centerx, panel.y+40)))
            self.VENTANA.blit(subt, subt.get_rect(center=(panel.centerx, panel.y+70)))
            for b in boxes:
                b.draw(self.VENTANA)
            pygame.display.flip(); clock.tick(60)

        return box_x.get_value("Jugador X"), box_o.get_value("Jugador O")

    # ─────────────────────────────────────────────────────────────────────────────
    # Dados, sorteo y reglas auxiliares de movimiento
    # ─────────────────────────────────────────────────────────────────────────────
    def sorteo_inicial(self, jx, jo):
        """Realiza un sorteo de inicio tirando un dado por jugador.

        En caso de empate, repite hasta desempatar. Muestra una pantalla
        rápida indicando quién comienza.

        Args:
            jx (str): Nombre del jugador X.
            jo (str): Nombre del jugador O.

        Returns:
            str: 'X' si empieza X, 'O' si empieza O.
        """
        while True:
            dx, do = random.randint(1,6), random.randint(1,6)
            if dx != do:
                break
        turno = "X" if dx > do else "O"
        self.dibujar_tablero(); self.dibujar_fichas(); self.dibujar_barra_comidas(); self.dibujar_nombres(jx, jo, turno)
        txt = self.FUENTE_TIT.render(f"🎲 Comienza {jx if turno=='X' else jo}", True, self.LIMA)
        self.VENTANA.blit(txt, txt.get_rect(center=(self.ANCHO//2, self.ALTO//2)))
        pygame.display.flip(); pygame.time.wait(1200)
        return turno

    def tirar_dados_y_preparar_movimientos(self):
        """Tira los dados y deja lista la lista de movimientos del turno."""
        d1, d2 = random.randint(1,6), random.randint(1,6)
        self.tirada_actual = (d1, d2)
        self.movimientos_restantes = [d1, d1, d1, d1] if d1 == d2 else [d1, d2]

    def distancia_segun_turno(self, turno, origen, destino):
        """Calcula la distancia de movimiento respetando dirección de cada color.

        Para 'X' la dirección válida es ascendente (destino > origen).
        Para 'O' la dirección válida es descendente (destino < origen).

        Args:
            turno (str): 'X' o 'O'.
            origen (int|None): Punto de origen.
            destino (int|None): Punto de destino.

        Returns:
            int|None: Distancia positiva si es válida; None si no lo es.
        """
        if origen is None or destino is None:
            return None
        if turno == "X":
            if destino <= origen:
                return None
            return destino - origen
        else:
            if destino >= origen:
                return None
            return origen - destino

    def consumir_movimiento(self, dist):
        """Intenta consumir un valor `dist` de la lista de movimientos.

        Args:
            dist (int): Distancia a consumir.

        Returns:
            bool: True si pudo consumirse; False en caso contrario.
        """
        if dist in self.movimientos_restantes:
            self.movimientos_restantes.remove(dist)
            return True
        return False

    # ─────────────────────────────────────────────────────────────────────────────
    # Bucle principal
    # ─────────────────────────────────────────────────────────────────────────────
    def main(self):
        """Ejecuta el bucle principal del juego.

        Maneja eventos (mouse/teclado), selección de origen/destino, intenta
        aplicar movimientos en el `Tablero`, y redibuja el frame a 60 FPS.
        """
        self.GEO = self.build_geo_full()

        jugador_x, jugador_o = self.pedir_nombres()
        turno = self.sorteo_inicial(jugador_x, jugador_o)
        self.tirar_dados_y_preparar_movimientos()

        seleccion = None
        reloj = pygame.time.Clock()
        corriendo = True

        while corriendo:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    corriendo = False

                elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    p = self.punto_desde_click(e.pos)
                    if p is None:
                        seleccion = None
                    elif seleccion is None:
                        fichas = self.tablero.tablero.get(p, [])
                        # origen válido: ficha propia o barra correspondiente
                        if (turno in fichas) or \
                           (p == 0 and turno == "X" and len(self.tablero.bar.get("X", [])) > 0) or \
                           (p == 25 and turno == "O" and len(self.tablero.bar.get("O", [])) > 0):
                            seleccion = p
                    else:
                        destino = p
                        dist = self.distancia_segun_turno(turno, seleccion, destino)
                        if dist and self.consumir_movimiento(dist):
                            if not self.tablero.mover_ficha(seleccion, destino):
                                # si el core rechaza, devolvemos el movimiento
                                self.movimientos_restantes.append(dist)
                                self.movimientos_restantes.sort()
                            elif not self.movimientos_restantes:
                                turno = "O" if turno == "X" else "X"
                                self.tirar_dados_y_preparar_movimientos()
                        seleccion = None

                elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 3:
                    seleccion = None

                elif e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                    # Pasar turno manualmente
                    self.movimientos_restantes.clear()
                    seleccion = None
                    turno = self.pasar_turno(turno)

            # Dibujo del frame
            self.dibujar_tablero()

            # Resaltado de selección
            if seleccion is not None:
                if seleccion in (0, 25):
                    self.dibujar_barra_seleccionada(seleccion)
                else:
                    self.dibujar_triangulo_seleccionado(seleccion)

            self.dibujar_fichas()
            self.dibujar_barra_comidas()
            self.dibujar_barra_salida()
            self.dibujar_nombres(jugador_x, jugador_o, turno)
            self.dibujar_hud()

            pygame.display.flip()
            reloj.tick(60)

        pygame.quit()


if __name__ == "__main__":
    PygameUI().main()
