import arcade
import tile
from classes.actor import Player
# Global variables are a complete mess
# but this can be fixed when we combine everything

# Set how many rows and columns we will have
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

ROW_COUNT = 40
COLUMN_COUNT = 70

class GameView(arcade.View):
    """
    Main application class.
    """

    def __init__(self):
        """
        Initializer
        """

        # Call the parent class initializer
        super().__init__()

        # Variables that will hold sprite lists
        self.actor_list = None

        # Grid
        self.grid = []

        # Set up the actor info
        self.player_sprite = None

        # Track the current state of what key is pressed

        self.left_pressed = False

        self.right_pressed = False

        self.up_pressed = False

        self.down_pressed = False

        # Set the background color
        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.actor_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = Player(filename="static/sprite.png",
                                    scale=SPRITE_SCALING)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50

        # This might all need to be in init
        for row in range(ROW_COUNT):
            # Add an empty array that will hold each cell
            # in this row
            self.grid.append([])
            for column in range(COLUMN_COUNT):
                self.grid[row].append(0)  # Append a cell
        
        self.recreate_grid()

    def on_draw(self):
        """ Render the screen. """

        # Clear the screen
        self.clear()

        # Draw the shapes representing our current grid
        self.shape_list.draw()

        # Draw all the sprites.
        self.actor_list.draw()

        self.player_sprite.draw()

    def on_update(self, delta_time):
        """ Movement and game logic """
        self.player_sprite.update()
        self.actor_list.update()

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """

        # Convert the clicked mouse position into grid coordinates
        column = int(x // (WIDTH + MARGIN))
        row = int(y // (HEIGHT + MARGIN))

        print(f"Click coordinates: ({x}, {y}). Grid coordinates: ({row}, {column})")

        # Make sure we are on-grid. It is possible to click in the upper right
        # corner in the margin and go to a grid location that doesn't exist
        if row >= ROW_COUNT or column >= COLUMN_COUNT:
            # Simply return from this method since nothing needs updating
            return

        # Flip the location between 1 and 0.
        if self.grid[row][column] == 0:
            self.grid[row][column] = 1
        else:
            self.grid[row][column] = 0

        # Rebuild the shapes
        self.recreate_grid()

    def on_key_press(self, key, modifiers):
        """
        Called whenever a key is pressed
        """

        if key == arcade.key.UP:
            self.player_sprite.move_dir("Up")
        elif key == arcade.key.DOWN:
            self.player_sprite.move_dir("Down")
        elif key == arcade.key.RIGHT:
            self.player_sprite.move_dir("Right")
        elif key == arcade.key.LEFT:
            self.player_sprite.move_dir("Left")

    # def on_key_release(self, key, modifiers):
    #     """
    #     Called when the user releases a key
    #     """
    #     if key == arcade.key.UP:
    #         self.up_pressed = False
    #     if key == arcade.key.DOWN:
    #         self.down_pressed = False
    #     if key == arcade.key.RIGHT:
    #         self.right_pressed = False
    #     if key == arcade.key.LEFT:
    #         self.left_pressed = False

    def recreate_grid(self):

        self.shape_list = arcade.ShapeElementList()
        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                if self.grid[row][column] == tile:
                    color = arcade.color.WHITE
                else:
                    color = arcade.color.BLACK

                x = (MARGIN + WIDTH) * column + MARGIN + WIDTH // 2
                y = (MARGIN + HEIGHT) * row + MARGIN + HEIGHT // 2

                current_rect = arcade.create_rectangle_filled(x, y, WIDTH, HEIGHT, color)
                self.shape_list.append(current_rect)
