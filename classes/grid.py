from classes.tile import *
from random import randint


class Rect:
    x: int
    y: int
    w: int
    h: int

    def __init__(self, x: int, y: int, w: int, h: int):
        self.x = x
        self.y = y
        self.w = w
        self.h = h


def rects_overlapping(r1: Rect, r2: Rect) -> bool:
    return r1.x < r2.x + r2.w and \
        r1.x + r1.w > r2.x and \
        r1.y < r2.y + r2.h and \
        r1.y + r1.h > r2.y


class Grid:
    grid: list[list[Tile]]
    n_rows: int
    n_cols: int
    n_rooms: int = 20

    def __init__(self, n_rows: int = 80, n_cols: int = 24):
        self.n_rows = n_rows
        self.n_cols = n_cols

        self.grid = []
        for x in range(n_cols):
            new_col: list[Tile] = []

            for y in range(n_rows):
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

    def populate_floor(self):
        max_room_size = 14
        min_room_size = 7

        for _ in range(self.n_rooms):
            room_width = randint(min_room_size, max_room_size)
            room_height = randint(min_room_size, max_room_size)

            room_x = randint(0, self.n_cols - room_width - 1)
            room_y = randint(0, self.n_rows - room_height - 1)

            for row in range(room_x, room_x + room_width):
                for col in range(room_y, room_y + room_height):
                    try:
                        if self.grid[row][col].tile_type == TileType.Floor:
                            return
                    except IndexError:
                        pass

            self.add_room(room_x, room_y, room_width, room_height)

    def add_room(self, x: int, y: int, w: int, h: int):
        for row in range(x, x + w):
            for col in range(y, y + h):
                try:
                    self.grid[row][col].tile_type = TileType.Floor
                except IndexError:
                    pass

    def print_grid(self):
        for row in self.grid:
            for tile in row:
                if tile.tile_type == TileType.Floor:
                    print('.', end='')
                elif tile.tile_type == TileType.Wall:
                    print('#', end='')
                elif tile.tile_type == TileType.Empty:
                    print('-', end='')

            print()


if __name__ == "__main__":
    grid = Grid(n_rows=120, n_cols=48)
    grid.populate_floor()
    grid.print_grid()
