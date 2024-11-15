import numpy as np
import json
from sklearn.metrics.pairwise import cosine_similarity

with open('csvs_and_jsons\\random_users.json', 'r') as file:
    data = json.load(file)

class Node:
    def __init__(self, state, parent, action, path_cost, movie_name):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.movie_name = movie_name

    @classmethod
    def root(cls, init_state, movie_name):
        return cls(init_state, None, None, 0, movie_name)

    @classmethod
    def child(cls, problem, parent, action, movie_name):
        return cls(
            problem.result(parent.state, action),
            parent,
            action,
            parent.path_cost + 1,
            movie_name
        )

class MovieRecommender:
    def __init__(self, initial_state, user_id, movie):
        self.initial_state = initial_state
        self.user_id = user_id
        self.movie = movie
        self.visited = set()

    def actions(self, vector, index):
        vector_copy = vector[:]
        vector_copy[index] = 1 - vector_copy[index]
        return vector_copy

    def goal_test(self, node):
        print(f"Checking goal for node with state: {node.state}")  
        for other_user, other_movies in data.items():
            if other_user == self.user_id:
                continue
            for movie, vector in other_movies.items():
                similarity = compute_similarity(node.state, vector)
                print(f"Comparing to movie '{movie}' with similarity {similarity}")  
                if similarity >= 0.8 and movie != self.movie:
                    return movie, node.path_cost  
        return None, None
    def result(self, state, action):
        return action  
    def get_movie_name_for_state(self, state):
        print(f"Getting movie name for state: {state}")  
        for other_user, other_movies in data.items():
             for movie, vector in other_movies.items():
                similarity = compute_similarity(state, vector)
                print(f"Comparing state with movie'{movie}'-Similarity:{similarity}")
                if similarity>=0.9: 
                    print(f"Found movie '{movie}'with high similarity")  
                    return movie  
        print("No movie found for state")  
        return None  
def compute_similarity(vector1, vector2):
    vector1 = np.array(vector1).reshape(1, -1)
    vector2 = np.array(vector2).reshape(1, -1)
    similarity = cosine_similarity(vector1, vector2)
    return similarity[0][0]
