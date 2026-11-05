import os
import pygame

class SoundManager:
    """Manages audio playback for slice sounds, bomb detonations, and game over."""
    def __init__(self, sounds_dir=None):
        self.enabled = False
        self.sounds = {}

        if sounds_dir is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            sounds_dir = os.path.join(base_dir, "assets", "sounds")

        self.sounds_dir = sounds_dir
        self._init_mixer()

    def _init_mixer(self):
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            self._load_sounds()
            self.enabled = True
        except Exception as e:
            # Fallback gracefully if audio hardware/driver is not available
            print(f"[SoundManager] Audio initialization notice: {e}. Running in silent mode.")
            self.enabled = False

    def _load_sounds(self):
        sound_files = {
            "slice": "slice.wav",
            "bomb": "bomb.wav",
            "game_over": "game_over.wav",
        }
        for name, filename in sound_files.items():
            path = os.path.join(self.sounds_dir, filename)
            if os.path.exists(path):
                try:
                    sound = pygame.mixer.Sound(path)
                    sound.set_volume(0.8)
                    self.sounds[name] = sound
                except Exception as e:
                    print(f"[SoundManager] Could not load sound {path}: {e}")
            else:
                print(f"[SoundManager] Warning: Sound file not found: {path}")

    def play_slice(self):
        if self.enabled and "slice" in self.sounds:
            try:
                self.sounds["slice"].play()
            except Exception:
                pass

    def play_bomb(self):
        if self.enabled and "bomb" in self.sounds:
            try:
                self.sounds["bomb"].play()
            except Exception:
                pass

    def play_game_over(self):
        if self.enabled and "game_over" in self.sounds:
            try:
                self.sounds["game_over"].play()
            except Exception:
                pass
