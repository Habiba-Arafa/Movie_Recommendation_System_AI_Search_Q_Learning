import json
from problem_modeling import MovieRecommender, Node
from pyvis.network import Network

with open('csvs_and_jsons\\random_users.json', 'r') as file:
    data = json.load(file)

def depth_first_tree_search(problem):
    frontier = [Node.root(problem.initial_state)]  # Stack (LIFO)
    net = Network(notebook=True, height="600px", width="100%")  
    while frontier:
        node = frontier.pop()  # Last-in, first-out (LIFO)
        state_tuple = tuple(node.state)
        if state_tuple in problem.visited:
            continue
        problem.visited.add(state_tuple)
        net.add_node(str(state_tuple), label=str(state_tuple), color="lightblue")

        if node.parent:
            parent_state = tuple(node.parent.state)
            # Add parent node and edge to the graph
            net.add_node(str(parent_state), label=str(parent_state), color="lightgreen")
            net.add_edge(str(parent_state), str(state_tuple))
        recommended_movie, cost = problem.goal_test(node)
        if recommended_movie and cost:
            net.show("dfs_tree.html")  
            return recommended_movie, cost
        for movie_index in range(len(problem.initial_state)):
            new_state = problem.actions(node.state, movie_index)
            child_node = Node.child(problem, node, new_state)
            if tuple(child_node.state) not in problem.visited:
                frontier.append(child_node)
    net.show("dfs_tree.html")  # Visualize and save the tree as an HTML file
    return None, None

user_id = 'user4'
movie = 'Ast\u00e9rix aux Jeux Olympiques'
initial_state = data[user_id][movie]
recommender = MovieRecommender(initial_state, user_id, movie)
print("Search is starting...")
recommended_movie, cost = depth_first_tree_search(recommender)
if recommended_movie and cost:
    print("Recommended movie:", recommended_movie, 'and the cost to get to that movie from the initial state is:', cost)
else:
    print("No similar preference found.")





