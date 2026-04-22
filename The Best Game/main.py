import pygame
import random
import sys
import time
import os

pygame.init()
pygame.mixer.init()

game_started = False
countdown_start = pygame.time.get_ticks()


# =========================
# SCREEN
# =========================
WIDTH, HEIGHT = 420, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("THE DUMB ZAID")

clock = pygame.time.Clock()

FONT = pygame.font.SysFont("arial", 22)
BIG = pygame.font.SysFont("arial", 42)

countdown_active = True
countdown_start = pygame.time.get_ticks()

# =========================
# COLORS
# =========================
BLUE = (135, 206, 235)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (255, 80, 80)
YELLOW = (255, 220, 0)
ORANGE = (255, 160, 60)
WHITE = (255, 255, 255)

# =========================
# SAFE AUDIO LOADER
# =========================
def load_sound(path):
    if os.path.exists(path):
        return pygame.mixer.Sound(path)
    return None

def load_music(path):
    if os.path.exists(path):
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

jump_snd = load_sound("assets/jump.wav")
score_snd = load_sound("assets/score.wav")
hit_snd = load_sound("assets/hit.wav")

load_music("assets/music.mp3")

def play(s):
    if s:
        s.play()

# =========================
# STATES
# =========================
MENU = "menu"
PLAY = "play"
CHARACTERS = "characters"
SETTINGS = "settings"
STATE_COUNTDOWN = "countdown"

state = MENU

# =========================
# MENU
# =========================
menu_buttons = [
    {"text": "Play", "rect": pygame.Rect(140, 280, 140, 40)},
    {"text": "Characters", "rect": pygame.Rect(120, 330, 180, 40)},
    {"text": "Settings", "rect": pygame.Rect(140, 380, 140, 40)}
]

menu_index = 0

# =========================
# CHARACTERS
# =========================
characters = ["Normal Zaid", "Confused Zaid", "Angry Zaid"]
selected_character = 0

# =========================
# PLAYER
# =========================
zaid_x = 90
zaid_y = HEIGHT // 2
zaid_vel = 0
gravity = 0.5

# =========================
# PIPES
# =========================
pipes = []
pipe_gap = 150
pipe_width = 70
pipe_timer = 0
score = 0

def create_pipe():
    h = random.randint(120, 380)
    return (
        pygame.Rect(WIDTH, 0, pipe_width, h),
        pygame.Rect(WIDTH, h + pipe_gap, pipe_width, HEIGHT)
    )

def move_pipes():
    for p in pipes:
        p[0].x -= 3
        p[1].x -= 3

def draw_pipes():
    for p in pipes:
        pygame.draw.rect(screen, GREEN, p[0])
        pygame.draw.rect(screen, GREEN, p[1])

def remove_pipes():
    global score
    if pipes and pipes[0][0].x < -pipe_width:
        pipes.pop(0)
        score += 1
        play(score_snd)

# =========================
# DRAW ZAID (CHARACTERS VISUAL DIFFERENCE)
# =========================
def draw_zaid(y):
    c = selected_character

    if c == 0:
        color = YELLOW
    elif c == 1:
        color = ORANGE
    else:
        color = RED

    pygame.draw.circle(screen, color, (zaid_x, int(y)), 18)

    pygame.draw.circle(screen, BLACK, (zaid_x - 6, int(y) - 5), 3)
    pygame.draw.circle(screen, BLACK, (zaid_x + 7, int(y) - 3), 3)

    pygame.draw.arc(screen, BLACK,
                    (zaid_x - 10, int(y) + 2, 22, 12),
                    3.14, 6.28, 2)

# =========================
# COLLISION
# =========================
def collision(y):
    rect = pygame.Rect(zaid_x, y, 18, 18)

    for p in pipes:
        if rect.colliderect(p[0]) or rect.colliderect(p[1]):
            play(hit_snd)
            return True

    return y < 0 or y > HEIGHT

# =========================
# RESET
# =========================
def reset():
    global zaid_y, zaid_vel, pipes, score
    zaid_y = HEIGHT // 2
    zaid_vel = 0
    pipes = []
    score = 0

# =========================
# DRAW BUTTON
# =========================
def draw_button(text, rect, active=False):
    col = GREEN if active else BLACK
    pygame.draw.rect(screen, col, rect, 2)
    screen.blit(FONT.render(text, True, col), (rect.x + 10, rect.y + 8))

def mouse_over(rect):
    return rect.collidepoint(pygame.mouse.get_pos())

# =========================
# MAIN LOOP
# =========================
running = True

while running:
    screen.fill(BLUE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

            if not game_started:
                elapsed = (pygame.time.get_ticks() - countdown_start) / 1000
                number = 3 - int(elapsed)

                if number > 0:
                    text = FONT.render(str(number), True, (255, 255, 255))

                elif number == 0:
                    text = FONT.render("GO!", True, (255, 255, 255))

                else:
                    game_started = True

                if not game_started:
                    rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                    screen.blit(text, rect)

                    pygame.display.update()
                    clock.tick(60)

                    continue



        # =========================
        # MOUSE
        # =========================
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()

            if state == MENU:
                for i, b in enumerate(menu_buttons):
                    if b["rect"].collidepoint((mx, my)):
                        if i == 0:
                            state = PLAY
                        elif i == 1:
                            state = CHARACTERS
                        elif i == 2:
                            state = SETTINGS

            if state == CHARACTERS:
                for i in range(3):
                    if 260 + i * 40 < my < 290 + i * 40:
                        selected_character = i

        # =========================
        # KEYBOARD
        # =========================
        if event.type == pygame.KEYDOWN:

            if state == MENU:
                if event.key == pygame.K_DOWN:
                    menu_index = (menu_index + 1) % len(menu_buttons)
                if event.key == pygame.K_UP:
                    menu_index = (menu_index - 1) % len(menu_buttons)
                if event.key == pygame.K_RETURN:
                    state = ["play", "characters", "settings"][menu_index]

            elif state == PLAY:
                if event.key == pygame.K_SPACE:
                    zaid_vel = -8
                    play(jump_snd)

            elif state == CHARACTERS:
                if event.key == pygame.K_LEFT:
                    selected_character = (selected_character - 1) % 3
                if event.key == pygame.K_RIGHT:
                    selected_character = (selected_character + 1) % 3

            if event.key == pygame.K_ESCAPE:
                state = MENU

    # =========================
    # MENU
    # =========================
    if state == MENU:
        screen.blit(BIG.render("THE DUMB ZAID", True, BLACK), (60, 150))

        for i, b in enumerate(menu_buttons):
            active = (i == menu_index)
            if mouse_over(b["rect"]):
                menu_index = i
                active = True
            draw_button(b["text"], b["rect"], active)

        pygame.display.update()
        continue

    # =========================
    # CHARACTERS SCREEN (FIXED VISUAL)
    # =========================
    if state == CHARACTERS:
        screen.blit(BIG.render("CHARACTERS", True, BLACK), (100, 120))

        for i, name in enumerate(characters):
            rect = pygame.Rect(90, 260 + i * 40, 240, 30)

            active = (i == selected_character)

            if rect.collidepoint(pygame.mouse.get_pos()):
                selected_character = i
                active = True

            pygame.draw.rect(screen, GREEN if active else BLACK, rect, 2)
            screen.blit(FONT.render(name, True, BLACK), (100, 265 + i * 40))

        pygame.display.update()
        continue

    # =========================
    # SETTINGS
    # =========================
    if state == SETTINGS:
        screen.blit(BIG.render("SETTINGS", True, BLACK), (120, 200))
        screen.blit(FONT.render("Nothing here yet", True, BLACK), (120, 300))
        pygame.display.update()
        continue

    # =========================
    # GAMEPLAY
    # =========================
    zaid_vel += gravity
    zaid_y += zaid_vel

    pipe_timer += 1
    if pipe_timer > 90:
        pipes.append(create_pipe())
        pipe_timer = 0

    move_pipes()
    remove_pipes()

    if collision(zaid_y):
        reset()
        state = MENU

    draw_pipes()
    draw_zaid(zaid_y)

    screen.blit(FONT.render(f"Score: {score}", True, BLACK), (10, 10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()