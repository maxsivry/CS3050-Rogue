import arcade
import tile
from classes.actor import Player
from gameview import GameView
from instructionsview import StartView

ROW_COUNT = 40
COLUMN_COUNT = 70

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 15
HEIGHT = 15

MARGIN = 2

# This needs to be changed later I just have it like this for
# an example sprite
SPRITE_SCALING = HEIGHT / 1920

# Do the math to figure out our screen dimensions
SCREEN_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN
SCREEN_TITLE = "Rogue Testing"


def main():
    """ Main function """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = StartView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
