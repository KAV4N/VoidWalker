import pygame
from src.config import *

class AssetManager:
    def __init__(self):
        self.images = {}
        self.load_images()

    def load_images(self):
        self.images[BACKGROUND] = {
            "default": [
                pygame.transform.scale(
                    pygame.image.load("../assets/img/black.png").convert_alpha(),
                    (TILE_SIZE, TILE_SIZE)
                )
            ]
        }
        self.images[FLOOR] = {
            "default": [
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
                    (TILE_SIZE, TILE_SIZE * 1.5)
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
                    (30, 30)
                )
            ]
        }

    def get_frames(self,key,state="default"):
        try:
            return self.images[key][state]
        except (KeyError, IndexError):
            print(f"Warning: Image not found for key: {key}, state: {state}")
            return None

    def get_image(self, key, state="default", frame=0):
        try:
            return self.images[key][state][frame]
        except (KeyError, IndexError):
            print(f"Warning: Image not found for key: {key}, state: {state}, frame: {frame}")
            return None