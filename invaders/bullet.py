from timeit import default_timer as timer

from invaders.actor import Actor


class Bullet(Actor):
    """
    Bullets are shot by the spaceship
    """

    def __init__(
        self, x, y, screen_width=None, screen_height=None, sprites_per_second=1 / 6
    ):
        super().__init__()
        self.load_sprites(sprites_glob="./assets/bullet_*.png")

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.x = x
        self.y = y
        self.sprites_per_second = sprites_per_second
        self.start = timer()

    def update(self, button: int):
        if timer() - self.start > self.sprites_per_second:
            self.start = timer()
            if self.top() > 0 and self.bottom() < self.screen_width:
                self.y -= 1
