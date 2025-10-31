# Justificación del Proyecto: Backgammon Computación 2025

## 1. Resumen del diseño general

El proyecto **Backgammon Computación 2025** implementa el clásico juego de Backgammon en **Python**, con una arquitectura modular que separa la **lógica central del juego** (módulo `core/`) de las **interfaces de usuario**, que incluyen:
- Una **interfaz de línea de comandos (CLI)** (`cli/cli.py`).
- Una **interfaz gráfica con Pygame** (`pygame_ui/game_pygame.py`).

Esta división permite mantener la lógica del juego independiente del modo de interacción, asegurando testabilidad, mantenibilidad y cumplimiento del principio **Single Responsibility**.

La estructura general del repositorio sigue la guía del documento base:

```
backgammon/
├── core/          → lógica del juego
├── cli/           → interfaz de línea de comandos
├── pygame_ui/     → interfaz gráfica
├── tests/         → pruebas unitarias
├── assets/        → imágenes o sonidos (si se agregan)
└── requirements.txt
```

---

## 2. Justificación de las clases elegidas

### **Dice**
Ubicada en `core/dice.py`.

Responsabilidad: modelar los dos dados del Backgammon y las operaciones sobre ellos.  
Motivo: encapsula el azar, simplificando la lógica de tiradas y movimientos.

Métodos clave:
- `roll()` → genera una tirada aleatoria.
- `is_double()` → detecta dobles.
- `movimientos()` → traduce tiradas a movimientos posibles.


---

### **Player**
Ubicada en `core/player.py`.

Responsabilidad: representar a un jugador con su nombre, ficha y sus dados.  
Motivo: agrupa toda la información del jugador y coordina sus tiradas sin conocer el tablero.

Atributos:
- `__name__`: nombre del jugador.
- `__ficha__`: símbolo del jugador ('X' o 'O').
- `__dice__`: instancia de `Dice`.


---

### **Tablero**
Ubicada en `core/board.py`.

Responsabilidad: representar el estado del tablero y aplicar las reglas del juego.  
Motivo: centraliza las validaciones de movimiento, capturas, reingresos y condiciones de victoria.

Funciones principales:
- `mostrar()` → renderiza el tablero en texto.
- `mover_ficha()` → ejecuta un movimiento aplicando reglas de Backgammon.
- `distancia_legal()` → determina la dirección válida según la ficha.
- `todas_en_cuadrante_final()` → valida si puede comenzar el “bearing off”.



---

### **Interfaz (CLI)**
Ubicada en `cli/cli.py`.

Responsabilidad: manejar la interacción en consola.  
Motivo: permite jugar sin entorno gráfico, siendo la interfaz obligatoria del proyecto.

Funciones:
- `sorteo_inicial()`: determina quién inicia.
- `tirar_dados_y_mostrar()`: muestra tiradas y movimientos.
- `jugar_turno()`: ejecuta un turno completo validando entradas.
- `main()`: orquesta el flujo general del juego.


---

### **PygameUI**
Ubicada en `pygame_ui/game_pygame.py`.

Responsabilidad: ofrecer una interfaz visual moderna del juego.  
Motivo: brindar experiencia visual y auditiva, manteniendo la lógica en `core/board.py`.

Componentes:
- Render del tablero, fichas y barras.
- Sistema de clicks → puntos del tablero.
- Clases auxiliares (`InputBox`) para ingresar nombres.
- HUD dinámico con movimientos y turno actual.


---

## 3. Justificación de los atributos

| Clase | Atributo | Tipo | Justificación |
|-------|-----------|------|---------------|
| `Dice` | `last_rolls` | list[int] | Guarda la última tirada para consistencia entre turnos. |
| `Player` | `__name__`, `__ficha__`, `__dice__` | str, str, Dice | Representan identidad, símbolo y azar del jugador. |
| `Tablero` | `tablero`, `bar`, `off` | dict[int,list[str]], dict, dict | Representan estado completo del juego: puntos, fichas comidas, retiradas. |
| `Interfaz` | `tablero`, `jugador_x`, `jugador_o` | objetos | Facilita la coordinación del flujo en CLI. |
| `PygameUI` | `VENTANA`, `GEO`, `movimientos_restantes` | pygame.Surface, dict, list[int] | Necesarios para representación visual y gestión de movimientos. |

---

## 4. Decisiones de diseño relevantes

1. **Separación en capas:**  
   - `core` (lógica del juego)  
   - `cli` (interfaz texto)  
   - `pygame_ui` (interfaz gráfica)  
   Esto permite testear la lógica sin abrir ventanas.

2. **Modelo orientado a objetos:**  
   Cada clase tiene un único propósito (principio SRP).  
   La lógica se distribuye de manera jerárquica y coherente.

3. **Uso de diccionarios en Tablero:**  
   Permite acceder dinámicamente a cada punto (`1–24`) y simplifica la serialización.

4. **Mensajes de consola y trazas en `mover_ficha`:**  
   Ayudan al debugging y mejoran la experiencia interactiva.

5. **PygameUI desacoplada:**  
   No replica lógica de Backgammon, solo invoca métodos de `Tablero`.

---

## 5. Excepciones y manejo de errores

No se definieron excepciones personalizadas; se optó por **control de flujo por validación**, priorizando simplicidad en CLI y tests:

- Entradas inválidas (formato, dirección, movimiento) se manejan con `try/except` y mensajes amigables.
- El método `mover_ficha()` retorna `False` en lugar de lanzar errores, para evitar interrupciones durante el juego.

Futuras versiones podrían incluir excepciones propias (`MovimientoInvalido`, `BloqueoDetectado`).

---

## 6. Estrategias de testing y cobertura

- **Framework usado:** `unittest`
- **Ubicación:** carpeta `tests/`
- **Cobertura alcanzada:** 93% (según `coverage` )
- **Estrategia:**  
  1. **Unitarios**: pruebas directas de métodos (`Dice`, `Player`, `Tablero`).  
  2. **Integración**: validación de interacción entre clases (`Interfaz`, `PygameUI`).  
  3. **Cobertura de ramas**: casos de empate, bloqueos, reingresos y retiros.

Cada módulo tiene su archivo de test correspondiente:
| Archivo | Cubre |
|----------|-------|
| `test_dice.py` | Tiradas, dobles y movimientos |
| `test_player.py` | Accesores, integración con `Dice` |
| `test_board.py` | Movimientos, capturas, barras, bearing off, ganador |
| `test_cli.py` | Sorteo, flujo de turnos y validación de entradas |
| `test_game.py` | Geometría, eventos, dibujado y bucle principal en Pygame |

---

## 7. Cumplimiento de principios SOLID

| Principio | Aplicación |
|------------|-------------|
| **S** - Single Responsibility | Cada clase cumple una función concreta. |
| **O** - Open/Closed | Posibilidad de extender (`Redis`, GUI) sin modificar la lógica. |
| **L** - Liskov Substitution | Las interfaces pueden cambiarse (CLI ↔ GUI) sin romper el core. |
| **I** - Interface Segregation | Métodos cortos y específicos, sin interfaces monolíticas. |
| **D** - Dependency Inversion | `Interfaz` y `PygameUI` dependen de abstracciones (`Tablero`, `Player`). |

---

## 8. Anexos: Diagrama UML simplificado

```
+------------------+
|     Player       |
+------------------+
| -__name__        |
| -__ficha__       |
| -__dice__ : Dice |
+------------------+
| +roll_dice()     |
| +has_double()    |
| +movimientos()   |
+------------------+

+------------------+
|      Dice        |
+------------------+
| -last_rolls      |
+------------------+
| +roll()          |
| +is_double()     |
| +movimientos()   |
+------------------+

+------------------+
|     Tablero      |
+------------------+
| -tablero         |
| -bar             |
| -off             |
+------------------+
| +mover_ficha()   |
| +mostrar()       |
| +ganador()       |
+------------------+

+------------------+
|    Interfaz      |
+------------------+
| -tablero         |
| -jugador_x, o    |
+------------------+
| +main()          |
| +jugar_turno()   |
+------------------+

+------------------+
|    PygameUI      |
+------------------+
| -tablero : Tablero|
| -movimientos_restantes |
+------------------+
| +main()          |
| +dibujar_*()     |
| +punto_desde_click() |
+------------------+
```

---

