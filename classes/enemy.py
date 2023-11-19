import arcade
from classes.tile import TileType
from classes.grid import Grid
import random
import sys
import project_constants as constants
from classes.actor import Actor

CRAB_CHANCE = 30
WRAITH_CHANCE = 10
DRAGON_CHANCE = 1


def create_monsters(level):
    # Create area to store created objects
    monster_list = []

    num_monsters = (int)(random.randint(5, 15) + level)

    for _ in range(num_monsters):
        monster_type = random.randint(0, 100 - level)
        if monster_type < DRAGON_CHANCE and level > 3:
            monster_list.append(Dragon(filename="static/dragon.png", scale=constants.SPRITE_SCALING))
        if monster_type < WRAITH_CHANCE:
            monster_list.append(Wraith(filename="static/wraith.png", scale=constants.SPRITE_SCALING))
        elif monster_type < CRAB_CHANCE:
            monster_list.append(Crab(filename="static/crab.png", scale=constants.SPRITE_SCALING))
        else:
            monster_list.append(Slime(filename="static/slime.png", scale=constants.SPRITE_SCALING))

    return monster_list


class Enemy(Actor):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1
    ):
        super().__init__(filename=filename, scale=scale)
        self.health = 7
        self.name = "Slime"
        self.is_alive = True
        # XP rewarded upon defeat
        self.reward = 1
        self.range = 15

    def get_damage(self):
        hit = random.randint(1, 10)
        if hit > 5:
            return random.randint(1, 3)
        return 0

    def attack(self, player):
        damage = self.get_damage()
        if damage > 0:
            true_damage = damage - player.get_defense()
            if true_damage > 0:
                if player.take_damage(true_damage):
                    self.log("You were killed by " + self.name)
            else:
                self.log("You took no damage")
        else:
            self.log("The " + self.name + " missed...")

    def take_damage(self, damage):
        self.health -= damage
        self.log("The " + self.name + " lost " + str(damage) + " health")
        if self.health <= 0:
            self.die()
            return True
        return False

    def die(self):
        self.log("You defeated the " + self.name)
        self.is_alive = False

    # Returns true if the enemy is one tile away from the player
    # Currently always returns false 
    def is_near(self, player, grid):

        # #convert location to tile location player
        player_col = int(player.center_x / constants.TILE_WIDTH)
        player_row = int(player.center_y / constants.TILE_HEIGHT)

        # convert location to tile location monster
        monster_col = int(self.center_x / constants.TILE_WIDTH)
        monster_row = int(self.center_y / constants.TILE_HEIGHT)
        row_diff = player_row - monster_row
        col_diff = player_col - monster_col

        if (abs(row_diff) <= 1) and (abs(col_diff) <= 1):
            return True
        else:
            return False

    def take_turn(self, player, game):
        if self.is_near(player, game):
            self.attack(player)
        else:
            self.chase(player, game)

    # The monsters movement turn
    # Takes in the player and the games state
    # to calculate where the monster should move
    # Default monster doesn't do anything
    def chase(self, player, grid):
        # function that takes in grid and returns true if move is valid
        def checkvalid(grid, rM, cM):
            return (
                    (grid[rM, cM].tile_type != TileType.Wall)
                    and (grid[rM, cM].tile_type != TileType.Empty)
                    and (rM < constants.ROW_COUNT)
                    and (cM < constants.COLUMN_COUNT)
                    and (rM >= 0)
                    and (cM >= 0)
            )

        # #convert location to tile location player
        player_col = int(player.center_x / constants.TILE_WIDTH)
        player_row = int(player.center_y / constants.TILE_HEIGHT)

        # convert location to tile location monster
        monster_col = int(self.center_x / constants.TILE_WIDTH)
        monster_row = int(self.center_y / constants.TILE_HEIGHT)
        row_diff = player_row - monster_row
        col_diff = player_col - monster_col

        # #if monster is close enough to "see" (if monster row or col is within 10)
        if (abs(row_diff) < self.range) and (abs(col_diff) < self.range):

            # check if either potential move is invalid
            # If the player is above or below the monster
            new_monster_row = monster_row + (1 if row_diff > 0 else -1)
            new_monster_col = monster_col
            valid1 = checkvalid(grid, new_monster_row, new_monster_col)
            # If the player is to the left or right of the monster
            new_monster_row2 = monster_row
            new_monster_col2 = monster_col + (1 if col_diff > 0 else -1)
            valid2 = checkvalid(grid, new_monster_row2, new_monster_col2)

            # if only one move is invalid, do the other
            if not valid1 and valid2:
                self.center_x = (new_monster_col2) * constants.TILE_WIDTH
                self.center_y = (new_monster_row2) * constants.TILE_HEIGHT
                grid[monster_row, monster_col].has_item = False
                grid[monster_row, monster_col].item = None
                grid[new_monster_row2, new_monster_col2].has_item = True
                grid[new_monster_row2, new_monster_col2].item = self

            elif not valid2 and valid1:
                self.center_x = (new_monster_col) * constants.TILE_WIDTH
                self.center_y = (new_monster_row) * constants.TILE_HEIGHT
                grid[monster_row, monster_col].has_item = False
                grid[monster_row, monster_col].item = None
                grid[new_monster_row, new_monster_col].has_item = True
                grid[new_monster_row, new_monster_col].item = self

            # if both moves are valid
            elif valid1 and valid2:
                if random.choice([True, False]):
                    self.center_x = (new_monster_col) * constants.TILE_WIDTH
                    self.center_y = (new_monster_row) * constants.TILE_HEIGHT
                    grid[monster_row, monster_col].has_item = False
                    grid[monster_row, monster_col].item = None
                    grid[new_monster_row, new_monster_col].has_item = True
                    grid[new_monster_row, new_monster_col].item = self
                else:
                    self.center_x = (new_monster_col2) * constants.TILE_WIDTH
                    self.center_y = (new_monster_row2) * constants.TILE_HEIGHT
                    grid[monster_row, monster_col].has_item = False
                    grid[monster_row, monster_col].item = None
                    grid[new_monster_row2, new_monster_col2].has_item = True
                    grid[new_monster_row2, new_monster_col2].item = self

        else:
            return


# Basic
class Slime(Enemy):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1
    ):
        super().__init__(filename=filename, scale=scale)
        self.health = 7
        self.name = "Slime"
        self.is_alive = True
        self.reward = random.randint(1, 2)
        self.range = 3

    def get_damage(self):
        hit = random.randint(1, 10)
        if hit > 5:
            return random.randint(1, 3)
        return 0


# Weak but has a lot of health
class Crab(Enemy):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1
    ):
        super().__init__(filename=filename, scale=scale)
        self.health = random.randint(10, 14)
        self.name = "Crab"
        self.is_alive = True
        self.reward = random.randint(2, 3)
        self.range = 15

    def get_damage(self):
        hit = random.randint(1, 10)
        if hit > 7:
            return random.randint(1, 2)
        return 0


# Glass Cannon
class Wraith(Enemy):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1
    ):
        super().__init__(filename=filename, scale=scale)
        self.health = random.randint(1, 4)
        self.name = "Wraith"
        self.is_alive = True
        self.reward = random.randint(3, 4)
        self.range = 20

    def get_damage(self):
        hit = random.randint(1, 10)
        if hit > 4:
            return random.randint(1, 2) + random.randint(1, 2)
        return 0


# Very rare; You're screwed if you try to fight this at low level
class Dragon(Enemy):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1
    ):
        super().__init__(filename=filename, scale=scale)
        self.health = random.randint(15, 20)
        self.name = "Dragon"
        self.is_alive = True
        self.reward = 100
        self.range = 20

    def get_damage(self):
        hit = random.randint(1, 10)
        if hit > 2:
            return random.randint(1, 3) + 5
        return 0
