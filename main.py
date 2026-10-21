import os
import sys
from obstacle import ObstacleManager
from movement.will_move import PlayerRunner

import pygame

pygame.init()

# --- Screen Settings ---
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(
    "Stranger Things - Upside Down Runner (Character & Background Only)"
)

clock = pygame.time.Clock()

# --- Assets Setup ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
BG_PATH = os.path.join(ASSETS_DIR, "BG2.jpeg")

# Load Background
try:
    background = pygame.image.load(BG_PATH).convert()
    # Scale background to be larger initially for zooming effect
    background = pygame.transform.smoothscale(background, (WIDTH * 2, HEIGHT * 2))
except pygame.error:
    print(f"Error: Could not load background image at {BG_PATH}")
    sys.exit()

# --- Zoom Variables ---
zoom = 1.0
ZOOM_SPEED = 0.0004535
MAX_ZOOM = 1.735

# --- Initialize Player from your movement folder ---
# This handles controls, physics, and animations internally.
player_runner = PlayerRunner(WIDTH, HEIGHT)

# --- Main Game Loop ---
running = True
while running:
    # dt: Time in milliseconds since last frame
    dt = clock.tick(60)

    # Collect Frame Events
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    # --- 1. Update Background Zoom Logic ---
    zoom += ZOOM_SPEED * dt

    # Reset zoom when it reaches the maximum limit
    if zoom >= MAX_ZOOM:
        zoom = 1.0

    scaled_width = int(WIDTH * zoom)
    scaled_height = int(HEIGHT * zoom)

    # Scale background relative to current zoom level
    zoomed_bg = pygame.transform.smoothscale(
        background, (scaled_width, scaled_height)
    )

    # Calculate positioning to keep zoom centered
    x = (WIDTH - scaled_width) // 2
    # Vertically offset slightly based on zoom level
    y = int((HEIGHT - scaled_height) // 2 + (zoom - 1.0) * 300)

    # --- 2. Update Player Controls & Physics ---
    # We pass events to the player object to handle key presses
    player_runner.update(events)

    # --- 3. Render Everything ---
    # Blit Background first
    screen.blit(zoomed_bg, (x, y))

    # Draw Character on top (the draw method handles transparent overlay)
    player_runner.draw(screen)

    pygame.display.flip()

# --- Cleanup ---
pygame.quit()
sys.exit()