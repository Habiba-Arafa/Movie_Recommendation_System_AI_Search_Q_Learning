from problem_modeling import MovieRecommender
import json
from problem_modeling import Node
from collections import deque
import time
from pyvis.network import Network

with open('csvs_and_jsons\\random_users_bigger.json', 'r') as file:
    data = json.load(file)

with open('csvs_and_jsons\\movie_vectors.json', 'r') as file:
    movies = json.load(file)

def breadth_first_tree_search(problem, movie):
    root= Node.root(problem.initial_state,movie)
    frontier = deque([root])
    net = Network(notebook=True, height="600px", width="100%")  
    net.add_node(root.movie_name, label=root.movie_name, color="lightgreen")
    while frontier:
        node = frontier.popleft()  # Used as a queue
        state_tuple = tuple(node.state)
        if state_tuple in problem.visited:
            continue
        problem.visited.add(state_tuple)
        if node.movie_name!=None:
            print(f"Popping {node.movie_name}")
        recommended_movie, cost = problem.goal_test(node)
        if recommended_movie and cost:
            net.show("bfs_tree.html")  
            return recommended_movie, cost
        for movie_index in range(len(problem.initial_state)):
            new_state = problem.actions(node.state, movie_index)
            child_name=None
            for name, vector in movies.items():
                if vector==new_state:
                    child_name=name
            child_node = Node.child(problem, node, new_state,child_name)
            frontier.append(child_node)
            parent_movie_name=node.movie_name
            if child_name==None and parent_movie_name!=None:
                net.add_node("no match", label="no match", color="lightblue")
                net.add_edge(parent_movie_name, "no match")
            elif parent_movie_name!=None:
                net.add_node(child_name, label=child_name, color="lightblue")
                net.add_edge(parent_movie_name, child_name)

    net.show("bfs_tree.html")  # Visualize and save the tree as an HTML file
    return None

user_id = 'user1'
movie ='Albert Nobbs'
initial_state = data[user_id][movie]
root= Node.root(initial_state,movie)
recommender = MovieRecommender(root,initial_state, user_id, movie)
print("Search has started...")
start_time = time.time()
recommended_movie, cost = breadth_first_tree_search(recommender,movie)
end_time = time.time()
run_time = end_time-start_time
if recommended_movie and cost:
    print("Recommended movie is", recommended_movie, 'and the cost is', cost)
else:
    print("No similar preference found.")
print()
print('Time taken by BFS is',round(run_time,2), "seconds")