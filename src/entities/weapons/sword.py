import pygame
from src.config import TILE_SIZE


class Sword:
    def __init__(self, player):
        self.player = player
        self.game = player.game
        self.damage = 1

        self.attack_rect = pygame.Rect(0, 0, TILE_SIZE * 1.5, TILE_SIZE)
        self.damaged_enemies = set()

        self.recharge_time = 0.15
        self.recharge_timer = 0

    def update(self):
        self.recharge_timer += self.game.dt
        if self.recharge_timer >= self.recharge_time:
            self.recharge_timer = self.recharge_time

    def start_attack(self):
        if self.recharge_timer >= self.recharge_time:
            self.damaged_enemies.clear()
            self.check_hits()
            self.recharge_timer = 0


    def check_hits(self):
        self.attack_rect.center = self.player.rect.center

        for enemy in self.game.enemies:
            if (
                hasattr(enemy, 'hp') and
                self.attack_rect.colliderect(enemy.rect) and
                enemy not in self.damaged_enemies  # Avoid damaging the same enemy multiple times
            ):
                enemy.take_damage(self.damage)
                self.damaged_enemies.add(enemy)  # Mark the enemy as damaged
                print(f"Enemy hit! Remaining HP: {enemy.hp}")
