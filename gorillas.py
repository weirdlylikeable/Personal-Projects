from raylibpy import *
import numpy as np
from random import randint

# Constants
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
MAX_BUILDINGS = 15
MAX_EXPLOSIONS = 200
MAX_PLAYERS = 2

BUILDING_RELATIVE_ERROR = 30
BUILDING_MIN_RELATIVE_HEIGHT = 20
BUILDING_MAX_RELATIVE_HEIGHT = 60
BUILDING_MIN_GRAYSCALE_COLOR = 120
BUILDING_MAX_GRAYSCALE_COLOR = 200

GRAVITY = 9.81
DELTA_FPS = 60.0

# Data classes
class Player:
    def __init__(self):
        self.position = Vector2(0, 0)
        self.size = Vector2(40, 40)
        self.aiming_point = Vector2(0, 0)
        self.aiming_angle = 0
        self.aiming_power = 0
        self.previous_point = Vector2(0, 0)
        self.previous_angle = 0
        self.previous_power = 0
        self.impact_point = Vector2(-100, -100)
        self.is_left_team = True
        self.is_player = True
        self.is_alive = True

class Building:
    def __init__(self):
        self.rect = Rectangle(0, 0, 0, 0)
        self.color = Color(0, 0, 0, 255)

class Explosion:
    def __init__(self):
        self.position = Vector2(0, 0)
        self.radius = 30
        self.active = False

class Ball:
    def __init__(self):
        self.position = Vector2(0, 0)
        self.speed = Vector2(0, 0)
        self.radius = 10
        self.active = False

# Globals
buildings = [Building() for _ in range(MAX_BUILDINGS)]
players = [Player() for _ in range(MAX_PLAYERS)]
explosions = [Explosion() for _ in range(MAX_EXPLOSIONS)]
ball = Ball()
player_turn = 0
ball_on_air = False
game_over = False
pause = False
explosion_index = 0
explosion_sound = True
explosion_audio = "C:\Programming\Gorillas Raylib in Python\explosion-9-340460.mp3"

# Initialization functions
def init_buildings():
    current_width = 0
    relative_width = 100 / (100 - BUILDING_RELATIVE_ERROR)
    building_width_mean = int(SCREEN_WIDTH * relative_width / MAX_BUILDINGS) + 1

    for b in buildings:
        b.rect.x = current_width
        b.rect.width = randint(
            int(building_width_mean * (100 - BUILDING_RELATIVE_ERROR / 2) / 100 + 1),
            int(building_width_mean * (100 + BUILDING_RELATIVE_ERROR) / 100),
        )
        current_width += int(b.rect.width)

        height_percent = randint(BUILDING_MIN_RELATIVE_HEIGHT, BUILDING_MAX_RELATIVE_HEIGHT)
        b.rect.height = SCREEN_HEIGHT * height_percent / 100 + 1
        b.rect.y = SCREEN_HEIGHT - b.rect.height

        gray = randint(BUILDING_MIN_GRAYSCALE_COLOR, BUILDING_MAX_GRAYSCALE_COLOR)
        b.color = Color(gray, gray, gray, 255)

def init_players():
    spacing = len(buildings) // MAX_PLAYERS
    for i, p in enumerate(players):
        p.is_alive = True
        p.is_left_team = (i % 2 == 0)
        p.is_player = True

        b = buildings[i * spacing]
        p.position.x = b.rect.x + b.rect.width / 2
        p.position.y = b.rect.y - p.size.y / 2

        p.aiming_point = Vector2(p.position.x, p.position.y)
        p.previous_point = Vector2(p.position.x, p.position.y)

def draw_predicted_path(p):
        angle = np.radians(p.aiming_angle)
        power = p.aiming_power * 3 / DELTA_FPS
        direction = 1 if p.is_left_team else -1

        pos = np.array([p.position.x, p.position.y], dtype=float)
        vel = np.array([direction * np.cos(angle) * power, -np.sin(angle) * power])

        for _ in range(15): 
            if abs(pos[0] - p.position.x) > SCREEN_WIDTH / 2:
                break
        
            draw_circle(int(pos[0]), int(pos[1]), 5, DARKGRAY)
            pos += vel
            vel[1] += GRAVITY / DELTA_FPS

def update_player(turn):
    global ball
    p = players[turn]
    mouse = get_mouse_position()

    if mouse.y <= p.position.y:
        dx, dy = mouse.x - p.position.x, p.position.y - mouse.y
        dist = np.sqrt(dx**2 + dy**2)

        if (p.is_left_team and dx >= 0) or (not p.is_left_team and dx <= 0):
            p.aiming_power = dist
            p.aiming_angle = np.degrees(np.arcsin(dy / dist))
            p.aiming_point = mouse

            if is_mouse_button_pressed(MOUSE_LEFT_BUTTON):
                p.previous_angle = p.aiming_angle
                p.previous_power = p.aiming_power
                p.previous_point = p.aiming_point
                ball.position = Vector2(p.position.x, p.position.y)
                return True

    return False

def update_ball(turn):
    global explosion_index
    if not ball.active:
        angle = np.radians(players[turn].previous_angle)
        power = players[turn].previous_power * 3 / DELTA_FPS
        direction = 1 if players[turn].is_left_team else -1

        ball.speed.x = direction * np.cos(angle) * power
        ball.speed.y = -np.sin(angle) * power
        ball.active = True

    ball.position.x += ball.speed.x
    ball.position.y += ball.speed.y
    ball.speed.y += GRAVITY / DELTA_FPS

    if ball.position.x + ball.radius < 0 or ball.position.x - ball.radius > SCREEN_WIDTH:
        return True

    for i, p in enumerate(players):
        if check_collision_circle_rec(ball.position, ball.radius, Rectangle(p.position.x - p.size.x/2, p.position.y - p.size.y/2, p.size.x, p.size.y)):
            if i != turn:
                p.is_alive = False
                return True

    for e in explosions:
        if e.active and check_collision_circles(ball.position, ball.radius, e.position, e.radius - ball.radius):
            return False

    for b in buildings:
        if check_collision_circle_rec(ball.position, ball.radius, b.rect):
            explosions[explosion_index % MAX_EXPLOSIONS].position = Vector2(ball.position.x, ball.position.y)
            explosions[explosion_index % MAX_EXPLOSIONS].active = True
            if explosion_sound: play_sound(explosion_sound)
            explosion_index += 1
            return True

    return False

def update_game():
    global ball_on_air, player_turn, game_over, pause
    if is_key_pressed(KEY_P):
        pause = not pause

    if not game_over and not pause:
        if not ball_on_air:
            ball_on_air = update_player(player_turn)
        else:
            if update_ball(player_turn):
                ball_on_air = False
                ball.active = False
                if not any(p.is_alive and p.is_left_team for p in players) or not any(p.is_alive and not p.is_left_team for p in players):
                    game_over = True
                else:
                    player_turn = (player_turn + 1) % MAX_PLAYERS
    elif game_over and is_key_pressed(KEY_ENTER):
        init_game()
        game_over = False

def draw_game():
    begin_drawing()
    clear_background(RAYWHITE)

    for b in buildings:
        draw_rectangle_rec(b.rect, b.color)
    for e in explosions:
        if e.active:
            draw_circle_v(e.position, e.radius, RAYWHITE)
    for p in players:
        if p.is_alive:
            color = BLUE if p.is_left_team else RED
            draw_rectangle(int(p.position.x - p.size.x/2), int(p.position.y - p.size.y/2), int(p.size.x), int(p.size.y), color)
            draw_predicted_path(p)
    if ball.active:
        draw_circle_v(ball.position, ball.radius, MAROON)

    if game_over:
        draw_text("PRESS [ENTER] TO PLAY AGAIN", SCREEN_WIDTH//2 - measure_text("PRESS [ENTER] TO PLAY AGAIN", 20)//2, SCREEN_HEIGHT//2 - 50, 20, GRAY)
    elif pause:
        draw_text("GAME PAUSED", SCREEN_WIDTH//2 - measure_text("GAME PAUSED", 40)//2, SCREEN_HEIGHT//2 - 40, 40, GRAY)

    end_drawing()

def init_game():
    global ball_on_air, player_turn, game_over, explosion_index
    ball_on_air = False
    player_turn = 0
    game_over = False
    explosion_index = 0
    ball.__init__()
    for e in explosions:
        e.__init__()
    init_buildings()
    init_players()

def main():
    global explosion_sound
    init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Gorillas, in Python")
    init_audio_device()
    explosion_sound = load_sound(explosion_audio)
    set_target_fps(60)
    init_game()
    while not window_should_close():
        update_game()
        draw_game()
    unload_sound(explosion_sound)
    close_audio_device()
    close_window()

if __name__ == "__main__":
    main()
