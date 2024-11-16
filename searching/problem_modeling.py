from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json

with open('csvs_and_jsons\\random_users.json', 'r') as file:
    data = json.load(file)

class Node:
    def __init__(self, state, parent, action, path_cost, movie_name):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.movie_name=movie_name

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
    def __init__(self,root,initial_state,movie):
        self.root=root
        self.initial_state = initial_state
        self.movie= movie
        self.visited = set()

    def actions(self, vector, index):
        vector_copy = vector[:]
        vector_copy[index] = 1 - vector_copy[index]
        return vector_copy

    def goal_test(self, node):
        if compute_similarity(node.state,self.root.state) >=0.80 and node.movie_name!= self.root.movie_name: 
            return node.movie_name, node.path_cost, node
        return None, None, None

    def result(self, state, action):
        return action 

def compute_similarity(vector1, vector2):
        vector1 = np.array(vector1).reshape(1, -1)
        vector2 = np.array(vector2).reshape(1, -1)
        similarity = cosine_similarity(vector1, vector2)
        return similarity[0][0]

def find_path_to_goal(node):
    path = []
    while node is not None:
        if node.movie_name== None:
            path.append(str(node.state))
        else:
            path.append(node.movie_name)  
        node = node.parent  
    path.reverse() 
    return path