import json
from problem_modeling import MovieRecommender, Node, find_path_to_goal
from pyvis.network import Network
import random
import time
import timeit

with open('csvs_and_jsons\\movie_vectors.json', 'r') as file:
    movies = json.load(file)

def depth_first_tree_search(problem, movie):
    root = Node.root(problem.initial_state,movie)
    frontier = [root]  # Stack (LIFO)
    net = Network(notebook=True, height="600px", width="100%")
    net.add_node(root.movie_name, label=root.movie_name, color="lightgreen")
    while frontier:
        node = frontier.pop()  # Last-in, first-out (LIFO)
        state_tuple = tuple(node.state)
        if state_tuple in problem.visited:
            continue
        problem.visited.add(state_tuple)
        if node.movie_name!=None:
            print(f"Popping {node.movie_name}")
        recommended_movie, cost , goal_node= problem.goal_test(node)
        if recommended_movie and cost and goal_node:
            net.show("html_files\\dfs_tree.html")  
            return recommended_movie, cost, goal_node
        for movie_index in range(len(problem.initial_state)):
            new_state = problem.actions(node.state, movie_index)
            child_name=None
            for name, vector in movies.items():
                if vector==new_state:
                    child_name=name
            child_node = Node.child(problem, node, new_state,child_name)
            if tuple(child_node.state) not in problem.visited:
                frontier.append(child_node)
            parent_movie_name=node.movie_name
            if child_name==None and parent_movie_name!=None:
                net.add_node(str(child_node.state), label=str(child_node.state), color="lightblue")
                net.add_edge(parent_movie_name, str(child_node.state))
            elif parent_movie_name!=None and child_name!=None:
                net.add_node(child_name, label=child_name, color="lightblue")
                net.add_edge(parent_movie_name, child_name)
            elif parent_movie_name==None and child_name!=None:
                net.add_node(child_name, label=child_name, color="lightblue")
                net.add_edge(str(node.state), child_name)
            else:
                net.add_node(str(child_node.state), label=str(child_node.state), color="lightblue")
                net.add_edge(str(node.state), str(child_node.state))

    net.show("html_files\\dfs_tree.html")  # Visualize and save the tree as an HTML file
    return None, None

def run_dfs():
    depth_first_tree_search(recommender, movie)

def dfs_time_calculation():
    number_of_times=5
    time_of_dfs = timeit.timeit(run_dfs, globals=globals(), number=number_of_times)
    dfs_average=time_of_dfs/number_of_times
    return dfs_average

movie='The Emperor\'s New Groove'
initial_state = movies[movie]
root= Node.root(initial_state,movie)
recommender = MovieRecommender(root,initial_state, movie)
print("Search is starting...")
start_time=time.time()
recommended_movie, cost , node= depth_first_tree_search(recommender, movie)
end_time=time.time()
time_taken=end_time-start_time

if recommended_movie and cost:
    print("Recommended movie is", recommended_movie, 'and the cost is', cost)
    print("Path to goal:", " -> ".join(find_path_to_goal(node)))

else:
    print("No similar preference found.")
print("Time taken by the DFS algorithm", round(time_taken,2),"seconds")
=======
webbrowser.open("html_files\\dfs_tree.html")
>>>>>>> Stashed changes
