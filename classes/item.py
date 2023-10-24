import arcade


# Super Class Item
class Item(arcade.Sprite):
    def __init__(self, quantity: int, spawn_chance: float, enchantment: bool):
        super().__init__()
        self.quantity = quantity or 0
        self.spawn_chance = spawn_chance or 0.0
        self.enchantment = enchantment or False

    def randomize_emplacement(self, top_left_coord: list, bottom_right_coord: list):  # , room: Room?
        # Create coordinate for center of sprite using bounds of a room
        # NOTE: May not even need this, could just randomly assign coordinates and check if tile is full or not
        # THis would result in some getting spawned outside of rooms but player would never notice anyway
        pass


# Subclass Armor (Super: Item)
# Subclasses Armor types (Super: Armor)
class Armor(Item):
    def __init__(self, quantity: int, spawn_chance: float, enchantment: bool):
        super().__init__(quantity, spawn_chance, enchantment)

# Subclass Scroll (Super: Item)
# Subclasses scrolls (Super: Scroll)

# Subclass Potion (Super: Item)
# Subclasses potions (Super: Potion)

# Subclass Rod (Super: Item)
# Subclass Wand (Super: Rod)
# Subclasses wand types (Super: Wand)
# Subclass Staff (Super: Rod)
# Subclasses staff types (Super: Staff)

# Subclass Ring (Super: Item)
# Subclasses ring types (Super: Ring)
