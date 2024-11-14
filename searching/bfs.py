import networkx as nx
import matplotlib.pyplot as plt
from problem_modeling import MovieRecommender
import json
from problem_modeling import Node
from collections import deque

with open('csvs_and_jsons\\random_users.json', 'r') as file:
    data = json.load(file)

def breadth_first_tree_search(problem):
    frontier = deque([Node.root(problem.initial_state)])
    tree_graph = nx.DiGraph()  # Directed graph to represent the tree structure
    while frontier:
        node = frontier.popleft()  # Used as a queue
        state_tuple = tuple(node.state)
        if state_tuple in problem.visited:
            continue
        problem.visited.add(state_tuple)
        if node.parent:
            tree_graph.add_edge(tuple(node.parent.state), state_tuple)
        recommended_movie, cost = problem.goal_test(node)
        if recommended_movie and cost:
            visualize_tree(tree_graph)  # Visualize the tree once a goal is found
            return recommended_movie, cost
        for movie_index in range(len(problem.initial_state)):
            new_state = problem.actions(node.state, movie_index)
            child_node = Node.child(problem, node, new_state)
            frontier.append(child_node)
    visualize_tree(tree_graph)  # Visualize the tree if no goal is found
    return None

def visualize_tree(tree_graph):
    pos = nx.spring_layout(tree_graph)
    nx.draw(tree_graph, pos, with_labels=True, node_color='lightgreen', edge_color='blue', font_size=10, node_size=1500)
    plt.title("Tree Visualization of BFS Traversal")
    plt.show()

# Main code
user_id = 'user4'
movie = 'Ast\u00e9rix aux Jeux Olympiques'
initial_state = data[user_id][movie]
recommender = MovieRecommender(initial_state, user_id, movie)
print("search is starting...")
recommended_movie, cost = breadth_first_tree_search(recommender)

if recommended_movie and cost:
    print("Recommended movie:", recommended_movie, 'and the cost to get to that movie from the initial state is:', cost)
else:
    print("No similar preference found.")
