from loguru import logger

import invaders.definitions as d
from invaders.actor import Actor


class Spaceship(Actor):
    """
    The spaceship is the good guy, the one controlled by the player
    """

    def __init__(self, screen_width=None, screen_height=None):
        super().__init__()
        self.load_sprites(sprites_glob="./assets/spaceship_*.png")

        self.screen_width = screen_width
        self.screen_height = screen_height

        # Starting position, bottom left
        self.x = 0
        self.y = screen_height - self.height

    def update(self, button: int):
        if button == d.LEFT:
            if self.left() > 0:
                # Move to left
                self.x -= 1

        if button == d.RIGHT:
            if self.right() < self.screen_width:
                # Move to right
                self.x += 1
