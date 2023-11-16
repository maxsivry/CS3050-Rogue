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

        # Initialize starting gold
        self.gold = 0

        # Initialize starting inventory.
        # Should start with 'some food', ring mail, short bow, 38 arrows
        self.inv = []
        self.inv.append(Mace())
        self.inv.append(RingMail())

        # Initialize weapon and armor
        self.weapon = self.inv[0]
        self.armor = self.inv[1]

        # Initialize active ring
        self.ring = None

        # Initialize hp to default starting hp (12) & max hp (initially the same)
        self.max_hp = 12
        self.health = 12

        # Initialize str to default starting str (16) & max str (initially the same)
        self.str_max = 16
        self.str = 16

        # Set Player's base defense and armor
        self.base_defense = 0
        self.armor = 0

        # main use is to calculate accuracy
        # can be used for other things if we want
        self.dex = 10

        # Indicates when the player has their turn
        self.has_turn = True

        # Is the Player alive?
        self.is_alive = True

    def display_player_info(self) -> str:
        """ Simply returns a string representing the most important stats. """
        return (f'Level: {self.level}\nGold: {self.gold}\nHP: {self.health}({self.max_hp})\n'
                f'Armor: {str(self.armor)}\nXP: {str(self.xp)}/{str(self.lvl_xp)}\n{self.str}')

    def player_inventory(self) -> str:
        """ Simply returns a formatted string representing the Player's inventory """
        # Create string object representing inventory
        return_str = ''
        
        # For each item in the Player's inventory
        for i in range(len(self.inv)):
            if (not constants.items_info[type(self.inv[i])][0] and not issubclass(type(self.inv[i]), Armor)
                    and type(self.inv[i]) is not Gold and not issubclass(type(self.inv[i]), Weapon)):
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
            validmove = False
            return None  # exits function
        # access tile information at direction moved
        if grid[rowindex, columnindex].tile_type == TileType.Wall or grid[rowindex, columnindex].tile_type == TileType.Empty:
            validmove = False
            return None

        item = None
        # Grab the item at that grid location, reset the grid location
        if grid[rowindex, columnindex].has_item:
            item = grid[rowindex, columnindex].getitem()
            if(isinstance(item, Item)):
                grid[rowindex, columnindex].has_item = False
                grid[rowindex, columnindex].item = None
                
            elif(isinstance(item, Actor)):
                self.attack(item)
                validmove = False # Prevents the player from moving after attacking
                if not item.is_alive:
                    grid[rowindex, columnindex].has_item = False
                    grid[rowindex, columnindex].item = None
                self.end_turn() # Ends turn as the player attacked
        
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
            self.end_turn() # Ends turn as the player moved to a valid location
        
        if isinstance(item, Item):
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

    # Damages the player, returns true if the damage kills the player
    def take_damage(self, damage):
        self.health -= damage
        print("You lost", damage, "health")
        if self.health <= 0:
            self.die()
            return True
        return False

    # Kills the player
    def die(self):
        # Filler at the moment should trigger the proper game over things when fully implemented
        self.is_alive = False

    def attack(self, enemy):
        # Damage should be calculated this way through the players weapon's damage function,
        # Which takes in a player and returns a damage amount based on the weapon and the players stats
        damage = self.weapon.get_damage(self)

        # right now it just returns 5 or 0 where 0 is a miss
        # damage = random.randint(0, 1)*5

        if damage > 0:
            enemy.take_damage(damage)
        else:
            print("You miss the " + enemy.name + "...", )
        
        if not enemy.is_alive:
            self.update_level(enemy.reward)
        self.end_turn()

    def get_defense(self):
        return self.base_defense + self.armor
    
    def end_turn(self):
        self.has_turn = False