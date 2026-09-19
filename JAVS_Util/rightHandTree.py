"""Right-hand binary tree for parsing natural language expressions."""
from __future__ import annotations

from typing import Optional


class RightHandTree:
    """Binary tree node used to build a tape from tokenized input.

    Each node holds a data value and optional left/right children.
    The tree is built left-associatively: a variable token pushes the
    current value to the left child and replaces the node's data.
    """

    def __init__(self) -> None:
        self.left: Optional[RightHandTree] = None
        self.right: Optional[RightHandTree] = None
        self.data: Optional[str] = None

    def insertNode(self, value: str) -> None:
        if self.data is None:
            self.data = value
        elif "$" in self.data:
            temp = self.data
            self.data = value
            self.right = None
            self.left = RightHandTree()
            self.left.insertNode(temp)
        elif self.right is None:
            self.right = RightHandTree()
            self.right.insertNode(value=value)
        else:
            self.right.insertNode(value=value)

    def PrintTree(self, node_position: str = "root", height: int = 0) -> None:
        print(f"{self.data} : {node_position}, Height : {height}")
        if self.left:
            self.left.PrintTree(node_position="left", height=height + 1)
        if self.right:
            self.right.PrintTree(node_position="right", height=height + 1)

    def makeTape(self) -> list[str]:
        tape: list[str] = []
        current: Optional[RightHandTree] = self
        while current is not None and current.data is not None:
            tape.append(current.data)
            if current.left is not None:
                tape.append(current.left.data)  # type: ignore[arg-type]
            if current.right is not None:
                current = current.right
            else:
                break
        return tape