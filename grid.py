from tile import *
from random import randint


class Grid:
    grid: list[list[Tile]]
    n_rows: int
    n_cols: int
    n_rooms: int = 5

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

    def populate_floor(self):
        max_room_size = 15
        min_room_size = 5

        room_width = randint(min_room_size, max_room_size)
        room_height = randint(min_room_size, max_room_size)

        room_x = randint(0, self.n_rows - 1)
        room_y = randint(0, self.n_cols - 1)

        for row in range(room_x, room_x + room_width):
            for col in range(room_y, room_y + room_height):
                if self.grid[row][col].tile_type == TileType.Floor:
                    return

        self.add_room(room_x, room_y, room_width, room_height)

    def add_room(self, x: int, y: int, w: int, h: int):
        for row in range(x, x + w):
            for col in range(y, y + h):
                self.grid[row][col].tile_type = TileType.Floor
