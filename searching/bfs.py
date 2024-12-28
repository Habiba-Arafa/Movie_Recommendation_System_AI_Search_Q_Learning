from problem_modeling import MovieRecommender,Node,find_path_to_goal
import json
from collections import deque
import time
import timeit
from pyvis.network import Network
import random
import webbrowser
import psutil
import os

with open('csvs_and_jsons\\movie_vectors.json', 'r') as file:
    movies = json.load(file)

def breadth_first_tree_search(problem, movie):
    root= Node.root(problem.initial_state,movie)
    frontier = deque([root])
    net = Network(notebook=True, height="600px", width="100%")  
    net.add_node(root.movie_name, label=root.movie_name, color="lightgreen")
    while frontier:
        node = frontier.popleft()  # Used as a queue
        state_tuple = tuple(node.state)
        if state_tuple in problem.visited:
            continue
        problem.visited.add(state_tuple)
        if node.movie_name!=None:
            print(f"Popping {node.movie_name}")
        recommended_movie, cost, goal_node,similarity = problem.goal_test(node)
        if recommended_movie and cost and goal_node:
            net.show("html_files\\bfs_tree.html")  
            return recommended_movie, cost, goal_node, similarity
        for movie_index in range(len(problem.initial_state)):
            new_state = problem.actions(node.state, movie_index)
            child_name=None
            for name, vector in movies.items():
                if vector==new_state:
                    child_name=name
            child_node = Node.child(problem, node, new_state,child_name)
            frontier.append(child_node)
            parent_movie_name=node.movie_name
            if child_name==None and parent_movie_name!=None:
                net.add_node(str(child_node.state), label=str(child_node.state), color="lightblue")
                net.add_edge(parent_movie_name, str(child_node.state))
            elif parent_movie_name!=None and child_name!=None:
                net.add_node(child_name, label=child_name, color="lightblue")
                net.add_edge(parent_movie_name, child_name)
            elif parent_movie_name==None and child_name!=None:
                net.add_node(child_name, label=child_name, color="lightblue")
                net.add_edge(str(node.state), child_name)
            else:
                net.add_node(str(child_node.state), label=str(child_node.state), color="lightblue")
                net.add_edge(str(node.state), str(child_node.state))

    net.show("html_files\\bfs_tree.html")  # Visualize and save the tree as an HTML file
    return None

def run_bfs():
    breadth_first_tree_search(recommender, movie)

def bfs_time_calculation():
    number_of_times=5
    time_of_bfs = timeit.timeit(run_bfs, globals=globals(), number=number_of_times)
    bfs_average=time_of_bfs/number_of_times
    return bfs_average
def bfs_space_ans():
    return start_rss,end_rss

def bfs_space_calculation():
    process = psutil.Process(os.getpid())  
    memory_info = process.memory_info()
    rss = memory_info.rss / (1024 * 1024)  
    vms = memory_info.vms / (1024 * 1024)  
    return rss, vms

def bfs_comparison(movies_list):
    sum_similarity=0
    for movie in movies_list:
        initial_state = movies[movie]
        root= Node.root(initial_state,movie)
        recommender = MovieRecommender(root,initial_state, movie)
        _,_,_,similarity= breadth_first_tree_search(recommender,movie)
        sum_similarity+=similarity
    return sum_similarity/len(movies_list)

# movie='Incendies'
# movie = random.choice(list(movies.keys()))
# movie="Deep Rising"

movie='The Emperor\'s New Groove'
initial_state = movies[movie]
root= Node.root(initial_state,movie)
recommender = MovieRecommender(root,initial_state, movie)
print("Search has started...")

# Track memory usage before and after
start_rss, start_vms = bfs_space_calculation()
print(f"Memory usage before search: RSS = {start_rss:.2f} MB, VMS = {start_vms:.2f} MB")

start_time = time.time()
recommended_movie, cost, goal_node, similarity= breadth_first_tree_search(recommender,movie)
end_time = time.time()
run_time = end_time-start_time
end_rss, end_vms = bfs_space_calculation()
print(f"Memory usage after search: RSS = {end_rss:.2f} MB, VMS = {end_vms:.2f} MB")

run_time = end_time - start_time
print(f'Time taken by GBFS is {round(run_time, 2)} seconds')

rss_diff = end_rss - start_rss
vms_diff = end_vms - start_vms
print(f'Memory usage increased by: RSS = {rss_diff:.2f} MB, VMS = {vms_diff:.2f} MB')


if recommended_movie and cost:
    print("Recommended movie is", recommended_movie, 'and the cost is', cost)
    print("Path to goal:", " -> ".join(find_path_to_goal(goal_node)))

else:
    print("No similar preference found.")
print()

# webbrowser.open("html_files\\bfs_tree.html")

