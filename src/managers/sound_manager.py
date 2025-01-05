import pygame

class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.load_sounds()
        self.configure_volumes()

    def load_sounds(self):
        sound_files = {
            "menu_music": "../assets/sound/menu.mp3",
            "ingame_music": "../assets/sound/ingame.mp3",
            "monolog": "../assets/sound/monolog.mp3",
            "ambient": "../assets/sound/demon_voices.mp3",
            "attack": "../assets/sound/attack_player.mp3",
            "enemy_attack": "../assets/sound/enemy_attack.mp3",
            "bullet_time": "../assets/sound/bullet_time.mp3",
            "player_hit": "../assets/sound/player_hit.mp3"
        }

        for sound_name, file_path in sound_files.items():
            try:
                self.sounds[sound_name] = pygame.mixer.Sound(file_path)
            except pygame.error as e:
                print(f"Error loading sound {sound_name}: {e}")

    def configure_volumes(self):
        volumes = {
            "ingame_music": 0.7,
            "ambient": 0.8,
            "attack": 0.6,
            "enemy_attack": 0.3,
            "bullet_time": 0.8
        }

        for sound_name, volume in volumes.items():
            if sound_name in self.sounds:
                self.sounds[sound_name].set_volume(volume)

    def play(self, sound_name, **kwargs):
        if sound_name in self.sounds:
            self.sounds[sound_name].play(**kwargs)
            return self.sounds[sound_name]
        return None

    def stop(self, sound_name=None):
        if sound_name:
            if sound_name in self.sounds:
                self.sounds[sound_name].stop()
        else:
            for sound in self.sounds.values():
                sound.stop()

    def set_volume(self, sound_name, volume):
        if sound_name in self.sounds:
            self.sounds[sound_name].set_volume(volume)