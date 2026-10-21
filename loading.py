import pygame
import sys
import time
import math
import random

GAME_TITLE = "DEMOGORGON ESCAPE"

pygame.init()
pygame.mixer.init()

display_info = pygame.display.Info()
WIDTH, HEIGHT = display_info.current_w, display_info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption(GAME_TITLE)
clock = pygame.time.Clock()

IMAGE_FILENAME = "bgfizz.jpeg"
AUDIO_FILENAME = "assets/s1.mpeg"  # Make sure your audio file is in the same folder

try:
    bg_image = pygame.image.load(IMAGE_FILENAME).convert()
    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
except Exception as e:
    print(f"Error: '{IMAGE_FILENAME}' not found! Details: {e}")
    pygame.quit()
    sys.exit()

# Load and loop your custom monster audio file infinitely
try:
    pygame.mixer.music.load(AUDIO_FILENAME)
    pygame.mixer.music.play(loops=-1)
except Exception as e:
    print(f"Audio Warning: Could not load '{AUDIO_FILENAME}'. Make sure it's in the project folder! Details: {e}")

load_font = pygame.font.SysFont("Courier New", max(16, HEIGHT // 35), bold=True)
menu_font = pygame.font.SysFont("Courier New", max(20, HEIGHT // 28), bold=True)

loading_progress = 0
is_loaded = False
start_time = time.time()

# Lightning visual strike variables (active from the very beginning)
lightning_active = False
lightning_timer = time.time()
next_lightning_time = random.uniform(0.3, 0.9)
lightning_duration = 0
bolt_segments = []


def create_lightning_bolt():
    start_x = random.randint(int(WIDTH * 0.1), int(WIDTH * 0.9))
    start_y = 0
    segments = [(start_x, start_y)]

    current_x, current_y = start_x, start_y
    while current_y < HEIGHT * 0.75:
        next_y = current_y + random.randint(30, 70)
        next_x = current_x + random.randint(-60, 60)
        segments.append((next_x, next_y))
        current_x, current_y = next_x, next_y

    return segments


running = True
selected_option = 0  # 0 for Start, 1 for Exit

while running:
    current_time = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif is_loaded:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    selected_option = 1 - selected_option
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        print("Starting Game...")
                        running = False
                    else:
                        running = False
                elif event.key == pygame.K_s:
                    print("Starting Game...")
                    running = False

    # Continuous lightning bolt triggers without flashing the screen white
    if current_time - lightning_timer > next_lightning_time:
        lightning_active = True
        lightning_duration = random.uniform(0.08, 0.18)
        bolt_segments = create_lightning_bolt()
        lightning_timer = current_time
        next_lightning_time = random.uniform(0.4, 1.2)

    if lightning_active and (current_time - lightning_timer > lightning_duration):
        lightning_active = False

    # Draw background image (stable, no white blinking)
    screen.blit(bg_image, (0, 0))

    # Draw only the visual jagged lightning strikes over the background
    if lightning_active and len(bolt_segments) > 1:
        pygame.draw.lines(screen, (255, 60, 60), False, bolt_segments, 10)
        pygame.draw.lines(screen, (255, 255, 255), False, bolt_segments, 4)

    center_x, center_y = WIDTH // 2, HEIGHT // 2

    if not is_loaded:
        elapsed = current_time - start_time
        loading_progress = int(min(100, (elapsed / 5.0) * 100))

        if loading_progress >= 100:
            is_loaded = True

        load_surface = load_font.render(f"CONNECTING TO UPSIDE DOWN... {loading_progress}%", True, (220, 30, 40))
        load_rect = load_surface.get_rect(center=(center_x, HEIGHT * 0.85))

        bar_width = int(WIDTH * 0.4)
        bar_height = int(HEIGHT * 0.025)
        bar_x = center_x - (bar_width // 2)
        bar_y = int(HEIGHT * 0.90)

        pygame.draw.rect(screen, (40, 40, 50), (bar_x, bar_y, bar_width, bar_height))
        fill_width = int(bar_width * (loading_progress / 100))
        pygame.draw.rect(screen, (220, 30, 40), (bar_x, bar_y, fill_width, bar_height))

        # Moving Bicycle Icon
        cycle_x = bar_x + fill_width
        cycle_y = bar_y - 12
        pygame.draw.circle(screen, (200, 200, 200), (cycle_x - 8, cycle_y + 10), 6, 2)
        pygame.draw.circle(screen, (200, 200, 200), (cycle_x + 8, cycle_y + 10), 6, 2)
        pygame.draw.line(screen, (220, 30, 40), (cycle_x - 8, cycle_y + 10), (cycle_x, cycle_y + 2), 2)
        pygame.draw.line(screen, (220, 30, 40), (cycle_x + 8, cycle_y + 10), (cycle_x, cycle_y + 2), 2)
        pygame.draw.line(screen, (220, 30, 40), (cycle_x - 12, cycle_y + 2), (cycle_x + 4, cycle_y + 2), 2)

        screen.blit(load_surface, load_rect)

    else:
        # Menu Options: Start & Exit
        options = ["START GAME", "EXIT REALM"]
        for i, option_text in enumerate(options):
            color = (255, 255, 255) if i == selected_option else (120, 120, 130)
            if i == selected_option:
                option_text = f"> {option_text} <"

            opt_surface = menu_font.render(option_text, True, color)
            opt_rect = opt_surface.get_rect(center=(center_x, HEIGHT * 0.82 + (i * HEIGHT * 0.06)))

            screen.blit(opt_surface, (opt_rect.x + 2, opt_rect.y + 2))
            screen.blit(opt_surface, opt_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()