import os
import pygame


class ProfessionalButton:

  def __init__(self, x, y, width, height, text, font, base_color, hover_color):
    self.rect = pygame.Rect(x, y, width, height)
    self.text = text
    self.font = font
    self.base_color = base_color
    self.hover_color = hover_color

  def draw(self, surface):
    mouse_pos = pygame.mouse.get_pos()
    current_color = (
        self.hover_color
        if self.rect.collidepoint(mouse_pos)
        else self.base_color
    )
    # Professional button layout with a clean dark accent border
    pygame.draw.rect(surface, current_color, self.rect, border_radius=6)
    pygame.draw.rect(surface, (110, 10, 10), self.rect, 2, border_radius=6)

    # Crisp white text centered inside the red button
    text_surf = self.font.render(self.text, True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=self.rect.center)
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

    # Professional Typography
    self.font_large = pygame.font.SysFont("Helvetica", 48, bold=True)
    self.font_medium = pygame.font.SysFont("Helvetica", 24, bold=True)

    # Load Sound Effect (s1.mpeg from assets folder)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sound_path = os.path.join(base_dir, "assets", "s1.mpeg")
    self.sound = None

    try:
      if os.path.exists(sound_path):
        self.sound = pygame.mixer.Sound(sound_path)
    except pygame.error as e:
      print(f"Note: Could not load pause sound ({e})")

    # Button Layout Configuration
    btn_width, btn_height = 280, 55
    center_x = width // 2 - btn_width // 2

    # Professional Crimson / Blood Red Palette
    RED_BASE = (165, 15, 15)
    RED_HOVER = (215, 35, 35)

    self.resume_btn = ProfessionalButton(
        center_x,
        height // 2 - 40,
        btn_width,
        btn_height,
        "RESUME",
        self.font_medium,
        RED_BASE,
        RED_HOVER,
    )
    self.restart_btn = ProfessionalButton(
        center_x,
        height // 2 + 30,
        btn_width,
        btn_height,
        "RESTART",
        self.font_medium,
        RED_BASE,
        RED_HOVER,
    )
    self.quit_btn = ProfessionalButton(
        center_x,
        height // 2 + 100,
        btn_width,
        btn_height,
        "QUIT GAME",
        self.font_medium,
        RED_BASE,
        RED_HOVER,
    )

  def play_audio(self):
    """Plays s1.mpeg sound effect when pause triggers."""
    if self.sound:
      self.sound.play()

  def handle_event(self, event):
    """Checks button clicks and returns the selected action."""
    if self.resume_btn.is_clicked(event):
      return "RESUME"
    elif self.restart_btn.is_clicked(event):
      return "RESTART"
    elif self.quit_btn.is_clicked(event):
      return "QUIT"
    return None

  def draw(self, surface, current_score):
    """Draws the pitch-black professional pause page with score and buttons."""
    # Pitch-black background overlay
    surface.fill((0, 0, 0))

    # GAME PAUSED Title Header
    title_surf = self.font_large.render("GAME PAUSED", True, (255, 255, 255))
    title_rect = title_surf.get_rect(
        center=(self.width // 2, self.height // 2 - 130)
    )
    surface.blit(title_surf, title_rect)

    # Current Score Tracker Display
    score_text = f"CURRENT SCORE: {int(current_score)}"
    score_surf = self.font_medium.render(score_text, True, (180, 180, 180))
    score_rect = score_surf.get_rect(
        center=(self.width // 2, self.height // 2 - 80)
    )
    surface.blit(score_surf, score_rect)

    # Draw Professional Red Buttons with White Text
    self.resume_btn.draw(surface)
    self.restart_btn.draw(surface)
    self.quit_btn.draw(surface)
