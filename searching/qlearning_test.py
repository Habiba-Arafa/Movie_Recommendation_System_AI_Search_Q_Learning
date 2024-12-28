import numpy as np
import json
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
from problem_modeling import MovieRecommender, Node, compute_similarity
from qlearning import toggle_bit

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

    # Select best action from Q-Table
    action = np.argmax(q_table[current_movie])
    print(f"Best action for movie '{current_movie}': {action}")

    # Perform action 
    next_vector = toggle_bit(current_vector.copy(), action)
    print(f"Next vector after toggling: {next_vector}")

    # Find most similar movie
    max_similarity = 0
    recommended_movie = None
    for movie, vector in movies.items():
        similarity = compute_similarity(next_vector, vector)
        if similarity > max_similarity and movie != current_movie:
            max_similarity = similarity
            recommended_movie = movie

    print(f"Recommended movie: {recommended_movie} with similarity {max_similarity}")
    return recommended_movie

test_movie = "Avatar"  
recommended = recommend_movie(test_movie, q_table, movies)
print(f"\nRecommended movie for '{test_movie}': {recommended}")
