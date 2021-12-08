class AVLNode:
    def __init__(self, key=0, value=None, right=None, left=None, height=0, parent=None):
        self.key = key
        self.value = value
        self.parent = parent
        self.left = left
        self.right = right
        self.height = height

    def to_string(self):
        return "key:" + str(self.key) + ", value: " + str(self.value)
