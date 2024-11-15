from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json

with open('csvs_and_jsons\\weighted_graph.json', 'r') as file:
    graph = json.load(file)

with open('csvs_and_jsons\\movie_vectors.json', 'r') as file:
    movies= json.load(file)

class Node:
    def __init__(self, parent,state,path_cost, movie_name):
        self.state = state
        self.parent = parent
        self.path_cost = path_cost
        self.movie_name=movie_name

    @classmethod
    def root(cls,init_state,name):
        return cls(None, init_state,0,name )

    @classmethod
    def child(cls,parent, state, cost, movie_name):
        return cls(
            parent,
            state,
            parent.path_cost + cost,
            movie_name
        )
    
    def __lt__(self, other):
        # This compares two nodes based on their path_cost(used for ucs)
        return self.path_cost < other.path_cost

class MovieRecommender:
    def __init__(self, initial_state):
        self.initial_state = initial_state
        self.visited = {}

    def goal_test(self, node, original_movie, movie):
        similarity = self.compute_similarity(movies[original_movie], movies[movie])
        if similarity >= 0.8 and movies[original_movie] != movies[movie]:
            return movie, node.path_cost  
        return None, None
    @classmethod
    def compute_similarity(self,vector1, vector2):
            vector1 = np.array(vector1).reshape(1, -1)
            vector2 = np.array(vector2).reshape(1, -1)
            similarity = cosine_similarity(vector1, vector2)
            return similarity[0][0]
    
    def result(self, state, action):
        return action


