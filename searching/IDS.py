import numpy as np
import json
from sklearn.metrics.pairwise import cosine_similarity
from IDS_problem_modeling import MovieRecommender, Node

with open('csvs_and_jsons\\random_users.json', 'r') as file:
    data = json.load(file)

def dls(problem, node, depth, visited):
    print(f"Depth {depth}: Current Movie: {node.movie_name}")  

    goal, cost = problem.goal_test(node)  
    if goal: 
        return goal, cost, node  
    if depth == 0: 
        return None, None, None
    for action_index in range(len(problem.initial_state)):
        new_state = problem.actions(node.state, action_index)
        movie_name = problem.get_movie_name_for_state(new_state)
        child_node = Node.child(problem, node, new_state, movie_name) 

        state_tuple = tuple(child_node.state)
        if state_tuple not in visited:
            visited.add(state_tuple)
            result = dls(problem, child_node, depth - 1, visited)
            if result[0]:  
                return result
            visited.remove(state_tuple)
    return None, None, None

def iddfs(problem, start_state):
    depth = 0
    while True:
        visited = set()
        start_node = Node.root(start_state, problem.movie) 
        print(f"Starting Iteration {depth}...")  
        result = dls(problem, start_node, depth, visited)
        if result[0]:  
            return result
        depth += 1

user_id = 'user1'
movie = 'College'
initial_state = data[user_id][movie]
recommender = MovieRecommender(initial_state, user_id, movie)
recommended_movie = iddfs(recommender, recommender.initial_state)
if recommended_movie:
    print(f"Recommended movie: {recommended_movie[0]}")  
    print("Total cost:", recommended_movie[1])  
else:
    print("No similar preference found.")