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
class MovieRecommender:
    def __init__(self, initial_state, user_id,movie):
        self.initial_state = initial_state
        self.user_id = user_id
        self.movie= movie
        self.visited = set()

    def actions(self, vector, index):
        vector_copy = vector[:]
        vector_copy[index] = 1 - vector_copy[index]
        return vector_copy

    def goal_test(self, node):
        for other_user, other_movies in data.items():
            if other_user == self.user_id:  
                continue
            for movie, vector in other_movies.items():
                if compute_similarity(node.state, vector) >=0.8 and movie != self.movie: 
                    return movie , node.path_cost 
        return None, None

    def result(self, state, action):
        return action 

def compute_similarity(vector1, vector2):
        vector1 = np.array(vector1).reshape(1, -1)
        vector2 = np.array(vector2).reshape(1, -1)
        similarity = cosine_similarity(vector1, vector2)
        return similarity[0][0]