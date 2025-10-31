# 🎲 Backgammon Computación 2025

Proyecto final de la materia **Computación II**, que implementa el clásico juego **Backgammon** en **Python**, con doble modalidad:
- **Interfaz de línea de comandos (CLI)**  
- **Interfaz gráfica con Pygame**

---

## 🧠 Descripción general

El proyecto replica las reglas oficiales del Backgammon, permitiendo jugar partidas completas entre dos jugadores humanos.  
Se respetan las reglas tradicionales: movimientos con dados, capturas, reingresos desde la barra y retiro final (*bearing off*).  



---

## 📂 Estructura del proyecto

```
backgammon/
├── core/                # Lógica central del juego
│   ├── board.py         # Estado del tablero y reglas
│   ├── player.py        # Jugadores y fichas
│   └── dice.py          # Tiradas de dados
│
├── cli/                 # Interfaz de línea de comandos
│   └── cli.py
│
├── pygame_ui/           # Interfaz gráfica
│   └── game_pygame.py
│
├── tests/               # Pruebas unitarias
│   ├── test_board.py
│   ├── test_player.py
│   ├── test_dice.py
│   ├── test_cli.py
│   └── test_game.py
│
├── JUSTIFICACION.md     # Justificación de diseño (requisito obligatorio)
├── CHANGELOG.md         # Registro de cambios (sprints)
└── requirements.txt     # Dependencias del proyecto
```

---

## ⚙️ Instalación

### 🔸 Requisitos previos
- Python 3.10 o superior  
- `pip` instalado  


### 🔸 Instalación manual

1. Clonar el repositorio:
   ```
   git clone https://github.com/um-computacion/computacion-2025-backgammon-Arielcohen1827.git

   ```

2. Instalar dependencias:
   ```
   pip install -r requirements.txt
   ```

3. Verificar instalación:
   ```
   python -m unittest discover -s tests
   ```

---

## 🖥️ Modo de ejecución

### ▶️ Interfaz de línea de comandos (CLI)

Ejecutar desde la raíz del proyecto:
```
python -m cli.cli
```

Esto abrirá una sesión en consola donde:
- Se solicitarán los nombres de los jugadores.
- Se realizará un sorteo inicial.
- Cada jugador podrá ingresar sus movimientos (`origen-destino`).
- El turno se alterna automáticamente o con `ENTER`.

---

### 🕹️ Interfaz gráfica (Pygame)

Ejecutar:
```
python -m pygame_ui.game_pygame
```

Controles:
- **Click izquierdo**: seleccionar origen y destino.  
- **Click derecho**: cancelar selección.  
- **ENTER**: pasar turno.  
- **Cierre de ventana**: salir del juego.  

---

## 🧪 Testing

El proyecto incluye una suite completa de **pruebas unitarias e integradas** con `unittest`.

Ejecutar todas las pruebas:
```
python -m unittest discover -s tests -v
```

Verificar cobertura (opcional):
```
coverage run -m unittest discover -s tests
coverage report -m
```

La cobertura supera el **90%**, cumpliendo con los criterios de evaluación.

---

---

## 📚 Documentación

- [JUSTIFICACION.md](./JUSTIFICACION.md) → explica decisiones de diseño y SOLID.  
- [CHANGELOG.md](./CHANGELOG.md) → detalla los sprints y commits relevantes.  
- [prompts-desarrollo.md](./prompts-desarrollo.md), [prompts-testing.md](./prompts-testing.md), [prompts-documentacion.md](./prompts-documentacion.md) → registro de uso de IA según pautas del proyecto.

---

## 🏁 Autoría y trazabilidad

Trabajo individual realizado en el marco de la materia **Computación II – 2025**.  


**Autor:** Ariel Cohen
**Lenguaje:** Python 3  
**Bibliotecas principales:** `pygame`, `unittest`, `coverage`

---

© 2025 — Universidad / Materia Computación
Proyecto: *Backgammon Computación 2025*
