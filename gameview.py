import arcade
import project_constants as constants
from classes.item import *
from classes.grid import Grid
from classes.actor import *
import arcade.gui


# TODO: Make it so items can't spawn on boundaries

class GameView(arcade.View):
    # Global variables
    grid = None
    actor_list = None
    player_sprite = None
    left_pressed = False
    right_pressed = False
    up_pressed = False
    down_pressed = False
    Inventory_open = False
    highlighted_item = 0
    appended = False

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
        self.player_sprite.center_x = 7.5
        self.player_sprite.center_y = 7.5
        self.player_sprite.inv.append(Gold(gold=0))
        self.player_sprite.inv.append(Weapon())
        self.player_sprite.inv.append(RingMail())

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

        #player stats
        stats_rect = arcade.create_rectangle_filled(1137, constants.SCREEN_HEIGHT / 2, 174, constants.SCREEN_HEIGHT, arcade.color.ICEBERG)
        self.shape_list.append(stats_rect)


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

        self.item_list.draw()

        #display player stats:
        arcade.draw_text("STATS", 1062, 
                        constants.SCREEN_HEIGHT - 50,
                        arcade.color.BLACK, font_size=10, font_name="Kenney Rocket",
                        width=150)

        arcade.draw_text(self.player_sprite.display_player_info(), 1062, 
                        constants.SCREEN_HEIGHT - 70,
                        arcade.color.BLACK, font_size=10, multiline=True, 
                        width=150)


        #if inventory is displayed
        inventory_rect = arcade.create_rectangle_filled(constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2, 300, 400, arcade.color.ICEBERG)
        if not self.Inventory_open:
            self.hide_inventory(inventory_rect)             
        else:
            self.display_inventory(inventory_rect)


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

    def on_key_press(self, key, modifiers):
        """
        Called whenever a key is pressed
        """
        #Open inventory command, e toggles inventory
        if key == arcade.key.E:
            self.Inventory_open = not self.Inventory_open
            self.highlighted_item = 0

        if not self.Inventory_open:
            #player movement, each movement potentially picks up item
            item = None
            if key == arcade.key.UP:
                item = self.player_sprite.move_dir("Up", self.grid)
            elif key == arcade.key.DOWN:
                item = self.player_sprite.move_dir("Down", self.grid)
            elif key == arcade.key.RIGHT:
                item = self.player_sprite.move_dir("Right", self.grid)
            elif key == arcade.key.LEFT:
                item = self.player_sprite.move_dir("Left", self.grid)
            self.pick_up_item(item)


        #if inventory is open
        if self.Inventory_open:

            #Up and down to determine item to interact with (highlighting appropriate line)
            if key == arcade.key.UP and self.highlighted_item > 0:
                self.highlighted_item -= 1
            elif key == arcade.key.DOWN and self.highlighted_item < len(self.player_sprite.inv) - 1:
                self.highlighted_item += 1

            #Dropping Item with D
            elif key == arcade.key.D:
                if 0 <= self.highlighted_item < len(self.player_sprite.inv)-1:
                    # Remove the highlighted item from the inventory
                    del self.player_sprite.inv[self.highlighted_item]

            #using item with U
            elif key == arcade.key.U:
                if 0 <= self.highlighted_item < len(self.player_sprite.inv)-1:
                    self.use(self.player_sprite.inv[self.highlighted_item])


    def recreate_grid(self):
        x: int = 0
        y: int = 0
        for row in self.grid.grid:
            for t in row:
                if t.tile_type == TileType.Floor:
                    color = arcade.color.DARK_GRAY
                else:
                    color = arcade.color.BLACK
                current_rect = arcade.create_rectangle_filled(x * constants.TILE_WIDTH+7.5, y * constants.TILE_HEIGHT+7.5,
                                                              constants.TILE_WIDTH, constants.TILE_HEIGHT, color)
                self.shape_list.append(current_rect)
                x += 1
            y += 1
            x = 0

    # Method to determine center_x and center_y of an item
    def rand_pos(self):
        """ Determines a randomized position on the grid/screen for each of a set of Items """

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
            item.set_position((col * constants.TILE_WIDTH) + 7.5, (row * constants.TILE_HEIGHT)+7.5)
            self.grid[row, col].setitem(item)

    def use(self, item, weapon=None, armor=None, monster=None):
        """ use function used to call an Item's use method with the correct parameters. """

        # Match the item's class
        # Use methods have different parameters dependent on the class
        # Call the corresponding use method with the correct parameters
        # NOTE: Cannot use a match statement here since each item has unique values for it's fields
        if isinstance(item, Gold):
            item.use(self.player_sprite)
        elif isinstance(item, MagicMapping):
            item.use(self.player_sprite, self.grid)
        elif isinstance(item, IdentifyWeapon):
            item.use(self.player_sprite, weapon)
        elif isinstance(item, IdentifyArmor):
            item.use(self.player_sprite, armor)
        elif isinstance(item, RemoveCurse):
            item.use(self.player_sprite)
        elif isinstance(item, Poison):
            item.use(self.player_sprite)
        elif isinstance(item, MonsterDetection):
            item.use(self.player_sprite, self.grid)
        elif isinstance(item, RestoreStrength):
            item.use(self.player_sprite)
        elif isinstance(item, Healing):
            item.use(self.player_sprite)
        elif isinstance(item, Light):
            item.use(self.player_sprite)
        elif isinstance(item, TeleportTo):
            item.use(self.player_sprite, self.grid)
        elif isinstance(item, TeleportAway):
            item.use(self.player_sprite, monster, self.grid)
        elif isinstance(item, SlowMonster):
            item.use(self.player_sprite, monster)
        elif isinstance(item, AddStrength):
            item.use(self.player_sprite)
        elif isinstance(item, IncreaseDamage):
            item.use(self.player_sprite)
        elif isinstance(item, Teleportation):
            item.use(self.player_sprite, self.grid)
        elif isinstance(item, Dexterity):
            item.use(self.player_sprite)
        else:  # Items that reach here do not have a use method. They should not be passed into this function
            pass


    def pick_up_item(self, item):
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
                    if type(self.item_list[i]) == Gold:
                        # Add the new gold value to the Player's gold value
                        self.use(self.item_list[i])
                    else:
                        # Otherwise, add the instance of the Item to the Player's inventory
                        self.player_sprite.inv.append(self.item_list[i])
                    print(self.player_sprite.player_inventory())
        # Check if index was changed
        if index != -1:
            self.item_list.pop(index)


    def display_inventory(self, rect):
        #draw box to contain inventory, title underline. draw another rectange to help with directons
        self.shape_list.append(rect)
        self.appended = True
        arcade.draw_text("INVENTORY", constants.SCREEN_WIDTH / 2 - 140, constants.SCREEN_HEIGHT / 2 + 175, arcade.color.BLACK, font_size=20, width=280, align="center", font_name="Kenney Rocket")
        arcade.draw_line(constants.SCREEN_WIDTH / 2 - 150, constants.SCREEN_HEIGHT / 2 + 165, constants.SCREEN_WIDTH / 2 + 150, constants.SCREEN_HEIGHT / 2 + 165, arcade.color.DARK_RED, line_width=2)
        arcade.draw_line(627, 487, 727, 487, arcade.color.DARK_RED, line_width=2)
        arcade.draw_line(627, 487, 627, 392, arcade.color.DARK_RED, line_width=2)
        arcade.draw_line(627, 392, 727, 392, arcade.color.DARK_RED, line_width=2)
        arcade.draw_line(727, 487, 727, 392, arcade.color.DARK_RED, line_width=2)
        instructions = [
            "UP/DOWN to select",
            "D to drop item",
            "U to use/equip item",
            "R to throw item",
            "E to exit inventory"
        ]
        text_x = 630
        text_y = 475
        for instruction in instructions:
            arcade.draw_text(instruction, text_x, text_y, arcade.color.BLACK, font_size=8, font_name="Arial")
            text_y -= 20 

        # Draw inventory items with highlighting
        for i, item in enumerate(self.player_sprite.inv):
            y = constants.SCREEN_HEIGHT / 2 + 150 - i * 15
            color = arcade.color.RED if i == self.highlighted_item else arcade.color.BLACK
            if (not constants.items_info[type(item)][0] and not issubclass(type(item), Armor)
                    and type(item) is not Gold and type(item) is not Weapon):
                arcade.draw_text(item.hidden_title, constants.SCREEN_WIDTH / 2 - 140, y, color, font_size=10, multiline=True, width=280)
            else:
                arcade.draw_text(item.title, constants.SCREEN_WIDTH / 2 - 140, y, color, font_size=10, multiline=True, width=280)
        
    
    def hide_inventory(self, rect):
        #how to remove inventory_rect ???
        if self.appended:
            self.shape_list.remove(rect)
        #self.shape_list.remove(inventory_rect)
        arcade.draw_text("INVENTORY", 1062, 
                        constants.SCREEN_HEIGHT - 200,
                        arcade.color.BLACK, font_size=10, font_name="Kenney Rocket",
                        width=150)
        arcade.draw_text(self.player_sprite.player_inventory(), 1062, 
                    constants.SCREEN_HEIGHT - 220,
                    arcade.color.BLACK, font_size=10, multiline=True, 
                    width=150) 


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

    