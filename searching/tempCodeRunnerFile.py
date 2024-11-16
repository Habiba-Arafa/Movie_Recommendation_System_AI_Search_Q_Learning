from problem_modeling import MovieRecommender
import json
from problem_modeling import Node
from pyvis.network import Network
import random
import time
import webbrowser

with open('csvs_and_jsons\\movie_vectors.json', 'r') as file:
    movies = json.load(file)


def find_movie_name_by_vector(vector, movies):
    """
    Finds the movie name based on the given vector.
    """
    for name, vec in movies.items():
        if vec == vector:
            return name
    return None  # Return None if no match is found


def depth_limited_search(problem, node, limit, net, parent_movie_name=None):
    """
    Perform a depth-limited version of DFS.
    """
    movie_name = find_movie_name_by_vector(node.state, movies) or str(node.state)

    print(f"Exploring {movie_name} at depth {limit}.")
    if limit == 0:
        print(f"Depth limit reached at {movie_name}.")
        return None, None  # Depth limit reached without finding a solution

    if tuple(node.state) in problem.visited:
        print(f"State already visited: {movie_name}")
        return None, None

    problem.visited.add(tuple(node.state))

    # Goal test
    recommended_movie, cost = problem.goal_test(node)
    if recommended_movie and cost:
        print(f"Goal found: {recommended_movie} with cost {cost}")
        return recommended_movie, cost

    # Explore children
    for movie_index in range(len(problem.initial_state)):
        new_state = problem.actions(node.state, movie_index)
        child_name = find_movie_name_by_vector(new_state, movies)
        child_node = Node.child(problem, node, new_state, child_name)

        # Add nodes and edges for visualization
        if parent_movie_name:
            if child_name:
                net.add_node(child_name, label=child_name, color="lightblue")
                net.add_edge(parent_movie_name, child_name)
            else:
                net.add_node(str(child_node.state), label=str(child_node.state), color="lightblue")
                net.add_edge(parent_movie_name, str(child_node.state))

        # Recursive call for depth-limited search
        result, cost = depth_limited_search(problem, child_node, limit - 1, net, child_name or str(child_node.state))
        if result and cost:
            return result, cost

    return None, None


def iterative_depth_first_search(problem, movie):
    """
    Perform Iterative Deepening Depth-First Search (IDDFS).
    """
    for depth in range(1, len(problem.initial_state) + 1):
        print(f"Starting depth-limited search with depth {depth}.")
        problem.visited.clear()  # Clear visited states for each depth
        net = Network(notebook=True, height="600px", width="100%")  # Visualization for the current depth
        net.add_node(movie, label=movie, color="lightgreen")  # Add root node
        root = Node.root(problem.initial_state, movie)
        result, cost = depth_limited_search(problem, root, depth, net, movie)
        if result and cost:
            net.show("html_files\\iddfs_tree.html")  # Show visualization
            return result, cost

    return None, None  # No solution found


# Initialize the problem and run IDDFS
movie = random.choice(list(movies.keys()))  # Random starting movie
initial_state = movies[movie]
root = Node.root(initial_state, movie)
recommender = MovieRecommender(root, initial_state, movie)

print("Search has started...")
start_time = time.time()
recommended_movie, cost = iterative_depth_first_search(recommender, movie)
end_time = time.time()
run_time = end_time - start_time

if recommended_movie and cost:
    print(f"Recommended movie is {recommended_movie} and the cost is {cost}")
else:
    print("No similar preference found.")

print()
print(f"Time taken by IDDFS is {round(run_time, 2)} seconds")
webbrowser.open("html_files\\iddfs_tree.html")
