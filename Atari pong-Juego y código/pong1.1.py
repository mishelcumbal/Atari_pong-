# pong.py - Juego tipo Atari Pong en Python usando Pygame
# Controles:
# Jugador izquierdo: W (arriba), S (abajo)
# Jugador derecho: Flechas arriba/abajo
# i - alternar IA (jugador derecho)
# Space - pausar / reanudar
# R - reiniciar marcador y posición
# Esc - salir

import pygame
import sys
import random
import json
import os

# --------- Configuración ---------
WIDTH, HEIGHT = 900, 500
FPS = 60
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 16
PADDLE_SPEED = 6
BALL_SPEED = 6
WINNING_SCORE = 5
FONT_NAME = None

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
LIGHT_BLUE = (100, 150, 255)
DARK_GRAY = (50, 50, 50)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong - Atari Style")
clock = pygame.time.Clock()
font = pygame.font.SysFont(FONT_NAME, 36)
small_font = pygame.font.SysFont(FONT_NAME, 20)
title_font = pygame.font.SysFont(FONT_NAME, 48)

# Archivo para guardar puntuaciones
SCORES_FILE = "pong_scores.json"

# --------- Funciones para manejar puntuaciones ---------
def load_scores():
    if os.path.exists(SCORES_FILE):
        try:
            with open(SCORES_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_score(player1, player2, score1, score2):
    scores = load_scores()
    
    # Determinar ganador
    if score1 > score2:
        winner = player1
        loser = player2
    else:
        winner = player2
        loser = player1
    
    # Añadir nueva puntuación
    scores.append({
        "player1": player1,
        "player2": player2,
        "score1": score1,
        "score2": score2,
        "winner": winner,
        "loser": loser,
        "date": pygame.time.get_ticks()  # Usamos ticks como timestamp simple
    })
    
    # Guardar
    with open(SCORES_FILE, 'w') as f:
        json.dump(scores, f)

# --------- Clases ---------
class Button:
    def __init__(self, x, y, width, height, text, color=LIGHT_BLUE, hover_color=WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        
    def draw(self, surf):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surf, color, self.rect, border_radius=5)
        pygame.draw.rect(surf, WHITE, self.rect, 2, border_radius=5)
        
        text_surf = font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surf.blit(text_surf, text_rect)
        
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered
        
    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

class InputBox:
    def __init__(self, x, y, width, height, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.active = False
        self.color_inactive = GRAY
        self.color_active = WHITE
        self.color = self.color_inactive
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = self.color_active if self.active else self.color_inactive
            
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return True
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    # Limitar la longitud del texto para que quepa en el cuadro
                    if len(self.text) < 15:  # Máximo 15 caracteres
                        self.text += event.unicode
        return False
                    
    def draw(self, surf):
        # Dibujar el fondo del cuadro de texto
        pygame.draw.rect(surf, DARK_GRAY, self.rect, border_radius=5)
        pygame.draw.rect(surf, self.color, self.rect, 2, border_radius=5)
        
        # Renderizar el texto
        text_surf = small_font.render(self.text, True, WHITE)
        
        # Calcular la posición del texto para que esté centrado verticalmente
        text_y = self.rect.y + (self.rect.height - text_surf.get_height()) // 2
        
        # Si el texto es demasiado largo, mostrar la parte final
        if text_surf.get_width() > self.rect.width - 10:
            # Crear una superficie para recortar el texto
            cropped_text = pygame.Surface((self.rect.width - 10, text_surf.get_height()))
            cropped_text.fill(DARK_GRAY)
            # Dibujar solo la parte final del texto
            cropped_text.blit(text_surf, (self.rect.width - 10 - text_surf.get_width(), 0))
            surf.blit(cropped_text, (self.rect.x + 5, text_y))
        else:
            surf.blit(text_surf, (self.rect.x + 5, text_y))
        
        # Dibujar cursor parpadeante si está activo
        if self.active and pygame.time.get_ticks() % 1000 < 500:
            cursor_x = self.rect.x + 5 + small_font.render(self.text, True, WHITE).get_width()
            pygame.draw.line(surf, WHITE, 
                           (cursor_x, self.rect.y + 5),
                           (cursor_x, self.rect.y + self.rect.height - 5), 2)
        
        # Dibujar texto de placeholder si está vacío y no activo
        if not self.text and not self.active:
            placeholder_surf = small_font.render("Escribe aquí...", True, GRAY)
            placeholder_y = self.rect.y + (self.rect.height - placeholder_surf.get_height()) // 2
            surf.blit(placeholder_surf, (self.rect.x + 5, placeholder_y))

class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = 0

    def move(self, dy):
        self.rect.y += dy
        self.rect.y = max(0, min(HEIGHT - PADDLE_HEIGHT, self.rect.y))

    def update(self):
        self.move(self.speed)

    def draw(self, surf):
        pygame.draw.rect(surf, WHITE, self.rect)

class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)
        self.reset()

    def reset(self, direction=None):
        self.rect.center = (WIDTH//2, HEIGHT//2)
        dir_x = random.choice([-1, 1]) if direction is None else direction
        angle = random.uniform(-0.7, 0.7)
        self.vx = BALL_SPEED * dir_x
        self.vy = BALL_SPEED * angle

    def update(self, left_paddle, right_paddle):
        self.rect.x += int(self.vx)
        self.rect.y += int(self.vy)

        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.vy = -self.vy

        if self.rect.colliderect(left_paddle.rect):
            offset = (self.rect.centery - left_paddle.rect.centery) / (PADDLE_HEIGHT / 2)
            self.vx = abs(self.vx)
            self.vy = BALL_SPEED * offset
            self.rect.left = left_paddle.rect.right

        if self.rect.colliderect(right_paddle.rect):
            offset = (self.rect.centery - right_paddle.rect.centery) / (PADDLE_HEIGHT / 2)
            self.vx = -abs(self.vx)
            self.vy = BALL_SPEED * offset
            self.rect.right = right_paddle.rect.left

    def draw(self, surf):
        pygame.draw.ellipse(surf, WHITE, self.rect)

# --------- Funciones de pantalla ---------
def show_menu():
    # Botones del menú
    start_button = Button(WIDTH//2 - 100, HEIGHT//2 - 50, 200, 50, "Iniciar Juego")
    scores_button = Button(WIDTH//2 - 100, HEIGHT//2 + 20, 200, 50, "Puntuaciones")
    quit_button = Button(WIDTH//2 - 100, HEIGHT//2 + 90, 200, 50, "Salir")
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
                
            if start_button.is_clicked(mouse_pos, event):
                return "start"
            if scores_button.is_clicked(mouse_pos, event):
                return "scores"
            if quit_button.is_clicked(mouse_pos, event):
                pygame.quit()
                sys.exit()
                
        # Actualizar estado de botones
        start_button.check_hover(mouse_pos)
        scores_button.check_hover(mouse_pos)
        quit_button.check_hover(mouse_pos)
        
        # Dibujar
        screen.fill(BLACK)
        
        # Título
        title_surf = title_font.render("PONG", True, WHITE)
        screen.blit(title_surf, (WIDTH//2 - title_surf.get_width()//2, 100))
        
        # Botones
        start_button.draw(screen)
        scores_button.draw(screen)
        quit_button.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)

def show_scores():
    back_button = Button(WIDTH//2 - 100, HEIGHT - 80, 200, 50, "Volver")
    scores = load_scores()
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
                
            if back_button.is_clicked(mouse_pos, event):
                return
                
        # Actualizar estado de botones
        back_button.check_hover(mouse_pos)
        
        # Dibujar
        screen.fill(BLACK)
        
        # Título
        title_surf = title_font.render("PUNTUACIONES", True, WHITE)
        screen.blit(title_surf, (WIDTH//2 - title_surf.get_width()//2, 50))
        
        # Mostrar puntuaciones
        if not scores:
            no_scores = font.render("No hay puntuaciones guardadas", True, WHITE)
            screen.blit(no_scores, (WIDTH//2 - no_scores.get_width()//2, HEIGHT//2))
        else:
            # Mostrar las últimas 10 puntuaciones
            y_pos = 120
            for i, score in enumerate(scores[-10:]):  # Mostrar las 10 más recientes
                score_text = f"{score['player1']} {score['score1']} - {score['score2']} {score['player2']} (Ganó: {score['winner']})"
                score_surf = small_font.render(score_text, True, WHITE)
                screen.blit(score_surf, (WIDTH//2 - score_surf.get_width()//2, y_pos))
                y_pos += 30
                
                if y_pos > HEIGHT - 100:
                    break
        
        # Botón volver
        back_button.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)

def get_player_names():
    player1_box = InputBox(WIDTH//2 - 100, HEIGHT//2 - 60, 200, 40)
    player2_box = InputBox(WIDTH//2 - 100, HEIGHT//2 + 10, 200, 40)
    start_button = Button(WIDTH//2 - 100, HEIGHT//2 + 80, 200, 50, "Comenzar")
    
    player1_name = "Jugador 1"
    player2_name = "Jugador 2"
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return None, None
                
            # Manejar entrada de texto
            player1_box.handle_event(event)
            player2_box.handle_event(event)
            
            # Verificar si se presionó el botón
            if start_button.is_clicked(mouse_pos, event):
                player1_name = player1_box.text if player1_box.text else "Jugador 1"
                player2_name = player2_box.text if player2_box.text else "Jugador 2"
                return player1_name, player2_name
                
        # Actualizar estado de botones
        start_button.check_hover(mouse_pos)
        
        # Dibujar
        screen.fill(BLACK)
        
        # Título
        title_surf = title_font.render("NOMBRES DE JUGADORES", True, WHITE)
        screen.blit(title_surf, (WIDTH//2 - title_surf.get_width()//2, 100))
        
        # Etiquetas
        player1_label = font.render("Jugador 1:", True, WHITE)
        player2_label = font.render("Jugador 2:", True, WHITE)
        
        screen.blit(player1_label, (WIDTH//3 - 150, HEIGHT//2 - 55))
        screen.blit(player2_label, (WIDTH//3 - 150, HEIGHT//2 + 15))
        
        # Cajas de entrada
        player1_box.draw(screen)
        player2_box.draw(screen)
        
        # Botón
        start_button.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)

def draw_net():
    for y in range(0, HEIGHT, 20):
        if (y // 20) % 2 == 0:
            pygame.draw.rect(screen, WHITE, (WIDTH//2 - 2, y, 4, 12))

def draw_scores(player1_name, player2_name, score_left, score_right):
    # Nombres de jugadores
    name1_surf = small_font.render(player1_name, True, WHITE)
    name2_surf = small_font.render(player2_name, True, WHITE)
    
    screen.blit(name1_surf, (WIDTH//4 - name1_surf.get_width()//2, 10))
    screen.blit(name2_surf, (3*WIDTH//4 - name2_surf.get_width()//2, 10))
    
    # Puntuaciones
    left_surf = font.render(str(score_left), True, WHITE)
    right_surf = font.render(str(score_right), True, WHITE)
    
    screen.blit(left_surf, (WIDTH//4 - left_surf.get_width()//2, 40))
    screen.blit(right_surf, (3*WIDTH//4 - right_surf.get_width()//2, 40))

def reset_game():
    global score_left, score_right, winner, paused, winner_timer
    score_left = 0
    score_right = 0
    winner = None
    winner_timer = 0
    paused = False
    left.rect.y = HEIGHT//2 - PADDLE_HEIGHT//2
    right.rect.y = HEIGHT//2 - PADDLE_HEIGHT//2
    ball.reset()

def ai_move(paddle, ball):
    if ball.rect.centery < paddle.rect.centery - 10:
        paddle.move(-PADDLE_SPEED + 1)
    elif ball.rect.centery > paddle.rect.centery + 10:
        paddle.move(PADDLE_SPEED - 1)

# --------- Bucle principal ---------
def main():
    global score_left, score_right, paused, use_ai, winner, winner_timer, left, right, ball
    
    # Inicializar objetos del juego
    left = Paddle(20, HEIGHT//2 - PADDLE_HEIGHT//2)
    right = Paddle(WIDTH - 20 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2)
    ball = Ball()
    
    # Variables del juego
    score_left = 0
    score_right = 0
    paused = False
    use_ai = False
    winner = None
    winner_timer = 0
    
    # Nombres de jugadores
    player1_name = "Jugador 1"
    player2_name = "Jugador 2"
    
    # Menú principal
    while True:
        menu_choice = show_menu()
        
        if menu_choice == "start":
            # Obtener nombres de jugadores
            names = get_player_names()
            if names is None:  # Si se presionó ESC
                continue
                
            player1_name, player2_name = names
            
            # Reiniciar juego
            reset_game()
            
            # Bucle del juego
            game_loop(player1_name, player2_name)
            
        elif menu_choice == "scores":
            show_scores()

def game_loop(player1_name, player2_name):
    global score_left, score_right, paused, use_ai, winner, winner_timer
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Guardar puntuación actual y volver al menú
                    if score_left > 0 or score_right > 0:
                        save_score(player1_name, player2_name, score_left, score_right)
                    return
                if event.key == pygame.K_w:
                    left.speed = -PADDLE_SPEED
                if event.key == pygame.K_s:
                    left.speed = PADDLE_SPEED
                if event.key == pygame.K_UP:
                    right.speed = -PADDLE_SPEED
                if event.key == pygame.K_DOWN:
                    right.speed = PADDLE_SPEED
                if event.key == pygame.K_SPACE:
                    paused = not paused
                if event.key == pygame.K_i:
                    use_ai = not use_ai
                if event.key == pygame.K_r:
                    reset_game()

            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_w, pygame.K_s):
                    left.speed = 0
                if event.key in (pygame.K_UP, pygame.K_DOWN):
                    right.speed = 0

        if not paused:
            if winner is None:
                left.update()
                if use_ai:
                    ai_move(right, ball)
                else:
                    right.update()

                ball.update(left, right)

                if ball.rect.right < 0:
                    score_right += 1
                    ball.reset(direction=1)
                    if score_right >= WINNING_SCORE:
                        winner = player2_name
                        winner_timer = pygame.time.get_ticks()
                        # Guardar puntuación
                        save_score(player1_name, player2_name, score_left, score_right)

                if ball.rect.left > WIDTH:
                    score_left += 1
                    ball.reset(direction=-1)
                    if score_left >= WINNING_SCORE:
                        winner = player1_name
                        winner_timer = pygame.time.get_ticks()
                        # Guardar puntuación
                        save_score(player1_name, player2_name, score_left, score_right)

            else:
                # Reinicia automáticamente tras 3 segundos
                if pygame.time.get_ticks() - winner_timer > 3000:
                    reset_game()

        # Dibujar todo
        screen.fill(BLACK)
        draw_net()
        left.draw(screen)
        right.draw(screen)
        ball.draw(screen)
        draw_scores(player1_name, player2_name, score_left, score_right)
        
        # Mostrar controles
        controls_text = "Controles: W/S (Izq), Flechas (Der), ESPACIO (Pausa), I (IA), R (Reiniciar), ESC (Menú)"
        controls_surf = small_font.render(controls_text, True, GRAY)
        screen.blit(controls_surf, (WIDTH//2 - controls_surf.get_width()//2, HEIGHT - 30))

        if winner:
            msg = font.render(f"GANADOR: {winner}", True, WHITE)
            screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 - msg.get_height()//2))
            sub = small_font.render("Reiniciando juego...", True, WHITE)
            screen.blit(sub, (WIDTH//2 - sub.get_width()//2, HEIGHT//2 + 30))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()