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



# Performance evaluation
def evaluate_agent(q_table, movies, test_cases):
    total_reward = 0
    for test_case in test_cases:
        current_movie = test_case
        current_vector = movies[current_movie].copy()
        for _ in range(10): 
            action = np.argmax(q_table[current_movie])  # Best action
            next_vector = toggle_bit(current_vector.copy(), action)

            max_similarity = 0
            recommended_movie = None
            for movie, vector in movies.items():
                similarity = compute_similarity(next_vector, vector)
                if similarity > max_similarity and movie != current_movie:
                    max_similarity = similarity
                    recommended_movie = movie

            total_reward += max_similarity
            current_movie = recommended_movie
            current_vector = movies[current_movie].copy()
    return total_reward / len(test_cases)

# test cases
test_cases = list(movies.keys())[:5]
performance = evaluate_agent(q_table, movies, test_cases)
print("Average reward across test cases:", performance)



