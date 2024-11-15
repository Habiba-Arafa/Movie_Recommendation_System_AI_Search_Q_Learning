import random
import json
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

with open('csvs_and_jsons\\movie_vectors.json', 'r') as file:
    data = json.load(file)

def compute_similarity(vector1, vector2):
        vector1 = np.array(vector1).reshape(1, -1)
        vector2 = np.array(vector2).reshape(1, -1)
        similarity = cosine_similarity(vector1, vector2)
        return similarity[0][0]

def generate_random_users(movies):
    graph = {}
    random.seed(None)  
    for key, value in movies.items():
        dictionary={}
        random_number = random.randint(1, 4)
        selected_movies = random.sample(list(movies), min(random_number, len(movies)))
        for movie in selected_movies:
            dictionary[movie]= 1-compute_similarity(value, data[movie])
        graph[key] = dictionary
    return graph

graph = generate_random_users(data)
with open('csvs_and_jsons\\weighted_graph.json', 'w') as json_file:
    json.dump(graph, json_file, indent=4)