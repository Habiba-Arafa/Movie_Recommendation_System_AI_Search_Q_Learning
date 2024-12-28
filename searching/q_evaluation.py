import numpy as np
import json
from sklearn.metrics.pairwise import cosine_similarity
from problem_modeling import MovieRecommender, Node, compute_similarity
from qlearning import toggle_bit




with open('csvs_and_jsons/movie_vectors.json', 'r') as file:
    movies = json.load(file)

with open('csvs_and_jsons/q_table_trained.json', 'r') as file:
    
    q_table = json.load(file)



# Performance evaluation
# def evaluate_agent(q_table, movies, test_cases):
#     total_reward = 0
#     for test_case in test_cases:
#         current_movie = test_case
#         current_vector = movies[current_movie].copy()
#         for _ in range(10): 
#             action = np.argmax(q_table[current_movie])  # Best action
#             next_vector = toggle_bit(current_vector.copy(), action)

#             max_similarity = 0
#             recommended_movie = None
#             for movie, vector in movies.items():
#                 similarity = compute_similarity(next_vector, vector)
#                 if similarity > max_similarity and movie != current_movie:
#                     max_similarity = similarity
#                     recommended_movie = movie

#             total_reward += max_similarity
#             current_movie = recommended_movie
#             current_vector = movies[current_movie].copy()
#     return total_reward / len(test_cases)

# # test cases
# test_cases = list(movies.keys())[:5]
# performance = evaluate_agent(q_table, movies, test_cases)
# print("Average reward across test cases:", performance)


def evaluate_agent(q_table, movies, test_cases, similarity_threshold=0.7):
 
    total_reward = 0
    true_positives = 0
    false_positives = 0
    false_negatives = 0

    for test_case in test_cases:
        current_movie = test_case
        current_vector = movies[current_movie].copy()

        print(f"\nEvaluating test case: {current_movie}")

        # Keep track of relevant movies (true matches)
        relevant_movies = [
            movie for movie, vector in movies.items()
            if compute_similarity(current_vector, vector) >= similarity_threshold and movie != current_movie
        ]
        print(f"Relevant movies: {relevant_movies}")

        for step in range(10):  
            print(f"  Step {step + 1}: Current movie: {current_movie}")

            # Select best action from Q-Table
            action = np.argmax(q_table[current_movie])
            next_vector = toggle_bit(current_vector.copy(), action)

            # Find most similar movie
            max_similarity = 0
            recommended_movie = None
            for movie, vector in movies.items():
                similarity = compute_similarity(next_vector, vector)
                if similarity > max_similarity and movie != current_movie:
                    max_similarity = similarity
                    recommended_movie = movie

            print(f"    Recommended movie: {recommended_movie} with similarity: {max_similarity}")

            # Collect reward
            total_reward += max_similarity

            # Evaluate recommendation
            if recommended_movie in relevant_movies:
                true_positives += 1
                print(f"    True Positive!")
            else:
                false_positives += 1
                print(f"    False Positive!")

            # Remove recommended movie from relevant list to avoid counting it again
            if recommended_movie in relevant_movies:
                relevant_movies.remove(recommended_movie)

            current_movie = recommended_movie
            current_vector = movies[current_movie].copy()

        # After all steps, remaining relevant movies are false negatives
        false_negatives += len(relevant_movies)

    # Calculate metrics
    avg_reward = total_reward / len(test_cases)
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0

    print(f"\nEvaluation complete!")
    print(f"Average Reward: {avg_reward}")
    print(f"Precision: {precision:.2%}")
    print(f"Recall: {recall:.2%}")

    return avg_reward, precision, recall

# Test cases
test_cases = list(movies.keys())[:20]
avg_reward, precision, recall = evaluate_agent(q_table, movies, test_cases)

print(f"\nEvaluation Results:")
print(f"Average Reward: {avg_reward}")
print(f"Precision: {precision:.2%}")
print(f"Recall: {recall:.2%}")
