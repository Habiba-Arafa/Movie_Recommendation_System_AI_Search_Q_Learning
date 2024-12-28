from problem_modeling import MovieRecommender
import json
from problem_modeling import Node, find_path_to_goal
from collections import deque
import time
from pyvis.network import Network
import random
import webbrowser
import timeit
import psutil
import os
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
            recommended_movie, cost , goal_node, similarity= problem.goal_test(node)
            if recommended_movie and cost and goal_node:
                net.show("html_files\\IDS_tree.html") 
                return recommended_movie, cost, goal_node,similarity
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

def ids_space_calculation():
    process = psutil.Process(os.getpid())  
    memory_info = process.memory_info()
    rss = memory_info.rss / (1024 * 1024)  
    vms = memory_info.vms / (1024 * 1024)  
    return rss, vms

def ids_comparison(movies_list):
    sum_similarity=0
    for movie in movies_list:
        initial_state = movies[movie]
        root = Node.root(initial_state, movie)
        recommender = MovieRecommender(root, initial_state, movie)
        _,_,_,similarity=iterative_depth_first_search(recommender, movie)
        sum_similarity+=similarity
    return sum_similarity/len(movies_list)

# movie = random.choice(list(movies.keys()))
movie='The Emperor\'s New Groove'

initial_state = movies[movie]
root = Node.root(initial_state, movie)
recommender = MovieRecommender(root, initial_state, movie)
print("Search has started...")
# Track memory usage before and after
start_rss, start_vms = ids_space_calculation()
print(f"Memory usage before search: RSS = {start_rss:.2f} MB, VMS = {start_vms:.2f} MB")

start_time = time.time()
recommended_movie, cost, goal_node, similarity=iterative_depth_first_search(recommender, movie)
end_time = time.time()
run_time = end_time-start_time

end_rss, end_vms = ids_space_calculation()
print(f"Memory usage after search: RSS = {end_rss:.2f} MB, VMS = {end_vms:.2f} MB")
def ids_space_ans():
    return start_rss ,end_rss
run_time = end_time - start_time
print(f'Time taken by ids is {round(run_time, 2)} seconds')

rss_diff = end_rss - start_rss
vms_diff = end_vms - start_vms
print(f'Memory usage increased by: RSS = {rss_diff:.2f} MB, VMS = {vms_diff:.2f} MB')

if recommended_movie and cost:
    print("Recommended movie is", recommended_movie, 'and the cost is', cost)
    print("Path to goal:", " -> ".join(find_path_to_goal(goal_node)))

else:
    print("No similar preference found.")
print()
print('Time taken by IDFS is', round(run_time, 2), "seconds")

# webbrowser.open("html_files\\IDS_tree.html")
