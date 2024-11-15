import heapq
import json
from Astar_problem_modeling import Node
import random
with open('csvs_and_jsons/random_connections_graph.json', 'r') as file:
    weighted_graph = json.load(file)

#Same as Astar, just return h(n) only instead of f(n)

class GreedyBestFirstSearch:
    def __init__(self, movie):
        self.movie = movie  
    
    def search(self):
        start_state = self.movie  
        start_node = Node.root(start_state)
        frontier = [(self.h(start_node), start_node)] 
        explored = set() 
        while frontier:
            _, node = heapq.heappop(frontier) 
            current_movie = node.state
            if current_movie in explored:
                continue
            explored.add(current_movie)
            if current_movie != self.movie and node.path_cost > 1:
                print(f"Expanding: {current_movie}, Path Cost: {node.path_cost}")
                return current_movie, node.path_cost
            
            for neighbor, similarity in weighted_graph.get(current_movie, {}).items():
                if neighbor not in explored:
                    print(f"Adding to Frontier: {neighbor} with Similarity: {similarity}")
                    print()
                    child_node = Node.child(node, neighbor)
                    heapq.heappush(frontier, (self.h(child_node), child_node))
            print(f"Frontier: {[node.state for _, node in frontier]}")
            print()
            print(f"Explored: {explored}")
            print('----------------------------------------------')
        return None, None 

    def h(self, node):
        current_movie = node.state
        similarity = weighted_graph.get(self.movie, {}).get(current_movie, 1)  
        difference = 1 - similarity  
        if difference <= 0.1: 
            return 0  
        else:
            return 4  

start_movie = random.choice(list(weighted_graph.keys()))
print(f'Currently getting recommendations for {start_movie}')
print()
gbfs = GreedyBestFirstSearch(start_movie)
recommended_movie, cost = gbfs.search()
if recommended_movie:
    print(f"Recommended Movie: {recommended_movie}, Cost: {cost}")
else:
    print("No recommendation found.")
