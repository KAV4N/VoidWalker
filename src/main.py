import pygame
import random
from dungeon_generator import DungeonGenerator
from room import Room
from entities.player import Player
from entities.stalker import Stalker
from camera import Camera
from entities.turret import Turret
from entities.buildings.wall import Wall
from entities.buildings.floor import Floor
from config import *
from src.entities.shooter import Shooter


class Game:
    def __init__(self):
        self.state = "START_MENU"
        self.initialize_pygame()
        self.initialize_game_variables()
        self.load_images()
        self.create_initial_map()
        self.new()

    def initialize_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.font = pygame.font.SysFont(None, 30)
        pygame.display.set_caption("Tilemap Game")
        self.clock = pygame.time.Clock()
        self.title_font = pygame.font.SysFont(None, 64)
        self.menu_font = pygame.font.SysFont(None, 36)

    def initialize_game_variables(self):
        self.all_sprites_group = pygame.sprite.Group()
        self.obstacle_group = pygame.sprite.Group()
        self.projectiles_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()

        self.player = None
        self.camera = None
        self.enemies = []
        self.playing = False
        self.dt = 0
        self.images = {}
        self.map_data = []
        self.room_objs = []
        self.root_room = None
        self.current_seed = -1

    def load_images(self):
        self.images[BACKGROUND] = pygame.transform.scale(
            pygame.image.load("../assets/black.png").convert_alpha(),
            (TILE_SIZE, TILE_SIZE)
        )
        self.images[FLOOR] = pygame.transform.scale(
            pygame.image.load("../assets/floor_light.png").convert_alpha(),
            (TILE_SIZE, TILE_SIZE)
        )
        self.images[WALL_CENTER] = pygame.transform.scale(
            pygame.image.load("../assets/wall_center.png").convert_alpha(),
            (TILE_SIZE, TILE_SIZE)
        )

    def create_initial_map(self):
        self.create_map(seed=123)

    def create_map(self, seed):
        self.cleanup_sprites()

        generator = DungeonGenerator(
            width=MAP_WIDTH,
            height=MAP_HEIGHT,
            min_size=25,
            min_room_size=8,
            seed=seed
        )
        self.map_data, self.room_objs, self.root_room, self.current_seed = generator.generate_dungeon()
        self.populate_map_with_tiles()
        if self.player:
            self.position_player_in_map()
            self.place_enemies()

    def cleanup_sprites(self):
        for sprite in self.all_sprites_group:
            if sprite != self.player:
                sprite.kill()

    def populate_map_with_tiles(self):
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == FLOOR:
                    Floor(self, col, row, self.images[tile])
                elif tile == WALL_CENTER:
                    Wall(self, col, row, self.images[tile])

    def position_player_in_map(self):
        for room in self.room_objs:
            center_x, center_y = room.center
            if self.map_data[center_y][center_x] == FLOOR:
                self.player.x, self.player.y = center_x * TILE_SIZE, center_y * TILE_SIZE
                self.player.rect.x, self.player.rect.y = self.player.x, self.player.y
                break

    def place_enemies(self):
        self.enemies.clear()
        for room in self.room_objs[1:]:
            self.add_shooter_to_room(room)
            self.add_turret_to_room(room)
        self.add_stalker_to_room(self.room_objs[-1])

    def add_shooter_to_room(self, room):
        random_x = random.randint(room.x + 1, room.x + room.width - 2)
        random_y = random.randint(room.y + 1, room.y + room.height - 2)
        if self.map_data[random_y][random_x] == FLOOR:
            self.enemies.append(Shooter(self, random_x, random_y))

    def add_stalker_to_room(self, room):
        random_x = random.randint(room.x + 1, room.x + room.width - 2)
        random_y = random.randint(room.y + 1, room.y + room.height - 2)
        if self.map_data[random_y][random_x] == FLOOR:
            self.enemies.append(Stalker(self, random_x, random_y))

    def add_turret_to_room(self, room):
        num_turrets = (room.width * room.height) // 250
        for _ in range(num_turrets):
            turret_x = random.randint(room.x + 1, room.x + room.width - 2)
            turret_y = random.randint(room.y + 1, room.y + room.height - 2)
            if self.map_data[turret_y][turret_x] == FLOOR:
                self.enemies.append(Turret(self, turret_x, turret_y))

    def new(self):
        if not self.player:
            self.initialize_player()
        if not self.camera:
            self.camera = Camera(MAP_WIDTH * TILE_SIZE, MAP_HEIGHT * TILE_SIZE)

    def initialize_player(self):
        for room in self.room_objs:
            center_x, center_y = room.center
            if self.map_data[center_y][center_x] == FLOOR:
                self.player = Player(self, center_x, center_y)
                break

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pygame.quit()

    def update(self):
        self.all_sprites_group.update()
        self.camera.update(self.player)

    def is_visible_on_screen(self, rect):
        return (
                rect.right >= 0 and rect.left <= WINDOW_WIDTH and
                rect.bottom >= 0 and rect.top <= WINDOW_HEIGHT
        )

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.draw_sprites()
        #self.draw_bsp_chunks(self.root_room)
        self.draw_fps()
        self.draw_bullet_time_status()
        pygame.display.flip()

    def draw_bullet_time_status(self):
        if self.player.bullet_time_active:
            text = f"BULLET TIME: {self.player.bullet_time_timer:.1f}"
            color = (0, 255, 255)
        elif self.player.bullet_time_cooldown_timer > 0:
            text = f"BULLET TIME COOLDOWN: {self.player.bullet_time_cooldown_timer:.1f}"
            color = (255, 165, 0)
        else:
            text = "BULLET TIME READY"
            color = (0, 255, 0)

        status_text = self.font.render(text, True, color)
        self.screen.blit(status_text, (10, 40))
    def draw_sprites(self):
        sorted_sprites = sorted(
            self.all_sprites_group,
            key=lambda sprite: (getattr(sprite, 'z', 0), sprite.rect.bottom)
        )
        for sprite in sorted_sprites:
            self.draw_sprite(sprite)

    def draw_sprite(self, sprite):
        screen_rect = self.camera.apply(sprite)
        if self.is_visible_on_screen(screen_rect):
            scaled_image = pygame.transform.scale(
                sprite.image,
                (int(sprite.image.get_width() * self.camera.zoom),
                 int(sprite.image.get_height() * self.camera.zoom))
            )
            self.screen.blit(scaled_image, screen_rect)



    def draw_fps(self):
        fps_text = self.font.render(f"FPS: {int(self.clock.get_fps())}", True, WHITE)
        self.screen.blit(fps_text, (10, 10))

    def draw_bsp_chunks(self, node, color=(0, 255, 0), level=0, max_level=None):
        if not node or (max_level is not None and level > max_level):
            return
        self.draw_node_rect(node, color, level)
        self.draw_bsp_chunks(node.left_child, color, level + 1, max_level)
        self.draw_bsp_chunks(node.right_child, color, level + 1, max_level)

    def draw_node_rect(self, node, color, level):
        rect_color = [c // (level + 1) for c in color]
        pygame.draw.rect(
            self.screen,
            rect_color,
            pygame.Rect(
                node.x * TILE_SIZE - self.camera.x * self.camera.zoom + WINDOW_WIDTH // 2,
                node.y * TILE_SIZE - self.camera.y * self.camera.zoom + WINDOW_HEIGHT // 2,
                node.width * TILE_SIZE * self.camera.zoom,
                node.height * TILE_SIZE * self.camera.zoom
            ),
            1
        )

    def events(self):
        for event in pygame.event.get():
            self.handle_event(event)

    def handle_event(self, event):
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            self.playing = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            self.create_map(seed=random.randint(0, 999999999))
        elif event.type == pygame.MOUSEWHEEL:
            self.camera.adjust_zoom(event.y * 0.5)



if __name__ == "__main__":
    game = Game()
    game.new()
    game.run()
    pygame.quit()
