import pygame
import os


class Demogorgon:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Demogorgon ki starting position (Right side se screen par aayega)
        self.x = screen_width + 100
        self.y = screen_height - 350  # Floor height ke mutabiq adjust kar sakti hain
        self.speed = 4

        # Images load karne ki list
        self.frames = []
        self.load_images()

        # Animation variables
        self.current_frame = 0
        self.animation_speed = 0.15  # Frame change hone ki speed
        self.anim_timer = 0

    def load_images(self):
        # demo1.jpeg se demo4.jpeg tak load karna (all small letters)
        for i in range(1, 5):
            img_path = os.path.join("assets", f"demo{i}.jpeg")
            try:
                img = pygame.image.load(img_path).convert()

                # White background remove karne ki koshish (JPEG par yeh thoda harsh ho sakta hai)
                img.set_colorkey((255, 255, 255))

                # Size adjust karna
                img = pygame.transform.scale(img, (120, 150))
                self.frames.append(img)
            except Exception as e:
                print(f"Warning: Could not load {img_path}. Error: {e}")
                # Fallback agar image na mile toh red box dikhayega taaki crash na ho
                fallback = pygame.Surface((120, 150))
                fallback.fill((100, 0, 0))
                self.frames.append(fallback)

    def update(self):
        # Left ki taraf chalna
        self.x -= self.speed

        # Screen se bahar jaye toh wapas right par le aana
        if self.x < -150:
            self.x = self.screen_width + 100

        # Animation frame update karna
        if self.frames:
            self.anim_timer += self.animation_speed
            if self.anim_timer >= 1:
                self.anim_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.frames)

    def draw(self, screen):
        # Current animation frame ko screen par draw karna
        if self.frames:
            current_image = self.frames[self.current_frame]
            screen.blit(current_image, (self.x, self.y))