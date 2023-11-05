import arcade
from classes.tile import TileType
from classes.grid import Grid
import random
import sys
import project_constants as constants
from classes.actor import Actor


def create_monsters(to_create: list) -> list:
    """ Creates an instance of a class dependent on whether that class was designated to spawn """

    # Create area to store created objects
    monster_list = []
    # for monster in to_create:
    #     monster_list.append(Enemy(filename="static/armor.png", scale=constants.SPRITE_SCALING))

    return monster_list


class Enemy(Actor):
    def __init__(self):
        Actor.__init__(self)
        self.health = 10
        self.name = "Slime"
        self.is_alive = True

    def attack(self, player):
        hit = random.randint(1, 10)
        if hit > 5:
            damage = random.randint(1, 3)
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

    def is_near(self, player, game):
        return True

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
