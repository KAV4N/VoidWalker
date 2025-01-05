import pygame
import math
from src.config import *


class Spell:
    def __init__(self, player):
        self.player = player
        self.game = player.game
        self.damage = 1

        self.particles = []
        self.particle_lifetime = 0.2
        self.particle_count = 12
        self.particle_speed = 200
        self.particle_size = TILE_SIZE // 4
        self.particle_color = PURPLE
        self.glow_radius = TILE_SIZE * 2

        self.max_radius = self.particle_speed * self.particle_lifetime

        self.attack_radius = self.max_radius

        self.recharge_time = 0.35
        self.recharge_timer = 0

    def create_particles(self):
        for i in range(self.particle_count):
            angle = (2 * math.pi * i) / self.particle_count
            particle = {
                'x': self.player.rect.centerx,
                'y': self.player.rect.centery,
                'dx': math.cos(angle) * self.particle_speed,
                'dy': math.sin(angle) * self.particle_speed,
                'lifetime': self.particle_lifetime,
                'alpha': 255
            }
            self.particles.append(particle)

    def update_particles(self):
        surviving_particles = []
        for particle in self.particles:
            particle['lifetime'] -= self.game.dt
            if particle['lifetime'] > 0:
                particle['x'] += particle['dx'] * self.game.dt
                particle['y'] += particle['dy'] * self.game.dt
                particle['alpha'] = int((particle['lifetime'] / self.particle_lifetime) * 255)
                surviving_particles.append(particle)
        self.particles = surviving_particles

    def draw_particles(self, surface, camera):
        if not self.particles:
            return

        for particle in self.particles:
            screen_x = (particle['x'] - camera.x) * camera.zoom + WINDOW_WIDTH // 2
            screen_y = (particle['y'] - camera.y) * camera.zoom + WINDOW_HEIGHT // 2

            scaled_particle_size = self.particle_size * camera.zoom

            particle_surface = pygame.Surface((scaled_particle_size, scaled_particle_size), pygame.SRCALPHA)
            particle_color = (*self.particle_color, particle['alpha'])
            pygame.draw.circle(particle_surface, particle_color,
                               (int(scaled_particle_size // 2), int(scaled_particle_size // 2)),
                               int(scaled_particle_size // 2))

            scaled_glow_radius = self.glow_radius * camera.zoom
            glow_surface = pygame.Surface((scaled_glow_radius * 2, scaled_glow_radius * 2), pygame.SRCALPHA)
            glow_color = (*self.particle_color, particle['alpha'] // 4)
            pygame.draw.circle(glow_surface, glow_color,
                               (int(scaled_glow_radius), int(scaled_glow_radius)),
                               int(self.particle_size * 2 * camera.zoom))

            surface.blit(glow_surface, (screen_x - scaled_glow_radius, screen_y - scaled_glow_radius))
            surface.blit(particle_surface, (screen_x - scaled_particle_size // 2,
                                            screen_y - scaled_particle_size // 2))

    def update(self):
        self.recharge_timer += self.game.dt
        if self.recharge_timer >= self.recharge_time:
            self.recharge_timer = self.recharge_time
        self.update_particles()

    def start_attack(self):
        if self.recharge_timer >= self.recharge_time:
            self.game.sound_manager.play("attack")
            self.check_hits()
            self.create_particles()
            self.recharge_timer = 0

    def check_hits(self):
        center_x = self.player.rect.centerx
        center_y = self.player.rect.centery

        for enemy in self.game.enemy_group:
            if not hasattr(enemy, 'hp'):
                continue

            dx = enemy.rect.centerx - center_x
            dy = enemy.rect.centery - center_y
            distance = math.sqrt(dx * dx + dy * dy)

            if distance <= self.attack_radius and enemy:
                enemy.take_damage(self.damage)

