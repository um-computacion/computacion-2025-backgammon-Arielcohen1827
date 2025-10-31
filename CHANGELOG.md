# 📜 CHANGELOG



---

## [1.0.0] - 2025-10-31
### 🚀 Versión final con interfaz Pygame
- Implementación completa del módulo `game_pygame.py`.
- Diseño visual del tablero con triángulos alternados y barra central.
- Agregado de barra de comidas y barra de salida (off).
- Incorporación de nombres de jugadores, HUD dinámico y control de turno.
- Soporte para clicks de selección, cancelación con botón derecho y paso de turno con ENTER.
- Validación de movimientos con `Tablero.mover_ficha()` desde la interfaz.
- Ajuste de geometría para que el tablero se muestre completo en resolución 1100x650.
- Revisión de código, documentación (`README.md`, `JUSTIFICACION.md`) y cobertura de tests >90%.

---

## [0.9.0] - 2025-10-26
### 🎮 Integración avanzada CLI y Pygame
- Pruebas de reingreso de fichas en barra (`test_reingreso_de_ficha_de_O`).
- Correcciones de reingresos y tests complementarios.
- Mejora en la función de cancelación de movimientos en CLI.
- Implementación de `coloco la barra` y `barra final`.
- Verificación del flujo de turnos con ENTER.

---

## [0.8.0] - 2025-10-14
### 🧩 Control de flujo de turnos y validaciones
- Implementación de cancelación de movimiento (`cancelacion de movimiento`).
- Tests unitarios de cancelación (`terminado la cancelación de movimiento`).
- Refinamiento de `Interfaz.jugar_turno()` para evitar repeticiones de movimientos.
- Integración de funciones para validar si hay fichas en la barra antes de mover.

---

## [0.7.0] - 2025-10-10
### 🎯 Finalización de la lógica del tablero
- Tests de ganador y fichas restantes (`test_ganador`, `test_fichas_restantes`).
- Correcciones en el manejo de “comer” y bloqueo de puntos.
- Preparación para interfaz con `turnos en interfaz` y `agregando test`.

---

## [0.6.0] - 2025-09-29
### 💡 Inicio de interfaz CLI y sorteo inicial
- Creación de `Interfaz` en `cli/cli.py`.
- Implementación de `sorteo_inicial()` y flujo de turnos básicos.
- Validaciones de entrada `origen-destino`.
- Primeras pruebas integradas (`test_cli.py`).
- “Coloco la norma para indicar quién empieza”.

---

## [0.5.0] - 2025-09-17
### 🧠 Implementación de clase Player
- Clase `Player` con integración a `Dice`.
- Accesores `get_name()`, `get_ficha()` y métodos `roll_dice()` / `has_double()`.
- Primeros tests unitarios para jugador y correcciones en fixtures.
- Refactorización de tests de movimiento.

---

## [0.4.0] - 2025-09-15
### 🎲 Reglas de movimiento y captura
- Implementación de reglas de movimiento en `Tablero.mover_ficha()`.
- Lógica para capturar fichas rivales (“comer”) y validaciones de dirección.
- Condición de reingreso desde la barra.
- Implementación de “guardar fichas” y tests asociados.

---

## [0.3.0] - 2025-09-14
### 🧱 Lógica del tablero inicial
- Sentido de movimiento y test de direcciones.
- Implementación de la clase `Checker` y condición de movimiento inicial.
- Validación de posiciones iniciales.
- Tests de movimiento y corrección en condiciones de desplazamiento.

---

## [0.2.0] - 2025-09-13
### ⚙️ Estructura base del juego
- Implementación de posiciones iniciales del tablero (`posiciones iniciales`).
- Creación de test de movimientos.
- Validación de la primera condición de movimiento.

---

## [0.1.0] - 2025-09-03
### 🧩 Configuración inicial
- Creación del repositorio y estructura del proyecto.
- Implementación de `Dice` (tirada, doble, verificación).
- Creación de tests iniciales para dados.
- Configuración del entorno de trabajo y primeros commits.

---


