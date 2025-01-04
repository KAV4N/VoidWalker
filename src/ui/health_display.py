import pygame
from src.config import WINDOW_HEIGHT

class HealthDisplay:
    def __init__(self, player):
        self.player = player
        self.font = pygame.font.SysFont(None, 36)
        self.heart_width = 30
        self.heart_spacing = 5

    def draw(self, surface):
        for i in range(self.player.hp):
            x = 10 + (self.heart_width + self.heart_spacing) * i
            y = WINDOW_HEIGHT - 40
            pygame.draw.polygon(surface, (255, 0, 0), [
                (x + 15, y + 5),
                (x + 5, y + 15),
                (x + 15, y + 25),
                (x + 25, y + 15)
            ])

    def set_player(self, player):
        self.player = player