import numpy as np
import json
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
from problem_modeling import MovieRecommender, Node, compute_similarity

with open('csvs_and_jsons/movie_vectors.json', 'r') as file:
    movies = json.load(file)

# def initialize_q_table(movie_vectors):
#     q_table = {}
#     for movie, vector in movie_vectors.items():
#         q_table[movie] = [0] * len(vector)  
#     return q_table

def toggle_bit(vector, index):
    vector[index] = 1 - vector[index]
    return vector

# alpha = 0.1  
# gamma = 0.9  # Discount factor
# epsilon = 0.1  # Exploration rate
# episodes = 1000 

# q_table = initialize_q_table(movies)

# for episode in range(episodes):
#     print(f"Starting Episode {episode + 1}/{episodes}")
#     current_movie = np.random.choice(list(movies.keys()))
#     current_vector = movies[current_movie].copy()

#     print(f"Initial movie: {current_movie}")
    
#     for step in range(10): 
#         print(f"  Step {step + 1}")
        
#         # Choose action (explore or exploit)
#         if np.random.rand() < epsilon:
#             action = np.random.randint(len(current_vector))  # Random action
#             print(f"    Exploring: Random action {action}")
#         else:
#             action = np.argmax(q_table[current_movie])  # Best known action
#             print(f"    Exploiting: Best action {action}")

#         next_vector = toggle_bit(current_vector.copy(), action)
#         print(f"    Current vector: {current_vector}")
#         print(f"    Next vector after action {action}: {next_vector}")

#         max_similarity = 0
#         recommended_movie = None
#         for movie, vector in movies.items():
#             similarity = compute_similarity(next_vector, vector)
#             if similarity > max_similarity and movie != current_movie:
#                 max_similarity = similarity
#                 recommended_movie = movie
        
#         print(f"    Recommended movie: {recommended_movie} with similarity {max_similarity}")

#         # Calculate reward
#         reward = max_similarity
#         print(f"    Reward: {reward}")

#         # Update Q-value
#         best_next_action = max(q_table[recommended_movie])
#         old_q_value = q_table[current_movie][action]
#         q_table[current_movie][action] += alpha * (
#             reward + gamma * best_next_action - old_q_value
#         )
#         print(f"    Updated Q-value for movie {current_movie}, action {action}: {q_table[current_movie][action]} (Old value: {old_q_value})")

#         # Transition to next state
#         current_movie = recommended_movie
#         current_vector = movies[current_movie].copy()
#         print(f"    Transitioning to new movie: {current_movie}")

#     print(f"Episode {episode + 1} completed\n")

# with open('csvs_and_jsons/q_table_trained.json', 'w') as file:
#     json.dump(q_table, file, indent=4)


# plt.figure(figsize=(10, 6))
# for movie, values in q_table.items():
#     plt.plot(values, label=f"Movie: {movie}")
# plt.title("Q-Values for Actions")
# plt.xlabel("Action (Bit Index)")
# plt.ylabel("Q-Value")
# plt.legend()
# plt.show()
