import random
import json

with open('csvs_and_jsons\\movie_vectors.json', 'r') as file:
    data = json.load(file)

def generate_random_users(num_users, movies, max_movies_per_user):
    users = {}
    for i in range(num_users):
        user_id = f'user{i + 1}'
        num_movies = random.randint(1, max_movies_per_user)
        selected_movies = random.sample(list(movies.items()), num_movies)
        users[user_id] = {movie: vector for movie, vector in selected_movies}
    return users

random_users = generate_random_users(num_users=6, movies=data, max_movies_per_user=6)
with open('csvs_and_jsons\\random_users.json', 'w') as json_file:
    json.dump(random_users, json_file, indent=4)