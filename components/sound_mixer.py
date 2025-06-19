import pygame
import random
import time
from typing import List


class SoundMixer:
    def __init__(self):
        pygame.mixer.init()
        self.last_ambient_time = time.time()
        self.ambient_delay = random.randint(25, 45)

        self.ambient_sounds: List[pygame.mixer.Sound] = [
            pygame.mixer.Sound("sound/music/echo-dungeon-70538.mp3"),
        ]

        # self.sfx = {
        #     "pickup": pygame.mixer.Sound("sounds/pickup.wav"),
        #     "attack": pygame.mixer.Sound("sounds/swing.wav"),
        #     "hit": pygame.mixer.Sound("sounds/hit.wav"),
        # }

        pygame.mixer.music.load("sound/music/a_dungeon_ambience_loop-79423.mp3")
        pygame.mixer.music.set_volume(0.5)

    def play_music(self, loop: bool = True):
        pygame.mixer.music.play(-1 if loop else 0)

    def stop_music(self):
        pygame.mixer.music.stop()

    def play_sfx(self, name: str):
        if name in self.sfx:
            self.sfx[name].play()

    def update_ambient(self):
        current_time = time.time()
        if current_time - self.last_ambient_time >= self.ambient_delay:
            random.choice(self.ambient_sounds).play()
            self.last_ambient_time = current_time
            self.ambient_delay = random.randint(15,30)