import pygame
from src.config import *
from src.entities.weapons.spell import Spell

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__([game.all_sprites_group])
        self.game = game

        self.image = self.game.images["player"]

        self.rect = self.image.get_rect()
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.rect.x = self.x
        self.rect.y = self.y

        self.bullet_time_active = False
        self.bullet_time_duration = 5.0
        self.bullet_time_timer = 0
        self.bullet_time_cooldown = 5.0
        self.bullet_time_cooldown_timer = 0

        self.weapon = Spell(self)
        self.hp = 100


        self.vx = 0
        self.vy = 0
        self.speed = 250
        self.z = 1

    def handle_damage(self, damage):
        self.hp -= damage

        if self.hp <= 0:
            self.kill()


    def update_bullet_time(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT] and self.bullet_time_cooldown_timer <= 0:
            self.bullet_time_active = True
            self.bullet_time_timer = self.bullet_time_duration

        if self.bullet_time_active:
            self.bullet_time_timer -= self.game.dt
            if self.bullet_time_timer <= 0:
                self.bullet_time_active = False
                self.bullet_time_cooldown_timer = self.bullet_time_cooldown

        if self.bullet_time_cooldown_timer > 0:
            self.bullet_time_cooldown_timer -= self.game.dt

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
        if keys[pygame.K_SPACE]:
            print("attack")
            self.weapon.start_attack()


        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071

    def check_collision(self):
        tile_x1 = self.rect.left // TILE_SIZE
        tile_x2 = self.rect.right // TILE_SIZE
        tile_y1 = self.rect.top // TILE_SIZE
        tile_y2 = self.rect.bottom // TILE_SIZE

        for y in range(tile_y1, tile_y2 + 1):
            for x in range(tile_x1, tile_x2 + 1):
                if (y >= 0 and y < len(self.game.map_data) and
                        x >= 0 and x < len(self.game.map_data[0])):
                    if self.game.map_data[y][x] != FLOOR:  # Wall tile
                        return True
        return False

    def move(self, dx, dy):
        self.x += dx
        self.rect.x = self.x
        if self.check_collision():
            if dx > 0:
                while self.check_collision():
                    self.x -= 1
                    self.rect.x = self.x
            elif dx < 0:
                while self.check_collision():
                    self.x += 1
                    self.rect.x = self.x

        self.y += dy
        self.rect.y = self.y
        if self.check_collision():
            if dy > 0:
                while self.check_collision():
                    self.y -= 1
                    self.rect.y = self.y
            elif dy < 0:
                while self.check_collision():
                    self.y += 1
                    self.rect.y = self.y

    def update(self):
        self.get_input()
        self.update_bullet_time()
        self.move(self.vx * self.game.dt, self.vy * self.game.dt)
        self.weapon.update()

