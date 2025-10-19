# 🕹️ Pong - Versión Atari en Python con Pygame

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Pygame](https://img.shields.io/badge/Pygame-2.x-green)
![Estado](https://img.shields.io/badge/Proyecto-Funcional-brightgreen)

## 🎯 Objetivo del Proyecto

El objetivo principal de este proyecto fue **recrear el clásico juego Atari Pong** utilizando el lenguaje de programación **Python** y la librería **Pygame**, aplicando conceptos de **programación orientada a objetos, diseño de interfaces, control de eventos y manejo de archivos**.

Además, se buscó implementar un sistema de **puntuaciones guardadas**, **modos de juego con IA**, **interfaz de menú interactivo**, y una **jugabilidad fluida** inspirada en el clásico de los años 70.

---

## 👥 Datos del Grupo

| Integrante | Rol | Contribución |
|-------------|-----|--------------|
| Mishel Cumbal | Programador / Diseñador | Desarrollo del código en Python, estructura del menú, IA y sistema de puntuaciones. |
| (Agregar nombres si hay más) |  |  |

📅 **Fecha de entrega:** 19 de octubre de 2025  
📘 **Materia:** Programación  
🏫 **Institución:** Universidad Internacional del Ecuador (UIDE)

---

## ⚙️ Principales Funcionalidades del Código

El archivo principal `pong.py` contiene toda la lógica del juego y está estructurado en módulos funcionales para mantener un código limpio y fácil de mantener.

### 🔧 1. Configuración general
- Definición de parámetros del juego (ancho, alto, velocidad, colores, FPS).
- Inicialización de la ventana con `pygame.display.set_mode()`.
- Creación de tipografías y temporizador de fotogramas.

### 💾 2. Sistema de puntuaciones (`pong_scores.json`)
- Guarda automáticamente las partidas jugadas con nombres de jugadores, marcador y ganador.
- Permite visualizar las **últimas 10 partidas** desde el menú principal.
- Uso de JSON para persistir los datos de manera local.

### 🧠 3. Inteligencia Artificial (IA)
- Modo de un jugador disponible: presionar la tecla **I** para activar/desactivar la IA.
- La IA controla la paleta derecha de forma automática siguiendo la posición de la pelota.

### 🎮 4. Interfaz gráfica y menús
- Pantalla de **inicio** con botones interactivos: *Iniciar Juego*, *Puntuaciones* y *Salir*.
- Pantalla de **ingreso de nombres** para personalizar a los jugadores.
- Pantalla de **puntuaciones** mostrando los resultados previos.

### 🧩 5. Clases implementadas
- **`Paddle`**: controla el movimiento de las paletas de los jugadores.  
- **`Ball`**: maneja el movimiento y colisiones de la pelota.  
- **`Button`**: crea botones con efecto hover y clic.  
- **`InputBox`**: permite la entrada de texto (nombres de los jugadores).  

### 🏆 6. Sistema de juego y reinicio
- Modo **versus** entre dos jugadores o contra la **IA**.  
- El juego se reinicia automáticamente al alcanzar el **puntaje máximo (5 puntos)**.  
- Permite **pausar, reiniciar o regresar al menú** con teclas rápidas.  

---

## 🎮 Instrucciones del Juego

| Acción | Jugador Izquierdo | Jugador Derecho |
|:-------|:------------------|:----------------|
| Mover hacia arriba | **W** | **Flecha ↑** |
| Mover hacia abajo | **S** | **Flecha ↓** |
| Activar/Desactivar IA | **I** | — |
| Pausar/Reanudar | **Espacio** | — |
| Reiniciar marcador | **R** | — |
| Volver al menú principal | **Esc** | — |

---

## 🧠 Mecánica del Juego

- La pelota rebota en los bordes superior e inferior y cambia de dirección al chocar con una paleta.  
- Cada vez que un jugador no logra devolver la pelota, el oponente suma un punto.  
- El primer jugador en llegar a **5 puntos** gana la partida.  
- Tras un ganador, el juego se reinicia automáticamente después de 3 segundos.  

---

## 🧩 Estructura del Proyecto

