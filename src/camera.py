from config import *
import pygame


class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.zoom = 1.0
        self.min_zoom = 1.0
        self.max_zoom = 3.0

        self.x = 0
        self.y = 0

        self.target_x = 0
        self.target_y = 0

        self.smoothing = 0.1

        self.view_width = WINDOW_WIDTH / self.zoom
        self.view_height = WINDOW_HEIGHT / self.zoom

    def apply(self, entity):
        screen_x = (entity.rect.x - self.x) * self.zoom + WINDOW_WIDTH / 2
        screen_y = (entity.rect.y - self.y) * self.zoom + WINDOW_HEIGHT / 2

        scaled_rect = pygame.Rect(
            screen_x,
            screen_y,
            entity.rect.width * self.zoom,
            entity.rect.height * self.zoom
        )

        return scaled_rect

    def update(self, target):
        self.target_x = target.rect.centerx
        self.target_y = target.rect.centery

        self.x += (self.target_x - self.x) * self.smoothing
        self.y += (self.target_y - self.y) * self.smoothing

        self.view_width = WINDOW_WIDTH / self.zoom
        self.view_height = WINDOW_HEIGHT / self.zoom

        max_x = self.width - self.view_width / 2
        max_y = self.height - self.view_height / 2
        min_x = self.view_width / 2
        min_y = self.view_height / 2

        self.x = max(min_x, min(self.x, max_x))
        self.y = max(min_y, min(self.y, max_y))

    def adjust_zoom(self, amount):
        self.zoom = round(max(self.min_zoom, min(self.max_zoom, self.zoom + amount)), 2)

