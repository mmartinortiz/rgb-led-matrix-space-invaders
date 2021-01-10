from itertools import product
from timeit import default_timer as timer

from loguru import logger

import invaders.definitions as d
from invaders.actor import Actor
from invaders.army import Army
from invaders.bullet import Bullet
from invaders.flaschen_screen import FlaschenScreen
from invaders.spaceship import Spaceship


class Game:
    """
    Class that keeps the state of the game
    """

    def __init__(self, screen: FlaschenScreen):
        # Screen where things are drawn
        self.screen = screen

        # The spaceship
        self.spaceship = Spaceship(
            screen_height=screen.height, screen_width=screen.width
        )

        # Bullets, none so far
        self.bullets = []

        # The army of aliens
        self.army = Army(
            number_of_aliens_per_row=4,
            screen_width=screen.width,
            screen_height=screen.height,
        )

        # Set a delay of 2 seconds between bullets
        # This will slow down the player capacity
        # for shooting
        self.lapse_between_bullets = 2
        self.last_bullet_at = timer() - self.lapse_between_bullets

    def new_bullet(self, x: int, y: int) -> None:
        """
        Creates a new bullet, at coordinates x and y

        Args:
            x (int): X coordinate for the new bullet
            y (int): Y coordinate for the new bullet
        """
        if timer() - self.last_bullet_at > self.lapse_between_bullets:
            self.last_bullet_at = timer()
            self.bullets.append(
                Bullet(
                    x=x,
                    y=y,
                    screen_height=self.screen.height,
                    screen_width=self.screen.width,
                )
            )

    def update(self, button: int) -> None:
        """
        Update the game status

        Args:
            button (int): Button pressed by the player
        """
        # Update spaceship
        if button is not None:
            self.spaceship.update(button)

        # Create new bullets
        if button == d.A:
            self.new_bullet(
                # Todo: calculate coordinates programatically
                x=self.spaceship.x + 2,
                y=self.spaceship.y - self.spaceship.shape[1] + 4,
            )

        # Move the aliens army
        self.army.move_army()

        # Move all the bullets
        for bullet in self.bullets:
            bullet.update(button)

        # Any bullet impacted an alien?
        for bullet, alien in product(self.bullets, self.army.aliens):
            if (
                bullet.top() <= alien.bottom()
                and bullet.bottom() >= alien.top()
                and bullet.left() >= alien.left()
                and bullet.right() <= alien.right()
            ):
                # Impact! "Hide" the bullet
                bullet.show = False

                # Make the alien explode
                alien.explosion()

        # Update alived aliens and bullets
        self.bullets = [bullet for bullet in self.bullets if bullet.show]
        self.army.update_army()

        # Keep only those bullets that are "in the screen"
        self.bullets = [bullet for bullet in self.bullets if bullet.y > 0]

    def set_leds(self, actor: Actor) -> None:
        """
        For a given actor, set on the leds on the screen according
        to the current sprite

        Args:
            actor (Actor): Actor to be drawn in the screen
        """

        # j --> y
        for j, row in enumerate(actor.current_sprite):
            # i --> x
            for i, color in enumerate(row):
                rgb = (color[0], color[1], color[2])

                x = i + actor.x
                y = j + actor.y

                self.screen.set_in_canvas(x, y, rgb)

    def draw(self, next_sprite: bool) -> None:
        """
        Draw the game status in the screen. Drawing is composed of
        two steps for each actor:

        1. If `next_sprite` then make active the next sprite
           as the current sprite
        2. Set on the leds according to the current sprite

        Args:
            next_sprite (bool): Is it time to draw the next sprite?
        """
        # Indicate the spachip if it is time to draw the next sprite
        self.spaceship.draw(next_sprite=next_sprite)
        self.set_leds(self.spaceship)

        # For each alien, activate current sprite and set leds on
        for alien in self.army.aliens:
            alien.draw(next_sprite=next_sprite)
            self.set_leds(alien)

        # Indicate the bullets if it is time to draw the next sprite
        for bullet in self.bullets:
            bullet.draw(next_sprite=next_sprite)
            self.set_leds(bullet)

        # Finally, draw the canvas
        self.screen.draw_canvas()
