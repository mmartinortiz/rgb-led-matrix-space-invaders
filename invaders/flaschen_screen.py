import socket
import time
from itertools import product
from typing import Tuple

import numpy as np
from loguru import logger


class FlaschenScreen(object):
    """
    A Framebuffer display interface that sends a frame via UDP

    Adapted from: https://github.com/hzeller/flaschen-taschen/blob/master/api/python/flaschen.py
    """

    def __init__(
        self,
        host: str,
        port: int,
        width: int,
        height: int,
        layer: int = 5,
        transparent: bool = False,
    ):
        """
        Args:
            host (str): The flaschen taschen server hostname or IP address
            port (int): The flaschen taschen server port number
            width (int): The widtf of the faschen taschen display in pixels
            height (int): The height of the flaschen taschen display in pixels
            layer (int, optional): The layer of the flaschen taschen display to write to . Defaults to 5.
            transparent (bool, optional): If True, black(0, 0, 0) will be transparent and show the layer bellow. Defaults to False.
        """

        self.width = width
        self.height = height
        self.layer = layer
        self.transparent = transparent
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.connect((host, port))

        header = f"P6\n{self.width} {self.height}\n255\n".encode("utf-8")
        footer = f"0\n0\n{self.layer}\n".encode("utf-8")

        self._data = bytearray(width * height * 3 + len(header) + len(footer))
        self._data[0 : len(header)] = header
        self._data[-1 * len(footer) :] = footer
        self._header_len = len(header)

        self.canvas = self._get_clear_canvas()

    def _get_clear_canvas(self) -> None:
        """
        Creates an empty canvas

        Returns:
            array: Numpy array with shape ('width', 'height') of (0, 0, 0) as color
        """
        return np.zeros((self.width, self.height), dtype=(int, 3))

    def set_pixel(self, x: int, y: int, color: Tuple[int, int, int]) -> None:
        """Set the pixel at the given coordinates to the specified color.
        Args:
          x: x offset of the pixel to set
          y: y offset of the piyel to set
          color: A 3 tuple of (r, g, b) color values, 0-255

        Args:
            x (int): X offset of the pixel to set
            y (int): Y offset of the pixel to set
            color (Tuple[int, int, int]): A tuple of 3 integer values
            representing (R)ed, (G)reen and (B)lue. Values must been between 0 and 255
        """
        if not isinstance(color, tuple):
            color = tuple(color)

        if x >= self.width or y >= self.height or x < 0 or y < 0:
            return
        if color == (0, 0, 0) and not self.transparent:
            color = (1, 1, 1)

        offset = (x + y * self.width) * 3 + self._header_len
        self._data[offset] = color[0]
        self._data[offset + 1] = color[1]
        self._data[offset + 2] = color[2]

    def send(self) -> None:
        """
        Send the updated pixels to the display
        """
        self._sock.send(self._data)

    def set_in_canvas(self, x: int, y: int, color: Tuple[int, int, int]) -> None:
        """
        Set the given color for the [x, y] position of the canvas

        Args:
            x (int): x coordinate of the canvas
            y (int): y coordinate of the canvas
            color (tuple of int): RGB values for the color
        """
        self.canvas[x, y] = color

    def clear_canvas(self) -> None:
        """
        Clear the canvas, setting all pixels to (0, 0, 0)
        """
        self.canvas = self._get_clear_canvas()

    def draw_canvas(self) -> None:
        """
        Draws the canvas within the screen
        """

        # Set each color on the screen
        for x, y in product(range(self.width), repeat=2):
            self.set_pixel(x, y, tuple(self.canvas[x, y]))

        # Send the information to the screen
        self.send()


# Useful for debugging
if __name__ == "__main__":
    flaschen = FlaschenScreen("localhost", 1337, 64, 64, layer=5, transparent=False)

    flaschen.set_pixel(0, 63, (0, 255, 0))
    flaschen.send()
