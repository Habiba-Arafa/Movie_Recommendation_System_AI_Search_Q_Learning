import json
from pyvis.network import Network
from IDS_problem_modeling import MovieRecommender, Node

# Load user data from JSON
with open('csvs_and_jsons\\random_users.json', 'r') as file:
    data = json.load(file)

# Function to visualize the search tree using pyvis
def visualize_tree(net):
    # Save and display the interactive visualization
    net.show("search_tree.html")
    print("Visualization saved as search_tree.html")

# Depth-Limited Search (DLS)
def dls(problem, node, depth, visited, net):
    print(f"Depth {depth}: Current Movie: {node.movie_name}")

    goal, cost = problem.goal_test(node)
    if goal:
        return goal, cost, node
    if depth == 0:
        return None, None, None

    # Add the node to the graph with edges if it has a parent
    if node.parent:
        net.add_edge(node.parent.movie_name, node.movie_name, title=node.action)
        print(f"Added edge from {node.parent.movie_name} to {node.movie_name} with action {node.action}")

    # Add node to the network for visualization
    net.add_node(node.movie_name, title=node.movie_name)
    print(f"Added node: {node.movie_name}")

    # For each possible action, explore the next state
    for action_index in range(len(problem.initial_state)):
        new_state = problem.actions(node.state, action_index)
        movie_name = problem.get_movie_name_for_state(new_state)
        print(f"Generated new state: {new_state} -> {movie_name}")

        child_node = Node.child(problem, node, new_state, movie_name)

        # Check if child node has been created correctly
        print(f"Created child node: {child_node.movie_name} with state: {child_node.state}")

        state_tuple = tuple(child_node.state)
        if state_tuple not in visited:
            visited.add(state_tuple)
            result = dls(problem, child_node, depth - 1, visited, net)
            if result[0]:  # If goal is found, return it
                return result
            visited.remove(state_tuple)

    return None, None, None

# Iterative Deepening Depth-First Search (IDDFS)
def iddfs(problem, start_state):
    depth = 0
    net = Network(notebook=True, height="600px", width="100%")  # Initialize PyVis Network
    
    while True:
        visited = set()
        start_node = Node.root(start_state, problem.movie)
        print(f"Starting Iteration {depth}...")  
        
        result = dls(problem, start_node, depth, visited, net)
        
        # Visualize after each depth iteration (only after depth 1 and greater)
        if depth > 0:  # Avoid plotting for depth 0 as it would be too early
            visualize_tree(net)
        
        if result[0]:  
            return result
        depth += 1

# Define the initial state and recommender
user_id = 'user1'
movie = 'The Five-Year Engagement'
initial_state = data[user_id][movie]
recommender = MovieRecommender(initial_state, user_id, movie)

# Run IDDFS and print the result
recommended_movie = iddfs(recommender, recommender.initial_state)
if recommended_movie:
    print(f"Recommended movie: {recommended_movie[0]}")  
    print("Total cost:", recommended_movie[1])  
else:
    print("No similar preference found.")
