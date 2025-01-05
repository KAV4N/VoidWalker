import pygame
import math
from src.entities.weapons.projectile import Projectile
from src.config import *
from src.entities.base_sprite import BaseSprite


class Wizard(BaseSprite):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, game.asset_manager.get_image("turret"))

        self.hp = 1
        self.z = 1

        self.animation_frames = game.asset_manager.get_frames("turret")
        self.current_frame = 0
        self.animation_time = 0
        self.animation_delay = 0.2

        self.shoot_delay = 0.5
        self.shoot_timer = 0
        self.detection_radius = 200

    def animate(self, dt):
        self.animation_time += dt
        if self.animation_time >= self.animation_delay:
            self.animation_time = 0
            self.current_frame = (self.current_frame + 1) % len(self.animation_frames)
            self.image = self.animation_frames[self.current_frame]

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.kill()

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

        self.animate(self.game.dt * time_scale)

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
            self.game.sound_manager.play("enemy_attack")
            Projectile(self.game, self.rect.centerx, self.rect.centery, dx, dy)