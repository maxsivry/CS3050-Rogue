import arcade
import project_constants as constants
from classes.item import *
from classes.grid import Grid
from classes.actor import *
import arcade.gui


# TODO: Make it so items can't spawn on boundaries
# TODO: Start use methods (each class will have a use method)

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

        # #
        # self.manager = arcade.gui.UIManager()
        # self.manager.enable()

        # # Create a box group to align the 'open' button in the center
        # self.v_box = arcade.gui.UIBoxLayout()

        # # Create a button. We'll click on this to open our window.
        # # Add it v_box for positioning.
        # inventory_box = arcade.gui.UIFlatButton(text="Inventory", width=200)
        # self.v_box.add(inventory_box)

        # # Add a hook to run when we click on the button.
        # inventory_box.on_click = self.on_click_open
        # # Create a widget to hold the v_box widget, that will center the buttons
        # self.manager.add(
        #     arcade.gui.UIAnchorWidget(
        #         anchor_x="100",
        #         anchor_y="10",
        #         child=self.v_box)
        # )

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.actor_list = arcade.SpriteList()
        self.item_list = arcade.SpriteList()
        self.shape_list = arcade.ShapeElementList()

        # Set up the player
        self.player_sprite = Player(filename="static/sprite.png",
                                    scale=constants.SPRITE_SCALING)
        self.player_sprite.center_x = 7.5
        self.player_sprite.center_y = 7.5

        # This might all need to be in init
        self.grid.add_room(0, 0, 15, 15)

        self.recreate_grid()

        # Create Items and place them in the item_list
        temp_list = create_items(determine_items())
        print(f"Number of classes: {len(temp_list)}")
        for item in temp_list:
            armors = [Leather, RingMail, StuddedLeather, ScaleMail, ChainMail, SplintMail, BandedMail,
                      PlateMail]
            if type(item) not in armors and type(item) is not Gold:
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
        self.item_list.draw()
        self.player_sprite.draw()
        # self.manager.draw()

        # Convert Player's position into grid coordinates
        # row_p = self.player_sprite.center_x // constants.TILE_WIDTH
        # col_p = self.player_sprite.center_x // constants.TILE_HEIGHT
        #
        # # For each item in item_list
        # for i in range(len(self.item_list) - 1):
        #
        #     # Convert Item's position into grid coordinates
        #     row_i = self.item_list[i].center_x // constants.TILE_WIDTH
        #     col_i = self.item_list[i].center_y // constants.TILE_HEIGHT
        #
        #     # Check if Player's coordinates overlap with Item's
        #     if row_i == row_p and col_i == col_p:
        #         # If it does, add item to Player's inventory and remove from item_list
        #         self.player_sprite.inv.append(self.item_list.pop(i))

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
        column = int(x / constants.TILE_WIDTH)
        row = int(y / constants.TILE_HEIGHT)

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
        item = None
        if key == arcade.key.UP:
            item = self.player_sprite.move_dir("Up", self.grid)
        elif key == arcade.key.DOWN:
            item = self.player_sprite.move_dir("Down", self.grid)
        elif key == arcade.key.RIGHT:
            item = self.player_sprite.move_dir("Right", self.grid)
        elif key == arcade.key.LEFT:
            item = self.player_sprite.move_dir("Left", self.grid)

        # Set index variable -> Will be used to pop item off of list AFTER loop as to not cause off-by-one error
        index = -1

        # If there is an item
        if item is not None:
            # Loop through to find the item in item_list
            for i in range(len(self.item_list)):
                # When the item is found
                if self.item_list[i].id == item.id:
                    # Grab it's index in item_list
                    index = i

                    # Add the item to the Player's inventory
                    self.player_sprite.inv.append(self.item_list[i])
                    print(self.player_sprite.player_inventory())
        # Check if index was changed
        if index != -1:
            self.item_list.pop(index)

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

            # While TileType != Floor and TileType != Trail and Tile has an item
            while ((temp_pos.tile_type != TileType.Floor and temp_pos.tile_type != TileType.Trail)
                   or temp_pos.has_item):
                # Determine random position again
                # Get random grid position
                row = randint(0, self.grid.n_rows - 1)
                col = randint(0, self.grid.n_cols - 1)

                # Set the temporary grid position
                temp_pos = self.grid.grid[row][col]

            # Set this Item's position
            item.set_position(col * constants.TILE_WIDTH, row * constants.TILE_HEIGHT)
            self.grid[row, col].setitem(item)

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

    # #textbox
    # def on_click_open(self, event):
    #     # The code in this function is run when we click the ok button.
    #     # The code below opens the message box and auto-dismisses it when done.
    #     message_box = arcade.gui.UIMessageBox(
    #         width=300,
    #         height=200,
    #         message_text=(
    #             self.player_sprite.player_inventory
    #         ),
    #         callback=self.on_message_box_close,buttons=["Ok", "Cancel"]
    #     )

    #     self.manager.add(message_box)
