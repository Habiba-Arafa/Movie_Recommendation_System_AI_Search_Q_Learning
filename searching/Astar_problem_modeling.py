import numpy as np

class Node:
    def __init__(self, state, parent, action, path_cost):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    @classmethod
    def root(cls, init_state):
        return cls(init_state, None, None, 0)

    @classmethod
    def child(cls, parent, action, path_cost_increment=1):
        return cls(
            action,  
            parent,
            action,
            parent.path_cost + path_cost_increment  
        )
  
    def __lt__(self, other):
        return self.path_cost < other.path_cost
