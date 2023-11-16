from classes.tile import *
from binarytree import Room


class Grid:
    grid: list[list[Tile]]
    n_rows: int
    n_cols: int

    def __init__(self, n_rows: int = 80, n_cols: int = 24):
        self.n_rows = n_rows
        self.n_cols = n_cols

        self.grid = []
        for x in range(n_rows):
            new_col: list[Tile] = []

            for y in range(n_cols):
                new_col.append(Tile())

            self.grid.append(new_col)

        print("made room")

    # method to get item at index
    def __getitem__(self, index):
        row, col = index
        return self.grid[row][col]

    # Method to set item at index
    def __setitem__(self, index, value):
        row, col = index
        self.grid[row][col] = value

    def add_room(self, room: Room):
        border_x: int = room.x - 1
        border_y: int = room.y - 1
        border_w: int = room.w + 1
        border_h: int = room.h + 1

        if border_x <= 0:
            room.x += 1
            border_x += 1
        elif border_x > self.n_rows:
            room.x -= 1
            border_x -= 1

        if border_y <= 0:
            room.y += 1
            border_y += 1
        elif border_y > self.n_cols:
            room.y -= 1
            border_y -= 1

        try:
            for x in range(border_x, border_x + border_w + 1):
                if self.grid[x][border_y].tile_type != TileType.Trail:
                    self.grid[x][border_y].tile_type = TileType.Wall
                if self.grid[x][border_y + border_h].tile_type != TileType.Trail:
                    self.grid[x][border_y + border_h].tile_type = TileType.Wall
            for y in range(border_y, border_y + border_h):
                if self.grid[border_x][y].tile_type != TileType.Trail:
                    self.grid[border_x][y].tile_type = TileType.Wall
                if self.grid[border_x + border_w][y].tile_type != TileType.Trail:
                    self.grid[border_x + border_w][y].tile_type = TileType.Wall
            for x in range(room.x, room.x + room.w):
                for y in range(room.y, room.y + room.h):
                    self.grid[x][y].tile_type = TileType.Floor
        except IndexError:
            pass


if __name__ == "__main__":
    grid = Grid(n_rows=120, n_cols=48)
