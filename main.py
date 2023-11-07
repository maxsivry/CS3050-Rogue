import arcade
from instructionsview import StartView
import project_constants as constants


def main():
    """ Main function """
    window = arcade.Window(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, constants.SCREEN_TITLE)
    start_view = StartView()
    window.show_view(start_view)
    arcade.run()

if __name__ == "__main__":
    main()
