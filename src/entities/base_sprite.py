import pygame
from src.config import TILE_SIZE

class BaseSprite(pygame.sprite.Sprite):
    def __init__(self, game, x, y, img=None, groups=None):
        if groups is None:
            groups = [game.all_sprites_group]
        self.groups = groups
        pygame.sprite.Sprite.__init__(self, *self.groups)

        self.game = game

        if img:
            self.image = img
        else:
            self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
            self.image.fill((200, 200, 200))

        self.rect = self.image.get_rect()
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.rect.x = self.x
        self.rect.y = self.y
