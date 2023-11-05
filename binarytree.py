from typing import Optional
from typing import Tuple
from random import randint
import arcade


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

    def __init__(self):
        self.root = None

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


def tree_to_list(node: Optional[Node]) -> list[RoomContainer]:
    rooms: list[RoomContainer] = []

    def walk_and_add(n: Optional[Node]):
        if n is not None:
            rooms.append(n.val)
            walk_and_add(n.lhs)
            walk_and_add(n.rhs)

    walk_and_add(node)
    return rooms
