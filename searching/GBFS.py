import heapq
import json
import random
from pyvis.network import Network
import webbrowser
import time
import timeit
import psutil
import os

with open('csvs_and_jsons\\movie_vectors.json', 'r') as file:
    movies = json.load(file)
with open('csvs_and_jsons/random_connections_graph.json', 'r') as file:
    weighted_graph = json.load(file)

class GreedyBFS:
    def __init__(self, movie):
        self.movie = movie  
        self.network = Network(height="800px", width="100%", notebook=True) 
        self.network.set_options(""" 
        var options = {
            "physics": {
                "enabled": true,
                "barnesHut": {
                    "gravitationalConstant": -20000,
                    "centralGravity": 0.3,
                    "springLength": 95,
                    "springConstant": 0.04
                },
                "minVelocity": 0.75
            }
        }
        """)
        self.recommendations = []  # To store all recommendations
        self.similairities=[]
    def search(self):
        start_state = self.movie
        print(f"Starting the search for movie: {start_state}")
        frontier=[(self.h(start_state), start_state)]   #h(n)
        explored=set()  
        all_nodes_added = set([start_state])
        self.network.add_node(start_state, label=f"{start_state} (h(n)={self.h(start_state)})", color="lightblue")
        print(f"Added start movie {start_state} to the network visualization.")
        while frontier and len(self.recommendations) < 5:  # the number of recommendations= 5
            print("\n---\nCurrent Frontier:", [node[1] for node in frontier])
            print("Explored Nodes:", explored)
            _, current_movie = heapq.heappop(frontier)
            print(f"Exploring movie: {current_movie} with heuristic h(n): {self.h(current_movie)}")
            if current_movie in explored:
                print(f"Movie {current_movie} already explored. Skipping.")
                continue

            explored.add(current_movie)
            if current_movie != self.movie and current_movie not in self.recommendations:
                print(f"Found a recommendation: {current_movie}")
                self.recommendations.append(current_movie)
                similarity = weighted_graph.get(self.movie, {}).get(current_movie, 1)
                self.similairities.append(similarity)
            print(f"Expanding neighbors of movie {current_movie}...")
            neighbors = weighted_graph.get(current_movie, {}).items()
            expanded_neighbors = 0  
            for neighbor, similarity in neighbors:
                print(f"Neighbor: {neighbor} with similarity: {similarity}")
                if neighbor not in explored and neighbor not in all_nodes_added:
                    print(f"Adding neighbor {neighbor} to the frontier with heuristic h(n): {self.h(neighbor)}")
                    heapq.heappush(frontier, (self.h(neighbor), neighbor)) 
                    if neighbor not in self.network.nodes:
                        self.network.add_node(neighbor, label=f"{neighbor} (h(n)={self.h(neighbor)})", color="lightblue")
                        all_nodes_added.add(neighbor)
                        print(f"Added{neighbor}to the network visualization.")
                    # Add the edge with similarity as the weight
                    self.network.add_edge(current_movie, neighbor, value=similarity)
                    expanded_neighbors+=1
                    print(f"Added edge from {current_movie} to {neighbor} with similarity value: {similarity}")
            print(f"Expanded {expanded_neighbors} neighbors for {current_movie}.")
            self.visualize_network()
        return self.recommendations, self.similairities

    def h(self, movie):
        similarity=weighted_graph.get(self.movie, {}).get(movie, 1)
        return 1-similarity  

    def visualize_network(self):
        self.network.show("html_files\\greedy_bfs_movie_recommendation.html")

def run_gbfs():
    GreedyBFS(start_movie)

def gbfs_time_calculation():
    number_of_times=5
    time_of_greedybfs = timeit.timeit(run_gbfs, globals=globals(), number=number_of_times)
    greedy_bfs_average=time_of_greedybfs/number_of_times
    return greedy_bfs_average

def gbfs_comparison():
    greedy_bfs = GreedyBFS(start_movie)
    _, similarities = greedy_bfs.search()
    return sum(similarities)/len(similarities)

# start_movie =random.choice(list(weighted_graph.keys()))
start_movie='The Emperor\'s New Groove'
print(f'\nStarting recommendation search for movie: {start_movie}\n')

def gbfs_space_calculation():
    process = psutil.Process(os.getpid())  
    memory_info = process.memory_info()
    rss = memory_info.rss / (1024 * 1024)  
    vms = memory_info.vms / (1024 * 1024)  
    return rss, vms

# Track memory usage before and after
start_rss, start_vms = gbfs_space_calculation()
print(f"Memory usage before search: RSS = {start_rss:.2f} MB, VMS = {start_vms:.2f} MB")

start_time = time.time()
greedy_bfs = GreedyBFS(start_movie)
recommended_movies = greedy_bfs.search()
end_time = time.time()

end_rss, end_vms = gbfs_space_calculation()
print(f"Memory usage after search: RSS = {end_rss:.2f} MB, VMS = {end_vms:.2f} MB")

run_time = end_time - start_time
print(f'Time taken by GBFS is {round(run_time, 2)} seconds')

rss_diff = end_rss - start_rss
vms_diff = end_vms - start_vms
print(f'Memory usage increased by: RSS = {rss_diff:.2f} MB, VMS = {vms_diff:.2f} MB')
def gbfs_space_ans():
    return start_rss,end_rss
