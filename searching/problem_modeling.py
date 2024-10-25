from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json

with open('csvs_and_jsons\\random_users.json', 'r') as file:
    data = json.load(file)

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
    def child(cls, problem, parent, action):
        return cls(
            problem.result(parent.state, action),
            parent,
            action,
            parent.path_cost + 1
        )

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

    def goal_test(self, current_vector):
        for other_user, other_movies in data.items():
            if other_user == self.user_id:  
                continue
            for movie, vector in other_movies.items():
                if self.compute_similarity(current_vector, vector) >=0.8 and movie != self.movie: 
                    return movie  
        return None

    def compute_similarity(self, vector1, vector2):
        vector1 = np.array(vector1).reshape(1, -1)
        vector2 = np.array(vector2).reshape(1, -1)
        similarity = cosine_similarity(vector1, vector2)
        return similarity[0][0]

    def result(self, state, action):
        return action 




