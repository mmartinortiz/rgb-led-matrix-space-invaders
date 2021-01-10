import time
from timeit import default_timer as timer

import invaders.definitions as d
from invaders.flaschen_screen import FlaschenScreen
from invaders.game import Game
from invaders.utils import get_input_device, get_user_input

# Gamepad, will provide input from the user to the game
input_device = get_input_device()

# Screen, will show the game state
screen = FlaschenScreen("localhost", 1337, 64, 64, transparent=True)

# Game, it will keep the state of the game
game = Game(screen=screen)

# Sprites per second
SPS = 6
start = timer()

print("Welcome to Space Invarers, LED version ;-)")
bye = False
while not bye:
    # Mainly, the game loop:
    # 1. Get input from the user
    # 2. Update the game state
    # 3. Draw the new state
    try:
        # User input
        key = get_user_input(input_device)

        # Update state
        game.update(key)

        if key == d.START:
            # Do we leave the game loop?
            bye = True

        # Draw
        screen.clear_canvas()

        # Calculate if the next sprite will be drawn
        next_sprite = False
        if timer() - start > 1 / SPS:
            next_sprite = True
            start = timer()

        # Ask the game to draw the current state
        game.draw(next_sprite=next_sprite)

        time.sleep(0.01)

    except KeyboardInterrupt:
        bye = True

# Close, clear and say goodbye
input_device.close()
screen.clear_canvas()
screen.draw_canvas()
print("bye")
