import numpy as np
import json
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
from problem_modeling import MovieRecommender, Node, compute_similarity
from qlearning import toggle_bit
import timeit
import psutil
import os

with open('csvs_and_jsons/movie_vectors.json', 'r') as file:
    movies = json.load(file)

with open('csvs_and_jsons/q_table_trained.json', 'r') as file:
    q_table = json.load(file)

def recommend_movie(test_movie, q_table, movies):

    if test_movie not in movies:
        print(f"Movie '{test_movie}' not found in dataset!")
        return None
        
    current_vector = movies[test_movie].copy()
    current_movie = test_movie

    print(f"Starting with movie: {current_movie}")
    exploration_path = [current_movie]
    visited_movies = set()
    visited_movies.add(current_movie)
    for step in range(10): 
        action = np.argmax(q_table[current_movie])
        print(f"Best action for movie '{current_movie}': {action}")
        next_vector = toggle_bit(current_vector.copy(), action)
        print(f"Next vector after toggling: {next_vector}")

        max_similarity = 0
        recommended_movie = None
        for movie, vector in movies.items():
            similarity = compute_similarity(next_vector, vector)
            if similarity > max_similarity and movie != current_movie and movie not in visited_movies:
                max_similarity = similarity
                recommended_movie = movie

        print(f"Recommended movie: {recommended_movie} with similarity {max_similarity}")
        exploration_path.append(recommended_movie)
        visited_movies.add(recommended_movie)
        current_movie = recommended_movie
        current_vector = movies[current_movie].copy()

    return exploration_path, max_similarity

def qlearning_space_calculation():
    process = psutil.Process(os.getpid())  
    memory_info = process.memory_info()
    rss = memory_info.rss / (1024 * 1024)  
    vms = memory_info.vms / (1024 * 1024)  
    return rss, vms

def qlearning_comparison(movies_list):
    sum_similarities=0
    for movie in movies_list:
        _,similarity= recommend_movie(movie, q_table, movies)
        sum_similarities+=similarity
    return sum_similarities/len(movies_list)

start_rss, start_vms = qlearning_space_calculation()
print(f"Memory usage before search: RSS = {start_rss:.2f} MB, VMS = {start_vms:.2f} MB")

test_movie = "Mad Max 2"
exploration_path, similarity = recommend_movie(test_movie, q_table, movies)
print(f"\nExploration path for '{test_movie}': {exploration_path}, and the similarity {similarity}")

end_rss, end_vms = qlearning_space_calculation()
print(f"Memory usage after search: RSS = {end_rss:.2f} MB, VMS = {end_vms:.2f} MB")
