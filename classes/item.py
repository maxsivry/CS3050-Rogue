import arcade
from arcade import Texture
from typing import Optional
from random import randint
import sys

# Constants
# Chances for individual items to spawn and the parent class the item corresponds to
ITEMS = {"Leather": [20, "armor"], "Ring Mail": [15, "armor"], "Studded Leather": [15, "armor"],
         "Scale Mail": [13, "armor"], "Chain Mail": [12, "armor"], "Splint Mail": [10, "armor"],
         "Banded Mail": [10, "armor"], "Plate Mail": [5, "armor"], "Magic Mapping": [4, "scroll"],
         "Identify Weapon": [6, "scroll"], "Identify Armor": [7, "scroll"], "Remove Curse": [7, "scroll"],
         "Poison": [8, "potion"], "Monster Detection": [6, "potion"], "Restore Strength": [13, "potion"],
         "Healing": [13, "potion"], "Light": [12, "wand"], "Teleport To": [6, "wand"], "Teleport Away": [6, "wand"],
         "Slow Monster": [11, "wand"], "Add Strength": [9, "ring"], "Increase Damage": [8, "ring"],
         "Teleportation": [5, "ring"], "Dexterity": [8, "ring"]}

# Colors of Potions
POTION_COLORS = ["blue", "red", "green", "black", "grey", "yellow", "orange", "purple"]

# Metals of Rings
RING_METALS = ["iron", "steel", "silver", "gold", "platinum", "copper", "bronze"]

# Wood of Wands
WAND_WOODS = ["walnut", "oak", "mahogany", "beech", "spruce", "ash", "birch", "cherry"]

# Paper of Scrolls
SCROLL_PAPERS = ["fresh parchment", "destroyed parchment", "burned", "cardboard", "papyrus", "rice paper"]


# TODO: Test This
def determine_items() -> list:
    # Create a return list of lists
    # Each sublist has the form [class, characteristic]
    items_list = []

    # Create lists of "defining characteristics" to be used in describing items
    potion_colors = ["blue", "red", "green", "black", "grey", "yellow", "orange", "purple"]
    ring_metals = ["iron", "steel", "silver", "gold", "platinum", "copper", "bronze"]
    wand_woods = ["walnut", "oak", "mahogany", "beech", "spruce", "ash", "birch", "cherry"]
    scroll_papers = ["fresh parchment", "destroyed parchment", "burned", "cardboard", "papyrus", "rice paper"]

    # Go through each class and determine if it spawns
    for item in ITEMS.keys():
        # Determine how many of the item will spawn
        item_respawn_chance = ITEMS[item][0]
        while randint(0, 100) <= item_respawn_chance:
            # If it spawns, put it in a sublist to be put in the return list
            sublist = [item, -1]

            # Determine defining characteristic based on class type
            match ITEMS[item][1]:
                case "scroll":
                    index = randint(0, len(scroll_papers) - 1)
                    sublist[1] = scroll_papers[index]
                    scroll_papers.pop(index)
                case "potion":
                    index = randint(0, len(potion_colors) - 1)
                    sublist[1] = potion_colors[index]
                    potion_colors.pop(index)
                case "wand":
                    index = randint(0, len(wand_woods) - 1)
                    sublist[1] = wand_woods[index]
                    wand_woods.pop(index)
                case "ring":
                    index = randint(0, len(ring_metals) - 1)
                    sublist[1] = ring_metals[index]
                    ring_metals.pop(index)
                case _:
                    pass

            # Append item to list
            items_list.append(sublist)

            # Make it harder to spawn again
            item_respawn_chance = int((item_respawn_chance / 100) * (ITEMS[item][0] / 100) * 100)
            print(item_respawn_chance)

    # Set the defining characteristics of the items that spawn (i.e., color for potions, wood type for wand, etc)
    return items_list


# ---Super Class Item---
class Item(arcade.Sprite):
    def __init__(
            self,
            is_hidden: bool = True,
            filename: str = None,
            scale: float = 1,
            enchantment: bool = False,
            title: str = '',
            hidden_title = '',
            spawn_chance: int = 0
    ):
        super().__init__(filename=filename, scale=scale)
        self.is_hidden = is_hidden
        self.hidden_title = hidden_title
        self.title = title
        self.spawn_chance = spawn_chance
        self.enchantment = enchantment
        self.id = randint(0, sys.maxsize)

    # def __eq__(self, item2):
    #     """ This overloads the '==' operator. It simply checks if the ids of both instances are the same.
    #     It returns True or False accordingly. """
    #     return self.id == item2


# ---Armor Classes---
# Subclass Armor (Super: Item)
# Fields:
# -ac -> gives chance of avoiding damage

# Armor types (Super: Armor)
# -Leather
# --ac = 2
# --spawn chance = 20
# -Ring Mail
# --ac = 3
# --spawn chance = 15
# -Studded Leather
# --ac = 3
# --spawn chance = 15
# -Scale Mail
# --ac = 4
# --spawn chance = 13
# -Chain Mail
# --ac = 5
# --spawn chance = 12
# -Splint Mail
# --ac = 6
# --spawn chance = 10
# -Banded Mail
# --ac = 6
# --spawn chance = 10
# -Plate Mail
# --ac = 7
# --spawn chance = 5
class Armor(Item):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            enchantment: bool = False,
            title: str = '',
            ac: int = 0,
            spawn_chance: int = 0
    ):
        Item.__init__(self, filename=filename, scale=scale, enchantment=enchantment, spawn_chance=spawn_chance,
                      title=title)
        self.ac = ac


class Leather(Armor):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            enchantment: bool = False,
    ):
        Armor.__init__(self, filename=filename, scale=scale, title="Leather Armor",
                       enchantment=enchantment, ac=2, spawn_chance=20)


class RingMail(Armor):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            enchantment: bool = False
    ):
        Armor.__init__(self, filename=filename, scale=scale, title="Ring Mail Armor",
                       enchantment=enchantment, ac=3, spawn_chance=15)


class StuddedLeather(Armor):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            enchantment: bool = False
    ):
        Armor.__init__(self, filename=filename, scale=scale, title="Studded Leather Armor",
                       enchantment=enchantment, ac=3, spawn_chance=15)


class ScaleMail(Armor):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            enchantment: bool = False
    ):
        Armor.__init__(self, filename=filename, scale=scale, title="Scale Mail Armor",
                       enchantment=enchantment, ac=4, spawn_chance=13)


class ChainMail(Armor):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            enchantment: bool = False
    ):
        Armor.__init__(self, filename=filename, scale=scale, title="Chain Mail Armor",
                       enchantment=enchantment, ac=5, spawn_chance=12)


class SplintMail(Armor):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            enchantment: bool = False
    ):
        Armor.__init__(self, filename=filename, scale=scale, title="Splint Mail Armor",
                       enchantment=enchantment, ac=6, spawn_chance=10)


class BandedMail(Armor):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            enchantment: bool = False
    ):
        Armor.__init__(self, filename=filename, scale=scale, title="Banded Mail Armor",
                       enchantment=enchantment, ac=6, spawn_chance=10)


class PlateMail(Armor):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            enchantment: bool = False
    ):
        Armor.__init__(self, filename=filename, scale=scale, title="Plate Mail Armor",
                       enchantment=enchantment, ac=7, spawn_chance=5)


# NOTE: For simplicity, will limit types of Potions, Rings, Rods, and Scrolls to Four
# ---Scroll Classes---
# Subclass Scroll (Super: Item)
# Fields:
# paper -> describes the paper of the scroll (no other scrolls can have this paper this session)
# TODO: Fill this out when classes fully fleshed

# Scroll types (Super: Scroll)
# -Magic Mapping
# Reveals the entire map
# --spawn chance = 4
# -Identify Weapon
# Identifies a weapon
# --spawn chance = 6
# -Identify Armor
# Identifies the armor
# --spawn chance = 7
# -Remove Curse
# Removes curse from an item
# --spawn chance = 7
class Scroll(Item):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            enchantment: bool = False,
            title: str = '',
            spawn_chance: int = 0
    ):
        Item.__init__(self, filename=filename, scale=scale, title=title,
                      enchantment=enchantment, spawn_chance=spawn_chance)


# Subclasses scrolls (Super: Scroll)
class MagicMapping(Scroll):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            enchantment: bool = False,
    ):
        Scroll.__init__(self, filename=filename, scale=scale, title="Scroll of Magic Mapping",
                        enchantment=enchantment, spawn_chance=4)


class IdentifyWeapon(Scroll):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            enchantment: bool = False,
    ):
        Scroll.__init__(self, filename=filename, scale=scale, title="Scroll of Identify Weapon",
                        enchantment=enchantment, spawn_chance=6)


class IdentifyArmor(Scroll):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            enchantment: bool = False,
    ):
        Scroll.__init__(self, filename=filename, scale=scale, title="Scroll of Identify Armor",
                        enchantment=enchantment, spawn_chance=7)


class RemoveCurse(Scroll):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            enchantment: bool = False,
    ):
        Scroll.__init__(self, filename=filename, scale=scale, title="Scroll of Remove Curse",
                        enchantment=enchantment, spawn_chance=7)


# ---Potion Classes---
# Subclass Potion (Super: Item)
# Fields:
# color -> describes the color of the potion (no other potions can have this color this session)
# TODO: Fill this out when classes fully fleshed

# Potion types (Super: Potion)
# -Poison
# Reduces strength by 1-3 points
# --spawn chance = 8
# -Monster Detection
# Reveals ONLY monsters
# --spawn chance = 6
# -Restore Strength
# Restores strength to max
# --spawn chance = 13
# -Healing
# Heals 1d4 per character level. Permanently increases hp by 1 if at full health
# --spawn chance = 13
class Potion(Item):
    # TODO: Add colors to potion (randomized every new game, no potion has this color this session)
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            enchantment: bool = False,
            title: str = '',
            spawn_chance: int = 0
    ):
        Item.__init__(self, filename=filename, scale=scale, title=title,
                      enchantment=enchantment, spawn_chance=spawn_chance)


# Subclasses: potion types (Super: Potion)
class PoisonPotion(Potion):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            enchantment: bool = False,
    ):
        Potion.__init__(self, filename=filename, scale=scale, title="Poison Potion",
                        enchantment=enchantment, spawn_chance=8)


class MonsterDetectionPotion(Potion):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            enchantment: bool = False
    ):
        Potion.__init__(self, filename=filename, scale=scale, title="Monster Detection Potion",
                        enchantment=enchantment, spawn_chance=6)


class RestoreStrengthPotion(Potion):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            enchantment: bool = False
    ):
        Potion.__init__(self, filename=filename, scale=scale, title="Restore Strength Potion",
                        enchantment=enchantment, spawn_chance=13)


class HealingPotion(Potion):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            enchantment: bool = False
    ):
        Potion.__init__(self, filename=filename, scale=scale, title="Healing Potion",
                        enchantment=enchantment, spawn_chance=13)


# ---Wand Classes---
# Subclass Wand (Super: Item)
# Fields:
# wood -> describes the wood of the Wand (no other wands can have this wood this session)
# TODO: Fill this out when classes fully fleshed

# Wand types (Super: Wand)
# -Light
# Has 1-3 charges, reveals map per charge
# --spawn chance = 12
# -Teleport To
# Teleports player to random empty floor tile/hallway on map
# --spawn chance = 6
# -Teleport Away
# Teleports MONSTER to random empty floor tile/hallway on map
# --spawn chance = 6
# -Slow Monster
# Slows monster (moves every three actions the player takes)
# --spawn chance = 11
class Wand(Item):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            enchantment: bool = False,
            title: str = '',
            spawn_chance: int = 0
    ):
        Item.__init__(self, filename=filename, scale=scale, title=title,
                      enchantment=enchantment, spawn_chance=spawn_chance)


# Subclasses wand types (Super: Wand)class
class Light(Wand):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            enchantment: bool = False
    ):
        Wand.__init__(self, filename=filename, scale=scale, title="Wand of Light",
                      enchantment=enchantment, spawn_chance=12)


class TeleportTo(Wand):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            enchantment: bool = False
    ):
        Wand.__init__(self, filename=filename, scale=scale, title="Wand of Teleport To",
                      enchantment=enchantment, spawn_chance=6)


class TeleportAway(Wand):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            enchantment: bool = False
    ):
        Wand.__init__(self, filename=filename, scale=scale, title="Wand of Teleport Away",
                      enchantment=enchantment, spawn_chance=6)


class SlowMonster(Wand):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            enchantment: bool = False
    ):
        Wand.__init__(self, filename=filename, scale=scale, title="Wand of Slow Monster",
                      enchantment=enchantment, spawn_chance=11)


# ---Ring Classes---
# Subclass Ring (Super: Item)
# Fields:
# metal -> describes the type of metal the ring is made up of (no other rings can have this metal this session)
# TODO: Fill this out when classes fully fleshed

# Ring types (Super: Ring)
# -Add Strength
# Permanently increases strength by 1
# --spawn chance = 9
# -Increase Damage
# Permanently increases weapon damage by 1
# --spawn chance = 8
# -Teleportation
# Teleports player to random location. Is removed from player inventory afterwards
# --spawn chance = 5
# -Dexterity
# Increases dex score by 1
# --spawn chance = 8
class Ring(Item):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            enchantment: bool = False,
            title: str = '',
            spawn_chance: int = 0
    ):
        Item.__init__(self, filename=filename, scale=scale, title=title,
                      enchantment=enchantment, spawn_chance=spawn_chance)


# Subclasses ring types (Super: Ring)
class AddStrength(Ring):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            enchantment: bool = False
    ):
        Ring.__init__(self, filename=filename, scale=scale, title="Ring of Add Strength",
                      enchantment=enchantment, spawn_chance=9)


class IncreaseDamage(Ring):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            enchantment: bool = False
    ):
        Ring.__init__(self, filename=filename, scale=scale, title="Ring of Increase Damage",
                      enchantment=enchantment, spawn_chance=8)


class Teleportation(Ring):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            enchantment: bool = False
    ):
        Ring.__init__(self, filename=filename, scale=scale, title="Ring of Teleportation",
                      enchantment=enchantment, spawn_chance=5)


class Dexterity(Ring):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            enchantment: bool = False
    ):
        Ring.__init__(self, filename=filename, scale=scale, title="Ring of Dexterity",
                      enchantment=enchantment, spawn_chance=8)
