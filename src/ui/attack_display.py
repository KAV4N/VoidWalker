import pygame
from src.config import WINDOW_HEIGHT

class AttackRechargeDisplay:
    def __init__(self, player):
        self.player = player
        self.bar_width = 200
        self.bar_height = 10

    def draw(self, surface):
        x = 10
        y = WINDOW_HEIGHT - 60

        pygame.draw.rect(surface, (100, 100, 100),
                         (x, y, self.bar_width, self.bar_height))

        recharge_width = (self.player.weapon.recharge_timer /
                          self.player.weapon.recharge_time) * self.bar_width
        pygame.draw.rect(surface, (0, 255, 0),
                         (x, y, recharge_width, self.bar_height))
    def set_player(self, player):
        self.player = player