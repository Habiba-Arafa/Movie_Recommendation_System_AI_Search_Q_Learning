import json
import heapq
from ucs_problem_modeling import Node, MovieRecommender
import random
import time
from pyvis.network import Network
from problem_modeling import find_path_to_goal
import timeit
import psutil
import os

with open('csvs_and_jsons\\movie_vectors.json','r') as file:
    movies= json.load(file)
with open('csvs_and_jsons\\weighted_graph.json', 'r') as file:
    graph= json.load(file)

def uniform_cost_search(problem, original_movie):
    net = Network(notebook=True, height="600px", width="100%")  
    priority_queue = []
    heapq.heappush(priority_queue, [0, Node.root(problem.initial_state,original_movie), original_movie])
    net.add_node(original_movie, label=original_movie, color="lightgreen")
    while priority_queue:
        frontier_movies=[item[2] for item in priority_queue]
        print(f"Frontier currently has {frontier_movies}")
        cost, node, movie = heapq.heappop(priority_queue)
        cosine_similarity = MovieRecommender.compute_similarity(movies[movie], movies[original_movie])
        print("The next movie is:", movie,"with cosine similarity",round(cosine_similarity,2),"and the cost to get to this movie:", cost)
        print()
        print("----------------------------------------------------------------------------")
        state_tuple = tuple(node.state)
        if state_tuple in problem.visited and problem.visited[state_tuple] <= cost:
            continue
        problem.visited[state_tuple] = cost
        recommended_movie, cost, goal_node = problem.goal_test(node,original_movie,movie)
        if recommended_movie and cost and goal_node:
            net.show("html_files\\ucs_tree.html")  
            return recommended_movie, cost, goal_node
        for name, transition_cost in graph[movie].items():
            child_node = Node.child(node, movies[name], transition_cost, name)
            child_cost = child_node.path_cost
            net.add_node(name, label=name, color="lightblue")
            net.add_edge(child_node.parent.movie_name, name)
            heapq.heappush(priority_queue, [child_cost, child_node, name])
    net.show("html_files\\ucs_tree.html")  
    return None, None

def run_ucs():
    uniform_cost_search(recommender, start_movie)

def ucs_time_calculation():
    number_of_times=5
    time_of_ucs = timeit.timeit(run_ucs, globals=globals(), number=number_of_times)
    ucs_average=time_of_ucs/number_of_times
    return ucs_average
def ucs_space_calculation():
    process = psutil.Process(os.getpid())  
    memory_info = process.memory_info()
    rss = memory_info.rss / (1024 * 1024)  
    vms = memory_info.vms / (1024 * 1024)  
    return rss, vms

# start_movie = random.choice(list(graph.keys()))

start_movie='The Emperor\'s New Groove'
initial_state = movies[start_movie]
recommender= MovieRecommender(initial_state)

# Track memory usage before and after
start_rss, start_vms = ucs_space_calculation()
print(f"Memory usage before search: RSS = {start_rss:.2f} MB, VMS = {start_vms:.2f} MB")

start_time= time.time()
recommended, cost, goal_node = uniform_cost_search(recommender, start_movie)
end_time= time.time()
time_taken= end_time- start_time

end_rss, end_vms = ucs_space_calculation()
print(f"Memory usage after search: RSS = {end_rss:.2f} MB, VMS = {end_vms:.2f} MB")

run_time = end_time - start_time
print(f'Time taken by UCS is {round(run_time, 2)} seconds')

rss_diff = end_rss - start_rss
vms_diff = end_vms - start_vms
print(f'Memory usage increased by: RSS = {rss_diff:.2f} MB, VMS = {vms_diff:.2f} MB')


if recommended and cost:
    print("Best match for", start_movie, "is", recommended," with a path cost of", cost)
    print("Path to goal:", " -> ".join(find_path_to_goal(goal_node)))
else:
    print("No similar movies found")

print("Time taken for UCS algorithm", round(time_taken,2) ,"seconds")
def ucs_space_ans():
    return start_rss ,end_rss
