from problem_modeling import MovieRecommender
import json
from problem_modeling import Node, find_path_to_goal
from collections import deque
import time
from pyvis.network import Network
import random
import webbrowser
import timeit

with open('csvs_and_jsons\\movie_vectors.json', 'r') as file:
    movies = json.load(file)

def iterative_depth_first_search(problem, movie, max_depth=10):
    root = Node.root(problem.initial_state, movie)
    net = Network(notebook=True, height="600px", width="100%")  
    net.add_node(root.movie_name, label=root.movie_name, color="lightgreen")
    for depth_limit in range(1, max_depth + 1): 
        print(f"Starting DFS with depth limit {depth_limit}")
        frontier = [(root, 0)]  
        visited = set()  
        while frontier:
            node, current_depth = frontier.pop()  
            state_tuple = tuple(node.state)
            if state_tuple in visited:
                continue
            visited.add(state_tuple)
            recommended_movie, cost , goal_node= problem.goal_test(node)
            if recommended_movie and cost and goal_node:
                net.show("html_files\\IDS_tree.html") 
                return recommended_movie, cost, goal_node
            if current_depth<depth_limit: # TO LIMIT THE DEPTH EACH TIME IT ITERATE
                for movie_index in range(len(problem.initial_state)):
                    new_state = problem.actions(node.state, movie_index)
                    child_name = None
                    for name, vector in movies.items():
                        if vector == new_state:
                            child_name = name
                    child_node = Node.child(problem, node, new_state, child_name)
                    frontier.append((child_node, current_depth + 1))

                    parent_movie_name = node.movie_name
                    if child_name is None and parent_movie_name is not None:
                        net.add_node(str(child_node.state), label=str(child_node.state), color="lightblue")
                        net.add_edge(parent_movie_name, str(child_node.state))
                    elif parent_movie_name is not None and child_name is not None:
                        net.add_node(child_name, label=child_name, color="lightblue")
                        net.add_edge(parent_movie_name, child_name)
                    elif parent_movie_name is None and child_name is not None:
                        net.add_node(child_name, label=child_name, color="lightblue")
                        net.add_edge(str(node.state), child_name)
                
    net.show("html_files\\IDS_tree.html")  
    return None

def run_ids():
    iterative_depth_first_search(recommender, movie)

def ids_time_calculation():
    number_of_times=5
    time_of_ids = timeit.timeit(run_ids, globals=globals(), number=number_of_times)
    ids_average=time_of_ids/number_of_times
    return ids_average

# movie = random.choice(list(movies.keys()))
movie='The Emperor\'s New Groove'

initial_state = movies[movie]
root = Node.root(initial_state, movie)
recommender = MovieRecommender(root, initial_state, movie)
print("Search has started...")
start_time = time.time()
recommended_movie, cost, goal_node=iterative_depth_first_search(recommender, movie)
end_time = time.time()
run_time = end_time-start_time
if recommended_movie and cost:
    print("Recommended movie is", recommended_movie, 'and the cost is', cost)
    print("Path to goal:", " -> ".join(find_path_to_goal(goal_node)))

else:
    print("No similar preference found.")
print()
print('Time taken by IDFS is', round(run_time, 2), "seconds")

# webbrowser.open("html_files\\IDS_tree.html")
