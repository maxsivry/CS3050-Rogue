import arcade
from classes.tile import TileType
from classes.grid import Grid
from random import randint
import sys
import project_constants as constants

# Constants
# Colors of Potions
POTION_COLORS = ["blue", "red", "green", "black", "grey", "yellow", "orange", "purple"]

# Metals of Rings
RING_METALS = ["iron", "steel", "silver", "gold", "platinum", "copper", "bronze"]

# Wood of Wands
WAND_WOODS = ["walnut", "oak", "mahogany", "beech", "spruce", "ash", "birch", "cherry"]

# Paper of Scrolls
SCROLL_PAPERS = ["fresh parchment", "destroyed parchment", "burned", "cardboard", "papyrus", "rice paper"]

# key: [spawn_chance, class type, discovered, description]
ITEMS = {"Leather": [20, "armor"], "Ring Mail": [15, "armor"],
         "Studded Leather": [15, "armor"], "Scale Mail": [13, "armor"],
         "Chain Mail": [12, "armor"], "Splint Mail": [10, "armor"],
         "Banded Mail": [10, "armor"], "Plate Mail": [5, "armor"],
         "Magic Mapping": [14, "scroll"], "Identify Weapon": [16, "scroll"],
         "Identify Armor": [17, "scroll"], "Remove Curse": [17, "scroll"],
         "Poison": [18, "potion"], "Monster Detection": [16, "potion"],
         "Restore Strength": [23, "potion"], "Healing": [23, "potion"],
         "Light": [22, "wand"], "Teleport To": [16, "wand"],
         "Teleport Away": [16, "wand"], "Slow Monster": [21, "wand"],
         "Add Strength": [19, "ring"], "Increase Damage": [18, "ring"],
         "Teleportation": [15, "ring"], "Dexterity": [18, "ring"]}


# Method to determine which items actually spawn
def determine_items() -> list:
    """ """
    # Create a return list of lists
    # Each sublist has the form [class, characteristic]
    items_list = []

    # Create lists of "defining characteristics" to be used in describing items
    potion_colors = POTION_COLORS
    ring_metals = RING_METALS
    wand_woods = WAND_WOODS
    scroll_papers = SCROLL_PAPERS

    # Create a flag to set if the item is getting spawned more than once
    spawn_again = False

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
                    if spawn_again:
                        sublist[1] = items_list[len(items_list) - 1][1]
                    else:
                        index = randint(0, len(scroll_papers) - 1)
                        sublist[1] = scroll_papers[index]
                        scroll_papers.pop(index)
                case "potion":
                    if spawn_again:
                        sublist[1] = items_list[len(items_list) - 1][1]
                    else:
                        index = randint(0, len(potion_colors) - 1)
                        sublist[1] = potion_colors[index]
                        potion_colors.pop(index)
                case "wand":
                    if spawn_again:
                        sublist[1] = items_list[len(items_list) - 1][1]
                    else:
                        index = randint(0, len(wand_woods) - 1)
                        sublist[1] = wand_woods[index]
                        wand_woods.pop(index)
                case "ring":
                    if spawn_again:
                        sublist[1] = items_list[len(items_list) - 1][1]
                    else:
                        index = randint(0, len(ring_metals) - 1)
                        sublist[1] = ring_metals[index]
                        ring_metals.pop(index)
                case _:
                    pass

            # Append item to list
            items_list.append(sublist)

            # Set spawn_again
            spawn_again = True

        # Reset spawn_again
        spawn_again = False

    # Set the defining characteristics of the items that spawn (i.e., color for potions, wood type for wand, etc)
    return items_list


# ---Super Class Item---
# Fields:
# -filename
# -scale
# -enchantment
# -is_hidden
# -title
# -hidden_title
# -spawn_chance
class Item(arcade.Sprite):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            enchantment: bool = False,
            is_hidden: bool = True,
            title: str = '',
            spawn_chance: int = 0
    ):
        super().__init__(filename=filename, scale=scale)
        self.is_hidden = is_hidden
        self.title = title
        self.spawn_chance = spawn_chance
        self.enchantment = enchantment
        self.id = randint(0, sys.maxsize)

    # Method to determine center_x and center_y of an item
    def rand_pos(self, grid: Grid):
        """ """

        # Get random absolute position
        x = randint(0, constants.SCREEN_WIDTH)
        y = randint(0, constants.SCREEN_HEIGHT)

        # Get random grid position
        row = int(y // (constants.TILE_HEIGHT + constants.MARGIN))
        col = int(x // (constants.TILE_WIDTH + constants.MARGIN))

        # Set the temporary grid position
        temp_pos = grid.grid[row][col]

        # While TileType != Floor or TileType != Trail
        while temp_pos.tile_type != TileType.Floor and temp_pos.tile_type != TileType.Trail:
            # Determine random position again
            # Get random absolute position
            x = randint(0, constants.SCREEN_WIDTH)
            y = randint(0, constants.SCREEN_HEIGHT)

            # Get random grid position
            row = int(y // (constants.TILE_HEIGHT + constants.MARGIN))
            col = int(x // (constants.TILE_WIDTH + constants.MARGIN))

            # Set the temporary grid position
            temp_pos = grid.grid[row][col]

        # Set this Item's position
        self.set_position(x, y)


# ---Armor Classes---
# Subclass Armor (Super: Item)
# Fields:
# filename: str
# scale: float
# enchantment: bool
# is_hidden: bool
# title: str
# ac: int
# spawn_chance: int
# -------------------------------
# Armor types (Super: Armor)
# -Leather
# --ac: int = 2
# --spawn chance: int = 20
# -Ring Mail
# --ac: int = 3
# --spawn chance: int = 15
# -Studded Leather
# --ac: int = 3
# --spawn chance: int = 15
# -Scale Mail
# --ac: int = 4
# --spawn chance: int = 13
# -Chain Mail
# --ac: int = 5
# --spawn chance: int = 12
# -Splint Mail
# --ac: int = 6
# --spawn chance: int = 10
# -Banded Mail
# --ac: int = 6
# --spawn chance: int = 10
# -Plate Mail
# --ac: int = 7
# --spawn chance: int = 5
class Armor(Item):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            enchantment: bool = False,
            is_hidden: bool = True,
            title: str = '',
            ac: int = 0,
            spawn_chance: int = 0
    ):
        Item.__init__(self, filename=filename, scale=scale, enchantment=enchantment, is_hidden=is_hidden,
                      title=title, spawn_chance=spawn_chance)
        self.ac = ac


class Leather(Armor):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            enchantment: bool = False,
            is_hidden: bool = True,
    ):
        Armor.__init__(self, filename=filename, scale=scale, is_hidden=is_hidden, title="Leather Armor",
                       enchantment=enchantment, ac=2, spawn_chance=ITEMS["Leather"][0])


class RingMail(Armor):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            enchantment: bool = False,
            is_hidden: bool = True,
    ):
        Armor.__init__(self, filename=filename, scale=scale, is_hidden=is_hidden, title="Ring Mail Armor",
                       enchantment=enchantment, ac=3, spawn_chance=ITEMS["Ring Mail"][0])


class StuddedLeather(Armor):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            enchantment: bool = False,
            is_hidden: bool = True
    ):
        Armor.__init__(self, filename=filename, scale=scale, is_hidden=is_hidden, title="Studded Leather Armor",
                       enchantment=enchantment, ac=3, spawn_chance=ITEMS["Studded Leather"][0])


class ScaleMail(Armor):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            enchantment: bool = False,
            is_hidden: bool = True
    ):
        Armor.__init__(self, filename=filename, scale=scale, is_hidden=is_hidden, title="Scale Mail Armor",
                       enchantment=enchantment, ac=4, spawn_chance=ITEMS["Scale Mail"][0])


class ChainMail(Armor):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            enchantment: bool = False,
            is_hidden: bool = True
    ):
        Armor.__init__(self, filename=filename, scale=scale, is_hidden=is_hidden, title="Chain Mail Armor",
                       enchantment=enchantment, ac=5, spawn_chance=ITEMS["Chain Mail"][0])


class SplintMail(Armor):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            enchantment: bool = False,
            is_hidden: bool = True
    ):
        Armor.__init__(self, filename=filename, scale=scale, is_hidden=is_hidden, title="Splint Mail Armor",
                       enchantment=enchantment, ac=6, spawn_chance=ITEMS["Splint Mail"][0])


class BandedMail(Armor):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            enchantment: bool = False,
            is_hidden: bool = True
    ):
        Armor.__init__(self, filename=filename, scale=scale, is_hidden=is_hidden, title="Banded Mail Armor",
                       enchantment=enchantment, ac=6, spawn_chance=ITEMS["Banded Mail"][0])


class PlateMail(Armor):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            enchantment: bool = False,
            is_hidden: bool = True
    ):
        Armor.__init__(self, filename=filename, scale=scale, is_hidden=is_hidden, title="Plate Mail Armor",
                       enchantment=enchantment, ac=7, spawn_chance=ITEMS["Plate Mail"][0])


# NOTE: For simplicity, will limit types of Potions, Rings, Rods, and Scrolls to Four
# ---Scroll Classes---
# Subclass Scroll (Super: Item)
# Fields:
# -filename: str
# -scale: float
# -enchantment: bool
# -is_hidden: bool
# -title: str
# -hidden_title: str
# -spawn_chance: int
# -------------------------------
# Scroll types (Super: Scroll)
# -Magic Mapping
# Reveals the entire map
# --desc: str = *Random Description*
# --spawn chance: int = 4
# --title: str = Scroll of Magic Mapping
# --hidden_title: str = *desc* scroll
# -Identify Weapon
# Identifies a weapon
# --desc: str = *Random Description*
# --spawn chance: int = 6
# --title: str = Scroll of Identify Weapon
# --hidden_title: str = *desc* scroll
# -Identify Armor
# Identifies the armor
# --desc: str = *Random Description*
# --spawn chance: int = 7
# --title: str = Scroll of Identify Armor
# --hidden_title: str = *desc* scroll
# -Remove Curse
# Removes curse from an item
# --desc: str = *Random Description*
# --spawn chance: int = 7
# --title: str = Scroll of Remove Curse
# --hidden_title: str = *desc* scroll
class Scroll(Item):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            enchantment: bool = False,
            is_hidden: bool = True,
            title: str = '',
            hidden_title: str = '',
            spawn_chance: int = 0
    ):
        Item.__init__(self, filename=filename, scale=scale, enchantment=enchantment, is_hidden=is_hidden, title=title,
                      spawn_chance=spawn_chance)
        self.hidden_title = hidden_title


# Subclasses scrolls (Super: Scroll)
class MagicMapping(Scroll):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            is_hidden: bool = True,
            enchantment: bool = False,
            desc: str = ''
    ):
        Scroll.__init__(self, filename=filename, scale=scale, is_hidden=is_hidden, title="Scroll of Magic Mapping",
                        hidden_title=f"{desc} scroll", enchantment=enchantment,
                        spawn_chance=ITEMS["Magic Mapping"][0])
        self.desc = desc


class IdentifyWeapon(Scroll):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            is_hidden: bool = True,
            enchantment: bool = False,
            desc: str = ''
    ):
        Scroll.__init__(self, filename=filename, scale=scale, is_hidden=is_hidden, title="Scroll of Identify Weapon",
                        hidden_title=f"{desc} scroll", enchantment=enchantment,
                        spawn_chance=ITEMS["Identify Weapon"][0])
        self.desc = desc


class IdentifyArmor(Scroll):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            is_hidden: bool = True,
            enchantment: bool = False,
            desc: str = ''
    ):
        Scroll.__init__(self, filename=filename, scale=scale, is_hidden=is_hidden, title="Scroll of Identify Armor",
                        hidden_title=f"{desc} scroll", enchantment=enchantment,
                        spawn_chance=ITEMS["Identify Armor"][0])
        self.desc = desc


class RemoveCurse(Scroll):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            is_hidden: bool = True,
            enchantment: bool = False,
            desc: str = ''
    ):
        Scroll.__init__(self, filename=filename, scale=scale, is_hidden=is_hidden, title="Scroll of Remove Curse",
                        hidden_title=f"{desc} scroll", enchantment=enchantment,
                        spawn_chance=ITEMS["Remove Curse"][0])
        self.desc = desc


# ---Potion Classes---
# Subclass Potion (Super: Item)
# Fields:
# -filename: str
# -scale: float
# -enchantment: bool
# -is_hidden: bool
# -title: str
# -hidden_title: str
# -spawn_chance: int
# -------------------------------
# Potion types (Super: Potion)
# -Poison
# Reduces strength by 1-3 points
# --desc: str = *Random Description*
# --spawn chance: int = 8
# --title: str = Poison Potion
# --hidden_title: str = *desc* potion
# -Monster Detection
# Reveals ONLY monsters
# --desc: str = *Random Description*
# --spawn chance: int = 6
# --title: str = Monster Detection Potion
# --hidden_title: str = *desc* potion
# -Restore Strength
# Restores strength to max
# --desc: str = *Random Description*
# --spawn chance: int = 13
# --title: str = Restore Strength Potion
# --hidden_title: str = *desc* potion
# -Healing
# Heals 1d4 per character level. Permanently increases hp by 1 if at full health
# --desc: str = *Random Description*
# --spawn chance: int = 13
# --title: str = Healing Potion
# --hidden_title: str = *desc* potion
class Potion(Item):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            enchantment: bool = False,
            is_hidden: bool = True,
            title: str = '',
            hidden_title: str = '',
            spawn_chance: int = 0
    ):
        Item.__init__(self, filename=filename, scale=scale, enchantment=enchantment, is_hidden=is_hidden, title=title,
                      spawn_chance=spawn_chance)
        self.hidden_title = hidden_title


# Subclasses: potion types (Super: Potion)
class Poison(Potion):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            is_hidden: bool = True,
            enchantment: bool = False,
            desc: str = ''
    ):
        Potion.__init__(self, filename=filename, scale=scale, is_hidden=is_hidden, title="Poison Potion",
                        hidden_title=f"{desc} potion", enchantment=enchantment,
                        spawn_chance=ITEMS["Poison"][0])
        self.desc = desc


class MonsterDetection(Potion):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            is_hidden: bool = True,
            enchantment: bool = False,
            desc: str = ''
    ):
        Potion.__init__(self, filename=filename, scale=scale, is_hidden=is_hidden, title="Monster Detection Potion",
                        hidden_title=f"{desc} potion", enchantment=enchantment,
                        spawn_chance=ITEMS["Monster Detection"][0])
        self.desc = desc


class RestoreStrength(Potion):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            is_hidden: bool = True,
            enchantment: bool = False,
            desc: str = ''
    ):
        Potion.__init__(self, filename=filename, scale=scale, is_hidden=is_hidden, title="Restore Strength Potion",
                        hidden_title=f"{desc} potion", enchantment=enchantment,
                        spawn_chance=ITEMS["Restore Strength"][0])
        self.desc = desc


class Healing(Potion):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            is_hidden: bool = True,
            enchantment: bool = False,
            desc: str = ''
    ):
        Potion.__init__(self, filename=filename, scale=scale, is_hidden=is_hidden, title="Healing Potion",
                        hidden_title=f"{desc} potion", enchantment=enchantment,
                        spawn_chance=ITEMS["Healing"][0])
        self.desc = desc


# ---Wand Classes---
# Subclass Wand (Super: Item)
# Fields:
# -filename: str
# -scale: float
# -enchantment: bool
# -is_hidden: bool
# -title: str
# -hidden_title: str
# -spawn_chance: int
# -------------------------------
# Wand types (Super: Wand)
# -Light
# Has 1-3 charges, reveals map per charge
# --desc: str = *Random Description*
# --spawn chance: int = 12
# --title: str = Wand of Light
# --hidden_title: str = *desc* wand
# -Teleport To
# Teleports player to random empty floor tile/hallway on map
# --desc: str = *Random Description*
# --spawn chance: int = 6
# --title: str = Wand of Teleport To
# --hidden_title: str = *desc* wand
# -Teleport Away
# Teleports MONSTER to random empty floor tile/hallway on map
# --desc: str = *Random Description*
# --spawn chance: int = 6
# --title: str = Wand of Teleport Away
# --hidden_title: str = *desc* wand
# -Slow Monster
# Slows monster (moves every three actions the player takes)
# --desc: str = *Random Description*
# --spawn chance: int = 11
# --title: str = Wand of Slow Monster
# --hidden_title: str = *desc* wand
class Wand(Item):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            enchantment: bool = False,
            is_hidden: bool = True,
            title: str = '',
            hidden_title: str = '',
            spawn_chance: int = 0
    ):
        Item.__init__(self, filename=filename, scale=scale, enchantment=enchantment, is_hidden=is_hidden, title=title,
                      spawn_chance=spawn_chance)
        self.hidden_title = hidden_title


# Subclasses wand types (Super: Wand)class
class Light(Wand):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            is_hidden: bool = True,
            enchantment: bool = False,
            desc: str = ''
    ):
        Wand.__init__(self, filename=filename, scale=scale, is_hidden=is_hidden, title="Wand of Light",
                      hidden_title=f"{desc} wand", enchantment=enchantment,
                      spawn_chance=ITEMS["Light"][0])
        self.desc = desc


class TeleportTo(Wand):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            is_hidden: bool = True,
            enchantment: bool = False,
            desc: str = ''
    ):
        Wand.__init__(self, filename=filename, scale=scale, is_hidden=is_hidden, title="Wand of Teleport To",
                      hidden_title=f"{desc} wand", enchantment=enchantment,
                      spawn_chance=ITEMS["Teleport To"][0])
        self.desc = desc


class TeleportAway(Wand):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            is_hidden: bool = True,
            enchantment: bool = False,
            desc: str = ''
    ):
        Wand.__init__(self, filename=filename, scale=scale, is_hidden=is_hidden, title="Wand of Teleport Away",
                      hidden_title=f"{desc} wand", enchantment=enchantment,
                      spawn_chance=ITEMS["Teleport Away"][0])
        self.desc = desc


class SlowMonster(Wand):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            is_hidden: bool = True,
            enchantment: bool = False,
            desc: str = ''
    ):
        Wand.__init__(self, filename=filename, scale=scale, is_hidden=is_hidden, title="Wand of Slow Monster",
                      hidden_title=f"{desc} wand", enchantment=enchantment,
                      spawn_chance=ITEMS["Slow Monster"][0])
        self.desc = desc


# ---Ring Classes---
# Subclass Ring (Super: Item)
# Fields:
# -filename: str
# -scale: float
# -enchantment: bool
# -is_hidden: bool
# -title: str
# -hidden_title: str
# -spawn_chance: int
# -------------------------------
# Ring types (Super: Ring)
# -Add Strength
# Permanently increases strength by 1
# --desc: str = *Random Description*
# --spawn chance: int = 9
# --title: str = Ring of Add Strength
# --hidden_title: str = *desc* ring
# -Increase Damage
# Permanently increases weapon damage by 1
# --desc: str = *Random Description*
# --spawn chance: int = 8
# --title: str = Ring of Increase Damage
# --hidden_title: str = *desc* ring
# -Teleportation
# Teleports player to random location. Is removed from player inventory afterwards
# --desc: str = *Random Description*
# --spawn chance: int = 5
# --title: str = Ring of Teleportation
# --hidden_title: str = *desc* ring
# -Dexterity
# Increases dex score by 1
# --desc: str = *Random Description*
# --spawn chance: int = 8
# --title: str = Ring of Dexterity
# --hidden_title: str = *desc* ring
class Ring(Item):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            enchantment: bool = False,
            is_hidden: bool = True,
            title: str = '',
            hidden_title: str = '',
            spawn_chance: int = 0
    ):
        Item.__init__(self, filename=filename, scale=scale, enchantment=enchantment, is_hidden=is_hidden, title=title,
                      spawn_chance=spawn_chance)
        self.hidden_title = hidden_title


# Subclasses ring types (Super: Ring)
class AddStrength(Ring):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            is_hidden: bool = True,
            enchantment: bool = False,
            desc: str = ''
    ):
        Ring.__init__(self, filename=filename, scale=scale, is_hidden=is_hidden, title="Ring of Add Strength",
                      hidden_title=f"{desc} ring", enchantment=enchantment,
                      spawn_chance=ITEMS["Add Strength"][0])
        self.desc = desc


class IncreaseDamage(Ring):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            is_hidden: bool = True,
            enchantment: bool = False,
            desc: str = ''
    ):
        Ring.__init__(self, filename=filename, scale=scale, is_hidden=is_hidden, title="Ring of Increase Damage",
                      hidden_title=f"{desc} ring", enchantment=enchantment,
                      spawn_chance=ITEMS["Increase Damage"][0])
        self.desc = desc


class Teleportation(Ring):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            is_hidden: bool = True,
            enchantment: bool = False,
            desc: str = ''
    ):
        Ring.__init__(self, filename=filename, scale=scale, is_hidden=is_hidden, title="Ring of Teleportation",
                      hidden_title=f"{desc} ring", enchantment=enchantment,
                      spawn_chance=ITEMS["Teleportation"][0])
        self.desc = desc


class Dexterity(Ring):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            is_hidden: bool = True,
            enchantment: bool = False,
            desc: str = ''
    ):
        Ring.__init__(self, filename=filename, scale=scale, is_hidden=is_hidden, title="Ring of Dexterity",
                      hidden_title=f"{desc} ring", enchantment=enchantment,
                      spawn_chance=ITEMS["Dexterity"][0])
        self.desc = desc
