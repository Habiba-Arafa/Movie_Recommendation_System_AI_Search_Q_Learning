import json
import random
with open('F:/CSAI/3rd year/Fall/AI/AI_Project/csvs_and_jsons/weighted_graph.json', 'r') as file:
    weighted_graph = json.load(file)
def generate_random_connections(weighted_graph, min_connections=1, max_connections=3):
    random_graph = {}
    for movie, connections in weighted_graph.items():
        num_connections = random.randint(min_connections, max_connections)
        possible_children=list(connections.keys())
        selected_children= random.sample(possible_children, min(len(possible_children), num_connections))
        random_graph[movie]={child:connections[child] for child in selected_children}
    return random_graph

random_connections_graph = generate_random_connections(weighted_graph)
with open('random_connections_graph.json', 'w') as file:
    json.dump(random_connections_graph, file, indent=2)

