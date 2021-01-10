import glob
from abc import ABCMeta, abstractclassmethod, abstractmethod
from itertools import cycle
from typing import Iterable, List, Tuple

import imageio
from loguru import logger
from numpy import ndarray


class Actor(metaclass=ABCMeta):
    """
    The Actor is the base class for every element in the screen. This class provides
    a common interface for all the actors and their actions

    """

    # X and Y coordinates of the actor in the screen
    x: int = None
    y: int = None

    # List of sprites
    sprites: List[ndarray] = None
    sprites_it: Iterable = None

    # Shape of the sprites
    shape: Tuple[int, int] = None

    current_sprite: ndarray = None
    width: int = None
    height: int = None

    # Flag to show or hide the actor
    show: bool = None

    def __init__(self):
        self.x = None
        self.y = None

        self.sprites = None
        self.sprites_it = None
        self.shape = None
        self.current_sprite = None
        self.width = None
        self.height = None

        self.show = None

    def load_sprites(self, sprites_glob: str) -> None:
        """
        Initializes the actor sprites

        Args:
            sprites_glob (str): Path to the sprite to load, it support wildcards like *
        """
        # Each sprite is saved in a separated file
        self.sprites = [imageio.imread(image) for image in glob.iglob(sprites_glob)]

        # Iterator for drawing the next sprite
        self.sprites_it = cycle(self.sprites)

        # Shape of the sprite
        self.shape = self.sprites[0].shape

        # Keep current sprite
        self.current_sprite = next(self.sprites_it)

        self.width = self.shape[1]
        self.height = self.shape[0]

        # Flag for showing actors
        self.show = True

    def left(self) -> int:
        """
        "Left side" of the actor, as a coordinate of the screen

        Returns:
            int: X most left coordinate
        """
        return self.x

    def right(self) -> int:
        """
        "Right side" of the actor, as a coordinate of the screen

        Returns:
            int: X most right coordinate
        """
        return self.x + self.width

    def top(self) -> int:
        """
        "Top" of the actor, as a coordinate of the screen

        Returns:
            int: Y most top coordinate
        """
        return self.y

    def bottom(self) -> int:
        """
        Bottom of the actor, as a screen coordinate

        Returns:
            int: Y coordinate of the actor's bottom
        """
        return self.y + self.height

    @abstractclassmethod
    def update(cls, button: int) -> None:
        """
        Method that updates the actor internal status according to
        the user's input

        Args:
            button (int): Button pressed by the user
        """
        ...

    def draw(self, next_sprite=False):
        """
        Set the current sprite of the actor

        Args:
            next_sprite (bool, optional): Indicates if the next sprite has to be drawn. Defaults to False.
        """
        if next_sprite:
            try:
                self.current_sprite = next(self.sprites_it)
            except StopIteration:
                # If there are not more sprites, it is not visible anymore
                # Used to manage the alien's explosions, that are not cyclic
                self.show = False
