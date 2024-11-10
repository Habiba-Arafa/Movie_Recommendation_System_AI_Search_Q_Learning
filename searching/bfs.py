from problem_modeling import MovieRecommender
import json
from problem_modeling import Node
from collections import deque

with open('csvs_and_jsons\\random_users.json', 'r') as file:
    data = json.load(file)

def breadth_first_tree_search(problem):
    frontier = deque([Node.root(problem.initial_state)])
    while frontier:
        node = frontier.popleft()
        state_tuple = tuple(node.state)
        if state_tuple in problem.visited:
            continue
        problem.visited.add(state_tuple)
        recommended_movie = problem.goal_test(node.state)
        if recommended_movie:
            return recommended_movie
        
        for movie_index in range(len(problem.initial_state)):
            new_state = problem.actions(node.state, movie_index)
            child_node = Node.child(problem, node, new_state)
            frontier.append(child_node)
    return None

user_id  = 'user1'
movie ='The Real Cancun'
initial_state = data[user_id][movie] 
recommender = MovieRecommender(initial_state, user_id,movie)
recommended_movie = breadth_first_tree_search(recommender)
if recommended_movie:
    print("Recommended movie:", recommended_movie)
else:
    print("No similar preference found.")