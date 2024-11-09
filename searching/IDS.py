from problem_modeling import MovieRecommender
import json

with open('csvs_and_jsons\\random_users2.json', 'r') as file:
    data = json.load(file)

def dls(problem, state, depth, visited):
    recommended_movie = problem.goal_test(state)
    if recommended_movie:
        return recommended_movie

    if depth == 0:
        return None

    for movie_index in range(len(problem.initial_state)):
        next_state = list(state)  
        new_state = problem.actions(next_state, movie_index)
        next_state_tuple = tuple(new_state)  

        if next_state_tuple not in visited:  
            visited.add(next_state_tuple)  
            result = dls(problem, new_state, depth - 1, visited)  # Use new_state for recursion
            if result:  
                return result
            visited.remove(next_state_tuple)  # Backtrack: unmark the state

    return None

def iddfs(problem, start_state):
    depth = 0
    while True:
        visited = set()  
        result = dls(problem, start_state, depth, visited)  
        if result:
            return result  
        depth += 1

user_id = 'user1'
movie = 'Dying of the Light'
initial_state = data[user_id][movie] 
recommender = MovieRecommender(initial_state, user_id, movie)

recommended_movie = iddfs(recommender, recommender.initial_state)
if recommended_movie:
    print("Recommended movie:", recommended_movie)
else:
    print("No similar preference found.")
