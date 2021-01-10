from invaders.alien import Alien


class Strategy:
    """
    Strategies for the army
    """

    # Move the army from left to right, and then to the left again...
    SYNC_LEFT_RIGHT = 0


class Army:
    """
    Army of aliens...
    Args:
        number_of_aliens_per_row (int, optional): [description]. Defaults to 4.
        rows_of_aliens (int, optional): [description]. Defaults to 2.
        strategy (Strategy, optional): [description]. Defaults to Strategy.SYNC_LEFT_RIGHT.
        screen_width (int, optional): [description]. Defaults to None.
        screen_height (int, optional): [description]. Defaults to None.
    """

    number_of_aliens_per_row: int = 4
    rows_of_aliens: int = 2
    strategy: Strategy = Strategy.SYNC_LEFT_RIGHT
    screen_width: int = None
    screen_height: int = None

    def __init__(
        self,
        number_of_aliens_per_row: int = 4,
        rows_of_aliens: int = 2,
        strategy: Strategy = None,
        screen_width: int = None,
        screen_height: int = None,
    ):
        self.strategy = Strategy.SYNC_LEFT_RIGHT if strategy is None else strategy
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Two rows of aliens, 4 aliens per row
        self.rows_of_aliens = rows_of_aliens
        self.number_of_aliens_per_row = number_of_aliens_per_row
        self.aliens = []
        self._generate_new_aliens_army()

        if self.strategy == Strategy.SYNC_LEFT_RIGHT:
            # Default moving direction
            self.moving = "left"

    def _generate_new_aliens_army(self):
        """
        Generates a new army of aliens!
        """
        # Distribute the aliens across the screen
        dummy_alien = Alien(0, 0)
        horizontal_space = int(self.screen_width / self.number_of_aliens_per_row)
        vertical_space = dummy_alien.height + 2

        self.aliens = [
            Alien(
                x=horizontal_space * i,
                y=vertical_space * j,
                screen_height=self.screen_height,
                screen_width=self.screen_width,
            )
            for j in range(self.rows_of_aliens)
            for i in range(self.number_of_aliens_per_row)
        ]

    def move_army(self):
        """
        Move the aliens of the army
        """
        if len(self.aliens) <= 0:
            self._generate_new_aliens_army()

        if self.strategy == Strategy.SYNC_LEFT_RIGHT:
            most_left = min([a.left() for a in self.aliens])
            if most_left > 0 and self.moving == "left":
                for alien in self.aliens:
                    alien.move_left()

            else:
                self.moving = "right"
                most_right = max([a.right() for a in self.aliens])
                if most_right < self.screen_width:
                    for alien in self.aliens:
                        alien.move_right()
                else:
                    self.moving = "left"

    def update_army(self):
        """
        Update the status of the army. If some aliens must not be shown,
        they are hidden.
        """
        self.aliens = [alien for alien in self.aliens if alien.show]
