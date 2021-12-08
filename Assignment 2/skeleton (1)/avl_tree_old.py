from avl_node import AVLNode


def get_smallest_recursively(node):
    """
    Helper function to get the smallest key in the tree, starting from a specific node (here: node).
    :param node:
    :return:
    """
    current_node = node
    # Go left as long as left child is not None
    while current_node.left is not None:
        current_node = current_node.left
    return current_node  # and return last node where child is not None


class AVLTree:
    def __init__(self):
        """Default constructor. Initializes the AVL tree."""
        self.root = None
        self.size = 0

    def get_tree_root(self):
        """
        Method to get the root node of the AVLTree
        :return AVLNode -- the root node of the AVL tree
        """
        return self.root

    def get_tree_height(self):
        """Retrieves tree height.
        :return -1 in case of empty tree, current tree height otherwise.
        """
        if self.root is None:
            return -1
        else:
            return self.root.height

    def get_tree_size(self):
        """Yields number of key/value pairs in the tree.
        :return Number of key/value pairs.
        """
        if self.root is None:
            return 0
        else:
            return self.size

    @property
    def to_array(self):
        """Yields an array representation of the tree's values (pre-order).
        :return Array representation of the tree values.
        """
        if self.root is None:
            return []
        else:
            pass

    def search_bst_helper(self, current_node, key):
        """
        Helper function for find(self, key) and find_comparison
        :param current_node: current node for comparison to key
        :param key: key which we want to find
        """
        if key == current_node.key:  # key is found
            return current_node
        elif key < current_node.key:
            if current_node.left:
                return self.search_bst_helper(current_node.left, key)
            else:
                raise KeyError("Key is not present in the tree!")
        elif key > current_node.key:
            if current_node.right:
                return self.search_bst_helper(
                    current_node.right,
                    key,
                )
            else:
                return None

    def find_by_key(self, key, return_node=False):
        """Returns value of node with given key.
        :param return_node: whether to return the node or the value
        :param key: Key to search.
        :return Corresponding value if key was found, None otherwise.
        :raises ValueError if the key is None
        """
        if key is None:
            raise ValueError("Key cannot be None")
        if self.root:  # tree is not empty, do search
            result = self.search_bst_helper(self.root, key)
            if result is not None:
                if return_node:
                    return result
                else:
                    return result.key
            else:
                return None
        else:
            return None

    def insert(self, key, value):
        """Inserts a new node into AVL tree.
        :param key: Key of the new node.
        :param value: Data of the new node. May be None. Nodes with the same key
        are not allowed. In this case False is returned. None-Keys and None-Values are
        not allowed. In this case an error is raised.
        :return True if the insert was successful, False otherwise.
        :raises ValueError if the key or value is None.
        """
        if key is None:
            raise ValueError("Key cannot be None")
        if value is None:
            raise ValueError("Value cannot be None")

        def insert_bst_helper(current_node, value, key):
            """
            Helper function for insert, as defined in the lecture slides
            """
            # Case 1: current node's key < key to insert
            if current_node.key < key:
                if current_node.right:
                    insert_bst_helper(current_node.right, value, key)
                else:
                    current_node.right = AVLNode(
                        value=value, key=key, parent=current_node
                    )
                    return True
            # Case 2: current node's key > key to insert
            elif current_node.key > key:
                if current_node.left:
                    insert_bst_helper(current_node.left, value, key)
                else:
                    current_node.left = AVLNode(
                        value=value, key=key, parent=current_node
                    )
                    return True
            # Case 3: current node's key == key to insert
            # This means key is already present in the tree --> not allowed; raise KeyError
            elif current_node.key == key:
                return False

        self.size += 1
        if self.root is None:  # tree is empty, add node as root
            self.root = AVLNode(key=key, value=value)
            return True
        else:  # tree not empty, add node at correct position
            return insert_bst_helper(current_node=self.root, value=value, key=key)

    def remove_by_key(self, key):
        """Removes node with given key.
        :param key: Key of node to remove.
        :return True If node was found and deleted, False otherwise.
        @raises ValueError if the key is None.
        """
        if key is None:
            raise ValueError("Key cannot be None")

            # KeyError is handled by next line
        key_to_remove = self.find_by_key(
            key, return_node=True
        )  # size always changes only by 1, since there are no duplicate keys
        if key_to_remove is None:
            return False
        # CASE 1: node has no child node
        if (not key_to_remove.right) and (not key_to_remove.left):
            parent = key_to_remove.parent
            if key_to_remove.key <= parent.key:
                parent.left = None
            elif key_to_remove.key > parent.key:
                parent.right = None
            self.size -= 1

        # CASE 2: node has only one child; replace it by child node
        # Case 2a: child is on the left to key_to_remove
        elif key_to_remove.left and not key_to_remove.right:
            parent = key_to_remove.parent
            child = key_to_remove.left
            if key_to_remove.key <= parent.key:
                parent.left = child
            elif key_to_remove.key > parent.key:
                parent.right = child
            self.size -= 1

        # Case 2b: child is on the right to key_to_remove
        elif not key_to_remove.left and key_to_remove.right:
            parent = key_to_remove.parent
            child = key_to_remove.right
            if key_to_remove.key <= parent.key:
                parent.left = child
            elif key_to_remove.key > parent.key:
                parent.right = child
            self.size -= 1

        # CASE 3: Node has 2 child node
        elif key_to_remove.left and key_to_remove.right:
            right_child = key_to_remove.right
            next_successor = get_smallest_recursively(
                right_child
            )  # get next in-order successor of key_to_remove
            if (
                next_successor.parent != key_to_remove
            ):  # make sure it is not a child of itself
                self.transplant(next_successor, next_successor.right)  # swap them
                next_successor.right = key_to_remove.right  # change links
                next_successor.right.parent = next_successor

            self.transplant(key_to_remove, next_successor)  # swap them
            next_successor.left = key_to_remove.left  # change links
            next_successor.left.parent = next_successor
            self.size -= 1

        return True

    @property
    def size_(self) -> int:
        """Return number of nodes contained in the tree."""

        def get_size_recursively(node):
            """
            Helper function to get size of the tree. Start with the root.
            """
            if node is None:
                return 0  # next node is not existent, do not increase count
            else:
                # increase count: from size of left/right subtree recursively, and current node (1)
                return (
                    get_size_recursively(node.left)
                    + 1
                    + get_size_recursively(node.right)
                )

        return get_size_recursively(self.root)  # Start with root

    def transplant(self, node_1, node_2):
        """
        Helper function for remove. node_1 is changing places with node_2.
        :return: None
        """
        if node_1.parent is None:  # node_1 is root
            self.root = node_2
        elif node_1 == node_1.parent.left:  # node_1 is left child
            node_1.parent.left = node_2
        else:  # node_1 is right child
            node_1.parent.right = node_2
        if node_2 is not None:  # change parent relationship
            node_2.parent = node_1.parent

    def update_heights(self, recurse=True):
        if self.root is not None:
            if recurse:
                if self.root.left is not None:
                    self.root.left.update_heights()
                if self.root.right is not None:
                    self.root.right.update_heights()

            self.height = max(self.root.left.height, self.root.right.height) + 1
        else:
            self.height = -1
