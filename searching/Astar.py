import heapq
import json
from Astar_problem_modeling import Node
import random

with open('csvs_and_jsons\\movie_vectors.json','r') as file:
    movies= json.load(file)

with open('csvs_and_jsons/random_connections_graph.json', 'r') as file:
    weighted_graph = json.load(file)

class AstarSearch:
    def __init__(self, movie):
        self.movie = movie  
    def search(self):
        start_state = self.movie  
        start_node = Node.root(start_state)
        frontier = [(self.h(start_node) + start_node.path_cost, start_node.path_cost, start_node)]  # Priority queue with f(n)
        explored = set()  

        while frontier:
            _, path_cost, node = heapq.heappop(frontier) 
            current_movie = node.state
            if current_movie in explored:
                continue
            explored.add(current_movie)
            if current_movie!=self.movie and path_cost>1:
                print(f"Expanding: {current_movie},Path Cost:{path_cost}")
                return current_movie, path_cost
            for neighbor, similarity in weighted_graph.get(current_movie,{}).items():
                if neighbor not in explored:
                    print(f"Adding to Frontier:{neighbor} with Similarity:{similarity}")
                    print()
                    child_node = Node.child(node, neighbor)  
                    heapq.heappush(frontier, (child_node.path_cost+self.h(child_node), child_node.path_cost, child_node))
            print(f"Frontier:{[node.state for _, _, node in frontier]}")
            print()
            print(f"Explored:{explored}")
            print('-------------------------------------------')

        return None, None 

    def h(self, node):
        current_movie=node.state
        similarity=weighted_graph.get(self.movie, {}).get(current_movie, 1)  
        difference= 1- similarity 
        if difference<= 0.1: 
            return 0  
        else:
            return 4  #just a high h(n) to make sure that we will not choose this branch


start_movie = random.choice(list(weighted_graph.keys()))
print(f'Currently getting recommendations for {start_movie}')
print()
astar_search = AstarSearch(start_movie)
recommended_movie, cost=astar_search.search()
if recommended_movie:
    print(f"Recommended Movie:{recommended_movie}, Cost: {cost}")
else:
    print("No recommendation found.")
