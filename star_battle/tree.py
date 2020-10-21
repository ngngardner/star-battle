
# package
import numpy as np


class Node:
    def __init__(self, data):
        self.data = data
        self.children = []
        self.parent = None
        self.height = 0
        self.star_loc = None

    def insert(self, data, star_loc):
        child = Node(data)
        self.children.append(child)
        child.parent = self
        child.update_height()
        child.star_loc = star_loc

    def delete_children(self):
        for child in self.children:
            child.delete_children()

    def update_height(self):
        if self.parent is not None:
            self.height = self.parent.height + 1
