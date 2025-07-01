from raylibpy import *
import numpy as np
from random import uniform, choice

# Constants and Globals
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
DELTA_FPS = 60.0
DELTA_TIME = 1.0 / DELTA_FPS
GRAVITY_MULTIPLIER = 100.0
NUM_GRAVITY_OBJECTS = 3
PLAYER_RADIUS = 50
BALL_RADIUS = 10
GRAVITY_COLORS = [YELLOW, ORANGE, VIOLET, GREEN, SKYBLUE]

# Classes and Initialization Functions
class Player:
    def __init__(self, x_range):
        self.radius = PLAYER_RADIUS
        min_y = SCREEN_HEIGHT * 0.5
        max_y = SCREEN_HEIGHT - 100
        x = uniform(x_range[0], x_range[1])
        y = uniform(min_y, max_y)
        x = max(self.radius, min(x, SCREEN_WIDTH - self.radius))
        y = max(self.radius, min(y, SCREEN_HEIGHT - self.radius))
        self.position = Vector2(x, y)
        self.aiming_point = Vector2(0, 0)
        self.aiming_angle = 0
        self.aiming_power = 0
        self.previous_point = Vector2(0, 0)
        self.previous_angle = 0
        self.previous_power = 0
        self.is_left_team = True
        self.is_player = True
        self.is_alive = True

class Ball:
    def __init__(self):
        self.position = Vector2(0, 0)
        self.speed = Vector2(0, 0)
        self.radius = BALL_RADIUS
        self.active = False

class FloatingObject:
    def __init__(self, x_range, gravity_source=False):
        self.radius = uniform(25, 75)
        self.position = Vector2(uniform(x_range[0], x_range[1]), uniform(100, SCREEN_HEIGHT - 100))
        self.gravity_source = gravity_source
        self.mass = self.radius * 100 if gravity_source else 0
        self.color = choice(GRAVITY_COLORS) if gravity_source else RAYWHITE

    def draw(self):
        draw_circle_v(self.position, self.radius, self.color)

players = []
floating_objects = []
ball = Ball()
player_turn = 0
ball_on_air = False
game_over = False
pause = False
trajectory_points = []

def init_players():
    players.clear()
    players.append(Player((0, SCREEN_WIDTH * 0.15)))
    players[-1].is_left_team = True
    players.append(Player((SCREEN_WIDTH * 0.85, SCREEN_WIDTH)))
    players[-1].is_left_team = False
    for p in players:
        p.aiming_point = Vector2(p.position.x, p.position.y)
        p.previous_point = Vector2(p.position.x, p.position.y)

def draw_predicted_path(p):
    angle = np.radians(p.aiming_angle)
    power = p.aiming_power * 3 / DELTA_FPS
    direction = 1 if p.is_left_team else -1
    pos = np.array([p.position.x, p.position.y], dtype=float)
    vel = np.array([direction * np.cos(angle) * power, -np.sin(angle) * power])
    for _ in range(15): 
        draw_circle(int(pos[0]), int(pos[1]), 4, DARKGRAY)
        pos += vel

def update_player(turn):
    global ball
    p = players[turn]
    mouse = get_mouse_position()
    dx = mouse.x - p.position.x
    dy = p.position.y - mouse.y
    dist = np.sqrt(dx**2 + dy**2)
    if dist > 0:
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
    global ball_on_air, player_turn, trajectory_points
    if not ball.active:
        angle = np.radians(players[turn].previous_angle)
        power = players[turn].previous_power * 1.5 / DELTA_FPS
        direction = 1 if players[turn].is_left_team else -1
        ball.speed.x = direction * np.cos(angle) * power
        ball.speed.y = -np.sin(angle) * power
        ball.active = True
        trajectory_points = []
    for obj in floating_objects:
        if obj.gravity_source:
            dx = obj.position.x - ball.position.x
            dy = obj.position.y - ball.position.y
            dist_sq = dx**2 + dy**2
            if dist_sq < 1: 
                dist_sq = 1
            force = GRAVITY_MULTIPLIER * obj.mass / dist_sq
            norm = np.sqrt(dist_sq)
            ax = force * dx / norm
            ay = force * dy / norm
            ball.speed.x += ax * DELTA_TIME
            ball.speed.y += ay * DELTA_TIME

    ball.position.x += ball.speed.x
    ball.position.y += ball.speed.y
    trajectory_points.append(Vector2(ball.position.x, ball.position.y))
    if ball.position.x + ball.radius < 0 or ball.position.x - ball.radius > SCREEN_WIDTH:
        ball_on_air = False
        ball.active = False
        player_turn = (player_turn + 1) % len(players)
        return
    for i, p in enumerate(players):
        if p.is_alive and check_collision_circles(ball.position, ball.radius, p.position, p.radius):
            if i != turn:
                p.is_alive = False
                ball_on_air = False
                ball.active = False
                player_turn = (player_turn + 1) % len(players)
                return
    for obj in floating_objects:
        if obj.gravity_source and check_collision_circles(ball.position, ball.radius, obj.position, obj.radius):
            obj.mass *= 0.9
            ball_on_air = False
            ball.active = False
            player_turn = (player_turn + 1) % len(players)
            return

def update_game():
    global ball_on_air, game_over, pause
    if is_key_pressed(KEY_P): pause = not pause
    if not game_over and not pause:
        if not ball_on_air:
            ball_on_air = update_player(player_turn)
        else:
            update_ball(player_turn)
        left_alive = any(p.is_alive and p.is_left_team for p in players)
        right_alive = any(p.is_alive and not p.is_left_team for p in players)
        if not (left_alive and right_alive):
            game_over = True
    elif game_over and is_key_pressed(KEY_ENTER):
        init_game()
        game_over = False

def draw_game():
    begin_drawing()
    clear_background(BLACK)
    for obj in floating_objects:
        obj.draw()
    for p in players:
        if p.is_alive:
            color = BLUE if p.is_left_team else RED
            draw_circle_v(p.position, p.radius, color)
            draw_predicted_path(p)
    for point in trajectory_points:
        draw_circle_v(point, 3, GRAY)
    if ball.active:
        draw_circle_v(ball.position, ball.radius, MAROON)
    if game_over:
        txt = "PRESS [ENTER] TO PLAY AGAIN"
        draw_text(txt, SCREEN_WIDTH//2 - measure_text(txt, 20)//2, SCREEN_HEIGHT//2 - 50, 20, GRAY)
    elif pause:
        txt = "GAME PAUSED"
        draw_text(txt, SCREEN_WIDTH//2 - measure_text(txt, 40)//2, SCREEN_HEIGHT//2 - 40, 40, GRAY)
    end_drawing()

def init_game():
    global ball_on_air, player_turn, game_over, trajectory_points
    ball_on_air = False
    player_turn = 0
    game_over = False
    trajectory_points = []
    ball.__init__()
    floating_objects.clear()
    margin = SCREEN_WIDTH * 0.15
    attempts = 0
    min_distance_from_players = SCREEN_WIDTH * 0.05
    while len(floating_objects) < NUM_GRAVITY_OBJECTS and attempts < 100:
        attempts += 1
        new_obj = FloatingObject((margin + 100, SCREEN_WIDTH - margin - 100), gravity_source=True)
        overlap = False
        for obj in floating_objects:
            dx = obj.position.x - new_obj.position.x
            dy = obj.position.y - new_obj.position.y
            dist_sq = dx**2 + dy**2
            min_dist = obj.radius + new_obj.radius + 10
            if dist_sq < min_dist**2:
                overlap = True
                break
        for p in players:
            if abs(new_obj.position.x - p.position.x) < min_distance_from_players:
                overlap = True
                break
        if not overlap:
            floating_objects.append(new_obj)
    init_players()

def main():
    init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Planetary Pathing")
    set_target_fps(60)
    init_game()
    while not window_should_close():
        update_game()
        draw_game()
    close_window()

if __name__ == "__main__":
    main()
