from problem_modeling import MovieRecommender
import json

with open('csvs_and_jsons\\random_users2.json', 'r') as file:
    data = json.load(file)













user_id = 'user1'
movie = 'Dying of the Light'
initial_state = data[user_id][movie] 
recommender = MovieRecommender(initial_state, user_id, movie)

recommended_movie = iddfs(recommender, recommender.initial_state)
if recommended_movie:
    print("Recommended movie:", recommended_movie)
else:
    print("No similar preference found.")
