import os
import pygame


class ProfessionalButton:

  def __init__(
      self,
      x,
      y,
      width,
      height,
      label="",
      base_color=(165, 15, 15),
      hover_color=(215, 35, 35),
      button_type="resume",
  ):
    self.rect = pygame.Rect(x, y, width, height)
    self.label = label
    self.base_color = base_color
    self.hover_color = hover_color
    self.button_type = button_type  # 'pause', 'resume', 'restart', 'quit_door'

  def draw(self, surface, font_small):
    mouse_pos = pygame.mouse.get_pos()
    current_color = (
        self.hover_color
        if self.rect.collidepoint(mouse_pos)
        else self.base_color
    )

    # Draw button body with subtle dark border
    pygame.draw.rect(surface, current_color, self.rect, border_radius=8)
    pygame.draw.rect(surface, (110, 10, 10), self.rect, 2, border_radius=8)

    center_x, center_y = self.rect.center

    if self.button_type == "pause":
      # Pause symbol (Two vertical bars)
      bar_w, bar_h = 6, 20
      bar_y = center_y - bar_h // 2
      pygame.draw.rect(
          surface,
          (255, 255, 255),
          (center_x - 9, bar_y, bar_w, bar_h),
          border_radius=2,
      )
      pygame.draw.rect(
          surface,
          (255, 255, 255),
          (center_x + 3, bar_y, bar_w, bar_h),
          border_radius=2,
      )

    elif self.button_type == "resume":
      # Play Triangle positioned higher, small text below
      tri_y = center_y - 6
      points = [
          (center_x - 8, tri_y - 8),
          (center_x - 8, tri_y + 8),
          (center_x + 10, tri_y),
      ]
      pygame.draw.polygon(surface, (255, 255, 255), points)

      text_surf = font_small.render(self.label, True, (230, 230, 230))
      text_rect = text_surf.get_rect(center=(center_x, center_y + 14))
      surface.blit(text_surf, text_rect)

    elif self.button_type == "restart":
      # Looping Arrow positioned higher, small text below
      arc_y = center_y - 6
      radius = 10
      pygame.draw.arc(
          surface,
          (255, 255, 255),
          (center_x - radius, arc_y - radius, radius * 2, radius * 2),
          0.8,
          5.5,
          2,
      )
      pygame.draw.polygon(
          surface,
          (255, 255, 255),
          [
              (center_x + 3, arc_y - 11),
              (center_x + 10, arc_y - 7),
              (center_x + 4, arc_y - 2),
          ],
      )

      text_surf = font_small.render(self.label, True, (230, 230, 230))
      text_rect = text_surf.get_rect(center=(center_x, center_y + 14))
      surface.blit(text_surf, text_rect)

    elif self.button_type == "quit_door":
      # Door with exit arrow positioned higher, small text below
      door_w, door_h = 14, 22
      door_x = center_x - door_w // 2
      door_y = center_y - 18

      pygame.draw.rect(
          surface, (255, 255, 255), (door_x, door_y, door_w, door_h), 2
      )
      pygame.draw.line(
          surface,
          (255, 255, 255),
          (door_x + 3, door_y + door_h // 2),
          (door_x + 7, door_y + door_h // 2),
          2,
      )

      arrow_start_x = door_x - 8
      arrow_end_x = door_x + 6
      arrow_y = door_y + door_h // 2
      pygame.draw.line(
          surface,
          (255, 255, 255),
          (arrow_start_x, arrow_y),
          (arrow_end_x, arrow_y),
          2,
      )
      pygame.draw.polygon(
          surface,
          (255, 255, 255),
          [
              (arrow_start_x + 5, arrow_y - 3),
              (arrow_start_x, arrow_y),
              (arrow_start_x + 5, arrow_y + 3),
          ],
      )

      text_surf = font_small.render(self.label, True, (230, 230, 230))
      text_rect = text_surf.get_rect(center=(center_x, center_y + 14))
      surface.blit(text_surf, text_rect)

  def is_clicked(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
      if self.rect.collidepoint(event.pos):
        return True
    return False


class PauseMenu:

  def __init__(self, width, height):
    self.width = width
    self.height = height

    # Typography
    self.font_large = pygame.font.SysFont("Helvetica", 48, bold=True)
    self.font_medium = pygame.font.SysFont("Helvetica", 24, bold=True)
    self.font_small = pygame.font.SysFont("Helvetica", 14, bold=True)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(base_dir, "assets")

    # Load Background Image (BG2.jpg / BG2.jpeg)[cite: 1]
    self.bg_image = None
    possible_bg_paths = [
        os.path.join(assets_dir, "BG2.jpg"),
        os.path.join(assets_dir, "BG2.jpeg"),
        os.path.join(assets_dir, "BG2.png"),
        os.path.join(base_dir, "BG2.jpg"),
        os.path.join(base_dir, "BG2.jpeg"),
        os.path.join(base_dir, "BG2.png"),
    ]

    for bg_path in possible_bg_paths:
      if os.path.exists(bg_path):
        try:
          loaded_bg = pygame.image.load(bg_path).convert()
          self.bg_image = pygame.transform.smoothscale(
              loaded_bg, (width, height)
          )
          break
        except pygame.error as e:
          print(f"Error loading background image: {e}")

    # Load Sound Effect (s1.mpeg)
    sound_path = os.path.join(assets_dir, "s1.mpeg")
    self.sound = None
    try:
      if os.path.exists(sound_path):
        self.sound = pygame.mixer.Sound(sound_path)
    except pygame.error as e:
      print(f"Note: Could not load sound ({e})")

    # Menu Buttons Configuration
    btn_width, btn_height = 220, 55
    center_x = width // 2 - btn_width // 2
    RED_BASE = (165, 15, 15)
    RED_HOVER = (215, 35, 35)

    self.resume_btn = ProfessionalButton(
        center_x,
        height // 2 - 40,
        btn_width,
        btn_height,
        label="RESUME",
        base_color=RED_BASE,
        hover_color=RED_HOVER,
        button_type="resume",
    )
    self.restart_btn = ProfessionalButton(
        center_x,
        height // 2 + 30,
        btn_width,
        btn_height,
        label="RESTART",
        base_color=RED_BASE,
        hover_color=RED_HOVER,
        button_type="restart",
    )
    self.quit_btn = ProfessionalButton(
        center_x,
        height // 2 + 100,
        btn_width,
        btn_height,
        label="QUIT GAME",
        base_color=RED_BASE,
        hover_color=RED_HOVER,
        button_type="quit_door",
    )

    # Top-Right Pause Symbol Button Instance
    self.top_pause_btn = ProfessionalButton(
        width - 70,
        20,
        50,
        40,
        base_color=(30, 30, 30),
        hover_color=(165, 15, 15),
        button_type="pause",
    )

  def play_audio(self):
    if self.sound:
      self.sound.play()

  def handle_event(self, event):
    if self.resume_btn.is_clicked(event):
      return "RESUME"
    elif self.restart_btn.is_clicked(event):
      return "RESTART"
    elif self.quit_btn.is_clicked(event):
      return "QUIT"
    return None

  def draw(self, surface, current_score):
    # Draw background image[cite: 1]
    if self.bg_image:
      surface.blit(self.bg_image, (0, 0))
    else:
      surface.fill((0, 0, 0))

    # Dark overlay
    overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    surface.blit(overlay, (0, 0))

    # GAME PAUSED Title Header
    title_surf = self.font_large.render("GAME PAUSED", True, (255, 255, 255))
    title_rect = title_surf.get_rect(
        center=(self.width // 2, self.height // 2 - 130)
    )
    surface.blit(title_surf, title_rect)

    # Current Score Display
    score_text = f"CURRENT SCORE: {int(current_score)}"
    score_surf = self.font_medium.render(score_text, True, (220, 220, 220))
    score_rect = score_surf.get_rect(
        center=(self.width // 2, self.height // 2 - 80)
    )
    surface.blit(score_surf, score_rect)

    # Draw Menu Buttons
    self.resume_btn.draw(surface, self.font_small)
    self.restart_btn.draw(surface, self.font_small)
    self.quit_btn.draw(surface, self.font_small)
