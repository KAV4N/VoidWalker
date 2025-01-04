import pygame

import pygame
from src.config import WHITE, CYAN, ORANGE, GREEN



class BulletTimeDisplay:
    def __init__(self, player):
        self.player = player
        self.font = pygame.font.SysFont(None, 30)
        self.position = (10, 40)

    def set_player(self, player):
        self.player = player

    def draw(self, screen):
        if self.player.bullet_time_active:
            text = f"BULLET TIME: {self.player.bullet_time_timer:.1f}"
            color = CYAN
        elif self.player.bullet_time_cooldown_timer > 0:
            text = f"BULLET TIME COOLDOWN: {self.player.bullet_time_cooldown_timer:.1f}"
            color = ORANGE
        else:
            text = "BULLET TIME READY"
            color = GREEN

        status_text = self.font.render(text, True, color)
        screen.blit(status_text, self.position)
