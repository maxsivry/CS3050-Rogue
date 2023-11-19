from typing import Optional, Tuple
from random import randint, randrange
from enum import Enum, auto


class RoomType(Enum):
    Normal = auto(),
    PlayerSpawn = auto(),
    Stairs = auto(),


class Room:
    x: int
    y: int
    w: int
    h: int
    center: Tuple[int, int]
    room_type: RoomType

    def __init__(self, x: int, y: int, w: int, h: int):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.center = ((x + w // 2), (y + h // 2))
        self.room_type = RoomType.Normal


class RoomContainer:
    x: int
    y: int
    w: int
    h: int
    center: Tuple[int, int]

    def __init__(self, x: int, y: int, w: int, h: int):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.center = ((x + w // 2), (y + h // 2))


class Node:
    lhs: Optional['Node']
    rhs: Optional['Node']
    val: RoomContainer

    def __init__(self, val):
        self.lhs = None
        self.rhs = None
        self.val = val


class Tree:
    root: Optional[Node]

    def __init__(self, x: int, y: int, w: int, h: int):
        self.root = Node(RoomContainer(x, y, w, h))

    def get_root(self):
        return self.root

    def insert(self, val):
        if self.root is None:
            self.root = Node(val)
        else:
            self.rec_ins(val, self.root)

    def rec_ins(self, val, node: Node):
        if val < node.val:
            if node.lhs is not None:
                self.rec_ins(val, node.lhs)
            else:
                node.lhs = Node(val)
        else:
            if node.rhs is not None:
                self.rec_ins(val, node.rhs)
            else:
                node.rhs = Node(val)


def populate_tree(node: Optional[Node], curr_split=3) -> Node:
    if curr_split != 0:
        room_l, room_r = split_room(node.val)
        node.lhs = populate_tree(Node(room_l), curr_split - 1)
        node.rhs = populate_tree(Node(room_r), curr_split - 1)
    return node


W_MIN_RATIO: float = 0.45
H_MIN_RATIO: float = 0.40


def split_room(room: RoomContainer) -> Tuple[RoomContainer, RoomContainer]:
    if (r := randint(0, 1)) == 0:
        lhs = RoomContainer(room.x, room.y, randint(1, room.w), room.h)
        rhs = RoomContainer(room.x + lhs.w, room.y, room.w - lhs.w, room.h)
        l_width_ratio = lhs.w / lhs.h
        r_width_ratio = rhs.w / rhs.h
        if l_width_ratio < W_MIN_RATIO or r_width_ratio < W_MIN_RATIO:
            return split_room(room)
        return lhs, rhs
    elif r == 1:
        lhs = RoomContainer(room.x, room.y, room.w, randint(1, room.h))
        rhs = RoomContainer(room.x, room.y + lhs.h, room.w, room.h - lhs.h)
        l_height_ratio = lhs.h / lhs.w
        r_height_ratio = rhs.h / rhs.w
        if l_height_ratio < H_MIN_RATIO or r_height_ratio < H_MIN_RATIO:
            return split_room(room)
        return lhs, rhs


def get_rooms(node: Optional[Node]) -> list[Room]:
    rooms: list[Room] = []

    def walk_and_add_rooms(n: Optional[Node]):
        if n is not None:
            if n.lhs is None and n.rhs is None:
                x = n.val.x
                y = n.val.y
                w = randint(int(n.val.w * 0.60), int(n.val.w * 0.80))
                h = randint(int(n.val.h * 0.60), int(n.val.h * 0.80))
                rooms.append(Room(x, y, w, h))
            walk_and_add_rooms(n.lhs)
            walk_and_add_rooms(n.rhs)

    walk_and_add_rooms(node)

    def assign_room_type(new_type: RoomType):
        idx = randrange(len(rooms))
        if rooms[idx].room_type == RoomType.Normal:
            rooms[idx].room_type = new_type
        else:
            assign_room_type(new_type)

    assign_room_type(RoomType.PlayerSpawn)
    assign_room_type(RoomType.Stairs)

    return rooms


def create_trails(node: Optional[Node]) -> list[Tuple[int, int]]:
    trails: list[Tuple[int, int]] = []

    def walk_and_add_trails(n: Optional[Node]):
        if n is not None:
            if n.lhs is None and n.rhs is None:
                return
            else:
                lhs_center_x, lhs_center_y = n.lhs.val.center
                rhs_center_x, rhs_center_y = n.rhs.val.center
                if abs(lhs_center_x - rhs_center_x) > abs(lhs_center_y - rhs_center_y):
                    if (r := randint(0, 1)) == 0:
                        for x in range(lhs_center_x, rhs_center_x):
                            trails.append((x, lhs_center_y))
                    elif r == 1:
                        for x in range(lhs_center_x, rhs_center_x):
                            trails.append((x, rhs_center_y))
                else:
                    if (r := randint(0, 1)) == 0:
                        for y in range(lhs_center_y, rhs_center_y):
                            trails.append((lhs_center_x, y))
                    elif r == 1:
                        for y in range(lhs_center_y, rhs_center_y):
                            trails.append((rhs_center_x, y))
            walk_and_add_trails(n.lhs)
            walk_and_add_trails(n.rhs)

    walk_and_add_trails(node)

    return trails
