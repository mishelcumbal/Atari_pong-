# 🕹️ Pong - Versión Atari en Python con Pygame

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Pygame](https://img.shields.io/badge/Pygame-2.x-green)
![Estado](https://img.shields.io/badge/Proyecto-Funcional-brightgreen)

---

## 🎯 Objetivo del Proyecto

El propósito de este proyecto fue **recrear el clásico videojuego Atari Pong**, aplicando los principios de **programación orientada a objetos**, **diseño de interfaces**, **manejo de eventos** y **persistencia de datos** mediante archivos JSON.  

El juego fue desarrollado con **Python** y la librería **Pygame**, buscando lograr una experiencia fluida, visualmente atractiva y fiel al estilo retro del Pong original, pero con un toque moderno que incluye menús, puntuaciones guardadas y una IA funcional.

---

## 👥 Datos del Grupo

| Integrante | Rol | Contribución |
|-------------|-----|--------------|
| **Mishel Cumbal** | Programador / Diseñador | Desarrollo completo del código, diseño de menús, IA, sistema de puntuaciones y documentación. |
| *(Agregar si hay más integrantes)* |  |  |

📅 **Fecha de entrega:** 19 de octubre de 2025  
📘 **Materia:** Programación  
🏫 **Universidad Internacional del Ecuador (UIDE)**  

---

## ⚙️ Descripción General del Software

El proyecto está compuesto por varios módulos integrados que gestionan los distintos aspectos del juego:

- **Configuración inicial:** Define el tamaño de la ventana, colores, velocidad, FPS y elementos gráficos.  
- **Interfaz de usuario:** Menú principal con botones interactivos, entrada de nombres y pantalla de puntuaciones.  
- **IA del juego:** Control automático de la paleta derecha cuando se activa el modo un jugador.  
- **Sistema de puntuaciones:** Registra automáticamente las partidas jugadas en un archivo `pong_scores.json`.  
- **Mecánica de colisiones y física:** Controla el rebote de la pelota y la detección de puntos.  

---

## 🧠 Análisis del Desarrollo

Durante el desarrollo se aplicaron principios de **modularidad** y **claridad estructural** para garantizar que cada parte del código tuviera una función específica.  
La librería **Pygame** permitió manejar con facilidad el bucle principal del juego, el sistema de eventos (teclas y clics), y el renderizado en tiempo real.

El proyecto también hace uso de:
- **Archivos JSON** para almacenamiento persistente.  
- **Listas y clases personalizadas** para manejar objetos en pantalla.  
- **Condicionales y estructuras de control** para detectar colisiones y determinar el ganador.  

---

## 🧩 Estructura del Proyecto

📁 Pong-Atari/
│
├── pong.py               # Código principal del juego
├── pong_scores.json      # Archivo de puntuaciones guardadas
├── assets/               # (Opcional) Recursos gráficos o de sonido
└── README.md             # Documentación del proyecto

---

## 🏗️ Clases Principales

### 🟩 `Paddle`
Controla el movimiento vertical de cada jugador, detecta límites de pantalla y responde a las teclas asignadas.

### ⚪ `Ball`
Gestiona el movimiento y las colisiones de la pelota con las paletas y los bordes, además del reinicio tras cada punto.

### 🔲 `Button`
Crea los botones interactivos del menú principal con animación *hover* y detección de clic.

### ✏️ `InputBox`
Gestiona el ingreso de texto para capturar los nombres de los jugadores antes de iniciar una partida.

> Cada clase está diseñada con independencia funcional y responsabilidad clara, favoreciendo el mantenimiento, la comprensión y futuras ampliaciones del código.

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

- La pelota rebota en los bordes superior e inferior.  
- Al chocar con una paleta, la dirección de la pelota cambia dinámicamente.  
- Si la pelota pasa una paleta, el jugador contrario suma un punto.  
- El primer jugador en alcanzar **5 puntos** gana la partida.  
- Al finalizar una partida, los resultados se guardan automáticamente en el archivo `pong_scores.json`.  

---

## 🚀 Cómo Ejecutar el Juego

### 🔹 Requisitos previos

1. Tener instalado **Python 3.8 o superior**.  
2. Instalar la librería **Pygame** ejecutando el siguiente comando:

```bash
pip install pygame


## 🧩 Estructura del Proyecto

