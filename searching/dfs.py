from problem_modeling import MovieRecommender
import json
from problem_modeling import Node
from collections import deque

with open('csvs_and_jsons\\random_users.json', 'r') as file:
    data = json.load(file)

def depth_first_tree_search(problem, verbose=False):
    frontier = [Node.root(problem.initial_state)]  # Stack (LIFO)
    problem.visited = set()  
    while frontier:
        node = frontier.pop()  # Last-in, first-out (LIFO)
        state_tuple = tuple(node.state)  # Convert state to a hashable type for set
        if state_tuple in problem.visited:
            continue

        problem.visited.add(state_tuple)
        recommended_movie = problem.goal_test(node.state)
        if recommended_movie:
            return recommended_movie  

        for movie_index in range(len(problem.initial_state)):
            new_state = problem.actions(node.state, movie_index)
            child_node = Node.child(problem, node, new_state)

            if tuple(child_node.state) not in problem.visited:
                frontier.append(child_node)  

        if verbose:
            visualizer = Visualizer(problem)
            visualizer.visualize(frontier) 

    return None 

user_id  = 'user1'
movie ='Swept Away'
initial_state = data[user_id][movie] 
print('original vector: ',initial_state)
recommender = MovieRecommender(initial_state, user_id,movie)
recommended_movie = depth_first_tree_search(recommender)
if recommended_movie:
    print("Recommended movie:", recommended_movie)
else:
    print("No similar preference found.")