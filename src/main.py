import pygame
import random
from dungeon_generator import DungeonGenerator
from entities.player import Player
from entities.stalker import Stalker
from camera import Camera
from entities.turret import Turret
from entities.buildings.wall import Wall
from entities.buildings.floor import Floor
from config import *
from src.entities.shooter import Shooter
from src.ui.attack_display import AttackRechargeDisplay
from src.ui.bullet_time_display import BulletTimeDisplay
from src.ui.health_display import HealthDisplay


class Game:
    def __init__(self):
        self.state = "START_MENU"
        self.initialize_pygame()
        self.initialize_game_variables()

        self.images = {}
        self.sounds = {}

        self.load_images()
        self.load_sounds()
        self.create_initial_map()
        self.level = 1
        self.game_over = False
        self.new()
        self.initialize_ui()

    def initialize_game_variables(self):
        self.all_sprites_group = pygame.sprite.Group()
        self.obstacle_group = pygame.sprite.Group()
        self.projectiles_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()

        self.player = None
        self.camera = None
        self.stalker_count = 1
        self.playing = False
        self.dt = 0

        self.map_data = []
        self.room_objs = []
        self.root_room = None
        self.current_seed = -1

    def initialize_ui(self):
        self.health_display = HealthDisplay(self.player, self.images["heart"]["default"][0])
        self.recharge_display = AttackRechargeDisplay(self.player)
        self.bullet_time_display = BulletTimeDisplay(self.player)

    def initialize_pygame(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.font = pygame.font.SysFont(None, 30)
        pygame.display.set_caption("Tilemap Game")
        self.clock = pygame.time.Clock()
        self.title_font = pygame.font.SysFont(None, 64)
        self.menu_font = pygame.font.SysFont(None, 36)

    def load_sounds(self):
        self.sounds["menu_music"] = pygame.mixer.Sound("../assets/sound/menu.mp3")
        self.sounds["ingame_music"] = pygame.mixer.Sound("../assets/sound/ingame.mp3")
        self.sounds["monolog"] = pygame.mixer.Sound("../assets/sound/monolog.mp3")
        self.sounds["ambient"] = pygame.mixer.Sound("../assets/sound/demon_voices.mp3")
        self.sounds["attack"] = pygame.mixer.Sound("../assets/sound/attack_player.mp3")
        self.sounds["enemy_attack"] = pygame.mixer.Sound("../assets/sound/enemy_attack.mp3")
        self.sounds["bullet_time"] = pygame.mixer.Sound("../assets/sound/bullet_time.mp3")

        self.sounds["ingame_music"].set_volume(0.7)
        self.sounds["ambient"].set_volume(0.8)
        self.sounds["attack"].set_volume(0.6)
        self.sounds["enemy_attack"].set_volume(0.3)


        self.sounds["bullet_time"].set_volume(0.8)

    def play_sound(self, sound_name, **kwargs):
        if sound_name in self.sounds:
            self.sounds[sound_name].play(**kwargs)
            return self.sounds[sound_name]
        return None

    def stop_all_sounds(self):
        for sound in self.sounds.values():
            sound.stop()

    def stop_sound(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].stop()

    def load_images(self):
        self.images[BACKGROUND] = {
            "default":[
                pygame.transform.scale(
                pygame.image.load("../assets/img/black.png").convert_alpha(),
                (TILE_SIZE, TILE_SIZE)
                )
            ]
        }
        self.images[FLOOR] = {
            "default":[
                pygame.transform.scale(
                pygame.image.load("../assets/img/floor_light.png").convert_alpha(),
                (TILE_SIZE, TILE_SIZE)
                )
            ]
        }
        self.images[WALL_CENTER] = {

            "default": [
                pygame.transform.scale(
                pygame.image.load("../assets/img/wall_center.png").convert_alpha(),
                (TILE_SIZE, TILE_SIZE)
                )
            ]
        }

        self.images["stalker"] = {
            "default": [
                pygame.transform.scale(
                pygame.image.load("../assets/img/big_demon_idle_anim_f0.png").convert_alpha(),
                (TILE_SIZE*4, TILE_SIZE*4)
                )
            ]
        }

        self.images["shooter"] = {
            "default": [
                pygame.transform.scale(
                pygame.image.load("../assets/img/wizzard_m_idle_anim_f0.png").convert_alpha(),
                (TILE_SIZE, TILE_SIZE*1.5)
                )
            ]
        }

        self.images["turret"] = {
            "default": [
                pygame.transform.scale(
                pygame.image.load("../assets/img/necromancer_anim_f0.png").convert_alpha(),
                (TILE_SIZE, TILE_SIZE * 1.5),
                ),
                pygame.transform.scale(
                    pygame.image.load("../assets/img/necromancer_anim_f1.png").convert_alpha(),
                    (TILE_SIZE, TILE_SIZE * 1.5),
                ),
                pygame.transform.scale(
                    pygame.image.load("../assets/img/necromancer_anim_f2.png").convert_alpha(),
                    (TILE_SIZE, TILE_SIZE * 1.5),
                ),
                pygame.transform.scale(
                    pygame.image.load("../assets/img/necromancer_anim_f3.png").convert_alpha(),
                    (TILE_SIZE, TILE_SIZE * 1.5),
                ),
            ]

        }

        self.images["projectile"] = {
            "default": [
                pygame.transform.scale(
                pygame.image.load("../assets/img/monster_elemental_fire.png").convert_alpha(),
                (TILE_SIZE // 2, TILE_SIZE // 2)
                )
            ]
        }

        self.images["player"] = {
            "default": [
                pygame.transform.scale(
                pygame.image.load("../assets/img/monster_necromancer.png").convert_alpha(),
                (TILE_SIZE * 1.25, TILE_SIZE * 1.25)
                ),
                pygame.transform.flip(
                    pygame.transform.scale(
                    pygame.image.load("../assets/img/monster_necromancer.png").convert_alpha(),
                    (TILE_SIZE * 1.25, TILE_SIZE * 1.25)
                    ),
                    True,
                    False
                )
            ]
        }

        self.images["heart"] = {
            "default": [
                pygame.transform.scale(
                pygame.image.load("../assets/img/heart.png").convert_alpha(),
                (40, 40)
                )
            ]
        }

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

    def cleanup_sprites(self):
        for sprite in self.all_sprites_group:
            if sprite != self.player:
                sprite.kill()

    def populate_map_with_tiles(self):
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == FLOOR:
                    Floor(self, col, row, self.images[tile]["default"][0])
                elif tile == WALL_CENTER:
                    Wall(self, col, row, self.images[tile]["default"][0])

    def position_player_in_map(self):
        for room in self.room_objs:
            center_x, center_y = room.center
            if self.map_data[center_y][center_x] == FLOOR:
                self.player.x, self.player.y = center_x * TILE_SIZE, center_y * TILE_SIZE
                self.player.rect.x, self.player.rect.y = self.player.x, self.player.y
                break

    def place_enemies(self):
        for room in self.room_objs[1:]:
            self.add_shooter_to_room(room)
            self.add_turret_to_room(room)

        self.add_stalker_to_room(self.room_objs[-1])

    def add_shooter_to_room(self, room):
        num_shooters = max((room.width * room.height) // 250, 1)
        for _ in range(num_shooters):
            shooter_x = random.randint(room.x + 1, room.x + room.width - 2)
            shooter_y = random.randint(room.y + 1, room.y + room.height - 2)
            if self.map_data[shooter_y][shooter_x] == FLOOR:
                shooter = Shooter(self, shooter_x, shooter_y)
                self.enemy_group.add(shooter)

    def add_stalker_to_room(self, room):
        random_x = random.randint(room.x + 1, room.x + room.width - 2)
        random_y = random.randint(room.y + 1, room.y + room.height - 2)
        if self.map_data[random_y][random_x] == FLOOR:
            stalker = Stalker(self, random_x, random_y)
            self.enemy_group.add(stalker)

    def add_turret_to_room(self, room):
        num_turrets = max((room.width * room.height) // 250, 1)
        for _ in range(num_turrets):
            turret_x = random.randint(room.x + 1, room.x + room.width - 2)
            turret_y = random.randint(room.y + 1, room.y + room.height - 2)
            if self.map_data[turret_y][turret_x] == FLOOR:
                turret = Turret(self, turret_x, turret_y)
                self.enemy_group.add(turret)

    def new(self):
        if not self.player:
            self.initialize_player()
        if not self.camera:
            self.camera = Camera(MAP_WIDTH * TILE_SIZE, MAP_HEIGHT * TILE_SIZE)
            self.place_enemies()

    def initialize_player(self):
        for room in self.room_objs:
            center_x, center_y = room.center
            if self.map_data[center_y][center_x] == FLOOR:
                self.player = Player(self, center_x, center_y)
                break



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
        self.draw_ui()
        self.draw_fps()
        self.draw_bsp_chunks(self.root_room, color=(255, 0, 0))
        pygame.display.flip()

    def draw_ui(self):
        self.health_display.draw(self.screen)
        self.recharge_display.draw(self.screen)
        self.bullet_time_display.draw(self.screen)

    def draw_sprites(self):
        sorted_sprites = sorted(
            self.all_sprites_group,
            key=lambda sprite: (getattr(sprite, 'z', 0), sprite.rect.bottom)
        )
        for sprite in sorted_sprites:
            self.draw_sprite(sprite)
        self.player.weapon.draw_particles(self.screen, self.camera)

    def draw_sprite(self, sprite):
        screen_rect = self.camera.apply(sprite)
        if self.is_visible_on_screen(screen_rect):
            scaled_image = pygame.transform.scale(
                sprite.image,
                (int(sprite.image.get_width() * self.camera.zoom),
                 int(sprite.image.get_height() * self.camera.zoom))
            )
            self.screen.blit(scaled_image, screen_rect)

    #----------------------------------- TEST  DRAWS ----------------------------------------------------------
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

    # ----------------------------------- TEST  DRAWS ----------------------------------------------------------

    def run(self):
        while not self.game_over:
            if self.state == "START_MENU":
                self.run_start_menu()
            elif self.state == "PLAYING":
                self.run_game_loop()
            elif self.state == "GAME_OVER":
                self.run_game_over()

    def run_start_menu(self):
        waiting = True
        self.stop_all_sounds()
        self.play_sound("monolog")
        self.play_sound("menu_music", loops=-1, maxtime=0, fade_ms=0)

        while waiting and not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        waiting = False
                        self.state = "PLAYING"

            self.screen.fill(BACKGROUND_COLOR)
            title = self.title_font.render("VOIDWALKER", True, WHITE)
            start = self.menu_font.render("Press ENTER to Start", True, WHITE)
            self.screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, WINDOW_HEIGHT // 3))
            self.screen.blit(start, (WINDOW_WIDTH // 2 - start.get_width() // 2, WINDOW_HEIGHT // 2))
            pygame.display.flip()
            self.clock.tick(FPS)

    def run_game_loop(self):
        self.playing = True
        self.stop_all_sounds()
        self.play_sound("ingame_music", loops=-1, maxtime=0, fade_ms=0)
        self.play_sound("ambient", loops=-1, maxtime=0, fade_ms=0)

        while self.playing and not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.game_over = True
                    self.playing = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.create_map(seed=random.randint(0, 999999999))
                elif event.type == pygame.MOUSEWHEEL:
                    self.camera.adjust_zoom(event.y * 0.5)
            self.dt = self.clock.tick(FPS) / 1000
            self.update()
            self.check_level_completion()
            self.check_player_status()
            self.draw()

    def check_level_completion(self):
        if len(self.enemy_group) <= self.stalker_count:
            self.level += 1
            self.create_map(seed=random.randint(0, 999999999))
            self.position_player_in_map()
            self.place_enemies()

    def check_player_status(self):
        if not self.player.alive():
            self.playing = False
            self.state = "GAME_OVER"

    def run_game_over(self):
        waiting = True
        self.stop_all_sounds()
        self.play_sound("menu_music", loops=-1, maxtime=0, fade_ms=0)
        while waiting and not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset_game()
                        waiting = False
                        break
                    elif event.key == pygame.K_ESCAPE:
                        self.game_over = True
            else:
                self.screen.fill(BACKGROUND_COLOR)
                game_over = self.title_font.render("GAME OVER", True, WHITE)
                score = self.menu_font.render(f"Evolutions Completed: {self.level - 1}", True, WHITE)
                restart = self.menu_font.render("Press R to Restart or ESC to Quit", True, WHITE)

                self.screen.blit(game_over, (WINDOW_WIDTH // 2 - game_over.get_width() // 2, WINDOW_HEIGHT // 3))
                self.screen.blit(score, (WINDOW_WIDTH // 2 - score.get_width() // 2, WINDOW_HEIGHT // 2))
                self.screen.blit(restart, (WINDOW_WIDTH // 2 - restart.get_width() // 2, WINDOW_HEIGHT * 2 // 3))
                pygame.display.flip()
                self.clock.tick(FPS)


    def reset_game(self):
        self.level = 1
        self.state = "PLAYING"
        self.initialize_game_variables()
        self.create_initial_map()
        self.new()
        self.health_display.set_player(self.player)
        self.recharge_display.set_player(self.player)
        self.bullet_time_display.set_player(self.player)




if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
