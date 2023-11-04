import arcade
import project_constants as constants
from classes.item import *
from classes.grid import Grid
from classes.actor import *


# TODO: Make it so items can be picked up by player, can't spawn on boundaries,
#  when item is used->sets items_info to True
# TODO: Start use methods (each class will have a use method) -> To start, use methods updates that Item's boolean in
#  items_info

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
        self.player_sprite.center_x = 15
        self.player_sprite.center_y = 15

        # This might all need to be in init
        self.grid.add_room(0, 0, 15, 15)

        self.recreate_grid()

        # Create Items and place them in the item_list
        temp_list = create_items(determine_items())
        print(f"Number of classes: {len(temp_list)}")
        for item in temp_list:
            armors = [Leather, RingMail, StuddedLeather, ScaleMail, ChainMail, SplintMail, BandedMail,
                      PlateMail]
            if type(item) not in armors:
                print(f"title: {item.title}, hidden title: {item.hidden_title}, id: {item.id}")
            else:
                print(f"title: {item.title}, id: {item.id}")
            self.item_list.append(item)
        self.rand_pos()

    def on_draw(self):
        """ Render the screen. """

        # Reset the screen
        self.clear()

        # Draw the shapes representing our current grid
        self.shape_list.draw()

        # Draw all the sprites.
        self.actor_list.draw()
        # for item in self.item_list:
        #     if not item.is_hidden:
        #         item.draw()
        self.player_sprite.draw()

        # Convert Player's position into grid coordinates
        row_p = self.player_sprite.center_x // constants.TILE_WIDTH
        col_p = self.player_sprite.center_x // constants.TILE_HEIGHT

        # For each item in item_list
        for i in range(len(self.item_list) - 1):

            # Convert Item's position into grid coordinates
            row_i = self.item_list[i].center_x // constants.TILE_WIDTH
            col_i = self.item_list[i].center_y // constants.TILE_HEIGHT

            # Check if Player's coordinates overlap with Item's
            if row_i == row_p and col_i == col_p:
                # If it does, add item to Player's inventory and remove from item_list
                self.player_sprite.inv.append(self.item_list.pop(i))

        self.item_list.draw()

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

        print(f"Click coordinates: ({x}, {y}). Grid coordinates: ({row}, {column}). ")

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

    # Method to determine center_x and center_y of an item
    def rand_pos(self):
        """ Determines a randomized position on the grid/screen for each of a set of Items """

        # Create a list of grid positions already chosen
        # Each position has the form [row, col]
        chosen_pos = []

        # For each item in item_list
        for item in self.item_list:
            # Get random grid position
            row = randint(0, self.grid.n_rows - 1)
            col = randint(0, self.grid.n_cols - 1)

            # Set the temporary grid position
            temp_pos = self.grid.grid[row][col]

            # While TileType != Floor or TileType != Trail
            while (temp_pos.tile_type != TileType.Floor and temp_pos.tile_type != TileType.Trail
                   and [row, col] not in chosen_pos):
                # Determine random position again
                # Get random grid position
                row = randint(0, self.grid.n_rows - 1)
                col = randint(0, self.grid.n_cols - 1)

                # Set the temporary grid position
                temp_pos = self.grid.grid[row][col]

            # Set this Item's position
            # if not temp_pos.is_hidden:  # If the tile is not hidden, this item is not hidden too
            #   item.set_position(x, y)
            #   item.is_hidden = False
            #   grid[row][col].item = self
            # else:  # If a tile is hidden, this item is hidden too
            #   item.set_position(x, y)
            #   grid[row][col].item = self
            item.set_position(row * constants.TILE_WIDTH, col * constants.TILE_HEIGHT)  # Delete when ^ uncommented
            chosen_pos.append([row, col])

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
