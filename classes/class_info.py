# Dependencies
from typing import Optional


# Define class for persistent class data
class ClassInfo:
    def __init__(self):
        # set initial state of dictionary
        self.item_info = {"Leather": [20, "armor", False, ''], "Ring Mail": [15, "armor", False, ''],
                          "Studded Leather": [15, "armor", False, ''], "Scale Mail": [13, "armor", False, ''],
                          "Chain Mail": [12, "armor", False, ''], "Splint Mail": [10, "armor", False, ''],
                          "Banded Mail": [10, "armor", False, ''], "Plate Mail": [5, "armor", False, ''],
                          "Magic Mapping": [14, "scroll", False, ''], "Identify Weapon": [16, "scroll", False, ''],
                          "Identify Armor": [17, "scroll", False, ''], "Remove Curse": [17, "scroll", False, ''],
                          "Poison": [18, "potion", False, ''], "Monster Detection": [16, "potion", False, ''],
                          "Restore Strength": [23, "potion", False, ''], "Healing": [23, "potion", False, ''],
                          "Light": [22, "wand", False, ''], "Teleport To": [16, "wand", False, ''],
                          "Teleport Away": [16, "wand", False, ''], "Slow Monster": [21, "wand", False, ''],
                          "Add Strength": [19, "ring", False, ''], "Increase Damage": [18, "ring", False, ''],
                          "Teleportation": [15, "ring", False, ''], "Dexterity": [18, "ring", False, '']}

    def set_item_info(self, key: str, index: int, val: Optional):
        self.item_info[key][index] = val

    def get_item_info(self, key: str, index: int):
        return self.item_info[key][index]

    def get_keys(self):
        return self.item_info.keys()
