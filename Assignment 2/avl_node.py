"""
Implements the AVLNode class.
"""
from typing import Any, Union


class AVLNode:
    """
    A node in the AVL tree.
    """

    def __init__(self, key: Union[int, float] = 0, value: Any = None):
        """
        Create a new node.
        :param key: Key value. Used for comparison.
        :param value: Value to store.
        """
        self.key = key
        self.value = value
        self.parent = None
        self.left = None
        self.right = None
        self.height = 0

    def to_string(self):
        """
        Return a string representation of the node.
        :return:None
        """
        return "key:" + str(self.key) + ", value: " + str(self.value)
