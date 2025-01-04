from src.entities.stalker import Stalker
from src.entities.weapons.projectile import Projectile
import math

class Shooter(Stalker):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.image = self.game.images["shooter"]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.hp = 1

        self.speed = 100
        self.detection_radius = 300

        self.shoot_range = 75
        self.shoot_cooldown = 3.0
        self.shoot_timer = 0

        self.path_recalc_cooldown = 3.5

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.kill()
            self.game.enemies.remove(self)

    def update(self):
        self.path_recalc_timer -= self.game.dt
        self.shoot_timer -= self.game.dt

        dist_to_player = self.distance_to(
            self.game.player.rect.centerx,
            self.game.player.rect.centery
        )

        if dist_to_player <= self.detection_radius:
            self.state = "chase"

            if dist_to_player <= self.shoot_range:
                if self.shoot_timer <= 0:
                    self.shoot_at_player()
                    self.shoot_timer = self.shoot_cooldown
                self.path = []
            else:
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

    def shoot_at_player(self):

        dx = self.game.player.rect.centerx - self.rect.centerx
        dy = self.game.player.rect.centery - self.rect.centery

        length = math.sqrt(dx * dx + dy * dy)
        if length > 0:
            dx = dx / length
            dy = dy / length

        Projectile(
            self.game,
            self.rect.centerx,
            self.rect.centery,
            dx,
            dy,
            300
        )
