from typing import Tuple

import arcade
from classes.tile import TileType
from classes.grid import Grid
from random import randint
import sys
import project_constants as constants

# Constants
# key: [spawn_chance, class type]
ITEMS = {"Leather": [20, "armor"], "Ring Mail": [15, "armor"],
         "Studded Leather": [15, "armor"], "Scale Mail": [13, "armor"],
         "Chain Mail": [12, "armor"], "Splint Mail": [10, "armor"],
         "Banded Mail": [10, "armor"], "Plate Mail": [5, "armor"],
         "Identify Ring": [16, "scroll"], "Increase Max Health": [17, "scroll"],
         "Identify Potion": [17, "scroll"], "Poison": [18, "potion"],
         "Restore Strength": [23, "potion"], "Healing": [23, "potion"],
         "Teleport To": [16, "wand"], "Drain Life": [21, "wand"], "Add Strength": [19, "ring"],
         "Increase Damage": [18, "ring"], "Teleportation": [15, "ring"],
         "Dexterity": [18, "ring"], "Gold": [35, "gold"], "Mace": [5, "weapon"],
         "Longsword": [5, "weapon"], "Club": [5, "weapon"], "Scimitar": [5, "weapon"]}


# Method to determine which items actually spawn
def determine_items() -> list:
    """ Determines a list of items to spawn and their corresponding characteristics (to be used if the Item
    has not been discovered by the player). """

    # Create a return list of lists
    # Each sublist has the form [class, characteristic]
    items_list = []

    # Create lists of "defining characteristics" to be used in describing items
    potion_colors = ["blue", "red", "green", "black", "grey", "yellow", "orange", "purple"]
    ring_metals = ["iron", "steel", "silver", "gold", "platinum", "copper", "bronze"]
    wand_woods = ["walnut", "oak", "mahogany", "beech", "spruce", "ash", "birch", "cherry"]
    scroll_papers = ["fresh parchment", "destroyed parchment", "burned", "cardboard", "papyrus", "rice paper",
                 "tattered paper"]

    # Create a flag to set if the item is getting spawned more than once
    spawn_again = False

    # Go through each class and determine if it spawns
    for item in ITEMS.keys():
        # Determine how many of the item will spawn
        item_respawn_chance = ITEMS[item][0]
        while randint(0, 100) <= item_respawn_chance:
            # If it spawns, put it in a sublist to be put in the return list
            sublist = [item, '']

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


def create_items(to_create: list) -> list:
    """ Creates an instance of a class dependent on whether that class was designated to spawn """

    # Create area to store created objects
    items_list = []
    for item in to_create:
        match item[0]:
            case "Leather":
                items_list.append(Leather(filename="static/armor.png", scale=constants.SPRITE_SCALING))
            case "Ring Mail":
                items_list.append(RingMail(filename="static/armor.png", scale=constants.SPRITE_SCALING))
            case "Studded Leather":
                items_list.append(StuddedLeather(filename="static/armor.png", scale=constants.SPRITE_SCALING))
            case "Scale Mail":
                items_list.append(ScaleMail(filename="static/armor.png", scale=constants.SPRITE_SCALING))
            case "Chain Mail":
                items_list.append(ChainMail(filename="static/armor.png", scale=constants.SPRITE_SCALING))
            case "Splint Mail":
                items_list.append(SplintMail(filename="static/armor.png", scale=constants.SPRITE_SCALING))
            case "Banded Mail":
                items_list.append(BandedMail(filename="static/armor.png", scale=constants.SPRITE_SCALING))
            case "Plate Mail":
                items_list.append(PlateMail(filename="static/armor.png", scale=constants.SPRITE_SCALING))
            case "Increase Max Health":
                if constants.items_info[IncreaseMaxHealth][1] == '':
                    constants.items_info[IncreaseMaxHealth][1] = item[1]
                items_list.append(IncreaseMaxHealth(filename="static/scroll.png", scale=constants.SPRITE_SCALING,
                                                    desc=constants.items_info[IncreaseMaxHealth][1]))

            case "Identify Ring":
                if constants.items_info[IdentifyRing][1] == '':
                    constants.items_info[IdentifyRing][1] = item[1]
                items_list.append(IdentifyRing(filename="static/scroll.png", scale=constants.SPRITE_SCALING,
                                               desc=constants.items_info[IdentifyRing][1]))
            case "Identify Potion":
                if constants.items_info[IdentifyPotion][1] == '':
                    constants.items_info[IdentifyPotion][1] = item[1]
                items_list.append(IdentifyPotion(filename="static/scroll.png", scale=constants.SPRITE_SCALING,
                                                 desc=constants.items_info[IdentifyPotion][1]))
            case "Poison":
                if constants.items_info[Poison][1] == '':
                    constants.items_info[Poison][1] = item[1]
                items_list.append(Poison(filename="static/potion.png", scale=constants.SPRITE_SCALING,
                                         desc=constants.items_info[Poison][1]))
            case "Restore Strength":
                if constants.items_info[RestoreStrength][1] == '':
                    constants.items_info[RestoreStrength][1] = item[1]
                items_list.append(RestoreStrength(filename="static/potion.png", scale=constants.SPRITE_SCALING,
                                                  desc=constants.items_info[RestoreStrength][1]))
            case "Healing":
                if constants.items_info[Healing][1] == '':
                    constants.items_info[Healing][1] = item[1]
                items_list.append(Healing(filename="static/potion.png", scale=constants.SPRITE_SCALING,
                                          desc=constants.items_info[Healing][1]))
            case "Teleport To":
                if constants.items_info[TeleportTo][1] == '':
                    constants.items_info[TeleportTo][1] = item[1]
                items_list.append(TeleportTo(filename="static/wand.png", scale=constants.SPRITE_SCALING,
                                             desc=constants.items_info[TeleportTo][1]))
            case "Drain Life":
                if constants.items_info[DrainLife][1] == '':
                    constants.items_info[DrainLife][1] = item[1]
                items_list.append(DrainLife(filename="static/wand.png", scale=constants.SPRITE_SCALING,
                                            desc=constants.items_info[DrainLife][1]))
            case "Add Strength":
                if constants.items_info[AddStrength][1] == '':
                    constants.items_info[AddStrength][1] = item[1]
                items_list.append(AddStrength(filename="static/ring.png", scale=constants.SPRITE_SCALING,
                                              desc=constants.items_info[AddStrength][1]))
            case "Increase Damage":
                if constants.items_info[IncreaseDamage][1] == '':
                    constants.items_info[IncreaseDamage][1] = item[1]
                items_list.append(IncreaseDamage(filename="static/ring.png", scale=constants.SPRITE_SCALING,
                                                 desc=constants.items_info[IncreaseDamage][1]))
            case "Teleportation":
                if constants.items_info[Teleportation][1] == '':
                    constants.items_info[Teleportation][1] = item[1]
                items_list.append(Teleportation(filename="static/ring.png", scale=constants.SPRITE_SCALING,
                                                desc=constants.items_info[Teleportation][1]))
            case "Dexterity":
                if constants.items_info[Dexterity][1] == '':
                    constants.items_info[Dexterity][1] = item[1]
                items_list.append(Dexterity(filename="static/ring.png", scale=constants.SPRITE_SCALING,
                                            desc=constants.items_info[Dexterity][1]))
            case "Gold":
                items_list.append(Gold(filename="static/gold.png", scale=constants.SPRITE_SCALING))
            case "Scimitar":
                items_list.append(Scimitar(filename="static/weapon.png", scale=constants.SPRITE_SCALING))
            case "Club":
                items_list.append(Club(filename="static/weapon.png", scale=constants.SPRITE_SCALING))
            case "Longsword":
                items_list.append(Longsword(filename="static/weapon.png", scale=constants.SPRITE_SCALING))
            case "Mace":
                items_list.append(Mace(filename="static/weapon.png", scale=constants.SPRITE_SCALING))
            case _:
                # Will never get here
                pass

    # Return the new list
    return items_list


# ---Super Class Item---
# Fields:
# -filename
# -scale
# -title
# -hidden_title
# -spawn_chance
class Item(arcade.Sprite):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            title: str = '',
            spawn_chance: int = 0
    ):
        super().__init__(filename=filename, scale=scale)
        self.title = title
        self.spawn_chance = spawn_chance
        self.id = randint(0, sys.maxsize)


# ---Gold Class---
# Subclass Gold (Super: Item)
# Fields:
# filename: str
# scale: float
# title: str
# spawn_chance: int
# gold: int
class Gold(Item):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            gold: int = -1
    ):
        self.gold = randint(1, 50) if gold == -1 else gold
        Item.__init__(self, filename=filename, scale=scale, title=f"{self.gold} gold", spawn_chance=ITEMS["Gold"][0])

    def use(self, player):
        # Update player with additional gold
        player.gold += self.gold


# ---Armor Classes---
# Subclass Armor (Super: Item)
# Fields:
# filename: str
# scale: float
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
            title: str = '',
            ac: int = 0,
            spawn_chance: int = 0
    ):
        Item.__init__(self, filename=filename, scale=scale, title=title, spawn_chance=spawn_chance)
        self.ac = ac


class Leather(Armor):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
    ):
        Armor.__init__(self, filename=filename, scale=scale, title="Leather Armor",
                       ac=2, spawn_chance=ITEMS["Leather"][0])


class RingMail(Armor):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
    ):
        Armor.__init__(self, filename=filename, scale=scale, title="Ring Mail Armor",
                       ac=3, spawn_chance=ITEMS["Ring Mail"][0])


class StuddedLeather(Armor):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
    ):
        Armor.__init__(self, filename=filename, scale=scale, title="Studded Leather Armor",
                       ac=3, spawn_chance=ITEMS["Studded Leather"][0])


class ScaleMail(Armor):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
    ):
        Armor.__init__(self, filename=filename, scale=scale, title="Scale Mail Armor",
                       ac=4, spawn_chance=ITEMS["Scale Mail"][0])


class ChainMail(Armor):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
    ):
        Armor.__init__(self, filename=filename, scale=scale, title="Chain Mail Armor",
                       ac=5, spawn_chance=ITEMS["Chain Mail"][0])


class SplintMail(Armor):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
    ):
        Armor.__init__(self, filename=filename, scale=scale, title="Splint Mail Armor",
                       ac=6, spawn_chance=ITEMS["Splint Mail"][0])


class BandedMail(Armor):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
    ):
        Armor.__init__(self, filename=filename, scale=scale, title="Banded Mail Armor",
                       ac=6, spawn_chance=ITEMS["Banded Mail"][0])


class PlateMail(Armor):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
    ):
        Armor.__init__(self, filename=filename, scale=scale, title="Plate Mail Armor",
                       ac=7, spawn_chance=ITEMS["Plate Mail"][0])


# NOTE: For simplicity, will limit types of Potions, Rings, Rods, and Scrolls to Four
# ---Scroll Classes---
# Subclass Scroll (Super: Item)
# Fields:
# -filename: str
# -scale: float
# -title: str
# -hidden_title: str
# -spawn_chance: int
# -------------------------------
# Scroll types (Super: Scroll)
# -Increase Max Health
# Increase Player's max hp by 5
# --desc: str = *Random Description*
# --spawn chance: int = 6
# --title: str = Scroll of Increase Max Health
# --hidden_title: str = *desc* scroll
# -Identify Ring
# Identifies a random ring for the player
# --desc: str = *Random Description*
# --spawn chance: int = 7
# --title: str = Scroll of Identify Ring
# --hidden_title: str = *desc* scroll
# -Identify Potion
# Identifies a random potion for the player
# --desc: str = *Random Description*
# --spawn chance: int = 7
# --title: str = Scroll of Identify Potion
# --hidden_title: str = *desc* scroll
class Scroll(Item):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            title: str = '',
            hidden_title: str = '',
            spawn_chance: int = 0,
            charges: int = 1
    ):
        Item.__init__(self, filename=filename, scale=scale, title=title,
                      spawn_chance=spawn_chance)
        self.hidden_title = hidden_title
        self.charges = charges


# Subclasses scrolls (Super: Scroll)
class IncreaseMaxHealth(Scroll):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            desc: str = ''
    ):
        Scroll.__init__(self, filename=filename, scale=scale, title="Scroll of\n Increase Max\n Health",
                        hidden_title=f"{desc} scroll", spawn_chance=ITEMS["Increase Max Health"][0])
        self.desc = desc

    def use(self, player):
        """ This increases the Player's max hp by 5 points. """
        # Make sure this hasn't already been used
        if self.charges != 0:
            # Check if the Player has already used the item
            if not constants.items_info[IncreaseMaxHealth][0]:
                # Set used in constants.items_info
                constants.items_info[IncreaseMaxHealth][0] = True

            # Increase max hp
            player.max_hp += 5

            # Set charges
            self.charges -= 1

            # Set title
            self.title = "USED\n Scroll of\n Increase Max\n Health"


class IdentifyRing(Scroll):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            desc: str = ''
    ):
        Scroll.__init__(self, filename=filename, scale=scale, title="Scroll of\n Identify Ring",
                        hidden_title=f"{desc} scroll", spawn_chance=ITEMS["Identify Ring"][0])
        self.desc = desc

    def use(self, player):
        """ This randomly sets a ring in the Player's inventory to be discovered. If there are none, none are
        discovered. """
        # Make sure this hasn't already been used
        if self.charges != 0:
            # Check if the Player has already used the item
            if not constants.items_info[IdentifyRing][0]:
                # Set used in constants.items_info
                constants.items_info[IdentifyRing][0] = True

            # Set a random ring to be discovered in Player's inventory
            # Create a variable to allow only one potion to be discovered
            disc = False
            for item in player.inv:
                if disc:
                    break
                elif issubclass(type(item), Ring):
                    # Discover the potion
                    constants.items_info[type(item)][0] = True

                    # Set discovered equal to true
                    disc = True

            # Set charges
            self.charges -= 1

            # Set title
            self.title = "USED\n Scroll of\n Identify Ring"


class IdentifyPotion(Scroll):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            desc: str = ''
    ):
        Scroll.__init__(self, filename=filename, scale=scale, title="Scroll of\n Identify Potion",
                        hidden_title=f"{desc} scroll", spawn_chance=ITEMS["Identify Potion"][0])
        self.desc = desc

    def use(self, player):
        """ This randomly sets a potion in the Player's inventory to be discovered. If there are none, none are
        discovered. """
        # Make sure this hasn't already been used
        if self.charges != 0:
            # Check if the Player has already used the item
            if not constants.items_info[IdentifyPotion][0]:
                # Set used in constants.items_info
                constants.items_info[IdentifyPotion][0] = True

            # Set a random potion to be discovered in Player's inventory
            # Create a variable to allow only one potion to be discovered
            disc = False
            for item in player.inv:
                if disc:
                    break
                elif issubclass(type(item), Potion):
                    # Discover the potion
                    constants.items_info[type(item)][0] = True

                    # Set discovered equal to true
                    disc = True

            # Set charges
            self.charges -= 1

            # Set title
            self.title = "USED\n Scroll of\n Identify Potion"


# ---Potion Classes---
# Subclass Potion (Super: Item)
# Fields:
# -filename: str
# -scale: float
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
            title: str = '',
            hidden_title: str = '',
            spawn_chance: int = 0,
            charges: int = 1
    ):
        Item.__init__(self, filename=filename, scale=scale, title=title, spawn_chance=spawn_chance)
        self.hidden_title = hidden_title
        self.charges = charges


# Subclasses: potion types (Super: Potion)
class Poison(Potion):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            desc: str = ''
    ):
        Potion.__init__(self, filename=filename, scale=scale, title="Poison Potion", hidden_title=f"{desc} potion",
                        spawn_chance=ITEMS["Poison"][0])
        self.desc = desc

    def use(self, player):
        """ Removes a random amount of strength from the Player (between 1-3). """
        # Make sure the Player can only activate this once
        if self.charges != 0 and player.str > 0:
            # Check if the Player has already used the item
            if not constants.items_info[Poison][0]:
                # Set used in constants.items_info
                constants.items_info[Poison][0] = True

            # Decide how much strength to reduce (1-3 points)
            rm_str = randint(1, 3)

            # If the Player does not have enough strength to remove
            while rm_str > player.str:
                rm_str = randint(1, 3)

            # Update the Player's strength
            player.str -= rm_str

            # Set charges
            self.charges -= 1

            # Update title
            self.title = "EMPTY\n Poison Potion"


class RestoreStrength(Potion):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            desc: str = ''
    ):
        Potion.__init__(self, filename=filename, scale=scale, title="Restore\n Strength Potion",
                        hidden_title=f"{desc} potion", spawn_chance=ITEMS["Restore Strength"][0])
        self.desc = desc

    def use(self, player):
        """ Simply restores the Player's strength to maximum. """
        # Check if the Player has already used the item
        if not constants.items_info[RestoreStrength][0]:
            # Set used in constants.items_info
            constants.items_info[RestoreStrength][0] = True

        # Restore Player's strength
        player.str = player.str_max

        # Update title
        self.title = "EMPTY\n Restore\n Strength Potion"


class Healing(Potion):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            desc: str = ''
    ):
        Potion.__init__(self, filename=filename, scale=scale, title="Healing Potion", hidden_title=f"{desc} potion",
                        spawn_chance=ITEMS["Healing"][0])
        self.desc = desc

    def use(self, player):
        """ For every level the Player has, add 1d4 worth of hp.
        If the Player is at max hp, add 1 to max and current hp. """
        # Make sure the Player can only use this item once
        if self.charges != 0:
            # Check if the Player has already used the item
            if not constants.items_info[Healing][0]:
                # Set used in constants.items_info
                constants.items_info[Healing][0] = True

            # Heal 1d4 per character level or Increase max hp if at full health
            if player.health == player.max_hp:  # Update hp and max hp if already at full health
                player.max_hp += 1
                player.health += 1
            else:  # Heal 1d4 for every level the Player has
                for level in range(player.level):
                    heal = randint(1, 4)
                    if player.max_hp < heal + player.health:  # Make sure the Player doesn't get 'over-healed'
                        player.health = player.max_hp
                    else:
                        player.health += heal

            # Update charges
            self.charges -= 1

            # Update title
            self.title = "EMPTY\n Healing Potion"


# ---Wand Classes---
# Subclass Wand (Super: Item)
# Fields:
# -filename: str
# -scale: float
# -title: str
# -hidden_title: str
# -spawn_chance: int
# -------------------------------
# Wand types (Super: Wand)
# -Teleport To
# Teleports player to selected floor tile/hallway on map
# --desc: str = *Random Description*
# --spawn chance: int = 6
# --title: str = Wand of Teleport To
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
            title: str = '',
            hidden_title: str = '',
            spawn_chance: int = 0,
            charges: int = -1
    ):
        Item.__init__(self, filename=filename, scale=scale, title=title,
                      spawn_chance=spawn_chance)
        self.hidden_title = hidden_title
        self.charges = charges if charges > -1 else randint(1, 5)


# Subclasses wand types (Super: Wand)class
class TeleportTo(Wand):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            desc: str = ''
    ):
        Wand.__init__(self, filename=filename, scale=scale, title=f"Wand of\n Teleport To", hidden_title=f"{desc} wand",
                      spawn_chance=ITEMS["Teleport To"][0])
        self.desc = desc

    def use(self, player, grid: Grid, click_coords: Tuple[int, int]):
        """ Based on the most recent grid coordinates (given by a mouse left-click), the Player is teleported
        there. """
        # Check if coords is a floor or trail
        row, col = click_coords

        # Check for valid coordinates
        if grid.grid[row][col].tile_type == TileType.Floor or grid.grid[row][col].tile_type == TileType.Trail:
            # Check if enough charges to use again
            if self.charges != 0:
                # Make this discovered
                if not constants.items_info[TeleportTo][0]:
                    # Set used in constants.items_info
                    constants.items_info[TeleportTo][0] = True

                # Set Player's position
                player.set_position(col * constants.TILE_WIDTH, row * constants.TILE_HEIGHT)

                # Update charges
                self.charges -= 1

                # Update title
                self.title = f"Wand of\n Teleport To\n Charges: {self.charges}"


class DrainLife(Wand):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            desc: str = ''
    ):
        Wand.__init__(self, filename=filename, scale=scale, title="Wand of\n Drain Life", hidden_title=f"{desc} wand",
                      spawn_chance=ITEMS["Drain Life"][0])
        self.desc = desc

    def use(self, player, monster_list):
        """ Removes half the player's current health and deals damage to all monsters on the level. """
        # Check if enough charges to use again
        if self.charges != 0:
            if not constants.items_info[DrainLife][0]:
                # Set used in constants.items_info
                constants.items_info[DrainLife][0] = True

            # Remove half hp (int)
            half_hp = player.health // 2
            player.health -= half_hp

            # Evenly remove amongst alive monsters
            to_drain = half_hp // len(monster_list)
            for monster in monster_list:
                monster.take_damage(to_drain)

            # Update charges
            self.charges -= 1

            # Update title
            self.title = f"Wand of\n Drain Life\n Charges: {self.charges}"


# ---Ring Classes---
# Subclass Ring (Super: Item)
# Fields:
# -filename: str
# -scale: float
# -title: str
# -hidden_title: str
# -spawn_chance: int
# -charges: int
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
            title: str = '',
            hidden_title: str = '',
            spawn_chance: int = 0,
            charges: int = 1
    ):
        Item.__init__(self, filename=filename, scale=scale, title=title, spawn_chance=spawn_chance)
        self.hidden_title = hidden_title
        self.charges = charges


# Subclasses ring types (Super: Ring)
class AddStrength(Ring):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            desc: str = ''
    ):
        Ring.__init__(self, filename=filename, scale=scale, title="Ring of\n Add Strength",
                      hidden_title=f"{desc} ring", spawn_chance=ITEMS["Add Strength"][0])
        self.desc = desc

    def use(self, player, grid: Grid = None):
        """ Adds one to current and max strength. """
        # Make sure this hasn't already been used
        if self.charges != 0:

            # Check if the Player has already used the item
            if not constants.items_info[AddStrength][0]:
                # Set used in constants.items_info
                constants.items_info[AddStrength][0] = True

            # Add one to current and maximum strength
            player.str_max += 1
            player.str += 1

            # Update charges
            self.charges -= 1

    def unequip(self, player, grid: Grid = None):
        """ When this ring is unequipped, the Player loses the benefits of having it equipped.
        This removes 1 from strength and max strength. """
        # Undo changes
        player.str -= 1
        player.str_max -= 1


class IncreaseDamage(Ring):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            desc: str = ''
    ):
        Ring.__init__(self, filename=filename, scale=scale, title="Ring of\n Increase\n Damage",
                      hidden_title=f"{desc} ring", spawn_chance=ITEMS["Increase Damage"][0])
        self.desc = desc

    def use(self, player, grid: Grid = None):
        """ Increases the Player's equipped weapon's power by 1. """
        # Make sure this hasn't already been used
        if self.charges != 0:
            # Check if the Player has already used the item
            if not constants.items_info[IncreaseDamage][0]:
                # Set used in constants.items_info
                constants.items_info[IncreaseDamage][0] = True

            # Update the weapon's power += 1
            player.weapon.power += 1

            # Call weapon.update
            player.weapon.update()

            # Update charges
            self.charges -= 1

    def unequip(self, player, grid: Grid = None):
        """ When this ring is unequipped, the Player loses the benefits of having it equipped.
        This removes 1 from weapon's power. """
        # Undo changes
        player.weapon.power -= 1
        player.weapon.update()


class Teleportation(Ring):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            desc: str = ''
    ):
        Ring.__init__(self, filename=filename, scale=scale, title="Ring of\n Teleportation",
                      hidden_title=f"{desc} ring", spawn_chance=ITEMS["Teleportation"][0])
        self.desc = desc

    def use(self, player, grid: Grid):
        """ Once initially put on, the Player is teleported to a random floor or trail. """
        # Make sure this hasn't already been used
        if self.charges != 0:
            # Check if the Player has already used the item
            if not constants.items_info[Teleportation][0]:
                # Set used in constants.items_info
                constants.items_info[Teleportation][0] = True

            # Get random grid position
            row = randint(0, grid.n_rows - 1)
            col = randint(0, grid.n_cols - 1)

            # Set the temporary grid position
            temp_pos = grid.grid[row][col]

            # While TileType != Floor and TileType != Trail and Tile has an item
            while temp_pos.tile_type != TileType.Floor and temp_pos.tile_type != TileType.Trail:
                # Determine random position again
                # Get random grid position
                row = randint(0, grid.n_rows - 1)
                col = randint(0, grid.n_cols - 1)

                # Set the temporary grid position
                temp_pos = grid.grid[row][col]

            # Set the Player's position
            player.set_position((col * constants.TILE_WIDTH) + 7.5, (row * constants.TILE_HEIGHT) + 7.5)

            # Update charges
            self.charges -= 1

            # Set title to reflect used charges
            self.title = f"(DEPLETED)\n {self.title}"

    def unequip(self, player=None, grid: Grid = None):
        """ Nothing happens when you unequip this ring. Must have an unequip method though. """
        pass


class Dexterity(Ring):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            desc: str = ''
    ):
        Ring.__init__(self, filename=filename, scale=scale, title="Ring of\n Dexterity",
                      hidden_title=f"{desc} ring", spawn_chance=ITEMS["Dexterity"][0])
        self.desc = desc

    def use(self, player, grid: Grid = None):
        """ Increases the Player's dex score by 1. """
        # Make sure this hasn't already been used
        if self.charges != 0:
            # Check if the Player has already used the item
            if not constants.items_info[Dexterity][0]:
                # Set used in constants.items_info
                constants.items_info[Dexterity][0] = True

            # Add one to Player's dex score
            player.dex += 1

            # Update charges
            self.charges -= 1

    def unequip(self, player, grid: Grid = None):
        """ When this ring is unequipped, the Player loses the benefits of having it equipped.
        This removes 1 from Player's dex. """
        # Update dex score
        player.dex -= 1


# ---Weapon Classes---
class Weapon(Item):
    def __init__(self,
                 filename: str = None,
                 scale: float = 1,
                 title: str = "Weapon",
                 spawn_chance: int = 0):
        Item.__init__(self, filename=filename, scale=scale, title=title, spawn_chance=spawn_chance)
        self.power = 2
        self.accuracy = 2

    # Returns 0 if misses and a damage value if it hits, uses the players stats for damage calculation
    def get_damage(self, player):
        hit = randint(1, 100)
        hit += player.dex + 2 * self.accuracy
        if hit > 50:
            # mace damage is 2d4 according to the wiki
            damage = randint(1, 4) + randint(1, 4)
            return damage
        else:
            return 0

    # Changes title to reflect if the weapon has been buffed or debuffed in any way
    def update(self):
        str_mod = self.power - self.power
        dex_mod = self.power - self.power
        change = ""
        if str_mod > 0:
            change += "+" + str(str_mod)
        elif str_mod < 0:
            change += str(str_mod)

        if dex_mod > 0:
            change += "+" + str(dex_mod)
        elif dex_mod < 0:
            change += str(dex_mod)

        change += self.title
        self.title = change
    
    def use(self, player):
        player.weapon = self


# Starting weapon
class Mace(Weapon):
    def __init__(self,
                 filename: str = None,
                 scale: float = 1):
        Weapon.__init__(self, filename=filename, scale=scale, title="Mace", spawn_chance=ITEMS["Mace"][0])
        self.power = 2
        self.accuracy = 2

    def get_damage(self, player):
        hit = randint(1, 100)
        hit += player.dex + 2 * self.accuracy
        if hit > 50:
            # mace damage is 2d4 according to the wiki
            damage = randint(1, 2 * self.power) + randint(1, 2 * self.power) + player.str // 16
            return damage
        else:
            return 0


# Good at everything
class Longsword(Weapon):
    def __init__(self,
                 filename: str = None,
                 scale: float = 1):
        Weapon.__init__(self, filename=filename, scale=scale, title="Longsword", spawn_chance=ITEMS["Longsword"][0])
        self.power = 3
        self.accuracy = 2

    def get_damage(self, player):
        hit = randint(1, 100)
        hit += player.dex + 2 * self.accuracy
        if hit > 50:
            damage = randint(self.power, self.power * 2) + randint(self.power, self.power * 2) + player.str // 10
            return damage
        else:
            return 0


# low accuracy high damage better str scaling
class Club(Weapon):
    def __init__(self,
                 filename: str = None,
                 scale: float = 1):
        Weapon.__init__(self, filename=filename, scale=scale, title="Club", spawn_chance=ITEMS["Club"][0])
        self.power = 4
        self.accuracy = 1

    def get_damage(self, player):
        hit = randint(1, 100)
        hit += player.dex + 2 * self.accuracy
        if hit > 50:
            damage = randint(0, self.power) + randint(0, self.power) + player.str // 4
            return damage
        else:
            return 0


# Accurate and has dex scaling
class Scimitar(Weapon):
    def __init__(self,
                 filename: str = None,
                 scale: float = 1):
        Weapon.__init__(self, filename=filename, scale=scale, title="Scimitar", spawn_chance=ITEMS["Scimitar"][0])
        self.power = 1
        self.accuracy = 4

    def get_damage(self, player):
        hit = randint(1, 100)
        hit += player.dex + 2 * self.accuracy
        if hit > 50:
            damage = randint(1, 2 * self.power) + player.str // 16 + player.dex // 6
            return damage
        else:
            return 0
