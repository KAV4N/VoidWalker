import pygame
from src.config import TILE_SIZE

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__([game.all_sprites_group])
        self.game = game

        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((255, 0, 0))

        self.rect = self.image.get_rect()
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.rect.x = self.x
        self.rect.y = self.y


        self.vx = 0
        self.vy = 0
        self.speed = 300
        self.z = 1

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
            self.vx *= 0.7071
            self.vy *= 0.7071

    def collide_with_walls(self, dir):
        for wall in self.game.obstacle_group:
            if wall.rect.colliderect(self.rect):
                if dir == 'x':
                    if self.vx > 0:
                        self.rect.right = wall.rect.left
                    elif self.vx < 0:
                        self.rect.left = wall.rect.right
                    self.rect.centerx = self.rect.centerx
                    self.x = self.rect.x
                elif dir == 'y':
                    if self.vy > 0:
                        self.rect.bottom = wall.rect.top
                    elif self.vy < 0:
                        self.rect.top = wall.rect.bottom
                    self.rect.centery = self.rect.centery
                    self.y = self.rect.y

    def update(self):
        self.get_input()
        self.x += self.vx * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')

        self.y += self.vy * self.game.dt
        self.rect.y = self.y
        self.collide_with_walls('y')