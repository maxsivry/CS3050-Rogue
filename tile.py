from enum import Enum, auto


class TileType(Enum):
    Empty = auto(),
    Wall = auto(),
    Floor = auto(),
    Trail = auto(),
    Stairs = auto(),
    Doorway = auto()


class Tile:
    is_hidden: bool
    tile_type: TileType

    def __init__(self):
        self.is_hidden = True
        self.tile_type = TileType.Empty

    def reveal(self):
        if self.tile_type != TileType.Empty:
            self.is_hidden = True
