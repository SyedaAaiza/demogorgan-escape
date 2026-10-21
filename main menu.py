import math
import sys
import pygame

# Initialize Pygame
pygame.init()

# 16:9 Widescreen Laptop Resolution
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Escape the Upside Down - Main Menu")
clock = pygame.time.Clock()

# --- Asset Loading ---
IMAGE_FILENAME = "assets/trees.jpeg"  # Use your exact cartoon image filename here

try:
  bg_original = pygame.image.load(IMAGE_FILENAME).convert()
except FileNotFoundError:
  print(f"Error: Could not find '{IMAGE_FILENAME}'.")
  pygame.quit()
  sys.exit()

# Menu Options
options = ["START GAME", "RESUME GAME", "SETTINGS", "EXIT"]
selected_option = 0

# Fonts
font_menu = pygame.font.Font(None, 36)
font_title = pygame.font.Font(None, 72)

# --- Infinite Smooth Zoom Variables ---
# We track progress using a single continuous timer/counter instead of abrupt resets
zoom_progress = 0.0
speed = 0.0015  # Adjust forward speed here (lower = smoother/slower)


def draw_styled_button(
    surface, text, center_x, center_y, width, height, is_selected
):
  """Draws an arcade-style graphic box with glowing borders for menu items."""
  rect = pygame.Rect(0, 0, width, height)
  rect.center = (center_x, center_y)

  if is_selected:
    bg_color = (180, 10, 10, 210)
    border_color = (255, 60, 60)
    text_color = (255, 255, 255)
    border_width = 3
  else:
    bg_color = (15, 15, 25, 170)
    border_color = (80, 80, 100)
    text_color = (180, 180, 180)
    border_width = 2

  box_surface = pygame.Surface((width, height), pygame.SRCALPHA)
  box_surface.fill(bg_color)
  surface.blit(box_surface, rect.topleft)
  pygame.draw.rect(surface, border_color, rect, border_width, border_radius=6)

  if is_selected:
    pygame.draw.circle(
        surface, border_color, (rect.left - 15, rect.centery), 6
    )
    pygame.draw.circle(
        surface, border_color, (rect.right + 15, rect.centery), 6
    )

  text_surface = font_menu.render(text, True, text_color)
  text_rect = text_surface.get_rect(center=rect.center)
  surface.blit(text_surface, text_rect)


# --- Main Game Loop ---
running = True
while running:
  # 1. Continuous Progress Tracker (Wraps cleanly using modulo without jarring snaps)
  zoom_progress += speed
  if zoom_progress >= 1.0:
    zoom_progress = 0.0

  screen.fill((0, 0, 0))

  # 2. Dual-Layer Seamless Cross-Fade Logic
  # Layer A (Main Zooming Stream)
  scale1 = 1.0 + zoom_progress
  w1, h1 = int(WIDTH * scale1), int(HEIGHT * scale1)
  surf1 = pygame.transform.smoothscale(bg_original, (w1, h1))

  # Smooth alpha transition curve so layers blend into each other invisibly
  alpha1 = int((1.0 - zoom_progress) * 255)
  surf1.set_alpha(alpha1)
  screen.blit(surf1, ((WIDTH - w1) // 2, (HEIGHT - h1) // 2))

  # Layer B (The succeeding stream that starts right behind Layer A)
  scale2 = 1.0 + (zoom_progress + 1.0) % 2.0
  # To make it cleanly loop from 1.0 when zoom_progress hits 0:
  scale2 = 1.0 + zoom_progress  # Offset precisely by half a cycle
  if zoom_progress < 0.5:
    scale2 = 1.0 + zoom_progress + 0.5
  else:
    scale2 = 1.0 + zoom_progress - 0.5

  w2, h2 = int(WIDTH * scale2), int(HEIGHT * scale2)
  surf2 = pygame.transform.smoothscale(bg_original, (w2, h2))

  alpha2 = int(
      (1.0 - abs(zoom_progress - 0.5) * 2) * 255
  )  # Sine-like cross fade
  # Alternative safer cross-fade matching complementary alpha:
  alpha2 = 255 - alpha1
  surf2.set_alpha(max(0, min(255, alpha2)))

  screen.blit(surf2, ((WIDTH - w2) // 2, (HEIGHT - h2) // 2))

  # 3. Dark Vignette / Atmospheric Overlay
  vignette = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
  vignette.fill((0, 0, 0, 80))
  screen.blit(vignette, (0, 0))

  # 4. Title Display with Shadow
  title_surface = font_title.render(
      "ESCAPE THE UPSIDE DOWN", True, (230, 20, 20)
  )
  title_rect = title_surface.get_rect(center=(WIDTH // 2, 110))
  shadow_surface = font_title.render("ESCAPE THE UPSIDE DOWN", True, (0, 0, 0))
  screen.blit(shadow_surface, (title_rect.x + 3, title_rect.y + 3))
  screen.blit(title_surface, title_rect)

  # 5. Render Graphic Menu Buttons
  button_w, button_h = 320, 50
  start_y = 280
  spacing = 70

  for i, option in enumerate(options):
    y_pos = start_y + (i * spacing)
    is_selected = i == selected_option
    draw_styled_button(
        screen, option, WIDTH // 2, y_pos, button_w, button_h, is_selected
    )

  # 6. Event Handling
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
    elif event.type == pygame.KEYDOWN:
      if event.key == pygame.K_DOWN or event.key == pygame.K_s:
        selected_option = (selected_option + 1) % len(options)
      elif event.key == pygame.K_UP or event.key == pygame.K_w:
        selected_option = (selected_option - 1) % len(options)
      elif event.key == pygame.K_RETURN:
        print(f"Option Triggered: {options[selected_option]}")
        if options[selected_option] == "EXIT":
          pygame.quit()
          sys.exit()

  pygame.display.flip()
  clock.tick(60)