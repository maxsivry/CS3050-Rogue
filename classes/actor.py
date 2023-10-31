from typing import Optional
import arcade
from arcade import Texture

# Global variables are a complete mess
# but this can be fixed when we combine everything

# Set how many rows and columns we will have
ROW_COUNT = 40
COLUMN_COUNT = 70

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 15
HEIGHT = 15

MARGIN = 2

# Do the math to figure out our screen dimensions
SCREEN_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN


class Actor(arcade.Sprite):

    # gets direction
    def move_dir(self, direction):
        if direction == 'Up' and self.center_y > 0:
            self.change_y += HEIGHT
            self.change_x = 0
        elif direction == 'Down' and self.center_y < SCREEN_HEIGHT:
            self.change_y -= HEIGHT
            self.change_x = 0
        elif direction == 'Left' and self.center_x > 0:
            self.change_x -= WIDTH
            self.change_y = 0
        elif direction == 'Right' and self.center_x < SCREEN_WIDTH:
            self.change_x += WIDTH
            self.change_y = 0

    # Physically moves
    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Check for out-of-bounds
        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - WIDTH:
            self.right = SCREEN_WIDTH

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - HEIGHT:
            self.top = SCREEN_HEIGHT

        self.change_x = 0
        self.change_y = 0


class Player(Actor):
    def __int__(self):
        Actor.__init__(self)

        # Initialize starting level
        self.level = 1

        # Initialize starting XP & XP till next level
        self.xp = 0
        self.lvl_xp = 0  # TODO: Decide how to represent and update xp till next level

        # TODO: Decide how to represent items
        # Initialize starting inventory.
        # Should start with 'some food', ring mail, short bow, 38 arrows
        self.inv = []

        # Initialize active effects list
        self.act_eff = []

        # Initialize hp to default starting hp (12) & max hp (initially the same)
        self.max_hp = 12
        self.hp = 12

        # Initialize str to default starting str (16) & max str (initially the same)
        self.str_max = 16
        self.str = 16

    def display_player_info(self) -> str:
        # NOTE: May use this, may not. Idea is that we can just call this to print character info at bottom of screen
        return f'Level: {self.level}   Gold: Decide how to represent gold   HP: {self.hp}({self.max_hp})\
               Armor: Decide how to represent armor   XP: {str(self.xp)}/{str(self.lvl_xp)}'

    def player_inventory(self) -> str:
        # NOTE: May use this, may not. Idea is that we can just call this to print character inventory
        # Create string object representing inventory
        return_str = ''
        for item in self.inv:
            # TODO: Decide how to represent items
            pass

        # Return the formatted string
        return return_str
    
    #ovverides super class mov_dir, checking tiles and items before moving player 
    #ERROR WITH MOTION IN GRID WITHOUT TILES   
    def move_dir(self, direction, grid):

        #initialize variables
        validmove = True
        #convert location to tile location
        columnindex = int(self.center_x // (WIDTH + MARGIN))
        rowindex = int(self.center_y // (HEIGHT + MARGIN))

        if (direction == "Up"):
            columnindex += 1
        elif (direction == "Down"):
            columnindex -= 1
        elif (direction == "Right"):
            rowindex += 1
        elif (direction == "Left"):
            rowindex -= 1
        #if potential move is out of grid 
        if ((rowindex >= ROW_COUNT) | (columnindex >= COLUMN_COUNT) | (rowindex < 0) | (columnindex < 0)):
            validmove = False
            return None     #exits function
        #access tile information at direction moved
        if (grid[rowindex][columnindex].tile_type == TileType.Wall):
            validmove = False
            return None

        #perform some action with t.tile_type (if trap/stairs etc)
        # ilif t.tile_type == TileType.Stairs
            # self.level += 1
            #game_view = GameView() #changing level
                # game_view.setup()
                # self.window.show_view(game_view)

        # elif t.tile_type == TileType.Trap
            # self.hp -= random.randint(1, 4)
        # . . .
        #check for items
        #for item in self.actor_list:
            #itemrow = item.center_x / WIDTH
            #itemcolumn = item.center_y / HEIGHT
            #if itemrow == rowidnex and itemcolumn == columnindex
            #perform item action / add item to inventory
        

        #update sprite location
        if (validmove):
            if direction == 'Up' and self.center_y > 0:
                self.change_y += HEIGHT
                self.change_x = 0
            elif direction == 'Down' and self.center_y < SCREEN_HEIGHT:
                self.change_y -= HEIGHT
                self.change_x = 0
            elif direction == 'Left' and self.center_x > 0:
                self.change_x -= WIDTH
                self.change_y = 0
            elif direction == 'Right' and self.center_x < SCREEN_WIDTH:
                self.change_x += WIDTH
                self.change_y = 0
