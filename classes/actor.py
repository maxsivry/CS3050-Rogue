from typing import Optional
import arcade
import random
from classes.tile import *
from classes.item import *
import project_constants as constants
from arcade import Texture

# Define xp levels
XP_LEVELS = {1: 0, 2: 10, 3: 20, 4: 40, 5: 80, 6: 160, 7: 320, 8: 640, 9: 1300, 10: 2600, 11: 5200, 12: 13000,
             13: 26000, 14: 50000, 15: 100000, 16: 200000, 17: 400000, 18: 800000, 19: 2000000, 20: 4000000,
             21: 8000000}


class Actor(arcade.Sprite):

    # # gets direction
    # def move_dir(self, direction, grid):
    #     if direction == 'Up' and self.center_y > 0:
    #         self.change_y += constants.TILE_HEIGHT
    #         self.change_x = 0
    #     elif direction == 'Down' and self.center_y < constants.SCREEN_HEIGHT:
    #         self.change_y -= constants.TILE_HEIGHT
    #         self.change_x = 0
    #     elif direction == 'Left' and self.center_x > 0:
    #         self.change_x -= constants.TILE_WIDTH
    #         self.change_y = 0
    #     elif direction == 'Right' and self.center_x < constants.SCREEN_WIDTH:
    #         self.change_x += constants.TILE_WIDTH
    #         self.change_y = 0

    # Physically moves
    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Check for out-of-bounds
        if self.left < 0:
            self.left = 0
        elif self.right > constants.SCREEN_WIDTH - constants.TILE_WIDTH:
            self.right = constants.SCREEN_WIDTH

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > constants.SCREEN_HEIGHT - constants.TILE_HEIGHT:
            self.top = constants.SCREEN_HEIGHT

        self.change_x = 0
        self.change_y = 0


class Player(Actor):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            image_x: float = 0,
            image_y: float = 0,
            image_width: float = 0,
            image_height: float = 0,
            center_x: float = 0,
            center_y: float = 0,
            repeat_count_x: int = 1,  # Unused
            repeat_count_y: int = 1,  # Unused
            flipped_horizontally: bool = False,
            flipped_vertically: bool = False,
            flipped_diagonally: bool = False,
            hit_box_algorithm: Optional[str] = "Simple",
            hit_box_detail: float = 4.5,
            texture: Texture = None,
            angle: float = 0
    ):
        super().__init__(filename, scale, image_x, image_y, image_width, image_height, center_x, center_y,
                         repeat_count_x, repeat_count_y, flipped_horizontally, flipped_vertically, flipped_diagonally,
                         hit_box_algorithm, hit_box_detail, texture, angle)

        # Start at default level (1)
        self.level = 1

        # Initialize starting XP & XP till next level
        self.xp = 0
        self.lvl_xp = XP_LEVELS[self.level + 1]

        # Initialize starting inventory.
        # Should start with 'some food', ring mail, short bow, 38 arrows
        self.inv = []

        # Initialize hp to default starting hp (12) & max hp (initially the same)
        self.max_hp = 12
        self.hp = 12

        # Initialize str to default starting str (16) & max str (initially the same)
        self.str_max = 16
        self.str = 16

    # TODO: Test this
    def display_player_info(self) -> str:
        # NOTE: May use this, may not. Idea is that we can just call this to print character info at bottom of screen
        return f'Level: {self.level}   Gold: Decide how to represent gold   HP: {self.hp}({self.max_hp})\
               Armor: Decide how to represent armor   XP: {str(self.xp)}/{str(self.lvl_xp)}'

    def player_inventory(self) -> str:
        """ Simply returns a formatted string representing the Player's inventory """
        # Create string object representing inventory
        return_str = ''

        # For each item in the Player's inventory
        for i in range(len(self.inv)):
            if (not constants.items_info[type(self.inv[i])][0] and not issubclass(type(self.inv[i]), Armor)
                    and type(self.inv[i]) is not Gold):
                # If it hasn't been discovered and is not an Armor class
                return_str += f"{i}. {self.inv[i].hidden_title}\n"  # The Player can only see the hidden title
            else:
                return_str += f"{i}. {self.inv[i].title}\n"  # The Player is allowed to see the actual title

        # Return the formatted string
        return return_str

    # overrides super class mov_dir, checking tiles and items before moving player
    # ERROR WITH MOTION IN GRID WITHOUT TILES
    def move_dir(self, direction, grid):
        # initialize variables
        validmove = True
        # convert location to tile location
        columnindex = int(self.center_x / constants.TILE_WIDTH)
        rowindex = int(self.center_y / constants.TILE_HEIGHT)

        if direction == "Up":
            rowindex += 1
        elif direction == "Down":
            rowindex -= 1
        elif direction == "Right":
            columnindex += 1
        elif direction == "Left":
            columnindex -= 1
        # if potential move is out of grid
        if ((rowindex >= constants.ROW_COUNT) | (columnindex >= constants.COLUMN_COUNT) | (rowindex < 0) |
                (columnindex < 0)):
            print(rowindex, columnindex, self.center_x, constants.TILE_WIDTH, (self.center_x // constants.TILE_WIDTH))
            validmove = False
            return None  # exits function
        # access tile information at direction moved
        if grid[rowindex, columnindex].tile_type == TileType.Wall:
            validmove = False
            return None

        if validmove:
            if direction == 'Up' and self.center_y > 0:
                self.change_y += constants.TILE_HEIGHT
                self.change_x = 0
            elif direction == 'Down' and self.center_y < constants.SCREEN_HEIGHT:
                self.change_y -= constants.TILE_HEIGHT
                self.change_x = 0
            elif direction == 'Left' and self.center_x > 0:
                self.change_x -= constants.TILE_WIDTH
                self.change_y = 0
            elif direction == 'Right' and self.center_x < constants.SCREEN_WIDTH:
                self.change_x += constants.TILE_WIDTH
                self.change_y = 0

        # Grab the item at that grid location, reset the grid location
        if grid[rowindex, columnindex].has_item:
            item = grid[rowindex, columnindex].getitem()
            grid[rowindex, columnindex].has_item = False
            grid[rowindex, columnindex].item = None
            return item

        # if tile type is stairs
        # elif grid[rowindex, columnindex].tile_type == TileType.Stairs:
        #     self.level += 1
        #     #change level
        #     if (self.level == 2):
        #         lvl2_view = Game2View() #change level
        #         lvl2_view.setup()
        #         self.window.show_view(lvl2_view)
        #     if (self.level == 3):
        #         lvl3_view = Game2View() #change level
        #         lvl3_view.setup()
        #         self.window.show_view(lvl2_view)

        # elif grid[rowindex, columnindex].tile_type == TileType.Trap:

        # self.hp -= random.randint(1, 4)
        # . . .
        # check for items
        # if (grid[rowindex][columnindex].has_item):
        # item = grid[rowindex][columnindex].get_item
        # call item method
        # perform item action / add item to inventory

    def update_level(self, input_xp: int):
        """ update_level takes an input xp increase and updates the players level
        (does any level ups if need be). """
        # Updates the Player's level given set xp increase
        # Add input_xp to xp
        self.xp += input_xp

        # If xp increase is enough to get to multiple levels
        while self.xp >= self.lvl_xp:
            # Check if there is an available next level (not max level)
            avail_lvl = True if self.level + 1 in XP_LEVELS.keys() else False

            # Update level, xp, and lvl_xp
            # NOTE: At max level, your level will stay the same and xp will equal lvl_xp at 8,000,000
            self.xp = self.xp - self.lvl_xp if avail_lvl else XP_LEVELS[21]
            self.level += 1 if avail_lvl else 21
            self.lvl_xp = XP_LEVELS[self.level + 1] if avail_lvl else XP_LEVELS[21]

    # TODO: Test this
    def update_health(self, level_increase: bool):
        # If increase in level, increase health by adding a random number 1-10
        if level_increase:
            self.hp += random.randint(1, 10)

        # Update health due to active effects
        pass

    # TODO: Test this
    def update_strength(self):
        # Update strength due to active effects
        pass
