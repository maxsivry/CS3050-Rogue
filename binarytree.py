from typing import Optional

class Node:
    lhs: Optional['Node']
    rhs: Optional['Node']

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

    def print(self):
        if self.root is not None:
            self.rec_prnt(self.root)

    def rec_prnt(self, node: Node):
        if node is not None:
            self.rec_prnt(node.lhs)
            print(str(node.val) + ' ')
            self.rec_prnt(node.rhs)


if __name__ == "__main__":
    tree = Tree()
    tree.insert(8)
    tree.insert(3)
    tree.insert(4)
    tree.insert(12)
    tree.insert(20)
    tree.insert(18)
    tree.print()
