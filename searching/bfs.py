from problem_modeling import MovieRecommender
import json
from problem_modeling import Node
from collections import deque
import time
from pyvis.network import Network


with open('csvs_and_jsons\\random_users.json', 'r') as file:
    data = json.load(file)

with open('csvs_and_jsons\\movie_vectors.json', 'r') as file:
    movies = json.load(file)


def breadth_first_tree_search(problem):
    frontier = deque([Node.root(problem.initial_state)])
    net = Network(notebook=True, height="600px", width="100%")  
    while frontier:
        node = frontier.popleft()  # Used as a queue
        state_tuple = tuple(node.state)
        if state_tuple in problem.visited:
            continue
        problem.visited.add(state_tuple)
        movie_name = ''
        for name, vector in movies.items():
            if vector == list(state_tuple):
                movie_name = name
                break
        net.add_node(str(state_tuple), label=movie_name, color="lightblue")
        if node.parent:
            parent_state = tuple(node.parent.state)
            net.add_node(str(parent_state), label=str(parent_state), color="lightgreen")
            net.add_edge(str(parent_state), str(state_tuple))
        recommended_movie, cost = problem.goal_test(node)
        if recommended_movie and cost:
            net.show("bfs_tree.html")  
            return recommended_movie, cost
        for movie_index in range(len(problem.initial_state)):
            new_state = problem.actions(node.state, movie_index)
            child_node = Node.child(problem, node, new_state)
            frontier.append(child_node)
    net.show("bfs_tree.html")  # Visualize and save the tree as an HTML file
    return None

user_id = 'user4'
movie = 'Ast\u00e9rix aux Jeux Olympiques'
initial_state = data[user_id][movie]
recommender = MovieRecommender(initial_state, user_id, movie)
print("Search has started...")
start_time= time.time()
recommended_movie, cost = breadth_first_tree_search(recommender)
end_time= time.time()
run_time= end_time-start_time
if recommended_movie and cost:
    print("Recommended movie is", recommended_movie, 'and the cost is', cost)
else:
    print("No similar preference found.")
print()
print('Time taken by BFS is',run_time)

