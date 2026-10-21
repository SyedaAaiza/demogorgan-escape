import os
import random
import pygame


class ObstacleManager:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.obstacles = []
        self.spawn_timer = 0
        self.spawn_interval = 1300
        self.HORIZON_Y = 320
        self.lane_positions = []

        base_dir = os.path.dirname(os.path.abspath(__file__))
        assets_dir = os.path.join(base_dir, "assets")
        self.obstacle_images = []
        for i in range(1, 10):
            img_path = os.path.join(assets_dir, f"obs{i}.png")
            if not os.path.exists(img_path):
                img_path = os.path.join(assets_dir, f"obs{i}.jpeg")
            if os.path.exists(img_path):
                try:
                    img = pygame.image.load(img_path).convert_alpha()
                    self.obstacle_images.append(img)
                except:
                    pass

    def update_and_spawn(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            lane_idx = random.randint(0, 2)
            chosen = random.choice(self.obstacle_images) if self.obstacle_images else None
            self.obstacles.append({
                "lane_idx": lane_idx,
                "y": self.HORIZON_Y,
                "base_w": 110,
                "base_h": 160,
                "base_speed": 3.0,
                "image": chosen
            })
        for obs in self.obstacles[:]:
            z = max(0.0, (obs["y"] - self.HORIZON_Y) / (self.height - self.HORIZON_Y))
            obs["y"] += obs["base_speed"] + (z * 5)
            if self.lane_positions:
                lane = self.lane_positions[obs["lane_idx"]]
                obs["current_x"] = lane["top_x"] * (1 - z) + lane["bottom_x"] * z
            scale = 0.5 + z * 1.3
            obs["width"] = int(obs["base_w"] * scale)
            obs["height"] = int(obs["base_h"] * scale)
            if obs["y"] > self.height:
                self.obstacles.remove(obs)

    def draw(self, screen):
        for obs in sorted(self.obstacles, key=lambda o: o["y"]):
            x = obs.get("current_x", 0)
            if obs.get("image"):
                scaled = pygame.transform.smoothscale(obs["image"], (obs["width"], obs["height"]))
                screen.blit(scaled, (x - obs["width"] // 2, obs["y"]))

    def check_collision(self, player_rect):
        for obs in self.obstacles:
            obs_x = obs.get("current_x", 0) - obs["width"] // 2
            obs_y = obs["y"]

            # Jab tak obstacle door (upar) hai, collision check nahi hoga
            if obs_y + obs["height"] < 380:
                continue

            obs_rect = pygame.Rect(obs_x, obs_y, obs["width"], obs["height"])

            # Compact rects to avoid false hits
            padded_obs = obs_rect.inflate(-30, -30)
            padded_player = player_rect.inflate(-30, -30)

            if padded_player.colliderect(padded_obs):
                print("HIT! Rect collision detected.")
                return True
        return False

    def get_player_lane_from_screen(self, screen_lanes, player_screen_x):
        if not screen_lanes or len(screen_lanes) < 3:
            return 1
        left_mid = (screen_lanes[0]["bottom_x"] + screen_lanes[1]["bottom_x"]) // 2
        right_mid = (screen_lanes[1]["bottom_x"] + screen_lanes[2]["bottom_x"]) // 2

        if player_screen_x < left_mid:
            return 0
        elif player_screen_x < right_mid:
            return 1
        else:
            return 2