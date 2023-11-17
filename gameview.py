import arcade
import project_constants as constants
from classes.item import *
from classes.grid import Grid
from binarytree import *
from classes.actor import *
from classes.enemy import *
import arcade.gui
from endview import EndView


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
    recent_coords = []

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
        self.enemy_list = None

        # Grid
        self.grid: Grid = Grid(40, 70)

        self.tree: Tree = Tree(0, 0, 40, 70)

        # Set up the actor info
        self.player_sprite = None

        # Track the current state of what key is pressed

        self.left_pressed = False

        self.right_pressed = False

        self.up_pressed = False

        self.down_pressed = False

        # Track the most recent set of grid coordinates given by a click (to be used with wands)
        self.recent_coords = [0, 0]

        # Set the background color
        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.actor_list = arcade.SpriteList()
        self.item_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.shape_list = arcade.ShapeElementList()

        # Set up the player
        self.player_sprite = Player(filename="static/sprite.png",
                                    scale=constants.SPRITE_SCALING)
        self.player_sprite.center_x = 30
        self.player_sprite.center_y = 30

        # This might all need to be in init
        populate_tree(self.tree.root, 4)

        rooms = get_rooms(self.tree.root)
        trails = create_trails(self.tree.root)
        for trail in trails:
            x, y = trail
            self.grid.grid[x][y].tile_type = TileType.Trail
        for room in rooms:
            self.grid.add_room(room)

        self.recreate_grid()

        monsters = create_monsters(self.player_sprite.level)
        for monster in monsters:
            self.enemy_list.append(monster)

        # # Create Items and place them in the item_list
        temp_list = create_items(determine_items())
        for item in temp_list:
            self.item_list.append(item)

        # Determine the Items' positions
        self.rand_pos()

        # player stats
        stats_rect = arcade.create_rectangle_filled(1137, constants.SCREEN_HEIGHT / 2, 174, constants.SCREEN_HEIGHT,
                                                    arcade.color.ICEBERG)
        self.shape_list.append(stats_rect)

        # title rect
        title = arcade.create_rectangle_filled(525, constants.SCREEN_HEIGHT - 41, 1050, 82, arcade.color.ICEBERG)
        self.shape_list.append(title)

        # player stats
        current_rect = arcade.create_rectangle_filled(1137, constants.SCREEN_HEIGHT / 2, 174, constants.SCREEN_HEIGHT,
                                                      arcade.color.ICEBERG)
        self.shape_list.append(current_rect)

    def on_draw(self):
        """ Render the screen. """
        # Reset the screen
        self.clear()
        # Draw the shapes representing our current grid
        self.shape_list.draw()

        # Draw all the sprites.
        self.actor_list.draw()
        self.enemy_list.draw()
        self.item_list.draw()
        self.player_sprite.draw()

        # display player stats:
        arcade.draw_text("STATS", 1062,
                         constants.SCREEN_HEIGHT - 50,
                         arcade.color.BLACK, font_size=10, font_name="Kenney Rocket",
                         width=150)

        arcade.draw_text(self.player_sprite.display_player_info(), 1062,
                         constants.SCREEN_HEIGHT - 70,
                         arcade.color.BLACK, font_size=10, multiline=True,
                         width=150)

        arcade.draw_text("TO WIN OR TO ROGUE", 525,
                         constants.SCREEN_HEIGHT - 41,
                         arcade.color.BLACK, font_size=20,
                         width=150, anchor_x="center", font_name="Kenney Rocket")

        # message = ""
        # for enemy in self.enemy_list:
        #     if enemy.message != "":
        #         message += enemy.message + "\n"
        #         #enemy.message = ""
        
        if constants.battle_message != "":
            self.battlemessage(constants.battle_message)

        # if inventory is displayed
        inventory_rect = arcade.create_rectangle_filled(constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2, 300,
                                                        400, arcade.color.ICEBERG)

        if not self.Inventory_open:
            self.hide_inventory()
        else:
            inventory_rect.draw()
            self.display_inventory()
        

    def on_update(self, delta_time):
        """ Movement and game logic """
        self.player_sprite.update()
        self.actor_list.update()
        self.item_list.update()
        self.enemy_list.update()
        if not self.player_sprite.has_turn:
            new_enemies = arcade.SpriteList()
            for enemy in self.enemy_list:
                if enemy.is_alive:
                    if self.player_sprite.is_alive:
                        enemy.take_turn(self.player_sprite, self.grid)
                    new_enemies.append(enemy)
            self.player_sprite.has_turn = True
            self.enemy_list = new_enemies

        if not self.player_sprite.is_alive:
            self.quit_game()

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """

        # Convert the clicked mouse position into grid coordinates
        column = int(x / constants.TILE_WIDTH)
        row = int(y / constants.TILE_HEIGHT)

        print(f"Click coordinates: ({x}, {y}). Grid coordinates: ({row}, {column}). ")

        self.recent_coords = [row, column]

        # Make sure we are on-grid. It is possible to click in the upper right
        # corner in the margin and go to a grid location that doesn't exist
        if row >= constants.ROW_COUNT or column >= constants.COLUMN_COUNT:
            # Simply return from this method since nothing needs updating
            return

    def on_key_press(self, key, modifiers):
        """
        Called whenever a key is pressed
        """

        constants.battle_message = ""

        # Open inventory command, e toggles inventory
        if key == arcade.key.E:
            self.Inventory_open = not self.Inventory_open
            self.highlighted_item = 0

        # display help message
        if key == arcade.key.H:
            self.help_message()

        if key == arcade.key.ESCAPE:
            self.quit_game()

        if not self.Inventory_open:
            # player movement, each movement potentially picks up item
            item = None
            if key == arcade.key.UP:
                direction = 'Up'
                item = self.player_sprite.move_dir(direction, self.grid)
            elif key == arcade.key.DOWN:
                direction = 'Down'
                item = self.player_sprite.move_dir(direction, self.grid)
            elif key == arcade.key.RIGHT:
                direction = 'Right'
                item = self.player_sprite.move_dir(direction, self.grid)
            elif key == arcade.key.LEFT:
                direction = 'Left'
                item = self.player_sprite.move_dir(direction, self.grid)
            # Pick up item
            self.pick_up_item(item)
        else:
            # Move the highlighted item up
            if key == arcade.key.UP and self.highlighted_item > 0:
                self.highlighted_item -= 1
            # Move the highlighted item down
            elif key == arcade.key.DOWN and self.highlighted_item < len(self.player_sprite.inv) - 1:
                self.highlighted_item += 1
            # Dropping Item with D (cant drop if there is already an item at location)
            elif key == arcade.key.D:
                if 0 <= self.highlighted_item < len(self.player_sprite.inv):

                    # if there is no item at location already:
                    col = int(self.player_sprite.center_x / constants.TILE_WIDTH)
                    row = int(self.player_sprite.center_y / constants.TILE_HEIGHT)
                    if not self.grid[row, col].has_item:
                        # drop item on correct tile, set tile to have item
                        self.player_sprite.inv[self.highlighted_item].set_position(self.player_sprite.center_x,
                                                                                   self.player_sprite.center_y)
                        self.item_list.append(self.player_sprite.inv[self.highlighted_item])
                        self.grid[row, col].setitem(self.player_sprite.inv[self.highlighted_item])
                        # Remove the highlighted item from the inventory
                        del self.player_sprite.inv[self.highlighted_item]

            # using item with U
            elif key == arcade.key.U:
                if 0 <= self.highlighted_item < len(self.player_sprite.inv):
                    self.use(self.player_sprite.inv[self.highlighted_item])

    # Method to determine center_x and center_y of an item
    def rand_pos(self):
        """ Determines a randomized position on the grid/screen for each of a set of Items """
        # For each item in item_list
        def rand_thing(obj_list):
            for obj in obj_list:
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
                obj.set_position((col * constants.TILE_WIDTH) + 7.5, (row * constants.TILE_HEIGHT) + 7.5)
                self.grid[row, col].setitem(obj)

        rand_thing(self.item_list)
        rand_thing(self.enemy_list)

    def use(self, item, weapon=None, armor=None, monster=None):
        """ use function used to call an Item's use method with the correct parameters. """
        # Match the item's class
        # Use methods have different parameters dependent on the class
        # Call the corresponding use method with the correct parameters
        # NOTE: Cannot use a match statement here since each item has unique values for it's fields
        if isinstance(item, Gold):
            item.use(self.player_sprite)
        elif isinstance(item, IncreaseMaxHealth):
            item.use(self.player_sprite)
        elif isinstance(item, IdentifyRing):
            item.use(self.player_sprite)
        elif isinstance(item, IdentifyPotion):
            item.use(self.player_sprite)
        elif isinstance(item, Poison):
            item.use(self.player_sprite)
        elif isinstance(item, RestoreStrength):
            item.use(self.player_sprite)
        elif isinstance(item, Healing):
            item.use(self.player_sprite)
        elif isinstance(item, TeleportTo):
            item.use(self.player_sprite, self.grid, self.recent_coords)
        elif isinstance(item, DrainLife):
            item.use(self.player_sprite, self.enemy_list)
        elif issubclass(type(item), Ring):
            if self.player_sprite.ring and item.charges > 0:
                self.player_sprite.ring.unequip(self.player_sprite, self.grid)
            item.use(self.player_sprite, self.grid)
            self.player_sprite.ring = item

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

    def recreate_grid(self):
        x: int = 0
        y: int = 0
        for row in self.grid.grid:
            for t in row:
                color: Tuple[int, int, int] = None
                match t.tile_type:
                    case TileType.Floor:
                        color = arcade.color.DARK_GRAY
                    case TileType.Wall:
                        color = arcade.color.WHITE
                    case TileType.Trail:
                        color = arcade.color.RED
                    case _:
                        color = arcade.color.BLACK

                current_rect = arcade.create_rectangle_filled(x * constants.TILE_WIDTH, y * constants.TILE_HEIGHT,
                                                              constants.TILE_WIDTH, constants.TILE_HEIGHT, color)
                self.shape_list.append(current_rect)
                x += 1
            y += 1
            x = 0

    def display_inventory(self):
        arcade.draw_text("INVENTORY", constants.SCREEN_WIDTH / 2 - 140, constants.SCREEN_HEIGHT / 2 + 175,
                         arcade.color.BLACK, font_size=20, width=280, align="center", font_name="Kenney Rocket")
        arcade.draw_line(constants.SCREEN_WIDTH / 2 - 150, constants.SCREEN_HEIGHT / 2 + 165,
                         constants.SCREEN_WIDTH / 2 + 150, constants.SCREEN_HEIGHT / 2 + 165, arcade.color.DARK_RED,
                         line_width=2)
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
                    and not issubclass(type(item), Weapon)
                    and type(item) is not Gold
                    and type(item) is not issubclass(type(self.player_sprite.inv[i]), Weapon)):
                arcade.draw_text(item.hidden_title, constants.SCREEN_WIDTH / 2 - 140, y, color, font_size=10,
                                 multiline=True, width=280)
            else:
                arcade.draw_text(item.title, constants.SCREEN_WIDTH / 2 - 140, y, color, font_size=10, multiline=True,
                                 width=280)

    def hide_inventory(self):
        arcade.draw_text("INVENTORY", 1062,
                         constants.SCREEN_HEIGHT - 200,
                         arcade.color.BLACK, font_size=10, font_name="Kenney Rocket",
                         width=150)
        arcade.draw_text(self.player_sprite.player_inventory(), 1062,
                         constants.SCREEN_HEIGHT - 220,
                         arcade.color.BLACK, font_size=10, multiline=True,
                         width=150)

    def help_message(self):
        pass

    def battlemessage(self, message):
        box_width = 300
        box_height = 150
        box_x = (constants.SCREEN_WIDTH / 2)
        box_y = (constants.SCREEN_HEIGHT / 2)
        box_color = arcade.color.ICEBERG
        border_color = arcade.color.DARK_RED
        rotation_angle = 0

        # Draw box
        arcade.draw_rectangle_filled(box_x, box_y, box_width, box_height, box_color)
        arcade.draw_rectangle_outline(box_x, box_y, box_width, box_height, border_color, 4)

        # Draw text
        arcade.draw_text("BATTLE!", box_x, box_y + (box_height / 2),
                         arcade.color.BLACK, font_size=16, anchor_x="center", anchor_y="top", font_name="Kenney Rocket")
        
        arcade.draw_text(message, box_x-140, box_y + (box_height / 4),
                         arcade.color.BLACK, font_size=10, width=150, anchor_x="left")

    def quit_game(self):
        end_view = EndView(self.player_sprite)
        self.window.show_view(end_view)
