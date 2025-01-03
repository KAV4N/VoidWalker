import pygame
import random
import heapq
import math
from src.config import *


class Stalker(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__([game.all_sprites_group])
        self.game = game
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.rect.x = self.x
        self.rect.y = self.y

        self.speed = 60
        self.detection_radius = 300
        self.path = []
        self.state = "patrol"
        self.patrol_timer = 0
        self.patrol_wait_time = 2
        self.waiting = False

        self.path_recalc_cooldown = 0.5
        self.path_recalc_timer = self.path_recalc_cooldown
        self.z = 1

    def find_random_patrol_point(self):
        while True:
            target_x = random.randint(0, len(self.game.map_data[0]) - 1)
            target_y = random.randint(0, len(self.game.map_data) - 1)
            if self.game.map_data[target_y][target_x] == FLOOR:
                return (target_x * TILE_SIZE + TILE_SIZE // 2,
                       target_y * TILE_SIZE + TILE_SIZE // 2)

    def patrol(self):
        if (not self.path and not self.waiting) or (self.waiting and self.patrol_timer <= 0):
            patrol_x, patrol_y = self.find_random_patrol_point()
            self.path = self.find_path(patrol_x, patrol_y)
            self.waiting = False

        if self.path and not self.waiting:
            self.move_along_path()
            if not self.path:
                self.waiting = True
                self.patrol_timer = self.patrol_wait_time

        if self.waiting:
            self.patrol_timer -= self.game.dt

    def distance_to(self, target_x, target_y):
        dx = target_x - self.rect.centerx
        dy = target_y - self.rect.centery
        return math.sqrt(dx ** 2 + dy ** 2)

    def find_path(self, target_x, target_y):
        start = (self.rect.centerx // TILE_SIZE, self.rect.centery // TILE_SIZE)
        goal = (target_x // TILE_SIZE, target_y // TILE_SIZE)

        frontier = [(0, start)]
        came_from = {start: None}
        cost_so_far = {start: 0}

        directions = [(dx, dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1]
                     if not (dx == 0 and dy == 0)]

        while frontier:
            _, current = heapq.heappop(frontier)
            if current == goal:
                break

            for dx, dy in directions:
                neighbor = (current[0] + dx, current[1] + dy)

                if not (0 <= neighbor[0] < len(self.game.map_data[0]) and
                       0 <= neighbor[1] < len(self.game.map_data)):
                    continue

                if self.game.map_data[neighbor[1]][neighbor[0]] != FLOOR:
                    continue

                movement_cost = 1.414 if abs(dx) + abs(dy) == 2 else 1
                new_cost = cost_so_far[current] + movement_cost

                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + math.sqrt(
                        (goal[0] - neighbor[0]) ** 2 +
                        (goal[1] - neighbor[1]) ** 2
                    )
                    heapq.heappush(frontier, (priority, neighbor))
                    came_from[neighbor] = current

        path = []
        current = goal
        while current and current != start:
            path.append(current)
            current = came_from.get(current)
        path.reverse()
        return path

    def move_along_path(self):
        if self.path:
            next_tile = self.path[0]
            target_x = next_tile[0] * TILE_SIZE + TILE_SIZE // 2
            target_y = next_tile[1] * TILE_SIZE + TILE_SIZE // 2

            dx = target_x - self.rect.centerx
            dy = target_y - self.rect.centery
            dist = math.sqrt(dx ** 2 + dy ** 2)

            if dist > 1:
                dx = (dx / dist) * self.speed * self.game.dt
                dy = (dy / dist) * self.speed * self.game.dt
                self.rect.x += dx
                self.rect.y += dy
            else:
                self.path.pop(0)

    def update(self):
        self.path_recalc_timer -= self.game.dt
        dist_to_player = self.distance_to(
            self.game.player.rect.centerx,
            self.game.player.rect.centery
        )

        if dist_to_player <= self.detection_radius:
            self.state = "chase"
            if self.path_recalc_timer <= 0:
                self.path = self.find_path(
                    self.game.player.rect.centerx,
                    self.game.player.rect.centery
                )

                self.path_recalc_timer = self.path_recalc_cooldown
            self.move_along_path()
        else:
            self.state = "patrol"
            self.patrol()
