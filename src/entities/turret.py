import pygame
import math
from src.entities.weapons.projectile import Projectile
from src.config import *


class Turret(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__([game.all_sprites_group])
        self.game = game
        self.image = self.game.images["turret"]
        self.rect = self.image.get_rect()
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.rect.x = self.x
        self.rect.y = self.y

        self.hp = 1

        self.shoot_delay = 0.35
        self.shoot_timer = 0
        self.detection_radius = 200
        self.z = 1

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.kill()
            self.game.enemies.remove(self)

    def can_see_player(self):
        dx = self.game.player.rect.centerx - self.rect.centerx
        dy = self.game.player.rect.centery - self.rect.centery
        distance = math.sqrt(dx * dx + dy * dy)

        if distance > self.detection_radius:
            return False

        steps = int(distance / TILE_SIZE)
        if steps == 0:
            return True

        step_x = dx / steps
        step_y = dy / steps

        x, y = self.rect.centerx, self.rect.centery
        for _ in range(steps):
            tile_x = int(x / TILE_SIZE)
            tile_y = int(y / TILE_SIZE)
            if (tile_x < 0 or tile_x >= MAP_WIDTH or
                    tile_y < 0 or tile_y >= MAP_HEIGHT or
                    self.game.map_data[tile_y][tile_x] != FLOOR):
                return False
            x += step_x
            y += step_y

        return True

    def update(self):
        time_scale = 0.25 if self.game.player.bullet_time_active else 1.0
        self.shoot_timer -= self.game.dt * time_scale

        if self.can_see_player() and self.shoot_timer <= 0:
            self.shoot()
            self.shoot_timer = self.shoot_delay
    def shoot(self):
        dx = self.game.player.rect.centerx - self.rect.centerx
        dy = self.game.player.rect.centery - self.rect.centery
        distance = math.sqrt(dx * dx + dy * dy)
        if distance > 0:
            dx = dx / distance
            dy = dy / distance
            Projectile(self.game, self.rect.centerx, self.rect.centery, dx, dy)
