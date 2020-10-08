
# package
import numpy as np


class Node:
    def __init__(self, data):
        self.data = data
        self.children = []
        self.parent = None

    def insert(self, data):
        child = Node(data)
        self.children.append(child)
        child.parent = self

    def delete_children(self):
        for child in self.children:
            child.delete_children()
