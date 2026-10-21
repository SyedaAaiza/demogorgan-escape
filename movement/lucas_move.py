import pygame
import os
from .keys_control import KeysController


class Character:
    def __init__(self):
        # 3 Lanes X coordinates (Foreground level matching main.py)
        self.lane_x = [280, 400, 520]
        self.current_lane = 1  # 0: Left, 1: Center, 2: Right

        # Position initialization
        self.x = self.lane_x[self.current_lane]
        self.y = 520

        # Keys controller instance
        self.controller = KeysController()

        # Sprites / Animation frames load karne ka setup
        # Agar aapke paas multiple sprite frames hain, toh aap yahan load kar sakte hain
        self.image_frames = []
        self.current_frame = 0
        self.animation_timer = 0

        # Example: Agar assets folder se frames load karne hon (jaise will1, will2, etc.)
        self.load_sprites()

    def load_sprites(self):
        # Yahan aap apne sprite frames load kar sakte hain
        # Main yahan safety ke liye check laga raha hoon taake error na aaye
        IMAGE_DIR = "assets"
        frame_names = ["will1.jpeg", "will2.jpeg", "will3.jpeg"]  # Aapke project ke mutabiq names

        for name in frame_names:
            path = os.path.join(IMAGE_DIR, name)
            if os.path.exists(path):
                img = pygame.image.load(path).convert_alpha()
                img = pygame.transform.scale(img, (60, 80))
                self.image_frames.append(img)

        # Fallback agar sprites na milein taake game crash na ho
        if not self.image_frames:
            surf = pygame.Surface((50, 70))
            surf.fill((50, 150, 255))
            self.image_frames.append(surf)

    def handle_event(self, event):
        # Keys control integration (Aapke controls ke mutabiq lane switching)
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_a) and self.current_lane > 0:
                self.current_lane -= 1
            elif event.key in (pygame.K_RIGHT, pygame.K_d) and self.current_lane < 2:
                self.current_lane += 1

    def update(self):
        # Smooth lane switching (Lerp effect)
        target_x = self.lane_x[self.current_lane]
        self.x += (target_x - self.x) * 0.2

        # Sprite animation frame update logic
        self.animation_timer += 1
        if self.animation_timer > 10:  # Speed of animation
            self.current_frame = (self.current_frame + 1) % len(self.image_frames)
            self.animation_timer = 0

    def draw(self, surface):
        # Current active sprite frame ko draw karna (No Background here!)
        current_image = self.image_frames[self.current_frame]
        rect = current_image.get_rect()
        rect.midbottom = (int(self.x), self.y)
        surface.blit(current_image, rect)