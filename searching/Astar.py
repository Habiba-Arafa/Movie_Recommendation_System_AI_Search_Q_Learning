import heapq
import json
import random
from pyvis.network import Network
import time
import webbrowser
import timeit
import psutil
import os

with open('csvs_and_jsons\\movie_vectors.json', 'r') as file:
    movies = json.load(file)
with open('csvs_and_jsons\\random_connections_graph.json', 'r') as file:
    weighted_graph = json.load(file)

class AstarSearch:
    def __init__(self, movie):
        self.movie = movie  
        self.network = Network(height="800px", width="100%", notebook=True) 
        # Set up the network physics options
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
    def search(self):
        start_state = self.movie
        frontier = [(self.h(start_state), 0, start_state)]  # f(n)=h(n) + g(n)
        explored = set()  
        self.network.add_node(start_state, label=f"{start_state} (h(n)={self.h(start_state)})", color="lightblue")
        while frontier:
            _, path_cost, current_movie = heapq.heappop(frontier)  
            if current_movie in explored:  
                continue
            explored.add(current_movie)
            f_n = path_cost + self.h(current_movie)  
            if current_movie != self.movie and path_cost > 1:
                print(f"Recommended Movie: {current_movie}, Path Cost: {path_cost}")
                self.visualize_network() 
                return current_movie, path_cost 

            for neighbor, similarity in weighted_graph.get(current_movie, {}).items():
                if neighbor not in explored:
                    print(f"Adding to Frontier: {neighbor} with Similarity: {similarity}")
                    new_cost = path_cost + similarity
                    heapq.heappush(frontier, (self.h(neighbor) + new_cost, new_cost, neighbor))
                    if neighbor not in self.network.nodes:
                        self.network.add_node(neighbor, label=f"{neighbor}\n h(n)={self.h(neighbor)} g(n)={new_cost} f(n)={new_cost + self.h(neighbor)}", color="lightblue")
                    self.network.add_edge(current_movie, neighbor, value=similarity)

            print(f"Frontier: {[node[2] for node in frontier]}")
            print(f"Explored: {explored}")
            print('-------------------------------------------')

        return None, None 

    def h(self, movie):
        similarity = weighted_graph.get(self.movie, {}).get(movie, 0)
        if similarity>=0.9:
            return 0  
        return 1-similarity  

    def visualize_network(self):
        self.network.show("html_files\\astar_movie_recommendation.html")

def run_astar():
    AstarSearch(start_movie)

def astar_time_calculation():
    number_of_times=5
    time_of_astar = timeit.timeit(run_astar, globals=globals(), number=number_of_times)
    astar_average=time_of_astar/number_of_times
    return astar_average

# start_movie = random.choice(list(weighted_graph.keys()))
start_movie='The Emperor\'s New Groove'
print(f'Currently getting recommendations for {start_movie}\n')
def astar_space_calculation():
    process = psutil.Process(os.getpid())  
    memory_info = process.memory_info()
    rss = memory_info.rss / (1024 * 1024)  
    vms = memory_info.vms / (1024 * 1024)  
    return rss, vms

# Track memory usage before and after
start_rss, start_vms = astar_space_calculation()
print(f"Memory usage before search: RSS = {start_rss:.2f} MB, VMS = {start_vms:.2f} MB")

start_time = time.time()
AstarSearch= AstarSearch(start_movie)
recommended_movies = AstarSearch.search()
end_time = time.time()

end_rss, end_vms = astar_space_calculation()
print(f"Memory usage after search: RSS = {end_rss:.2f} MB, VMS = {end_vms:.2f} MB")

run_time = end_time - start_time
print(f'Time taken by GBFS is {round(run_time, 2)} seconds')

rss_diff = end_rss - start_rss
vms_diff = end_vms - start_vms
print(f'Memory usage increased by: RSS = {rss_diff:.2f} MB, VMS = {vms_diff:.2f} MB')
def astar_space_ans():
    return start_rss,end_rss
