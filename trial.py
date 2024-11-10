# Function to toggle the one-hot encoding
def toggle_encoding(encoding):
    return {key: 1 - value for key, value in encoding.items()}

# Function to calculate similarity between two profiles
def calculate_similarity(user_profile, other_user_profile):
    matches = 0
    total = 0

    # Check genres
    for key in user_profile["genre"]:
        if key in other_user_profile["genre"] and user_profile["genre"][key] == other_user_profile["genre"][key]:
            matches += 1
        total += 1  # Increment total for each genre checked

    # Check directors
    for key in user_profile["director"]:
        if key in other_user_profile["director"] and user_profile["director"][key] == other_user_profile["director"][key]:
            matches += 1
        total += 1  # Increment total for each director checked

    return (matches / total) * 100 if total > 0 else 0  # Avoid division by zero

# Function to recommend movies based on similarity between users
def recommend_movies(user1_profile, other_users_profiles, movies_data, similarity_threshold, user1_watched_movies, search_method='bfs'):
    recommendations = {}

    for user, user_profile in other_users_profiles.items():
        # Skip if comparing with itself
        if user_profile == user1_profile:
            continue

        # Calculate similarity between User1 and another user
        similarity_score = calculate_similarity(user1_profile, user_profile)

        if similarity_score >= similarity_threshold:
            # If similar, check which movies they have that User1 does not
            if search_method == 'bfs':
                recommendations.update(bfs(user_profile, movies_data, user1_profile, similarity_threshold, user1_watched_movies))
            elif search_method == 'dfs':
                recommendations.update(dfs(user_profile, movies_data, user1_profile, similarity_threshold, user1_watched_movies))

    return recommendations

def bfs(other_user_profile, movies_data, user1_profile, similarity_threshold, user1_watched_movies):
    recommendations = {}
    queue = list(movies_data.keys())  # Start with all movie titles

    while queue:
        movie_title = queue.pop(0)  # Dequeue the first movie
        if movie_title in user1_watched_movies:  # Check if User1 has watched this movie
            continue

        movie_profile = movies_data[movie_title]

        # Toggle the movie profile to find a new state
        temp_encoding = {
            "genre": toggle_encoding(movie_profile["genre"]),
            "director": toggle_encoding(movie_profile["director"])
        }

        # Calculate similarity score based on the toggled encoding
        toggle_similarity_score = calculate_similarity(user1_profile, temp_encoding)

        # If similarity with toggled profile is high, recommend this movie
        if toggle_similarity_score >= similarity_threshold:
            recommendations[movie_title] = other_user_profile  # Store recommended movie with the user who has it

    return recommendations

def dfs(other_user_profile, movies_data, user1_profile, similarity_threshold, user1_watched_movies):
    recommendations = {}
    
    def dfs_helper(movies_list):
        for movie_title in movies_list:
            if movie_title in user1_watched_movies:  # Check if User1 has watched this movie
                continue

            movie_profile = movies_data[movie_title]
            temp_encoding = {
                "genre": toggle_encoding(movie_profile["genre"]),
                "director": toggle_encoding(movie_profile["director"])
            }

            toggle_similarity_score = calculate_similarity(user1_profile, temp_encoding)

            if toggle_similarity_score >= similarity_threshold:
                recommendations[movie_title] = other_user_profile  # Store recommended movie with the user who has it

    # Start DFS traversal from the list of movie titles
    dfs_helper(list(movies_data.keys()))
    return recommendations

# User Profiles for other users
other_users_profiles = {
    "User2": {
        "genre": {"Sci-Fi": 1, "Action": 0, "Drama": 0},
        "director": {"Christopher Nolan": 1, "Steven Spielberg": 0, "Quentin Tarantino": 0}
    },
    "User3": {
        "genre": {"Drama": 1, "Crime": 0, "Action": 0},
        "director": {"Francis Ford Coppola": 1, "Christopher Nolan": 0, "Martin Scorsese": 0}
    },
    "User4": {
        "genre": {"Action": 1, "Drama": 0, "Sci-Fi": 0},
        "director": {"Christopher Nolan": 1, "Quentin Tarantino": 0, "Martin Scorsese": 0}
    },
    "User5": {
        "genre": {"Drama": 1, "Crime": 0, "Action": 0},
        "director": {"Quentin Tarantino": 1, "Christopher Nolan": 0, "Martin Scorsese": 0}
    }
}

# Movies Data
movies_data = {
    "Inception": {
        "genre": {"Sci-Fi": 1, "Action": 0, "Drama": 0},
        "director": {"Christopher Nolan": 1, "Steven Spielberg": 0, "Quentin Tarantino": 0}
    },
    "The Godfather": {
        "genre": {"Drama": 1, "Crime": 0, "Action": 0},
        "director": {"Francis Ford Coppola": 1, "Christopher Nolan": 0, "Martin Scorsese": 0}
    },
    "The Dark Knight": {
        "genre": {"Action": 1, "Drama": 0, "Sci-Fi": 0},
        "director": {"Christopher Nolan": 1, "Quentin Tarantino": 0, "Martin Scorsese": 0}
    },
    "Pulp Fiction": {
        "genre": {"Drama": 1, "Crime": 0, "Action": 0},
        "director": {"Quentin Tarantino": 1, "Christopher Nolan": 0, "Martin Scorsese": 0}
    },
    "Avatar": {
        "genre": {"Sci-Fi": 1, "Action": 0, "Drama": 0},
        "director": {"James Cameron": 1, "Christopher Nolan": 0, "Quentin Tarantino": 0}
    }
}

# User1 Profile
user1_profile = {
    "genre": {"Sci-Fi": 1, "Action": 0, "Drama": 0},
    "director": {"Christopher Nolan": 1, "Steven Spielberg": 0, "Quentin Tarantino": 0}
}

# List of movies watched by User1
user1_watched_movies = ["Inception", "Avatar"]  # Example list

# Define the similarity threshold
similarity_threshold = 50

# Get recommendations for User1 from other users using BFS
recommendations_bfs = recommend_movies(user1_profile, other_users_profiles, movies_data, similarity_threshold, user1_watched_movies, search_method='bfs')
print("BFS Recommended Movies for User1:")
for movie, user in recommendations_bfs.items():
    print(f"{movie} from {user}")

# Get recommendations for User1 from other users using DFS
recommendations_dfs = recommend_movies(user1_profile, other_users_profiles, movies_data, similarity_threshold, user1_watched_movies, search_method='dfs')
print("\nDFS Recommended Movies for User1:")
for movie, user in recommendations_dfs.items():
    print(f"{movie} from {user}")
