from timeit import default_timer as timer

from loguru import logger

from invaders.actor import Actor


class Alien(Actor):
    """
    An alien, the bad guy of the game
    """

    def __init__(
        self, x, y, screen_width=None, screen_height=None, sprites_per_second=1 / 6
    ):
        super().__init__()
        self.load_sprites(sprites_glob="./assets/alien_*.png")

        self.screen_width = screen_width
        self.screen_height = screen_height

        # Starting position
        self.x = x
        self.y = y

        self.sprites_per_second = sprites_per_second
        self.start = timer()

    def update(self, button: int):
        # Aliens do not care about the user input
        pass

    def move_left(self):
        """
        Move the alien to the left.

        The movement is done according to the value of "sprites_per_second".
        This attribute indicates the number of sprites per second shown on the scrren.
        """
        if timer() - self.start > self.sprites_per_second:
            self.start = timer()
            if self.left() > 0:
                self.x -= 1

    def move_right(self):
        """
        Move the alien to the right.

        The movement is done according to the value of "sprites_per_second".
        This attribute indicates the number of sprites per second shown on the scrren.
        """
        if timer() - self.start > self.sprites_per_second:
            self.start = timer()
            if self.right() < self.screen_width:
                self.x += 1

    def explosion(self):
        """
        Explosions are represented with a different animation
        """
        self.load_sprites(sprites_glob="./assets/alien-explosion_*.png")

        # Replace the iterator by one that is not cyclic
        self.sprites_it = iter(self.sprites)
