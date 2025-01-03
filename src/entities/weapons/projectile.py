import pygame
from src.config import TILE_SIZE

class Projectile(pygame.sprite.Sprite):
    def __init__(self, game, x, y, dx, dy, speed = 150):
        self.groups = [game.all_sprites_group, game.projectiles_group]
        super().__init__(self.groups)
        self.game = game

        self.image = pygame.Surface((TILE_SIZE // 2, TILE_SIZE // 2))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()

        self.damage = 1

        self.x = x
        self.y = y
        self.rect.centerx = x
        self.rect.centery = y

        self.speed = speed
        self.dx = dx * self.speed
        self.dy = dy * self.speed

        self.lifetime = 2.0
        self.z = 1

    def update(self):
        time_scale = 0.25 if self.game.player.bullet_time_active else 1.0

        self.lifetime -= self.game.dt * time_scale
        if self.lifetime <= 0:
            self.kill()
            return

        self.x += self.dx * self.game.dt * time_scale
        self.y += self.dy * self.game.dt * time_scale
        self.rect.centerx = self.x
        self.rect.centery = self.y

        for wall in self.game.obstacle_group:
            if self.rect.colliderect(wall.rect):
                self.kill()
                return

        if self.rect.colliderect(self.game.player.rect):
            self.game.player.handle_damage(self.damage)
            self.kill()

