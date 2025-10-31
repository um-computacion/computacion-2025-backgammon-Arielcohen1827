# prompt 1 ( quiero que me hagas el volver desde la barra)
    # board.py
 #pone esto en la funcion mover_ficha

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



# prompt 2 (hace el tablero en pygame)
    # pygame_ui/game_pygame.py
    import pygame
    from core.board import Tablero

    # --- Configuración inicial ---
    pygame.init()
    ANCHO, ALTO = 900, 600
    VENTANA = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Backgammon - Pygame")

    # 🎨 Colores (nueva paleta)
    MADERA_CLARA = (222, 206, 180)   # fondo del tablero
    ARENA        = (243, 228, 211)   # triángulo claro
    BORDO        = (128, 0, 32)      # triángulo oscuro (bordó)
    BARRA_GRIS   = (60, 60, 60)      # barra central
    CONTORNO     = (40, 30, 20)      # contorno suave de triángulos

    NEGRO = (0, 0, 0)
    BLANCO = (255, 255, 255)

    # --- Dimensiones del tablero ---
    MARGEN_X = 50
    MARGEN_Y = 50
    ANCHO_TRIANGULO = (ANCHO - 2 * MARGEN_X) // 12
    ALTO_TRIANGULO = 250

    # --- Inicializar tablero lógico ---
    tablero = Tablero()

    def dibujar_tablero():
        # Fondo
        VENTANA.fill((26, 36, 48))  # fondo exterior (azul grisáceo oscuro)
        # Rectángulo del tablero
        pygame.draw.rect(VENTANA, MADERA_CLARA, (MARGEN_X, MARGEN_Y, ANCHO - 2*MARGEN_X, ALTO - 2*MARGEN_Y), border_radius=10)

        # Triángulos superiores (13–24) - punta hacia abajo
        for i in range(12):
            x = MARGEN_X + i * ANCHO_TRIANGULO
            color = ARENA if i % 2 == 0 else BORDO
            puntos = [(x, MARGEN_Y),
                    (x + ANCHO_TRIANGULO, MARGEN_Y),
                    (x + ANCHO_TRIANGULO / 2, MARGEN_Y + ALTO_TRIANGULO)]
            pygame.draw.polygon(VENTANA, color, puntos)
            pygame.draw.polygon(VENTANA, CONTORNO, puntos, 1)

        # Triángulos inferiores (12–1) - punta hacia arriba
        for i in range(12):
            x = MARGEN_X + i * ANCHO_TRIANGULO
            color = ARENA if i % 2 == 0 else BORDO
            puntos = [(x, ALTO - MARGEN_Y),
                    (x + ANCHO_TRIANGULO, ALTO - MARGEN_Y),
                    (x + ANCHO_TRIANGULO / 2, ALTO - MARGEN_Y - ALTO_TRIANGULO)]
            pygame.draw.polygon(VENTANA, color, puntos)
            pygame.draw.polygon(VENTANA, CONTORNO, puntos, 1)

        # Barra central
        pygame.draw.rect(VENTANA, BARRA_GRIS, (ANCHO // 2 - 5, MARGEN_Y, 10, ALTO - 2 * MARGEN_Y), border_radius=3)

    def dibujar_fichas():
        radio = 15
        for punto, fichas in tablero.tablero.items():
            for idx, ficha in enumerate(fichas):
                if 1 <= punto <= 12:
                    x = MARGEN_X + (12 - punto) * ANCHO_TRIANGULO + ANCHO_TRIANGULO // 2
                    y = ALTO - MARGEN_Y - idx * 2 * radio - radio
                elif 13 <= punto <= 24:
                    x = MARGEN_X + (punto - 13) * ANCHO_TRIANGULO + ANCHO_TRIANGULO // 2
                    y = MARGEN_Y + idx * 2 * radio + radio
                else:
                    continue

                color = NEGRO if ficha == "X" else BLANCO
                pygame.draw.circle(VENTANA, color, (int(x), int(y)), radio)
                pygame.draw.circle(VENTANA, CONTORNO, (int(x), int(y)), radio, 1)

    # --- Bucle principal ---
    def main():
        corriendo = True
        reloj = pygame.time.Clock()

        while corriendo:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    corriendo = False

            dibujar_tablero()
            dibujar_fichas()
            pygame.display.flip()
            reloj.tick(60)

        pygame.quit()

    if __name__ == "__main__":
        main()

# prompt 3 (agregame que muestre y y pida los nombres de los jugadores)
    # pygame_ui/game_pygame.py
import pygame
from core.board import Tablero

#--- Configuración inicial ---
pygame.init()
ANCHO, ALTO = 900, 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Backgammon - Pygame")

#🎨 Colores
MADERA_CLARA = (222, 206, 180)
ARENA        = (243, 228, 211)
BORDO        = (128, 0, 32)
BARRA_GRIS   = (60, 60, 60)
CONTORNO     = (40, 30, 20)
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
FONDO_EXTERIOR = (26, 36, 48)
CELESTE = (90, 170, 255)

#--- Dimensiones del tablero ---
MARGEN_X = 50
MARGEN_Y = 50
ANCHO_TRIANGULO = (ANCHO - 2 * MARGEN_X) // 12
ALTO_TRIANGULO = 250

#--- Fuentes ---
pygame.font.init()
FUENTE = pygame.font.SysFont("arial", 22, bold=True)
FUENTE_UI = pygame.font.SysFont("arial", 24)
FUENTE_TIT = pygame.font.SysFont("arial", 28, bold=True)

#--- Inicializar tablero lógico ---
tablero = Tablero()

def dibujar_tablero():
    # Fondo exterior
    VENTANA.fill(FONDO_EXTERIOR)
    # Madera del tablero
    pygame.draw.rect(VENTANA, MADERA_CLARA, (MARGEN_X, MARGEN_Y, ANCHO - 2*MARGEN_X, ALTO - 2*MARGEN_Y), border_radius=10)

    # Triángulos superiores (13–24)
    for i in range(12):
        x = MARGEN_X + i * ANCHO_TRIANGULO
        color = ARENA if i % 2 == 0 else BORDO
        puntos = [(x, MARGEN_Y),
                  (x + ANCHO_TRIANGULO, MARGEN_Y),
                  (x + ANCHO_TRIANGULO / 2, MARGEN_Y + ALTO_TRIANGULO)]
        pygame.draw.polygon(VENTANA, color, puntos)
        pygame.draw.polygon(VENTANA, CONTORNO, puntos, 1)

    # Triángulos inferiores (12–1)
    for i in range(12):
        x = MARGEN_X + i * ANCHO_TRIANGULO
        color = ARENA if i % 2 == 0 else BORDO
        puntos = [(x, ALTO - MARGEN_Y),
                  (x + ANCHO_TRIANGULO, ALTO - MARGEN_Y),
                  (x + ANCHO_TRIANGULO / 2, ALTO - MARGEN_Y - ALTO_TRIANGULO)]
        pygame.draw.polygon(VENTANA, color, puntos)
        pygame.draw.polygon(VENTANA, CONTORNO, puntos, 1)

    # Barra central
    pygame.draw.rect(VENTANA, BARRA_GRIS, (ANCHO // 2 - 5, MARGEN_Y, 10, ALTO - 2 * MARGEN_Y), border_radius=3)

def dibujar_fichas():
    radio = 15
    for punto, fichas in tablero.tablero.items():
        for idx, ficha in enumerate(fichas):
            if 1 <= punto <= 12:
                x = MARGEN_X + (12 - punto) * ANCHO_TRIANGULO + ANCHO_TRIANGULO // 2
                y = ALTO - MARGEN_Y - idx * 2 * radio - radio
            elif 13 <= punto <= 24:
                x = MARGEN_X + (punto - 13) * ANCHO_TRIANGULO + ANCHO_TRIANGULO // 2
                y = MARGEN_Y + idx * 2 * radio + radio
            else:
                continue

            color = NEGRO if ficha == "X" else BLANCO
            pygame.draw.circle(VENTANA, color, (int(x), int(y)), radio)
            pygame.draw.circle(VENTANA, CONTORNO, (int(x), int(y)), radio, 1)

def dibujar_nombres(jugador_x, jugador_o):
    # Superior: Jugador O (blancas)
    texto_o = FUENTE.render(f"{jugador_o} (Blancas)", True, BLANCO)
    rect_o = texto_o.get_rect(center=(ANCHO // 2, MARGEN_Y // 2))
    VENTANA.blit(texto_o, rect_o)

    # Inferior: Jugador X (negras)
    texto_x = FUENTE.render(f"{jugador_x} (Negras)", True, BLANCO)
    rect_x = texto_x.get_rect(center=(ANCHO // 2, ALTO - MARGEN_Y // 2))
    VENTANA.blit(texto_x, rect_x)

#-------- Pantalla de entrada de nombres (en la ventana) --------
class InputBox:
    def __init__(self, x, y, w, h, placeholder=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_idle = (200, 200, 200)
        self.color_active = CELESTE
        self.color = self.color_idle
        self.text = ""
        self.txt_surf = FUENTE_UI.render("", True, (20, 20, 20))
        self.active = False
        self.placeholder = placeholder
        self.placeholder_surf = FUENTE_UI.render(placeholder, True, (130, 130, 130))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.active = self.rect.collidepoint(event.pos)
            self.color = self.color_active if self.active else self.color_idle

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                # No hacer nada aquí; el main decide cuando avanzar
                pass
            elif event.key == pygame.K_TAB:
                # El main maneja el cambio de foco, ignoramos aquí
                pass
            else:
                if len(self.text) < 24:
                    self.text += event.unicode
            self.txt_surf = FUENTE_UI.render(self.text, True, (20, 20, 20))

    def draw(self, surface):
        pygame.draw.rect(surface, (250, 250, 250), self.rect, border_radius=6)
        pygame.draw.rect(surface, self.color, self.rect, 2, border_radius=6)
        if self.text:
            surface.blit(self.txt_surf, (self.rect.x + 10, self.rect.y + 8))
        else:
            surface.blit(self.placeholder_surf, (self.rect.x + 10, self.rect.y + 8))

    def get_value(self, default_value):
        return self.text.strip() or default_value

def pedir_nombres_en_ventana():
    clock = pygame.time.Clock()
    running = True

    # Layout
    VENTANA.fill(FONDO_EXTERIOR)
    panel = pygame.Rect(ANCHO//2 - 320, ALTO//2 - 140, 640, 280)

    box_x = InputBox(panel.x + 40, panel.y + 90, 560, 40, "Nombre del Jugador X (Negras)")
    box_o = InputBox(panel.x + 40, panel.y + 170, 560, 40, "Nombre del Jugador O (Blancas)")
    boxes = [box_x, box_o]
    focus = 0
    boxes[focus].active = True
    boxes[focus].color = boxes[focus].color_active

    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_TAB:
                    # Cambia foco
                    boxes[focus].active = False
                    boxes[focus].color = boxes[focus].color_idle
                    focus = (focus + 1) % len(boxes)
                    boxes[focus].active = True
                    boxes[focus].color = boxes[focus].color_active
                elif ev.key == pygame.K_RETURN:
                    # Si ambas tienen algo (o se acepta default), salir
                    running = False

            # Pasar eventos a las cajas
            for b in boxes:
                b.handle_event(ev)

        # Dibujar panel
        VENTANA.fill(FONDO_EXTERIOR)
        pygame.draw.rect(VENTANA, (245, 245, 245), panel, border_radius=12)
        pygame.draw.rect(VENTANA, (210, 210, 210), panel, 2, border_radius=12)

        titulo = FUENTE_TIT.render("Ingresá los nombres de los jugadores", True, (30, 30, 30))
        subt = FUENTE_UI.render("TAB cambia de campo · ENTER para comenzar", True, (60, 60, 60))
        VENTANA.blit(titulo, titulo.get_rect(center=(panel.centerx, panel.y + 40)))
        VENTANA.blit(subt, subt.get_rect(center=(panel.centerx, panel.y + 70)))

        # Dibujar inputs
        for b in boxes:
            b.draw(VENTANA)

        pygame.display.flip()
        clock.tick(60)

    nombre_x = box_x.get_value("Jugador X")
    nombre_o = box_o.get_value("Jugador O")
    return nombre_x, nombre_o

#--- Bucle principal ---
def main():
    # 1) Pedimos nombres en la ventana
    jugador_x, jugador_o = pedir_nombres_en_ventana()

    # 2) Iniciar juego/visualización normal
    corriendo = True
    reloj = pygame.time.Clock()

    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

        dibujar_tablero()
        dibujar_fichas()
        dibujar_nombres(jugador_x, jugador_o)
        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()

# prompt 4 (ahora hace un sorteo para ver que jugador inicia)
    # pygame_ui/game_pygame.py
import pygame, random
from core.board import Tablero

#--- Configuración inicial ---
pygame.init()
ANCHO, ALTO = 900, 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Backgammon - Pygame")

#🎨 Colores
MADERA_CLARA = (222, 206, 180)
ARENA        = (243, 228, 211)
BORDO        = (128, 0, 32)
BARRA_GRIS   = (60, 60, 60)
CONTORNO     = (40, 30, 20)
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
FONDO_EXTERIOR = (26, 36, 48)
CELESTE = (90, 170, 255)

#--- Dimensiones ---
MARGEN_X = 50
MARGEN_Y = 50
ANCHO_TRIANGULO = (ANCHO - 2 * MARGEN_X) // 12
ALTO_TRIANGULO = 250

#--- Fuentes ---
pygame.font.init()
FUENTE = pygame.font.SysFont("arial", 22, bold=True)
FUENTE_UI = pygame.font.SysFont("arial", 24)
FUENTE_TIT = pygame.font.SysFont("arial", 28, bold=True)

#--- Tablero lógico ---
tablero = Tablero()


#------------------------------------------------------------
#DIBUJO DEL TABLERO Y FICHAS
#------------------------------------------------------------
def dibujar_tablero():
    VENTANA.fill(FONDO_EXTERIOR)
    pygame.draw.rect(VENTANA, MADERA_CLARA, (MARGEN_X, MARGEN_Y, ANCHO - 2*MARGEN_X, ALTO - 2*MARGEN_Y), border_radius=10)

    for i in range(12):
        x = MARGEN_X + i * ANCHO_TRIANGULO
        color = ARENA if i % 2 == 0 else BORDO
        # Triángulos arriba
        puntos_arriba = [(x, MARGEN_Y), (x + ANCHO_TRIANGULO, MARGEN_Y),
                         (x + ANCHO_TRIANGULO / 2, MARGEN_Y + ALTO_TRIANGULO)]
        pygame.draw.polygon(VENTANA, color, puntos_arriba)
        pygame.draw.polygon(VENTANA, CONTORNO, puntos_arriba, 1)
        # Triángulos abajo
        puntos_abajo = [(x, ALTO - MARGEN_Y), (x + ANCHO_TRIANGULO, ALTO - MARGEN_Y),
                        (x + ANCHO_TRIANGULO / 2, ALTO - MARGEN_Y - ALTO_TRIANGULO)]
        pygame.draw.polygon(VENTANA, color, puntos_abajo)
        pygame.draw.polygon(VENTANA, CONTORNO, puntos_abajo, 1)

    # Barra central
    pygame.draw.rect(VENTANA, BARRA_GRIS, (ANCHO // 2 - 5, MARGEN_Y, 10, ALTO - 2 * MARGEN_Y), border_radius=3)

def dibujar_fichas():
    radio = 15
    for punto, fichas in tablero.tablero.items():
        for idx, ficha in enumerate(fichas):
            if 1 <= punto <= 12:
                x = MARGEN_X + (12 - punto) * ANCHO_TRIANGULO + ANCHO_TRIANGULO // 2
                y = ALTO - MARGEN_Y - idx * 2 * radio - radio
            elif 13 <= punto <= 24:
                x = MARGEN_X + (punto - 13) * ANCHO_TRIANGULO + ANCHO_TRIANGULO // 2
                y = MARGEN_Y + idx * 2 * radio + radio
            else:
                continue
            color = NEGRO if ficha == "X" else BLANCO
            pygame.draw.circle(VENTANA, color, (int(x), int(y)), radio)
            pygame.draw.circle(VENTANA, CONTORNO, (int(x), int(y)), radio, 1)

def dibujar_nombres(jugador_x, jugador_o, turno_actual=None):
    color_o = CELESTE if turno_actual == "O" else BLANCO
    color_x = CELESTE if turno_actual == "X" else BLANCO
    texto_o = FUENTE.render(f"{jugador_o} (Blancas)", True, color_o)
    texto_x = FUENTE.render(f"{jugador_x} (Negras)", True, color_x)
    rect_o = texto_o.get_rect(center=(ANCHO // 2, MARGEN_Y // 2))
    rect_x = texto_x.get_rect(center=(ANCHO // 2, ALTO - MARGEN_Y // 2))
    VENTANA.blit(texto_o, rect_o)
    VENTANA.blit(texto_x, rect_x)


#------------------------------------------------------------
#INPUT BOXES PARA LOS NOMBRES
#-----------------------------------------------------------
class InputBox:
    def __init__(self, x, y, w, h, placeholder=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_idle = (200, 200, 200)
        self.color_active = CELESTE
        self.color = self.color_idle
        self.text = ""
        self.txt_surf = FUENTE_UI.render("", True, (20, 20, 20))
        self.active = False
        self.placeholder = placeholder
        self.placeholder_surf = FUENTE_UI.render(placeholder, True, (130, 130, 130))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.active = self.rect.collidepoint(event.pos)
            self.color = self.color_active if self.active else self.color_idle

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key in (pygame.K_RETURN, pygame.K_TAB):
                pass
            else:
                if len(self.text) < 24:
                    self.text += event.unicode
            self.txt_surf = FUENTE_UI.render(self.text, True, (20, 20, 20))

    def draw(self, surface):
        pygame.draw.rect(surface, (250, 250, 250), self.rect, border_radius=6)
        pygame.draw.rect(surface, self.color, self.rect, 2, border_radius=6)
        if self.text:
            surface.blit(self.txt_surf, (self.rect.x + 10, self.rect.y + 8))
        else:
            surface.blit(self.placeholder_surf, (self.rect.x + 10, self.rect.y + 8))

    def get_value(self, default_value):
        return self.text.strip() or default_value


def pedir_nombres_en_ventana():
    clock = pygame.time.Clock()
    running = True
    panel = pygame.Rect(ANCHO//2 - 320, ALTO//2 - 140, 640, 280)
    box_x = InputBox(panel.x + 40, panel.y + 90, 560, 40, "Nombre del Jugador X (Negras)")
    box_o = InputBox(panel.x + 40, panel.y + 170, 560, 40, "Nombre del Jugador O (Blancas)")
    boxes = [box_x, box_o]
    focus = 0
    boxes[focus].active = True
    boxes[focus].color = boxes[focus].color_active

    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); raise SystemExit
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_TAB:
                    boxes[focus].active = False
                    boxes[focus].color = boxes[focus].color_idle
                    focus = (focus + 1) % len(boxes)
                    boxes[focus].active = True
                    boxes[focus].color = boxes[focus].color_active
                elif ev.key == pygame.K_RETURN:
                    running = False
            for b in boxes: b.handle_event(ev)

        VENTANA.fill(FONDO_EXTERIOR)
        pygame.draw.rect(VENTANA, (245, 245, 245), panel, border_radius=12)
        pygame.draw.rect(VENTANA, (210, 210, 210), panel, 2, border_radius=12)
        titulo = FUENTE_TIT.render("Ingresá los nombres de los jugadores", True, (30, 30, 30))
        subt = FUENTE_UI.render("TAB cambia de campo · ENTER para comenzar", True, (60, 60, 60))
        VENTANA.blit(titulo, titulo.get_rect(center=(panel.centerx, panel.y + 40)))
        VENTANA.blit(subt, subt.get_rect(center=(panel.centerx, panel.y + 70)))
        for b in boxes: b.draw(VENTANA)
        pygame.display.flip(); clock.tick(60)

    return box_x.get_value("Jugador X"), box_o.get_value("Jugador O")


#------------------------------------------------------------
#SORTEO AUTOMÁTICO (muestra quién empieza)
#------------------------------------------------------------
def sorteo_inicial(jugador_x, jugador_o):
    while True:
        dx = random.randint(1, 6)
        do = random.randint(1, 6)
        if dx != do:
            break

    turno = "X" if dx > do else "O"

    # Mostrar ganador por un instante sobre el tablero
    dibujar_tablero()
    dibujar_fichas()
    dibujar_nombres(jugador_x, jugador_o, turno_actual=turno)
    ganador = jugador_x if turno == "X" else jugador_o
    texto = FUENTE_TIT.render(f"Comienza {ganador}", True, BLANCO)
    VENTANA.blit(texto, texto.get_rect(center=(ANCHO // 2, ALTO // 2)))
    pygame.display.flip()
    pygame.time.wait(1500)

    return turno


#------------------------------------------------------------
#MAIN LOOP
#------------------------------------------------------------
def main():
    jugador_x, jugador_o = pedir_nombres_en_ventana()
    turno_actual = sorteo_inicial(jugador_x, jugador_o)

    corriendo = True
    reloj = pygame.time.Clock()
    while corriendo:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                corriendo = False

        dibujar_tablero()
        dibujar_fichas()
        dibujar_nombres(jugador_x, jugador_o, turno_actual)
        pygame.display.flip()
        reloj.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()

# prompt 5 ( cambia el color del ganador del sorteo)
    # pygame_ui/game_pygame.py

import pygame, random
from core.board import Tablero

#--- Configuración inicial ---
pygame.init()
ANCHO, ALTO = 900, 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Backgammon - Pygame")

#🎨 Colores
MADERA_CLARA = (222, 206, 180)
ARENA        = (243, 228, 211)
BORDO        = (128, 0, 32)
BARRA_GRIS   = (60, 60, 60)
CONTORNO     = (40, 30, 20)
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
FONDO_EXTERIOR = (26, 36, 48)
CELESTE = (90, 170, 255)
LIMA = (150, 255, 150)  # 💚 nuevo color para resaltar al ganador

#--- Dimensiones ---
MARGEN_X = 50
MARGEN_Y = 50
ANCHO_TRIANGULO = (ANCHO - 2 * MARGEN_X) // 12
ALTO_TRIANGULO = 250

#--- Fuentes ---
pygame.font.init()
FUENTE = pygame.font.SysFont("arial", 22, bold=True)
FUENTE_UI = pygame.font.SysFont("arial", 24)
FUENTE_TIT = pygame.font.SysFont("arial", 28, bold=True)

#--- Tablero lógico ---
tablero = Tablero()


#------------------------------------------------------------
#DIBUJO DEL TABLERO Y FICHAS
#------------------------------------------------------------
def dibujar_tablero():
    VENTANA.fill(FONDO_EXTERIOR)
    pygame.draw.rect(VENTANA, MADERA_CLARA, (MARGEN_X, MARGEN_Y, ANCHO - 2*MARGEN_X, ALTO - 2*MARGEN_Y), border_radius=10)

    for i in range(12):
        x = MARGEN_X + i * ANCHO_TRIANGULO
        color = ARENA if i % 2 == 0 else BORDO
        # Triángulos arriba
        puntos_arriba = [(x, MARGEN_Y), (x + ANCHO_TRIANGULO, MARGEN_Y),
                         (x + ANCHO_TRIANGULO / 2, MARGEN_Y + ALTO_TRIANGULO)]
        pygame.draw.polygon(VENTANA, color, puntos_arriba)
        pygame.draw.polygon(VENTANA, CONTORNO, puntos_arriba, 1)
        # Triángulos abajo
        puntos_abajo = [(x, ALTO - MARGEN_Y), (x + ANCHO_TRIANGULO, ALTO - MARGEN_Y),
                        (x + ANCHO_TRIANGULO / 2, ALTO - MARGEN_Y - ALTO_TRIANGULO)]
        pygame.draw.polygon(VENTANA, color, puntos_abajo)
        pygame.draw.polygon(VENTANA, CONTORNO, puntos_abajo, 1)

    # Barra central
    pygame.draw.rect(VENTANA, BARRA_GRIS, (ANCHO // 2 - 5, MARGEN_Y, 10, ALTO - 2 * MARGEN_Y), border_radius=3)

def dibujar_fichas():
    radio = 15
    for punto, fichas in tablero.tablero.items():
        for idx, ficha in enumerate(fichas):
            if 1 <= punto <= 12:
                x = MARGEN_X + (12 - punto) * ANCHO_TRIANGULO + ANCHO_TRIANGULO // 2
                y = ALTO - MARGEN_Y - idx * 2 * radio - radio
            elif 13 <= punto <= 24:
                x = MARGEN_X + (punto - 13) * ANCHO_TRIANGULO + ANCHO_TRIANGULO // 2
                y = MARGEN_Y + idx * 2 * radio + radio
            else:
                continue
            color = NEGRO if ficha == "X" else BLANCO
            pygame.draw.circle(VENTANA, color, (int(x), int(y)), radio)
            pygame.draw.circle(VENTANA, CONTORNO, (int(x), int(y)), radio, 1)

def dibujar_nombres(jugador_x, jugador_o, turno_actual=None):
    color_o = CELESTE if turno_actual == "O" else BLANCO
    color_x = CELESTE if turno_actual == "X" else BLANCO
    texto_o = FUENTE.render(f"{jugador_o} (Blancas)", True, color_o)
    texto_x = FUENTE.render(f"{jugador_x} (Negras)", True, color_x)
    rect_o = texto_o.get_rect(center=(ANCHO // 2, MARGEN_Y // 2))
    rect_x = texto_x.get_rect(center=(ANCHO // 2, ALTO - MARGEN_Y // 2))
    VENTANA.blit(texto_o, rect_o)
    VENTANA.blit(texto_x, rect_x)


#------------------------------------------------------------
#INPUT BOXES PARA LOS NOMBRES
#------------------------------------------------------------
class InputBox:
    def __init__(self, x, y, w, h, placeholder=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_idle = (200, 200, 200)
        self.color_active = CELESTE
        self.color = self.color_idle
        self.text = ""
        self.txt_surf = FUENTE_UI.render("", True, (20, 20, 20))
        self.active = False
        self.placeholder = placeholder
        self.placeholder_surf = FUENTE_UI.render(placeholder, True, (130, 130, 130))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.active = self.rect.collidepoint(event.pos)
            self.color = self.color_active if self.active else self.color_idle

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key in (pygame.K_RETURN, pygame.K_TAB):
                pass
            else:
                if len(self.text) < 24:
                    self.text += event.unicode
            self.txt_surf = FUENTE_UI.render(self.text, True, (20, 20, 20))

    def draw(self, surface):
        pygame.draw.rect(surface, (250, 250, 250), self.rect, border_radius=6)
        pygame.draw.rect(surface, self.color, self.rect, 2, border_radius=6)
        if self.text:
            surface.blit(self.txt_surf, (self.rect.x + 10, self.rect.y + 8))
        else:
            surface.blit(self.placeholder_surf, (self.rect.x + 10, self.rect.y + 8))

    def get_value(self, default_value):
        return self.text.strip() or default_value


def pedir_nombres_en_ventana():
    clock = pygame.time.Clock()
    running = True
    panel = pygame.Rect(ANCHO//2 - 320, ALTO//2 - 140, 640, 280)
    box_x = InputBox(panel.x + 40, panel.y + 90, 560, 40, "Nombre del Jugador X (Negras)")
    box_o = InputBox(panel.x + 40, panel.y + 170, 560, 40, "Nombre del Jugador O (Blancas)")
    boxes = [box_x, box_o]
    focus = 0
    boxes[focus].active = True
    boxes[focus].color = boxes[focus].color_active

    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); raise SystemExit
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_TAB:
                    boxes[focus].active = False
                    boxes[focus].color = boxes[focus].color_idle
                    focus = (focus + 1) % len(boxes)
                    boxes[focus].active = True
                    boxes[focus].color = boxes[focus].color_active
                elif ev.key == pygame.K_RETURN:
                    running = False
            for b in boxes: b.handle_event(ev)

        VENTANA.fill(FONDO_EXTERIOR)
        pygame.draw.rect(VENTANA, (245, 245, 245), panel, border_radius=12)
        pygame.draw.rect(VENTANA, (210, 210, 210), panel, 2, border_radius=12)
        titulo = FUENTE_TIT.render("Ingresá los nombres de los jugadores", True, (30, 30, 30))
        subt = FUENTE_UI.render("TAB cambia de campo · ENTER para comenzar", True, (60, 60, 60))
        VENTANA.blit(titulo, titulo.get_rect(center=(panel.centerx, panel.y + 40)))
        VENTANA.blit(subt, subt.get_rect(center=(panel.centerx, panel.y + 70)))
        for b in boxes: b.draw(VENTANA)
        pygame.display.flip(); clock.tick(60)

    return box_x.get_value("Jugador X"), box_o.get_value("Jugador O")


#------------------------------------------------------------
#SORTEO AUTOMÁTICO (con mensaje colorido)
#-----------------------------------------------------------
def sorteo_inicial(jugador_x, jugador_o):
    while True:
        dx = random.randint(1, 6)
        do = random.randint(1, 6)
        if dx != do:
            break

    turno = "X" if dx > do else "O"

    # Mostrar el tablero con mensaje de inicio en color verde lima
    dibujar_tablero()
    dibujar_fichas()
    dibujar_nombres(jugador_x, jugador_o, turno_actual=turno)
    ganador = jugador_x if turno == "X" else jugador_o
    texto = FUENTE_TIT.render(f"🎲 Comienza {ganador}", True, LIMA)
    rect = texto.get_rect(center=(ANCHO // 2, ALTO // 2))
    VENTANA.blit(texto, rect)
    pygame.display.flip()
    pygame.time.wait(1500)  # espera 1.5 segundos

    return turno


#------------------------------------------------------------
#MAIN LOOP
#------------------------------------------------------------
def main():
    jugador_x, jugador_o = pedir_nombres_en_ventana()
    turno_actual = sorteo_inicial(jugador_x, jugador_o)

    corriendo = True
    reloj = pygame.time.Clock()
    while corriendo:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                corriendo = False

        dibujar_tablero()
        dibujar_fichas()
        dibujar_nombres(jugador_x, jugador_o, turno_actual)
        pygame.display.flip()
        reloj.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()

# prompt 6 (agregame ejecuccion de movimientos)
    # pygame_ui/game_pygame.py
import pygame, random
from core.board import Tablero

#--- Configuración inicial ---
pygame.init()
ANCHO, ALTO = 900, 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Backgammon - Pygame")

#🎨 Colores
MADERA_CLARA = (222, 206, 180)
ARENA        = (243, 228, 211)
BORDO        = (128, 0, 32)
BARRA_GRIS   = (60, 60, 60)
CONTORNO     = (40, 30, 20)
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
FONDO_EXTERIOR = (26, 36, 48)
CELESTE = (90, 170, 255)
LIMA = (150, 255, 150)
HIGHLIGHT = (80, 180, 250)

#--- Dimensiones ---
MARGEN_X = 50
MARGEN_Y = 50
ANCHO_TRIANGULO = (ANCHO - 2 * MARGEN_X) // 12
ALTO_TRIANGULO = 250
BARRA_W = 10

#--- Fuentes ---
pygame.font.init()
FUENTE = pygame.font.SysFont("arial", 22, bold=True)
FUENTE_UI = pygame.font.SysFont("arial", 24)
FUENTE_TIT = pygame.font.SysFont("arial", 28, bold=True)
FUENTE_MINI = pygame.font.SysFont("arial", 16)

#--- Tablero lógico ---
tablero = Tablero()

#------------------------------------------------------------
#DIBUJO DEL TABLERO, FICHAS, NOMBRES
#-----------------------------------------------------------
def dibujar_tablero():
    VENTANA.fill(FONDO_EXTERIOR)
    pygame.draw.rect(VENTANA, MADERA_CLARA, (MARGEN_X, MARGEN_Y, ANCHO - 2*MARGEN_X, ALTO - 2*MARGEN_Y), border_radius=10)

    for i in range(12):
        x = MARGEN_X + i * ANCHO_TRIANGULO
        color = ARENA if i % 2 == 0 else BORDO
        # Triángulos arriba (13..24)
        puntos_arriba = [(x, MARGEN_Y), (x + ANCHO_TRIANGULO, MARGEN_Y),
                         (x + ANCHO_TRIANGULO / 2, MARGEN_Y + ALTO_TRIANGULO)]
        pygame.draw.polygon(VENTANA, color, puntos_arriba)
        pygame.draw.polygon(VENTANA, CONTORNO, puntos_arriba, 1)
        # Triángulos abajo (12..1)
        puntos_abajo = [(x, ALTO - MARGEN_Y), (x + ANCHO_TRIANGULO, ALTO - MARGEN_Y),
                        (x + ANCHO_TRIANGULO / 2, ALTO - MARGEN_Y - ALTO_TRIANGULO)]
        pygame.draw.polygon(VENTANA, color, puntos_abajo)
        pygame.draw.polygon(VENTANA, CONTORNO, puntos_abajo, 1)

    # Barra central
    pygame.draw.rect(VENTANA, BARRA_GRIS, (ANCHO // 2 - BARRA_W//2, MARGEN_Y, BARRA_W, ALTO - 2 * MARGEN_Y), border_radius=3)

def dibujar_fichas():
    radio = 15
    for punto, fichas in tablero.tablero.items():
        for idx, ficha in enumerate(fichas):
            if 1 <= punto <= 12:
                x = MARGEN_X + (12 - punto) * ANCHO_TRIANGULO + ANCHO_TRIANGULO // 2
                y = ALTO - MARGEN_Y - idx * 2 * radio - radio
            elif 13 <= punto <= 24:
                x = MARGEN_X + (punto - 13) * ANCHO_TRIANGULO + ANCHO_TRIANGULO // 2
                y = MARGEN_Y + idx * 2 * radio + radio
            else:
                continue
            color = NEGRO if ficha == "X" else BLANCO
            pygame.draw.circle(VENTANA, color, (int(x), int(y)), radio)
            pygame.draw.circle(VENTANA, CONTORNO, (int(x), int(y)), radio, 1)

def dibujar_nombres(jugador_x, jugador_o, turno_actual=None):
    color_o = CELESTE if turno_actual == "O" else BLANCO
    color_x = CELESTE if turno_actual == "X" else BLANCO
    texto_o = FUENTE.render(f"{jugador_o} (Blancas)", True, color_o)
    texto_x = FUENTE.render(f"{jugador_x} (Negras)", True, color_x)
    rect_o = texto_o.get_rect(center=(ANCHO // 2, MARGEN_Y // 2))
    rect_x = texto_x.get_rect(center=(ANCHO // 2, ALTO - MARGEN_Y // 2))
    VENTANA.blit(texto_o, rect_o)
    VENTANA.blit(texto_x, rect_x)

def dibujar_bar_info():
    # Muestra cantidades en barra (si tu Tablero expone bar["X"]/["O"])
    try:
        o_bar = len(tablero.bar["O"])
        x_bar = len(tablero.bar["X"])
        txt_o = FUENTE_MINI.render(f"BAR O: {o_bar}", True, BLANCO)
        txt_x = FUENTE_MINI.render(f"BAR X: {x_bar}", True, BLANCO)
        VENTANA.blit(txt_o, (MARGEN_X + 8, ALTO//2 - 12))
        VENTANA.blit(txt_x, (ANCHO - MARGEN_X - 100, ALTO//2 - 12))
    except Exception:
        pass

#------------------------------------------------------------
#MAPEO DE CLIC A PUNTO (1..24) Y BARRA (0 / 25)
#------------------------------------------------------------
def punto_desde_click(pos):
    x, y = pos
    # Dentro del rectángulo del tablero
    if not (MARGEN_X <= x <= ANCHO - MARGEN_X and MARGEN_Y <= y <= ALTO - MARGEN_Y):
        return None

    # ¿click en barra central?
    barra_rect = pygame.Rect(ANCHO // 2 - BARRA_W//2, MARGEN_Y, BARRA_W, ALTO - 2*MARGEN_Y)
    if barra_rect.collidepoint(x, y):
        # Arriba → 25 (O reingresa), Abajo → 0 (X reingresa)
        if y < ALTO // 2:
            return 25
        else:
            return 0

    # Parte superior (13..24)
    if MARGEN_Y <= y <= MARGEN_Y + ALTO_TRIANGULO:
        i = int((x - MARGEN_X) // ANCHO_TRIANGULO)
        if 0 <= i <= 11:
            return 13 + i

    # Parte inferior (12..1)
    if ALTO - MARGEN_Y - ALTO_TRIANGULO <= y <= ALTO - MARGEN_Y:
        i = int((x - MARGEN_X) // ANCHO_TRIANGULO)
        if 0 <= i <= 11:
            return 12 - i

    return None

def centro_punto(p):
    # Para dibujar highlight del origen seleccionado
    if 13 <= p <= 24:
        idx = p - 13
        cx = MARGEN_X + idx * ANCHO_TRIANGULO + ANCHO_TRIANGULO // 2
        cy = MARGEN_Y + ALTO_TRIANGULO - 18
    elif 1 <= p <= 12:
        idx = 12 - p
        cx = MARGEN_X + idx * ANCHO_TRIANGULO + ANCHO_TRIANGULO // 2
        cy = ALTO - MARGEN_Y - ALTO_TRIANGULO + 18
    elif p == 25:  # barra arriba
        cx = ANCHO // 2
        cy = MARGEN_Y + 20
    elif p == 0:   # barra abajo
        cx = ANCHO // 2
        cy = ALTO - MARGEN_Y - 20
    else:
        cx, cy = ANCHO//2, ALTO//2
    return int(cx), int(cy)

#------------------------------------------------------------
#ENTRADA DE NOMBRES (UI)
#------------------------------------------------------------
class InputBox:
    def __init__(self, x, y, w, h, placeholder=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_idle = (200, 200, 200)
        self.color_active = CELESTE
        self.color = self.color_idle
        self.text = ""
        self.txt_surf = FUENTE_UI.render("", True, (20, 20, 20))
        self.active = False
        self.placeholder = placeholder
        self.placeholder_surf = FUENTE_UI.render(placeholder, True, (130, 130, 130))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.active = self.rect.collidepoint(event.pos)
            self.color = self.color_active if self.active else self.color_idle
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key in (pygame.K_RETURN, pygame.K_TAB):
                pass
            else:
                if len(self.text) < 24:
                    self.text += event.unicode
            self.txt_surf = FUENTE_UI.render(self.text, True, (20, 20, 20))

    def draw(self, surface):
        pygame.draw.rect(surface, (250, 250, 250), self.rect, border_radius=6)
        pygame.draw.rect(surface, self.color, self.rect, 2, border_radius=6)
        if self.text:
            surface.blit(self.txt_surf, (self.rect.x + 10, self.rect.y + 8))
        else:
            surface.blit(self.placeholder_surf, (self.rect.x + 10, self.rect.y + 8))

    def get_value(self, default_value):
        return self.text.strip() or default_value

def pedir_nombres_en_ventana():
    clock = pygame.time.Clock()
    running = True
    panel = pygame.Rect(ANCHO//2 - 320, ALTO//2 - 140, 640, 280)
    box_x = InputBox(panel.x + 40, panel.y + 90, 560, 40, "Nombre del Jugador X (Negras)")
    box_o = InputBox(panel.x + 40, panel.y + 170, 560, 40, "Nombre del Jugador O (Blancas)")
    boxes = [box_x, box_o]
    focus = 0
    boxes[focus].active = True
    boxes[focus].color = boxes[focus].color_active

    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); raise SystemExit
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_TAB:
                    boxes[focus].active = False
                    boxes[focus].color = boxes[focus].color_idle
                    focus = (focus + 1) % len(boxes)
                    boxes[focus].active = True
                    boxes[focus].color = boxes[focus].color_active
                elif ev.key == pygame.K_RETURN:
                    running = False
            for b in boxes: b.handle_event(ev)

        VENTANA.fill(FONDO_EXTERIOR)
        pygame.draw.rect(VENTANA, (245, 245, 245), panel, border_radius=12)
        pygame.draw.rect(VENTANA, (210, 210, 210), panel, 2, border_radius=12)
        titulo = FUENTE_TIT.render("Ingresá los nombres de los jugadores", True, (30, 30, 30))
        subt = FUENTE_UI.render("TAB cambia de campo · ENTER para comenzar", True, (60, 60, 60))
        VENTANA.blit(titulo, titulo.get_rect(center=(panel.centerx, panel.y + 40)))
        VENTANA.blit(subt, subt.get_rect(center=(panel.centerx, panel.y + 70)))
        for b in boxes: b.draw(VENTANA)
        pygame.display.flip(); clock.tick(60)

    return box_x.get_value("Jugador X"), box_o.get_value("Jugador O")

#------------------------------------------------------------
#SORTEO AUTOMÁTICO
#------------------------------------------------------------
def sorteo_inicial(jugador_x, jugador_o):
    while True:
        dx = random.randint(1, 6)
        do = random.randint(1, 6)
        if dx != do:
            break
    turno = "X" if dx > do else "O"
    dibujar_tablero(); dibujar_fichas(); dibujar_nombres(jugador_x, jugador_o, turno_actual=turno)
    ganador = jugador_x if turno == "X" else jugador_o
    texto = FUENTE_TIT.render(f"🎲 Comienza {ganador}", True, LIMA)
    VENTANA.blit(texto, texto.get_rect(center=(ANCHO // 2, ALTO // 2)))
    pygame.display.flip()
    pygame.time.wait(1200)
    return turno

#------------------------------------------------------------
#MAIN LOOP (turnos + movimientos con mouse, sin dados)
#------------------------------------------------------------
def main():
    jugador_x, jugador_o = pedir_nombres_en_ventana()
    turno_actual = sorteo_inicial(jugador_x, jugador_o)

    seleccion_origen = None  # punto int (1..24, 0, 25) o None
    reloj = pygame.time.Clock()
    corriendo = True

    while corriendo:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                corriendo = False

            elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                p = punto_desde_click(ev.pos)
                if p is None:
                    seleccion_origen = None
                else:
                    if seleccion_origen is None:
                        # Selección de ORIGEN: debe tener ficha del jugador en turno
                        fichas = tablero.tablero.get(p, [])
                        if turno_actual in fichas:
                            seleccion_origen = p
                        else:
                            # También permitir origen en barra si corresponde
                            if p in (0, 25):
                                try:
                                    if (p == 0 and len(tablero.bar["X"]) > 0 and turno_actual == "X") or \
                                       (p == 25 and len(tablero.bar["O"]) > 0 and turno_actual == "O"):
                                        seleccion_origen = p
                                except Exception:
                                    pass
                    else:
                        destino = p
                        # Intentar movimiento con la lógica del Tablero
                        exito = tablero.mover_ficha(seleccion_origen, destino)
                        if exito:
                            # Cambiar turno
                            turno_actual = "O" if turno_actual == "X" else "X"
                        # Limpiar selección en cualquier caso
                        seleccion_origen = None

            elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 3:
                # Click derecho: cancelar selección
                seleccion_origen = None

        # DIBUJO
        dibujar_tablero()
        dibujar_fichas()
        dibujar_nombres(jugador_x, jugador_o, turno_actual)
        dibujar_bar_info()

        # Resaltar origen seleccionado
        if seleccion_origen is not None:
            cx, cy = centro_punto(seleccion_origen)
            pygame.draw.circle(VENTANA, HIGHLIGHT, (cx, cy), 20, 3)

        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
# prompt 7 (ahora quiero que en cada turno tires los dados y limites los movimientos con respecto a los dados (siguiendo con lo si toca doble que hay 4 movimientos))
    # pygame_ui/game_pygame.py
import pygame, random
from core.board import Tablero

#--- Configuración inicial ---
pygame.init()
ANCHO, ALTO = 900, 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Backgammon - Pygame")

#🎨 Colores
MADERA_CLARA = (222, 206, 180)
ARENA        = (243, 228, 211)
BORDO        = (128, 0, 32)
BARRA_GRIS   = (60, 60, 60)
CONTORNO     = (40, 30, 20)
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
FONDO_EXTERIOR = (26, 36, 48)
CELESTE = (90, 170, 255)
LIMA = (150, 255, 150)
HIGHLIGHT = (80, 180, 250)
ROJO = (220, 80, 80)

#--- Dimensiones ---
MARGEN_X = 50
MARGEN_Y = 50
ANCHO_TRIANGULO = (ANCHO - 2 * MARGEN_X) // 12
ALTO_TRIANGULO = 250
BARRA_W = 10

#--- Fuentes ---
pygame.font.init()
FUENTE = pygame.font.SysFont("arial", 22, bold=True)
FUENTE_UI = pygame.font.SysFont("arial", 24)
FUENTE_TIT = pygame.font.SysFont("arial", 28, bold=True)
FUENTE_MINI = pygame.font.SysFont("arial", 16)

#--- Tablero lógico ---
tablero = Tablero()

#-- Estado de juego (dados / movimientos restantes) ---
tirada_actual = (0, 0)  # (d1, d2) solo para mostrar
movimientos_restantes = []  # lista de distancias por consumir (p.ej. [3,5] o [4,4,4,4])

#------------------------------------------------------------
#DIBUJO DEL TABLERO, FICHAS, NOMBRES, HUD
#------------------------------------------------------------
def dibujar_tablero():
    VENTANA.fill(FONDO_EXTERIOR)
    pygame.draw.rect(VENTANA, MADERA_CLARA, (MARGEN_X, MARGEN_Y, ANCHO - 2*MARGEN_X, ALTO - 2*MARGEN_Y), border_radius=10)

    for i in range(12):
        x = MARGEN_X + i * ANCHO_TRIANGULO
        color = ARENA if i % 2 == 0 else BORDO
        # Triángulos arriba (13..24)
        puntos_arriba = [(x, MARGEN_Y), (x + ANCHO_TRIANGULO, MARGEN_Y),
                         (x + ANCHO_TRIANGULO / 2, MARGEN_Y + ALTO_TRIANGULO)]
        pygame.draw.polygon(VENTANA, color, puntos_arriba)
        pygame.draw.polygon(VENTANA, CONTORNO, puntos_arriba, 1)
        # Triángulos abajo (12..1)
        puntos_abajo = [(x, ALTO - MARGEN_Y), (x + ANCHO_TRIANGULO, ALTO - MARGEN_Y),
                        (x + ANCHO_TRIANGULO / 2, ALTO - MARGEN_Y - ALTO_TRIANGULO)]
        pygame.draw.polygon(VENTANA, color, puntos_abajo)
        pygame.draw.polygon(VENTANA, CONTORNO, puntos_abajo, 1)

    # Barra central
    pygame.draw.rect(VENTANA, BARRA_GRIS, (ANCHO // 2 - BARRA_W//2, MARGEN_Y, BARRA_W, ALTO - 2 * MARGEN_Y), border_radius=3)

def dibujar_fichas():
    radio = 15
    for punto, fichas in tablero.tablero.items():
        for idx, ficha in enumerate(fichas):
            if 1 <= punto <= 12:
                x = MARGEN_X + (12 - punto) * ANCHO_TRIANGULO + ANCHO_TRIANGULO // 2
                y = ALTO - MARGEN_Y - idx * 2 * radio - radio
            elif 13 <= punto <= 24:
                x = MARGEN_X + (punto - 13) * ANCHO_TRIANGULO + ANCHO_TRIANGULO // 2
                y = MARGEN_Y + idx * 2 * radio + radio
            else:
                continue
            color = NEGRO if ficha == "X" else BLANCO
            pygame.draw.circle(VENTANA, color, (int(x), int(y)), radio)
            pygame.draw.circle(VENTANA, CONTORNO, (int(x), int(y)), radio, 1)

def dibujar_nombres(jugador_x, jugador_o, turno_actual=None):
    color_o = CELESTE if turno_actual == "O" else BLANCO
    color_x = CELESTE if turno_actual == "X" else BLANCO
    texto_o = FUENTE.render(f"{jugador_o} (Blancas)", True, color_o)
    texto_x = FUENTE.render(f"{jugador_x} (Negras)", True, color_x)
    rect_o = texto_o.get_rect(center=(ANCHO // 2, MARGEN_Y // 2))
    rect_x = texto_x.get_rect(center=(ANCHO // 2, ALTO - MARGEN_Y // 2))
    VENTANA.blit(texto_o, rect_o)
    VENTANA.blit(texto_x, rect_x)

def dibujar_bar_info():
    try:
        o_bar = len(tablero.bar["O"])
        x_bar = len(tablero.bar["X"])
        txt_o = FUENTE_MINI.render(f"BAR O: {o_bar}", True, BLANCO)
        txt_x = FUENTE_MINI.render(f"BAR X: {x_bar}", True, BLANCO)
        VENTANA.blit(txt_o, (MARGEN_X + 8, ALTO//2 - 12))
        VENTANA.blit(txt_x, (ANCHO - MARGEN_X - 100, ALTO//2 - 12))
    except Exception:
        pass

def dibujar_hud(jugador_x, jugador_o, turno_actual):
    # Tirada y movimientos restantes
    d1, d2 = tirada_actual
    dados_txt = f"Tirada: {d1}-{d2}" if d1 and d2 else "Tirada: —"
    movs_txt = f"Movimientos: {movimientos_restantes if movimientos_restantes else '—'}"
    hud1 = FUENTE.render(dados_txt, True, BLANCO)
    hud2 = FUENTE.render(movs_txt, True, BLANCO)
    VENTANA.blit(hud1, (ANCHO//2 - 120, 8))
    VENTANA.blit(hud2, (ANCHO//2 + 40, 8))

#------------------------------------------------------------
#MAPEO DE CLIC A PUNTO (1..24) Y BARRA (0 / 25)
#------------------------------------------------------------
def punto_desde_click(pos):
    x, y = pos
    if not (MARGEN_X <= x <= ANCHO - MARGEN_X and MARGEN_Y <= y <= ALTO - MARGEN_Y):
        return None
    barra_rect = pygame.Rect(ANCHO // 2 - BARRA_W//2, MARGEN_Y, BARRA_W, ALTO - 2*MARGEN_Y)
    if barra_rect.collidepoint(x, y):
        return 25 if y < ALTO // 2 else 0
    if MARGEN_Y <= y <= MARGEN_Y + ALTO_TRIANGULO:  # arriba 13..24
        i = int((x - MARGEN_X) // ANCHO_TRIANGULO)
        if 0 <= i <= 11: return 13 + i
    if ALTO - MARGEN_Y - ALTO_TRIANGULO <= y <= ALTO - MARGEN_Y:  # abajo 12..1
        i = int((x - MARGEN_X) // ANCHO_TRIANGULO)
        if 0 <= i <= 11: return 12 - i
    return None

def centro_punto(p):
    if 13 <= p <= 24:
        idx = p - 13
        cx = MARGEN_X + idx * ANCHO_TRIANGULO + ANCHO_TRIANGULO // 2
        cy = MARGEN_Y + ALTO_TRIANGULO - 18
    elif 1 <= p <= 12:
        idx = 12 - p
        cx = MARGEN_X + idx * ANCHO_TRIANGULO + ANCHO_TRIANGULO // 2
        cy = ALTO - MARGEN_Y - ALTO_TRIANGULO + 18
    elif p == 25:
        cx, cy = ANCHO // 2, MARGEN_Y + 20
    elif p == 0:
        cx, cy = ANCHO // 2, ALTO - MARGEN_Y - 20
    else:
        cx, cy = ANCHO//2, ALTO//2
    return int(cx), int(cy)

#------------------------------------------------------------
#ENTRADA DE NOMBRES (UI)
#------------------------------------------------------------
class InputBox:
    def __init__(self, x, y, w, h, placeholder=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_idle = (200, 200, 200)
        self.color_active = CELESTE
        self.color = self.color_idle
        self.text = ""
        self.txt_surf = FUENTE_UI.render("", True, (20, 20, 20))
        self.active = False
        self.placeholder = placeholder
        self.placeholder_surf = FUENTE_UI.render(placeholder, True, (130, 130, 130))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.active = self.rect.collidepoint(event.pos)
            self.color = self.color_active if self.active else self.color_idle
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key in (pygame.K_RETURN, pygame.K_TAB):
                pass
            else:
                if len(self.text) < 24:
                    self.text += event.unicode
            self.txt_surf = FUENTE_UI.render(self.text, True, (20, 20, 20))

    def draw(self, surface):
        pygame.draw.rect(surface, (250, 250, 250), self.rect, border_radius=6)
        pygame.draw.rect(surface, self.color, self.rect, 2, border_radius=6)
        if self.text:
            surface.blit(self.txt_surf, (self.rect.x + 10, self.rect.y + 8))
        else:
            surface.blit(self.placeholder_surf, (self.rect.x + 10, self.rect.y + 8))

    def get_value(self, default_value):
        return self.text.strip() or default_value

def pedir_nombres_en_ventana():
    clock = pygame.time.Clock()
    running = True
    panel = pygame.Rect(ANCHO//2 - 320, ALTO//2 - 140, 640, 280)
    box_x = InputBox(panel.x + 40, panel.y + 90, 560, 40, "Nombre del Jugador X (Negras)")
    box_o = InputBox(panel.x + 40, panel.y + 170, 560, 40, "Nombre del Jugador O (Blancas)")
    boxes = [box_x, box_o]
    focus = 0
    boxes[focus].active = True
    boxes[focus].color = boxes[focus].color_active

    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); raise SystemExit
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_TAB:
                    boxes[focus].active = False
                    boxes[focus].color = boxes[focus].color_idle
                    focus = (focus + 1) % len(boxes)
                    boxes[focus].active = True
                    boxes[focus].color = boxes[focus].color_active
                elif ev.key == pygame.K_RETURN:
                    running = False
            for b in boxes: b.handle_event(ev)

        VENTANA.fill(FONDO_EXTERIOR)
        pygame.draw.rect(VENTANA, (245, 245, 245), panel, border_radius=12)
        pygame.draw.rect(VENTANA, (210, 210, 210), panel, 2, border_radius=12)
        titulo = FUENTE_TIT.render("Ingresá los nombres de los jugadores", True, (30, 30, 30))
        subt = FUENTE_UI.render("TAB cambia de campo · ENTER para comenzar", True, (60, 60, 60))
        VENTANA.blit(titulo, titulo.get_rect(center=(panel.centerx, panel.y + 40)))
        VENTANA.blit(subt, subt.get_rect(center=(panel.centerx, panel.y + 70)))
        for b in boxes: b.draw(VENTANA)
        pygame.display.flip(); clock.tick(60)

    return box_x.get_value("Jugador X"), box_o.get_value("Jugador O")

#------------------------------------------------------------
#SORTEO AUTOMÁTICO + DADOS POR TURNO
#-----------------------------------------------------------
def sorteo_inicial(jugador_x, jugador_o):
    while True:
        dx = random.randint(1, 6)
        do = random.randint(1, 6)
        if dx != do:
            break
    turno = "X" if dx > do else "O"

    dibujar_tablero(); dibujar_fichas(); dibujar_nombres(jugador_x, jugador_o, turno_actual=turno)
    ganador = jugador_x if turno == "X" else jugador_o
    texto = FUENTE_TIT.render(f"🎲 Comienza {ganador}", True, LIMA)
    VENTANA.blit(texto, texto.get_rect(center=(ANCHO // 2, ALTO // 2)))
    pygame.display.flip()
    pygame.time.wait(1200)
    return turno

def tirar_dados_y_preparar_movimientos():
    global tirada_actual, movimientos_restantes
    d1 = random.randint(1, 6)
    d2 = random.randint(1, 6)
    tirada_actual = (d1, d2)
    if d1 == d2:
        movimientos_restantes = [d1, d1, d1, d1]
    else:
        movimientos_restantes = [d1, d2]

#------------------------------------------------------------
#REGLAS BÁSICAS PARA DISTANCIA SEGÚN FICHA
#------------------------------------------------------------
def distancia_segun_turno(turno, origen, destino):
    """
    Devuelve la distancia positiva si el movimiento respeta la dirección,
    o None si la dirección es inválida.
    - X mueve en sentido ascendente (números crecientes).
    - O mueve en sentido descendente (números decrecientes).
    """
    if destino is None or origen is None:
        return None

    if turno == "X":
        if destino <= origen:
            return None
        return destino - origen
    else:  # turno == "O"
        if destino >= origen:
            return None
        return origen - destino

def consumir_movimiento(dist):
    """Intenta consumir un movimiento con distancia 'dist' exacta."""
    global movimientos_restantes
    if dist in movimientos_restantes:
        movimientos_restantes.remove(dist)
        return True
    return False

#------------------------------------------------------------
#MAIN LOOP (turnos + movimientos con mouse + dados)
#------------------------------------------------------------
def main():
    global movimientos_restantes
    jugador_x, jugador_o = pedir_nombres_en_ventana()
    turno_actual = sorteo_inicial(jugador_x, jugador_o)

    # Tirada inicial del primer turno
    tirar_dados_y_preparar_movimientos()

    seleccion_origen = None
    reloj = pygame.time.Clock()
    corriendo = True

    while corriendo:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                corriendo = False

            elif ev.type == pygame.KEYDOWN:
                # Opción: volver a tirar manualmente si ya no quedan movimientos (por seguridad)
                if ev.key == pygame.K_SPACE and not movimientos_restantes:
                    tirar_dados_y_preparar_movimientos()

            elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                p = punto_desde_click(ev.pos)
                if p is None:
                    seleccion_origen = None
                else:
                    if seleccion_origen is None:
                        # Selección de ORIGEN: debe tener ficha del jugador en turno, o ser barra correspondiente
                        fichas = tablero.tablero.get(p, [])
                        if turno_actual in fichas:
                            seleccion_origen = p
                        else:
                            # Origen desde barra si hay fichas en barra
                            try:
                                if (p == 0 and turno_actual == "X" and len(tablero.bar["X"]) > 0) or \
                                   (p == 25 and turno_actual == "O" and len(tablero.bar["O"]) > 0):
                                    seleccion_origen = p
                            except Exception:
                                pass
                    else:
                        destino = p

                        # Calcular distancia con regla de dirección (desde barra usa 0 para X o 25 para O ya mapeado)
                        dist = distancia_segun_turno(turno_actual, seleccion_origen, destino)

                        if dist is None:
                            # dirección inválida
                            seleccion_origen = None
                        else:
                            # Chequear si la distancia está en movimientos restantes
                            if consumir_movimiento(dist):
                                # Intentar mover en el tablero lógico
                                exito = tablero.mover_ficha(seleccion_origen, destino)
                                if not exito:
                                    # Revertir consumo si el movimiento fue inválido por reglas internas
                                    movimientos_restantes.append(dist)
                                    movimientos_restantes.sort()
                                else:
                                    # Si no quedan movimientos -> cambio de turno + tirar de nuevo
                                    if not movimientos_restantes:
                                        turno_actual = "O" if turno_actual == "X" else "X"
                                        tirar_dados_y_preparar_movimientos()
                            else:
                                # Distancia no disponible en los dados
                                # (Opcional: mostrar feedback visual)
                                pass
                            seleccion_origen = None

            elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 3:
                # Click derecho: cancelar selección
                seleccion_origen = None

        # DIBUJO
        dibujar_tablero()
        dibujar_fichas()
        dibujar_nombres(jugador_x, jugador_o, turno_actual)
        dibujar_bar_info()
        dibujar_hud(jugador_x, jugador_o, turno_actual)

        # Resaltar origen seleccionado
        if seleccion_origen is not None:
            cx, cy = centro_punto(seleccion_origen)
            pygame.draw.circle(VENTANA, HIGHLIGHT, (cx, cy), 20, 3)

        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()

# prompt 8 (haceme unala barra a donde se van las fichas comidas)
    # pygame_ui/game_pygame.py
import pygame, random
from core.board import Tablero

#--- Configuración inicial ---
pygame.init()
ANCHO, ALTO = 900, 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Backgammon - Pygame")

#🎨 Colores
MADERA_CLARA = (222, 206, 180)
ARENA        = (243, 228, 211)
BORDO        = (128, 0, 32)
BARRA_GRIS   = (60, 60, 60)
CONTORNO     = (40, 30, 20)
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
FONDO_EXTERIOR = (26, 36, 48)
CELESTE = (90, 170, 255)
LIMA = (150, 255, 150)
HIGHLIGHT = (80, 180, 250)

#--- Dimensiones ---
MARGEN_X = 50
MARGEN_Y = 50
ANCHO_TRIANGULO = (ANCHO - 2 * MARGEN_X) // 12  # base para cálculos
ALTO_TRIANGULO = 250
BARRA_W = 80                 # barra visible y con aire
BAR_PILA_RADIO = 14          # fichas en barra
BAR_PILA_SEP = 6

#--- Fuentes ---
pygame.font.init()
FUENTE = pygame.font.SysFont("arial", 22, bold=True)
FUENTE_UI = pygame.font.SysFont("arial", 24)
FUENTE_TIT = pygame.font.SysFont("arial", 28, bold=True)
FUENTE_MINI = pygame.font.SysFont("arial", 16)

#--- Tablero lógico ---
tablero = Tablero()

#--- Estado de juego ---
tirada_actual = (0, 0)
movimientos_restantes = []

#--- Geometría (se calcula en main) ---
GEO = None

def build_geo():
    board = pygame.Rect(MARGEN_X, MARGEN_Y, ANCHO - 2*MARGEN_X, ALTO - 2*MARGEN_Y)
    bar = pygame.Rect(board.centerx - BARRA_W//2, board.top, BARRA_W, board.height)

    left  = pygame.Rect(board.left, board.top, (board.width - BARRA_W)//2, board.height)
    right = pygame.Rect(bar.right,  board.top, (board.width - BARRA_W)//2, board.height)

    top_left  = pygame.Rect(left.left,  left.top,  left.width,  left.height//2)
    bot_left  = pygame.Rect(left.left,  left.centery, left.width,  left.height//2)
    top_right = pygame.Rect(right.left, right.top, right.width, right.height//2)
    bot_right = pygame.Rect(right.left, right.centery, right.width, right.height//2)

    return {
        "board": board, "bar": bar,
        "top_left": top_left, "bot_left": bot_left,
        "top_right": top_right, "bot_right": bot_right,
        "col_w_left":  top_left.width / 6,
        "col_w_right": top_right.width / 6,
    }

#------------------------------------------------------------
#DIBUJO DEL TABLERO, FICHAS, BARRA Y HUD
#------------------------------------------------------------
def dibujar_tablero():
    VENTANA.fill(FONDO_EXTERIOR)
    pygame.draw.rect(VENTANA, MADERA_CLARA, GEO["board"], border_radius=10)

    def draw_region(rect: pygame.Rect, up: bool, left_side: bool):
        col_w = GEO["col_w_left"] if left_side else GEO["col_w_right"]
        for i in range(6):
            x0 = rect.left + i * col_w
            x1 = x0 + col_w
            xm = x0 + col_w/2
            color = ARENA if i % 2 == 0 else BORDO
            if up:   # punta hacia arriba
                pts = [(x0, rect.bottom), (x1, rect.bottom), (xm, rect.top)]
            else:    # punta hacia abajo
                pts = [(x0, rect.top), (x1, rect.top), (xm, rect.bottom)]
            pygame.draw.polygon(VENTANA, color, pts)
            pygame.draw.polygon(VENTANA, CONTORNO, pts, 1)

    # arriba: puntas hacia abajo
    draw_region(GEO["top_left"],  up=False, left_side=True)   # 13..18
    draw_region(GEO["top_right"], up=False, left_side=False)  # 19..24
    # abajo: puntas hacia arriba
    draw_region(GEO["bot_left"],  up=True,  left_side=True)   # 12..7
    draw_region(GEO["bot_right"], up=True,  left_side=False)  # 6..1

    # barra visible y centrada
    pygame.draw.rect(VENTANA, (120, 80, 40), GEO["bar"], border_radius=6)
    pygame.draw.rect(VENTANA, (40, 20, 10), GEO["bar"], 4, border_radius=6)

def dibujar_fichas():
    radio = 15
    for punto, fichas in tablero.tablero.items():
        for idx, ficha in enumerate(fichas):
            # 13..18 → arriba izquierda
            if 13 <= punto <= 18:
                col_w = GEO["col_w_left"]; rect = GEO["top_left"]
                x = rect.left + (punto - 13 + 0.5) * col_w
                y = rect.bottom - (idx * 2 * radio + radio)
            # 19..24 → arriba derecha
            elif 19 <= punto <= 24:
                col_w = GEO["col_w_right"]; rect = GEO["top_right"]
                x = rect.left + (punto - 19 + 0.5) * col_w
                y = rect.bottom - (idx * 2 * radio + radio)
            # 12..7 → abajo izquierda
            elif 7 <= punto <= 12:
                col_w = GEO["col_w_left"]; rect = GEO["bot_left"]
                x = rect.left + (12 - punto + 0.5) * col_w
                y = rect.top + (idx * 2 * radio + radio)
            # 6..1 → abajo derecha
            elif 1 <= punto <= 6:
                col_w = GEO["col_w_right"]; rect = GEO["bot_right"]
                x = rect.left + (6 - punto + 0.5) * col_w
                y = rect.top + (idx * 2 * radio + radio)
            else:
                continue

            color = NEGRO if ficha == "X" else BLANCO
            pygame.draw.circle(VENTANA, color, (int(x), int(y)), radio)
            pygame.draw.circle(VENTANA, CONTORNO, (int(x), int(y)), radio, 1)

def dibujar_barra_comidas():
    barra = GEO["bar"]
    inner = barra.inflate(-10, -10)
    pygame.draw.rect(VENTANA, (180, 140, 100), inner, border_radius=8)
    pygame.draw.rect(VENTANA, (50, 30, 20), inner, 2, border_radius=8)

    cx = barra.centerx

    # O (arriba, blancas)
    n_o = len(tablero.bar.get("O", []))
    y_top = inner.top + 14
    for i in range(n_o):
        y = y_top + i * (2*BAR_PILA_RADIO + BAR_PILA_SEP)
        if y + BAR_PILA_RADIO > inner.centery - 12: break
        pygame.draw.circle(VENTANA, BLANCO, (cx, y), BAR_PILA_RADIO)
        pygame.draw.circle(VENTANA, CONTORNO, (cx, y), BAR_PILA_RADIO, 1)
    if n_o:
        text = FUENTE_MINI.render(f"O:{n_o}", True, BLANCO)
        VENTANA.blit(text, text.get_rect(center=(cx, inner.top + 8)))

    # X (abajo, negras)
    n_x = len(tablero.bar.get("X", []))
    y_bottom = inner.bottom - 14
    for i in range(n_x):
        y = y_bottom - i * (2*BAR_PILA_RADIO + BAR_PILA_SEP)
        if y - BAR_PILA_RADIO < inner.centery + 12: break
        pygame.draw.circle(VENTANA, NEGRO, (cx, y), BAR_PILA_RADIO)
        pygame.draw.circle(VENTANA, CONTORNO, (cx, y), BAR_PILA_RADIO, 1)
    if n_x:
        text = FUENTE_MINI.render(f"X:{n_x}", True, BLANCO)
        VENTANA.blit(text, text.get_rect(center=(cx, inner.bottom - 8)))

def dibujar_nombres(jugador_x, jugador_o, turno_actual=None):
    color_o = CELESTE if turno_actual == "O" else BLANCO
    color_x = CELESTE if turno_actual == "X" else BLANCO
    texto_o = FUENTE.render(f"{jugador_o} (Blancas)", True, color_o)
    texto_x = FUENTE.render(f"{jugador_x} (Negras)", True, color_x)
    rect_o = texto_o.get_rect(topleft=(20, MARGEN_Y - 20))
    rect_x = texto_x.get_rect(bottomleft=(20, ALTO - MARGEN_Y + 20))
    VENTANA.blit(texto_o, rect_o)
    VENTANA.blit(texto_x, rect_x)

def dibujar_hud():
    d1, d2 = tirada_actual
    hud1 = FUENTE.render(f"Tirada: {d1}-{d2}" if d1 else "Tirada: —", True, BLANCO)
    hud2 = FUENTE.render(f"Movimientos: {movimientos_restantes if movimientos_restantes else '—'}", True, BLANCO)
    VENTANA.blit(hud1, (ANCHO//2 - 120, 8))
    VENTANA.blit(hud2, (ANCHO//2 + 40, 8))

#------------------------------------------------------------
#MAPEO CLICK ↔ PUNTO y CENTRO PARA HIGHLIGHT
#------------------------------------------------------------
def punto_desde_click(pos):
    x, y = pos
    if not GEO["board"].collidepoint(x, y):
        return None

    # barra
    if GEO["bar"].collidepoint(x, y):
        return 25 if y < GEO["board"].centery else 0

    # arriba izquierda (13..18)
    if GEO["top_left"].collidepoint(x, y):
        i = int((x - GEO["top_left"].left) // GEO["col_w_left"])
        return 13 + max(0, min(5, i))
    # arriba derecha (19..24)
    if GEO["top_right"].collidepoint(x, y):
        i = int((x - GEO["top_right"].left) // GEO["col_w_right"])
        return 19 + max(0, min(5, i))
    # abajo izquierda (12..7)
    if GEO["bot_left"].collidepoint(x, y):
        i = int((x - GEO["bot_left"].left) // GEO["col_w_left"])
        return 12 - max(0, min(5, i))
    # abajo derecha (6..1)
    if GEO["bot_right"].collidepoint(x, y):
        i = int((x - GEO["bot_right"].left) // GEO["col_w_right"])
        return 6 - max(0, min(5, i))

    return None

def centro_punto(p):
    if 13 <= p <= 18:
        col_w = GEO["col_w_left"]; rect = GEO["top_left"]
        x = rect.left + (p - 13 + 0.5) * col_w; y = rect.bottom - 18
    elif 19 <= p <= 24:
        col_w = GEO["col_w_right"]; rect = GEO["top_right"]
        x = rect.left + (p - 19 + 0.5) * col_w; y = rect.bottom - 18
    elif 7 <= p <= 12:
        col_w = GEO["col_w_left"]; rect = GEO["bot_left"]
        x = rect.left + (12 - p + 0.5) * col_w; y = rect.top + 18
    elif 1 <= p <= 6:
        col_w = GEO["col_w_right"]; rect = GEO["bot_right"]
        x = rect.left + (6 - p + 0.5) * col_w; y = rect.top + 18
    elif p == 25:
        x, y = GEO["bar"].centerx, GEO["bar"].top + 20
    elif p == 0:
        x, y = GEO["bar"].centerx, GEO["bar"].bottom - 20
    else:
        x, y = ANCHO//2, ALTO//2
    return int(x), int(y)

#------------------------------------------------------------
#ENTRADA DE NOMBRES (UI)
#------------------------------------------------------------
class InputBox:
    def __init__(self, x, y, w, h, placeholder=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_idle = (200, 200, 200)
        self.color_active = CELESTE
        self.color = self.color_idle
        self.text = ""
        self.txt_surf = FUENTE_UI.render("", True, (20,20,20))
        self.active = False
        self.placeholder = placeholder
        self.placeholder_surf = FUENTE_UI.render(placeholder, True, (130,130,130))
    def handle_event(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            self.active = self.rect.collidepoint(e.pos)
            self.color = self.color_active if self.active else self.color_idle
        if e.type == pygame.KEYDOWN and self.active:
            if e.key == pygame.K_BACKSPACE: self.text = self.text[:-1]
            elif e.key not in (pygame.K_RETURN, pygame.K_TAB):
                if len(self.text) < 24: self.text += e.unicode
            self.txt_surf = FUENTE_UI.render(self.text, True, (20,20,20))
    def draw(self, surf):
        pygame.draw.rect(surf, (250,250,250), self.rect, border_radius=6)
        pygame.draw.rect(surf, self.color, self.rect, 2, border_radius=6)
        if self.text: surf.blit(self.txt_surf, (self.rect.x+10, self.rect.y+8))
        else: surf.blit(self.placeholder_surf, (self.rect.x+10, self.rect.y+8))
    def get_value(self, default): return self.text.strip() or default

def pedir_nombres():
    clock = pygame.time.Clock()
    running = True
    panel = pygame.Rect(ANCHO//2-320, ALTO//2-140, 640, 280)
    box_x = InputBox(panel.x+40, panel.y+90, 560, 40, "Nombre del Jugador X (Negras)")
    box_o = InputBox(panel.x+40, panel.y+170, 560, 40, "Nombre del Jugador O (Blancas)")
    boxes = [box_x, box_o]; focus = 0
    boxes[focus].active = True; boxes[focus].color = boxes[focus].color_active
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); raise SystemExit
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_TAB:
                    boxes[focus].active=False; boxes[focus].color=boxes[focus].color_idle
                    focus=(focus+1)%2; boxes[focus].active=True; boxes[focus].color=boxes[focus].color_active
                elif e.key == pygame.K_RETURN: running=False
            for b in boxes: b.handle_event(e)
        VENTANA.fill(FONDO_EXTERIOR)
        pygame.draw.rect(VENTANA, (245,245,245), panel, border_radius=12)
        pygame.draw.rect(VENTANA, (210,210,210), panel,2,border_radius=12)
        titulo = FUENTE_TIT.render("Ingresá los nombres de los jugadores", True, (30,30,30))
        subt = FUENTE_UI.render("TAB cambia de campo · ENTER para comenzar", True, (60,60,60))
        VENTANA.blit(titulo, titulo.get_rect(center=(panel.centerx, panel.y+40)))
        VENTANA.blit(subt, subt.get_rect(center=(panel.centerx, panel.y+70)))
        for b in boxes: b.draw(VENTANA)
        pygame.display.flip(); clock.tick(60)
    return box_x.get_value("Jugador X"), box_o.get_value("Jugador O")

#------------------------------------------------------------
#DADOS, SORTEO y REGLAS DE MOVIMIENTO
#------------------------------------------------------------
def sorteo_inicial(jx, jo):
    while True:
        dx, do = random.randint(1,6), random.randint(1,6)
        if dx != do: break
    turno = "X" if dx > do else "O"
    dibujar_tablero(); dibujar_fichas(); dibujar_barra_comidas(); dibujar_nombres(jx, jo, turno)
    txt = FUENTE_TIT.render(f"🎲 Comienza {jx if turno=='X' else jo}", True, LIMA)
    VENTANA.blit(txt, txt.get_rect(center=(ANCHO//2, ALTO//2)))
    pygame.display.flip(); pygame.time.wait(1200)
    return turno

def tirar_dados_y_preparar_movimientos():
    global tirada_actual, movimientos_restantes
    d1, d2 = random.randint(1,6), random.randint(1,6)
    tirada_actual = (d1, d2)
    movimientos_restantes = [d1, d1, d1, d1] if d1 == d2 else [d1, d2]

def distancia_segun_turno(turno, origen, destino):
    if origen is None or destino is None:
        return None
    if turno == "X":
        if destino <= origen: return None
        return destino - origen
    else:
        if destino >= origen: return None
        return origen - destino

def consumir_movimiento(dist):
    if dist in movimientos_restantes:
        movimientos_restantes.remove(dist)
        return True
    return False

#------------------------------------------------------------
#MAIN LOOP
#------------------------------------------------------------
def main():
    global GEO
    GEO = build_geo()

    jugador_x, jugador_o = pedir_nombres()
    turno = sorteo_inicial(jugador_x, jugador_o)
    tirar_dados_y_preparar_movimientos()

    seleccion = None
    reloj = pygame.time.Clock()
    corriendo = True
    while corriendo:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                corriendo = False

            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                p = punto_desde_click(e.pos)
                if p is None:
                    seleccion = None
                elif seleccion is None:
                    fichas = tablero.tablero.get(p, [])
                    # origen válido: ficha propia o barra correspondiente
                    if (turno in fichas) or \
                       (p == 0 and turno == "X" and len(tablero.bar.get("X", [])) > 0) or \
                       (p == 25 and turno == "O" and len(tablero.bar.get("O", [])) > 0):
                        seleccion = p
                else:
                    destino = p
                    dist = distancia_segun_turno(turno, seleccion, destino)
                    if dist and consumir_movimiento(dist):
                        if not tablero.mover_ficha(seleccion, destino):
                            # si el core rechaza, devolvemos el movimiento
                            movimientos_restantes.append(dist)
                            movimientos_restantes.sort()
                        elif not movimientos_restantes:
                            turno = "O" if turno == "X" else "X"
                            tirar_dados_y_preparar_movimientos()
                    seleccion = None

            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 3:
                seleccion = None

        # --- Dibujar frame ---
        dibujar_tablero()
        dibujar_fichas()
        dibujar_barra_comidas()
        dibujar_nombres(jugador_x, jugador_o, turno)
        # HUD
        d1, d2 = tirada_actual
        hud1 = FUENTE.render(f"Tirada: {d1}-{d2}" if d1 else "Tirada: —", True, BLANCO)
        hud2 = FUENTE.render(f"Movimientos: {movimientos_restantes if movimientos_restantes else '—'}", True, BLANCO)
        VENTANA.blit(hud1, (ANCHO//2 - 120, 8))
        VENTANA.blit(hud2, (ANCHO//2 + 40, 8))

        # Resaltado de origen
        if seleccion:
            cx, cy = centro_punto(seleccion)
            pygame.draw.circle(VENTANA, HIGHLIGHT, (cx, cy), 20, 3)

        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()

# prompt 9 (ahora cuando quiera seleccionar una ficha quiero que se seleccione el triangulo donde esta)
    # pygame_ui/game_pygame.py
    1) Colores (arriba, con el resto de constantes)
    HIGHLIGHT_TRI_FILL   = (80, 180, 250, 90)   # celeste con transparencia
    HIGHLIGHT_TRI_BORDER = (80, 180, 250)       # borde del triángulo seleccionado
    2) Helper: obtener el polígono del triángulo por punto (1..24)
    def triangulo_polygon(punto):
        """
        Devuelve la lista de puntos (x,y) del triángulo asociado a `punto`
        respetando la geometría GEO (izq/dcha · arriba/abajo).
        """
        if 13 <= punto <= 18:            # arriba izquierda (punta hacia abajo)
            rect = GEO["top_left"];  col_w = GEO["col_w_left"];  i = punto - 13
            x0 = rect.left + i * col_w;  x1 = x0 + col_w;  xm = x0 + col_w/2
            pts = [(x0, rect.top), (x1, rect.top), (xm, rect.bottom)]
        elif 19 <= punto <= 24:          # arriba derecha (punta hacia abajo)
            rect = GEO["top_right"]; col_w = GEO["col_w_right"]; i = punto - 19
            x0 = rect.left + i * col_w;  x1 = x0 + col_w;  xm = x0 + col_w/2
            pts = [(x0, rect.top), (x1, rect.top), (xm, rect.bottom)]
        elif 7 <= punto <= 12:           # abajo izquierda (punta hacia arriba)
            rect = GEO["bot_left"];  col_w = GEO["col_w_left"];  i = 12 - punto
            x0 = rect.left + i * col_w;  x1 = x0 + col_w;  xm = x0 + col_w/2
            pts = [(x0, rect.bottom), (x1, rect.bottom), (xm, rect.top)]
        elif 1 <= punto <= 6:            # abajo derecha (punta hacia arriba)
            rect = GEO["bot_right"]; col_w = GEO["col_w_right"]; i = 6 - punto
            x0 = rect.left + i * col_w;  x1 = x0 + col_w;  xm = x0 + col_w/2
            pts = [(x0, rect.bottom), (x1, rect.bottom), (xm, rect.top)]
        else:
            return None

        # pequeño “inset” para que el borde no tape las líneas
        inset = 2
        if pts[2][1] > pts[0][1]:  # punta hacia abajo
            return [(pts[0][0]+inset, pts[0][1]+inset),
                    (pts[1][0]-inset, pts[1][1]+inset),
                    (pts[2][0],       pts[2][1]-inset)]
        else:                      # punta hacia arriba
            return [(pts[0][0]+inset, pts[0][1]-inset),
                    (pts[1][0]-inset, pts[1][1]-inset),
                    (pts[2][0],       pts[2][1]+inset)]
    3) Dibujo del highlight del triángulo seleccionado
    def dibujar_triangulo_seleccionado(punto):
        poly = triangulo_polygon(punto)
        if not poly:
            return
        # superficie con alpha para el relleno translúcido
        s = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        pygame.draw.polygon(s, HIGHLIGHT_TRI_FILL, poly)
        VENTANA.blit(s, (0, 0))
        # borde por encima (opcional: 3 px)
        pygame.draw.polygon(VENTANA, HIGHLIGHT_TRI_BORDER, poly, 3)
    4) Usarlo en el bucle de render
    # --- Dibujo frame ---
    dibujar_tablero()

    # 🔹 si hay origen seleccionado, resaltar su triángulo ANTES de dibujar fichas
    if seleccion is not None:
        dibujar_triangulo_seleccionado(seleccion)

    dibujar_fichas()
    dibujar_barra_comidas()
    dibujar_nombres(jugador_x, jugador_o, turno)
    dibujar_hud()

    pygame.display.flip()

# prompt 10( ahora quiero la barra donde salen las fichas)
    # pygame_ui/game_pygame.py
    1) Helper: posición de la ficha superior en la barra
    def pos_ficha_barra(punto):
        """
        Devuelve (cx, y) de la ficha superior en la barra.
        punto = 25 (O, arriba) o 0 (X, abajo)
        """
        barra = GEO["bar"]
        inner = barra.inflate(-10, -10)
        cx = barra.centerx

        if punto == 25:  # O / blancas (arriba)
            n = len(tablero.bar.get("O", []))
            if n <= 0: 
                return None
            y_top = inner.top + 14
            y = y_top + (n - 1) * (2*BAR_PILA_RADIO + BAR_PILA_SEP)
            # limitar a la mitad superior
            y = min(y, inner.centery - 12)
            return (cx, int(y))

        if punto == 0:   # X / negras (abajo)
            n = len(tablero.bar.get("X", []))
            if n <= 0:
                return None
            y_bottom = inner.bottom - 14
            y = y_bottom - (n - 1) * (2*BAR_PILA_RADIO + BAR_PILA_SEP)
            # limitar a la mitad inferior
            y = max(y, inner.centery + 12)
            return (cx, int(y))

        return None
    2) Dibujo del highlight cuando la selección es la barra
    def dibujar_barra_seleccionada(punto):
        # resalta la mitad correspondiente y la ficha superior
        barra = GEO["bar"]
        s = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)

        if punto == 25:
            half = pygame.Rect(barra.left, barra.top, barra.width, barra.height//2)
        elif punto == 0:
            half = pygame.Rect(barra.left, barra.centery, barra.width, barra.height//2)
        else:
            return

        # fondo translúcido en la mitad activa
        pygame.draw.rect(s, (80, 180, 250, 90), half, border_radius=6)
        VENTANA.blit(s, (0, 0))
        # borde
        pygame.draw.rect(VENTANA, (80, 180, 250), half, 3, border_radius=6)

        # aro sobre la ficha superior del montón (si existe)
        pos = pos_ficha_barra(punto)
        if pos:
            cx, cy = pos
            pygame.draw.circle(VENTANA, (80, 180, 250), (cx, cy), BAR_PILA_RADIO + 4, 3)
    3) Usarlo en el render (reemplaza el viejo círculo)
    # --- Dibujo del frame ---
    dibujar_tablero()

    # highlight de selección
    if seleccion is not None:
        if seleccion in (0, 25):
            dibujar_barra_seleccionada(seleccion)
        else:
            dibujar_triangulo_seleccionado(seleccion)

    dibujar_fichas()
    dibujar_barra_comidas()
    dibujar_barra_salida()
    dibujar_nombres(jugador_x, jugador_o, turno)
    dibujar_hud()

    pygame.display.flip()

# prompt 11 ( ahora quiero poder saltearme el turno tocando enter)
    # pygame_ui/game_pygame.py
    1) Helper para cambiar de turno
    def pasar_turno(turno_actual):
        """Pasa el turno al otro jugador y tira dados nuevos."""
        nuevo_turno = "O" if turno_actual == "X" else "X"
        tirar_dados_y_preparar_movimientos()
        return nuevo_turno
    2) Capturar ENTER en el loop de eventos (dentro de main())
    Buscá tu bloque for e in pygame.event.get(): y agregá este elif:
        elif e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
        # Pasar turno manualmente
        movimientos_restantes.clear()   # por claridad, no es estrictamente necesario
        seleccion = None                # limpia selección si había
        turno = pasar_turno(turno)      # cambia el turno y tira dados
    3) (Opcional) Mostrar pista en el HUD
    def dibujar_hud():
        d1, d2 = tirada_actual
        hud1 = FUENTE.render(f"Tirada: {d1}-{d2}" if d1 else "Tirada: —", True, BLANCO)
        hud2 = FUENTE.render(f"Movimientos: {movimientos_restantes if movimientos_restantes else '—'}", True, BLANCO)
        hint = FUENTE_MINI.render("ENTER: pasar turno", True, BLANCO)
        VENTANA.blit(hud1, (ANCHO//2 - 120, 8))
        VENTANA.blit(hud2, (ANCHO//2 + 40, 8))
        VENTANA.blit(hint, (ANCHO//2 + 300, 12))  # ajustá si querés otro lugar








