import pygame
from src.config import TILE_SIZE, FLOOR

class Projectile(pygame.sprite.Sprite):
    def __init__(self, game, x, y, dx, dy, speed=150):
        self.groups = [game.all_sprites_group, game.projectiles_group]
        super().__init__(self.groups)
        self.game = game

        self.image = self.game.images["projectile"]["default"][0]
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

    def check_collision(self):
        tile_x1 = self.rect.left // TILE_SIZE
        tile_x2 = self.rect.right // TILE_SIZE
        tile_y1 = self.rect.top // TILE_SIZE
        tile_y2 = self.rect.bottom // TILE_SIZE

        for y in range(tile_y1, tile_y2 + 1):
            for x in range(tile_x1, tile_x2 + 1):
                if (y >= 0 and y < len(self.game.map_data) and
                        x >= 0 and x < len(self.game.map_data[0])):
                    if self.game.map_data[y][x] != FLOOR:
                        return True
        return False

    def resolve_horizontal_collision(self, movement_direction):
        while self.check_collision():
            self.x -= movement_direction
            self.rect.centerx = self.x
        self.kill()

    def resolve_vertical_collision(self, movement_direction):
        while self.check_collision():
            self.y -= movement_direction
            self.rect.centery = self.y
        self.kill()

    def move_horizontally(self, dx):
        if dx == 0:
            return

        self.x += dx
        self.rect.centerx = self.x

        if self.check_collision():
            movement_direction = 1 if dx > 0 else -1
            self.resolve_horizontal_collision(movement_direction)

    def move_vertically(self, dy):
        if dy == 0:
            return

        self.y += dy
        self.rect.centery = self.y

        if self.check_collision():
            movement_direction = 1 if dy > 0 else -1
            self.resolve_vertical_collision(movement_direction)

    def move(self, dx, dy):
        self.move_horizontally(dx)
        self.move_vertically(dy)

    def check_player_collision(self):
        if self.rect.colliderect(self.game.player.rect):
            self.game.player.handle_damage(self.damage)
            self.kill()
            return True
        return False

    def update_lifetime(self, time_scale):
        self.lifetime -= self.game.dt * time_scale
        return self.lifetime <= 0

    def update(self):
        time_scale = 0.25 if self.game.player.bullet_time_active else 1.0

        if self.update_lifetime(time_scale):
            self.kill()
            return

        dx = self.dx * self.game.dt * time_scale
        dy = self.dy * self.game.dt * time_scale

        self.move(dx, dy)
        self.check_player_collision()