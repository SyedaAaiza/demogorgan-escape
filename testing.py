import os
import sys
import pygame
from obstacle import ObstacleManager
from movement.will_move import PlayerRunner

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stranger Things - Runner")
clock = pygame.time.Clock()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
BG_PATH = os.path.join(ASSETS_DIR, "BG2.jpeg")

try:
    background = pygame.image.load(BG_PATH).convert()
    background = pygame.transform.smoothscale(background, (WIDTH * 2, HEIGHT * 2))
except pygame.error:
    print(f"Error: Could not load background at {BG_PATH}")
    sys.exit()

zoom = 1.0
ZOOM_SPEED = 0.0004535
MAX_ZOOM = 1.735

player_runner = PlayerRunner(WIDTH, HEIGHT)
obstacle_manager = ObstacleManager(WIDTH, HEIGHT)

LANE_RATIOS = [
    {"top_x": 0.435, "bottom_x": 0.22, "top_y": 0.38},
    {"top_x": 0.498, "bottom_x": 0.475, "top_y": 0.38},
    {"top_x": 0.565, "bottom_x": 0.74, "top_y": 0.38},
]

running = True
game_over = False
font = pygame.font.SysFont(None, 50)

while running:
    dt = clock.tick(60)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                game_over = False
                obstacle_manager.obstacles.clear()
                zoom = 1.0

    if not game_over:
        zoom += ZOOM_SPEED * dt
        if zoom >= MAX_ZOOM:
            zoom = 1.0

        scaled_width = int(WIDTH * zoom)
        scaled_height = int(HEIGHT * zoom)
        zoomed_bg = pygame.transform.smoothscale(background, (scaled_width, scaled_height))
        x = (WIDTH - scaled_width) // 2
        y = int((HEIGHT - scaled_height) // 2 + (zoom - 1.0) * 300)

        screen_lanes = []
        horizon_y_screen = 0
        for ratio in LANE_RATIOS:
            top_x_screen = x + int(ratio["top_x"] * scaled_width)
            bottom_x_screen = x + int(ratio["bottom_x"] * scaled_width)
            top_y_screen = y + int(ratio["top_y"] * scaled_height)
            screen_lanes.append({"top_x": top_x_screen, "bottom_x": bottom_x_screen})
            horizon_y_screen = top_y_screen

        obstacle_manager.lane_positions = screen_lanes
        obstacle_manager.HORIZON_Y = horizon_y_screen
        obstacle_manager.update_and_spawn(dt)
        player_runner.update(events)

        # --- PLAYER RECT GET KAREIN ---
        if hasattr(player_runner, 'get_rect'):
            player_rect = player_runner.get_rect()
        elif hasattr(player_runner, 'rect'):
            player_rect = player_runner.rect
        else:
            px = getattr(player_runner, 'char_x', getattr(player_runner, 'x', WIDTH // 2))
            py = getattr(player_runner, 'y', getattr(player_runner, 'player_y', HEIGHT - 150))
            player_rect = pygame.Rect(px + 30, py + 10, 70, 120)

        # --- RECT COLLISION CHECK ---
        if obstacle_manager.check_collision(player_rect):
            game_over = True

        screen.blit(zoomed_bg, (x, y))
        obstacle_manager.draw(screen)
        player_runner.draw(screen)

    else:
        text = font.render("HIT! GAME OVER - Press R to Restart", True, (255, 200, 0))
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 20))

    pygame.display.flip()

pygame.quit()
sys.exit()