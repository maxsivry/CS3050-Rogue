from classes.item import *

# Project-Wide Constants
# Number of rows and columns
ROW_COUNT = 40
COLUMN_COUNT = 70

# This sets the WIDTH and HEIGHT of each grid location
TILE_WIDTH = 15
TILE_HEIGHT = 15

MARGIN = 2

# This needs to be changed later I just have it like this for
# an example sprite
SPRITE_SCALING = TILE_HEIGHT / 1920

# Do the math to figure out our screen dimensions

# 15 * 70 + x = 17 * 72
SCREEN_WIDTH = (TILE_WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
SCREEN_HEIGHT = (TILE_HEIGHT + MARGIN) * ROW_COUNT + MARGIN
SCREEN_TITLE = "Rogue"

battle_message = ""

# Project-Wide dictionary
# To allow undiscovered items to maintain the same description even when new instances of the discovered items are made
# Format: Class: [Revealed by Player, Description]
items_info = {Leather: [False, ''], RingMail: [False, ''], StuddedLeather: [False, ''], ScaleMail: [False, ''],
              ChainMail: [False, ''], SplintMail: [False, ''], BandedMail: [False, ''], PlateMail: [False, ''],
              IdentifyRing: [False, ''], IncreaseMaxHealth: [False, ''], IdentifyPotion: [False, ''],
              Poison: [False, ''], RestoreStrength: [False, ''], Healing: [False, ''],
              TeleportTo: [False, ''], DrainLife: [False, ''], AddStrength: [False, ''],
              IncreaseDamage: [False, ''], Teleportation: [False, ''], Dexterity: [False, ''],
              Gold: [True, ''], Weapon: [False, ''], Mace: [False, ''], Longsword: [False, ''], Club: [False, ''],
              Scimitar: [False, '']}
