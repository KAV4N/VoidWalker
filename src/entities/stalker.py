import random
import heapq
import math
import pygame
from src.config import *
from src.entities.base_sprite import BaseSprite

class Stalker(BaseSprite):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, game.asset_manager.get_image("stalker"))
        self.z = 1

        self.visualization_data = {
            'explored': set()
        }

        self.init_movement_params()
        self.init_patrol_params()
        self.init_pathfinding_params()
        self.init_combat_params()

    def init_movement_params(self):
        self.directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        self.speed = 150
        self.detection_radius = 400

    def init_patrol_params(self):
        self.state = "patrol"
        self.patrol_timer = 0
        self.patrol_wait_time = 2
        self.waiting = False

    def init_pathfinding_params(self):
        self.path = []
        self.path_recalc_cooldown = 0.5
        self.path_recalc_timer = self.path_recalc_cooldown

    def init_combat_params(self):
        self.damage = 5
        self.damage_cooldown = 1.0
        self.damage_timer = 0

    #ONLY FOR DEBUG ------------------------------------------------
    def draw_pathfinding(self, screen, camera):
        explored = self.visualization_data.get('explored', set())
        for pos in explored:
            screen_x = (pos[0] * TILE_SIZE - camera.x) * camera.zoom + WINDOW_WIDTH / 2
            screen_y = (pos[1] * TILE_SIZE - camera.y) * camera.zoom + WINDOW_HEIGHT / 2

            node_surface = pygame.Surface((TILE_SIZE * camera.zoom, TILE_SIZE * camera.zoom), pygame.SRCALPHA)
            pygame.draw.rect(node_surface, (100, 100, 255, 128),
                             (0, 0, TILE_SIZE * camera.zoom, TILE_SIZE * camera.zoom))
            screen.blit(node_surface, (screen_x, screen_y))

        if self.path:
            points = [(self.rect.centerx, self.rect.centery)]
            for node in self.path:
                x = node[0] * TILE_SIZE + TILE_SIZE // 2
                y = node[1] * TILE_SIZE + TILE_SIZE // 2
                points.append((x, y))

            screen_points = []
            for x, y in points:
                screen_x = (x - camera.x) * camera.zoom + WINDOW_WIDTH / 2
                screen_y = (y - camera.y) * camera.zoom + WINDOW_HEIGHT / 2
                screen_points.append((screen_x, screen_y))

            if len(screen_points) > 1:
                pygame.draw.lines(screen, (255, 0, 0), False, screen_points, max(1, int(2 * camera.zoom)))

            for point in screen_points:
                pygame.draw.circle(screen, (255, 100, 100),
                                   (int(point[0]), int(point[1])),
                                   max(3, int(4 * camera.zoom)))
    #------------------------------------------------------------------


    def update(self):
        self.update_timers()
        dist_to_player = self.distance_to(
            self.game.player.rect.centerx,
            self.game.player.rect.centery
        )
        if self.is_player_detected(dist_to_player):
            self.chase_player()
        else:
            self.patrol_area()
        self.check_player_collision()

    def patrol_area(self):
        self.state = "patrol"
        self.patrol()

    def chase_player(self):
        self.state = "chase"
        if self.path_recalc_timer <= 0:
            self.recalculate_path_to_player()
        self.move_along_path()

    def patrol(self):
        if self.should_find_new_patrol_point():
            self.set_new_patrol_path()
        elif self.path and not self.waiting:
            self.move_along_path()
            self.check_path_completion()
        elif self.waiting:
            self.patrol_timer -= self.game.dt

    def check_player_collision(self):
        if self.rect.colliderect(self.game.player.rect):
            if self.damage_timer <= 0:
                self.game.player.handle_damage(self.damage)
                self.game.sound_manager.play("enemy_attack")
                self.damage_timer = self.damage_cooldown

    def take_damage(self, damage):
        pass

    def update_timers(self):
        self.path_recalc_timer -= self.game.dt
        if self.damage_timer > 0:
            self.damage_timer -= self.game.dt

    def should_find_new_patrol_point(self):
        return (not self.path and not self.waiting) or \
            (self.waiting and self.patrol_timer <= 0)

    def set_new_patrol_path(self):
        patrol_x, patrol_y = self.find_random_patrol_point()
        self.path = self.find_path(patrol_x, patrol_y)
        self.waiting = False

    def check_path_completion(self):
        if not self.path:
            self.waiting = True
            self.patrol_timer = self.patrol_wait_time

    def recalculate_path_to_player(self):
        self.path = self.find_path(
            self.game.player.rect.centerx,
            self.game.player.rect.centery
        )
        self.path_recalc_timer = self.path_recalc_cooldown

    def move_along_path(self):
        if self.path:
            next_tile = self.path[0]
            target_x, target_y = self.calculate_tile_center(*next_tile)
            self.move_towards_target(target_x, target_y)

    def move_towards_target(self, target_x, target_y):
        dx = target_x - self.rect.centerx
        dy = target_y - self.rect.centery
        dist = math.sqrt(dx * dx + dy * dy)
        if dist > 1:
            self.apply_movement(dx, dy, dist)
        else:
            self.path.pop(0)

    def apply_movement(self, dx, dy, dist):
        time_scale = 0.25 if self.game.player.bullet_time_active else 1.0
        movement_x = (dx / dist) * self.speed * self.game.dt * time_scale
        movement_y = (dy / dist) * self.speed * self.game.dt * time_scale
        self.rect.x += movement_x
        self.rect.y += movement_y

    def find_path(self, target_x, target_y):
        start = (self.rect.centerx // TILE_SIZE, self.rect.centery // TILE_SIZE)
        goal = (target_x // TILE_SIZE, target_y // TILE_SIZE)
        return self.a_star_pathfinding(start, goal)

    def a_star_pathfinding(self, start, goal):
        frontier = [(0, start)]
        came_from = {start: None}
        cost_so_far = {start: 0}

        explored = set()

        while frontier:
            _, current = heapq.heappop(frontier)
            self.visualization_data['current'] = current
            explored.add(current)

            if current == goal:
                break
            for direction in self.directions:
                neighbor = self.get_neighbor(current, direction)
                if not self.is_valid_position(neighbor):
                    continue
                new_cost = self.calculate_new_cost(current, direction, cost_so_far)
                if self.is_better_path(neighbor, new_cost, cost_so_far):
                    self.update_path_data(neighbor, new_cost, current, goal, frontier, came_from, cost_so_far)

        self.visualization_data = {
            'explored': explored.copy()
        }

        return self.reconstruct_path(start, goal, came_from)

    def get_neighbor(self, current, direction):
        return current[0] + direction[0], current[1] + direction[1]

    def is_valid_position(self, pos):
        return (0 <= pos[0] < len(self.game.map_data[0]) and
                0 <= pos[1] < len(self.game.map_data) and
                (self.game.map_data[pos[1]][pos[0]] == FLOOR))

    def calculate_new_cost(self, current, direction, cost_so_far):
        movement_cost = 2 if abs(direction[0]) + abs(direction[1]) == 2 else 1
        return cost_so_far[current] + movement_cost

    def is_better_path(self, neighbor, new_cost, cost_so_far):
        return neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]

    def update_path_data(self, neighbor, new_cost, current, goal, frontier, came_from, cost_so_far):
        cost_so_far[neighbor] = new_cost
        priority = new_cost + self.calculate_heuristic(neighbor, goal)
        heapq.heappush(frontier, (priority, neighbor))
        came_from[neighbor] = current

    def calculate_heuristic(self, pos, goal):
        return math.sqrt((goal[0] - pos[0]) ** 2 + (goal[1] - pos[1]) ** 2)

    def reconstruct_path(self, start, goal, came_from):
        path = []
        current = goal
        while current and current != start:
            path.append(current)
            current = came_from.get(current)
        path.reverse()
        return path

    def find_random_patrol_point(self):
        while True:
            target_x = random.randint(0, len(self.game.map_data[0]) - 1)
            target_y = random.randint(0, len(self.game.map_data) - 1)
            if self.game.map_data[target_y][target_x] == FLOOR:
                return self.calculate_tile_center(target_x, target_y)

    def calculate_tile_center(self, tile_x, tile_y):
        return (tile_x * TILE_SIZE + TILE_SIZE // 2,
                tile_y * TILE_SIZE + TILE_SIZE // 2)

    def distance_to(self, target_x, target_y):
        dx = target_x - self.rect.centerx
        dy = target_y - self.rect.centery
        return math.sqrt(dx * dx + dy * dy)

    def is_player_detected(self, distance):
        return distance <= self.detection_radius
