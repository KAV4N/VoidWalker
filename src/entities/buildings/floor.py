from src.entities.base_sprite import BaseSprite
class Floor(BaseSprite):
    def __init__(self, game, x, y, img):
        super().__init__(game, x, y, img, groups=[game.all_sprites_group])

