import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Step 1: Load the movie vectors from the JSON file
with open('csvs_and_jsons\\movie_vectors.json', 'r') as file:
    movie_vectors = json.load(file)

# Convert movie vectors to NumPy arrays for easier calculations
movie_array = {movie: np.array(vector) for movie, vector in movie_vectors.items()}

# Step 2: Calculate average cosine similarity for each movie
avg_cosine_similarity = {}

for movie_a in movie_array.keys():
    total_similarity = 0
    count = 0
    for movie_b in movie_array.keys():
        if movie_a != movie_b:
            # Calculate cosine similarity between movie_a and movie_b
            similarity = cosine_similarity(movie_array[movie_a].reshape(1, -1), movie_array[movie_b].reshape(1, -1))[0][0]
            total_similarity += similarity
            count += 1
    
    # Calculate average similarity
    avg_similarity = total_similarity / count if count > 0 else 0
    avg_cosine_similarity[movie_a] = avg_similarity

# Step 3: Update the movie_vectors dictionary to include average similarity
for movie in movie_vectors.keys():
    movie_vectors[movie].append(avg_cosine_similarity[movie])  # Append average similarity to the movie's vector

# Step 4: Save the updated movie vectors with average similarity back to a new JSON file
with open('csvs_and_jsons\\updated_movie_vectors.json', 'w') as file:
    json.dump(movie_vectors, file)

# Optional: Print updated movie vectors
print("Updated Movie Vectors with Average Similarity:")
for movie, vector in movie_vectors.items():
    print(f"{movie}: {vector}")
