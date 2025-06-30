import pygame
import os
from typing import List


class Sprite:
    def __init__(self, path: str, frame_duration: float):
        self.frames: List[pygame.Surface] = self.load_frames(path)
        self.frame_duration = frame_duration  # seconds per frame
        self.current_time = 0.0
        self.current_frame_index = 0

    def load_frames(self, path: str) -> List[pygame.Surface]:
        frame_files = sorted([f for f in os.listdir(path) if f.endswith(".png")])
        return [pygame.image.load(os.path.join(path, f)) for f in frame_files]

    def update(self, delta_time: float):
        self.current_time += delta_time
        if self.current_time >= self.frame_duration:
            self.current_time = 0.0
            self.current_frame_index = (self.current_frame_index + 1) % len(self.frames)

    def get_current_frame(self) -> pygame.Surface:
        return self.frames[self.current_frame_index]
