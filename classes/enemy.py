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

    num_monsters = (int) (random.randint(2,5) + level*.8)

    for _ in range(num_monsters):
        monster_type = random.randint(0, 100-level)
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
                    print("You were killed by " + self.name)
            else:
                print("You took no damage")
        else:
            print("The " + self.name + " missed...")

    def take_damage(self, damage):
        self.health -= damage
        print("The " + self.name + " lost", damage, "health")
        if self.health <= 0:
            self.die()
            return True
        return False

    def die(self):
        print("You defeated the " + self.name)
        self.is_alive = False

    # Returns true if the enemy is one tile away from the player
    # Currently always returns false 
    def is_near(self, player, game):
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
    def chase(self, player, game):
        pass


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
        self.reward = random.randint(1,2)
    
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
        self.health = random.randint(10,14)
        self.name = "Crab"
        self.is_alive = True
        self.reward = random.randint(2,3)
    
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
        self.health = random.randint(1,4)
        self.name = "Wraith"
        self.is_alive = True
        self.reward = random.randint(3,4)
    
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
        self.health = random.randint(15,20)
        self.name = "Dragon"
        self.is_alive = True
        self.reward = 20
    
    def get_damage(self):
        hit = random.randint(1, 10)
        if hit > 2:
            return random.randint(1, 3) + 5
        return 0
