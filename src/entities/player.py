import pygame
from src.config import *
from src.entities.weapons.spell import Spell
from src.entities.base_sprite import BaseSprite

class Player(BaseSprite):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, game.asset_manager.get_image("player"))
        self.vx = 0
        self.vy = 0
        self.speed = 275

        self.bullet_time_active = False
        self.bullet_time_duration = 10.0
        self.bullet_time_timer = 0
        self.bullet_time_cooldown = 5.0
        self.bullet_time_cooldown_timer = 0

        self.weapon = Spell(self)
        self.max_hp = 30
        self.hp = self.max_hp
        self.z = 2

    def heal(self, hp):
        if hp+self.hp > self.max_hp:
            self.hp = self.max_hp
        else:
            self.hp += hp

    def flip_image(self):
        if self.vx > 0:
            self.image = self.game.asset_manager.get_image("player", "default", 1)
        elif self.vx < 0:
            self.image = self.game.asset_manager.get_image("player", "default", 0)

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
            self.rect.x = self.x

    def resolve_vertical_collision(self, movement_direction):
        while self.check_collision():
            self.y -= movement_direction
            self.rect.y = self.y

    def move_horizontally(self, dx):
        if dx == 0:
            return

        self.x += dx
        self.rect.x = self.x

        if self.check_collision():
            movement_direction = 1 if dx > 0 else -1
            self.resolve_horizontal_collision(movement_direction)

    def move_vertically(self, dy):
        if dy == 0:
            return

        self.y += dy
        self.rect.y = self.y

        if self.check_collision():
            movement_direction = 1 if dy > 0 else -1
            self.resolve_vertical_collision(movement_direction)

    def move(self, dx, dy):
        self.move_horizontally(dx)
        self.move_vertically(dy)

    def get_input(self):
        self.vx, self.vy = 0, 0
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx = self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.vy = -self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.vy = self.speed

        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071  # 1/√2
            self.vy *= 0.7071

        if keys[pygame.K_SPACE]:
            self.weapon.start_attack()
        self.flip_image()

    def update_bullet_time(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LSHIFT] and self.bullet_time_cooldown_timer <= 0 and not self.bullet_time_active:
            self.bullet_time_active = True
            self.game.sound_manager.play("bullet_time")
            self.bullet_time_timer = self.bullet_time_duration

        if self.bullet_time_active:
            self.bullet_time_timer -= self.game.dt
            if self.bullet_time_timer <= 0:
                self.bullet_time_active = False
                self.bullet_time_cooldown_timer = self.bullet_time_cooldown

        if self.bullet_time_cooldown_timer > 0:
            self.bullet_time_cooldown_timer -= self.game.dt

    def handle_damage(self, damage):
        self.game.sound_manager.play("player_hit")
        self.hp -= damage
        self.game.start_damage_effect()
        if self.hp <= 0:
            self.kill()

    def update(self):
        self.get_input()
        self.update_bullet_time()
        self.move(self.vx * self.game.dt, self.vy * self.game.dt)
        self.weapon.update()