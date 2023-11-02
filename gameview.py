import arcade
import project_constants as constants
from classes.item import *
from classes.grid import Grid
from classes.actor import *


class GameView(arcade.View):
    # Global variables
    grid = None
    actor_list = None
    player_sprite = None
    left_pressed = False
    right_pressed = False
    up_pressed = False
    down_pressed = False

    def __init__(self):
        """
        Initializer
        """

        # Call the parent class initializer
        super().__init__()

        # Variables that will hold sprite lists
        self.shape_list = None
        self.actor_list = None
        self.item_list = None

        # Grid
        self.grid: Grid = Grid(46, 80)

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
        self.item_list = arcade.SpriteList()
        self.shape_list = arcade.ShapeElementList()

        # Set up the player
        self.player_sprite = Player(filename="static/sprite.png",
                                    scale=constants.SPRITE_SCALING)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50

        # This might all need to be in init
        self.grid.add_room(0, 0, 15, 15)

        self.recreate_grid()

        # Create Items and place them in the item_list
        # KEEP
        temp_list = create_items(determine_items())
        # TEST
        print(f"Number of classes: {len(temp_list)}")
        for item in temp_list:
            armors = [Leather, RingMail, StuddedLeather, ScaleMail, ChainMail, SplintMail, BandedMail,
                      PlateMail]
            if type(item) not in armors:
                print(f"title: {item.title}, hidden title: {item.hidden_title}, id: {item.id}")
            else:
                print(f"title: {item.title}, id: {item.id}")
            # KEEP
            item.rand_pos(self.grid)
            # KEEP
            self.item_list.append(item)

    def on_draw(self):
        """ Render the screen. """
        # TODO: On creation of new level, grab the descriptions and values of the classes seen so far and put them
        #  in a list for data persistence

        # Reset the screen
        self.clear()

        # Draw the shapes representing our current grid
        self.shape_list.draw()

        # Draw all the sprites.
        self.actor_list.draw()
        self.item_list.draw()
        self.player_sprite.draw()

    def on_update(self, delta_time):
        """ Movement and game logic """
        self.player_sprite.update()
        self.actor_list.update()
        self.item_list.update()

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """

        # Convert the clicked mouse position into grid coordinates
        column = int(x // (constants.TILE_WIDTH + constants.MARGIN))
        row = int(y // (constants.TILE_HEIGHT + constants.MARGIN))

        print(f"Click coordinates: ({x}, {y}). Grid coordinates: ({row}, {column})")

        # Make sure we are on-grid. It is possible to click in the upper right
        # corner in the margin and go to a grid location that doesn't exist
        if row >= constants.ROW_COUNT or column >= constants.COLUMN_COUNT:
            # Simply return from this method since nothing needs updating
            return

        # Flip the location between 1 and 0.
        # if self.grid[row][column] == 0:
        #     self.grid[row][column] = 1
        # else:
        #     self.grid[row][column] = 0

        # Rebuild the shapes
        self.recreate_grid()

    def on_key_press(self, key, modifiers):
        """
        Called whenever a key is pressed
        """

        if key == arcade.key.UP:
            self.player_sprite.move_dir("Up", self.grid)
        elif key == arcade.key.DOWN:
            self.player_sprite.move_dir("Down", self.grid)
        elif key == arcade.key.RIGHT:
            self.player_sprite.move_dir("Right", self.grid)
        elif key == arcade.key.LEFT:
            self.player_sprite.move_dir("Left", self.grid)

    def recreate_grid(self):
        x: int = 0
        y: int = 0
        for row in self.grid.grid:
            for t in row:
                if t.tile_type == TileType.Floor:
                    color = arcade.color.DARK_GRAY
                else:
                    color = arcade.color.BLACK
                current_rect = arcade.create_rectangle_filled(x * constants.TILE_WIDTH, y * constants.TILE_HEIGHT,
                                                              constants.TILE_WIDTH, constants.TILE_HEIGHT, color)
                self.shape_list.append(current_rect)
                x += 1
            y += 1
            x = 0

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
