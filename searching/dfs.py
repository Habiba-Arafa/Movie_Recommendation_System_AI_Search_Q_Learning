from problem_modeling import MovieRecommender
import json
from problem_modeling import Node

with open('csvs_and_jsons\\random_users2.json', 'r') as file:
    data = json.load(file)


def depth_first_tree_search(problem):
    print("Starting depth-first search...")
    frontier = [Node.root(problem.initial_state)]  
    while frontier:
        node = frontier.pop() 
        state_tuple = tuple(node.state)
        print(f"Current state: {state_tuple}") 
        
        if state_tuple in problem.visited:
            print("State already visited, skipping...")
            continue
            
        problem.visited.add(state_tuple)
        recommended_movie = problem.goal_test(node.state)
        if recommended_movie:
            print("Found recommended movie:", recommended_movie)  
            return recommended_movie

        for movie_index in range(len(problem.initial_state)):
            new_state = problem.actions(node.state, movie_index)
            if new_state != node.state:  
                child_node = Node.child(problem, node, new_state)  
                frontier.append(child_node) 
                print(f"Added new state to frontier: {tuple(new_state)}")
            else:
                print(f"Action at index {movie_index} did not change the state.")

    print("No more states to explore.")
    return None



user_id = 'user1'
movie = 'Dying of the Light'
initial_state = data[user_id][movie]
recommender = MovieRecommender(initial_state, user_id, movie)
recommended_movie = depth_first_tree_search(recommender)

if recommended_movie:
    print("Recommended movie:", recommended_movie)
else:
    print("No similar preference found.")