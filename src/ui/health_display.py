import pygame
from src.config import WINDOW_HEIGHT

class HealthDisplay:
    def __init__(self, player, heart_image):
        self.player = player
        self.heart_image = heart_image
        self.heart_width = heart_image.get_width()  # Use the image width
        self.heart_spacing = 5  # Space between hearts

    def draw(self, surface):
        for i in range(self.player.hp):
            x = 10 + (self.heart_width + self.heart_spacing) * i
            y = WINDOW_HEIGHT - 40
            surface.blit(self.heart_image, (x, y))

    def set_player(self, player):
        self.player = player
