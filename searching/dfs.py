from problem_modeling import MovieRecommender
import json
from problem_modeling import Node

# with open('csvs_and_jsons\\random_users2.json', 'r') as file:
#     data = json.load(file)

# def depth_first_tree_search(problem):
#     print("print1")
#     frontier = [Node.root(problem.initial_state)]  # Use a list to simulate a stack
#     while frontier:
#         node = frontier.pop()  # Remove the last element (depth-first)
#         state_tuple = tuple(node.state)
#         print("print2")

#         if state_tuple in problem.visited:
#             continue
            
#         problem.visited.add(state_tuple)
#         recommended_movie = problem.goal_test(node.state)
#         if recommended_movie:
#             return recommended_movie
#             print("print3")


#         for movie_index in range(len(problem.initial_state)):
#             new_state = problem.actions(node.state, movie_index)
#             child_node = Node.child(problem, node, new_state)
#               # Pass new_state instead of movie_index
#             frontier.append(child_node)  # Add child to the stack
#         print("print4")

#     return None

# # Example usage
# user_id = 'user1'
# movie = 'Dying of the Light'
# initial_state = data[user_id][movie]
# recommender = MovieRecommender(initial_state, user_id, movie)
# recommended_movie = depth_first_tree_search(recommender)

# if recommended_movie:
#     print("Recommended movie:", recommended_movie)
# else:
#     print("No similar preference found.")

def depth_first_tree_search(problem):
    print("Starting depth-first search...")
    frontier = [Node.root(problem.initial_state)]  # Use a list to simulate a stack
    while frontier:
        node = frontier.pop()  # Remove the last element (depth-first)
        state_tuple = tuple(node.state)
        print(f"Current state: {state_tuple}")  # Log current state
        
        if state_tuple in problem.visited:
            print("State already visited, skipping...")
            continue
            
        problem.visited.add(state_tuple)
        recommended_movie = problem.goal_test(node.state)
        if recommended_movie:
            print("Found recommended movie:", recommended_movie)  # Log recommendation
            return recommended_movie

        for movie_index in range(len(problem.initial_state)):
            new_state = problem.actions(node.state, movie_index)
            if new_state != node.state:  # Check if the new state is different
                child_node = Node.child(problem, node, new_state)  # Pass new_state instead of movie_index
                frontier.append(child_node)  # Add child to the stack
                print(f"Added new state to frontier: {tuple(new_state)}")
            else:
                print(f"Action at index {movie_index} did not change the state.")

    print("No more states to explore.")
    return None
