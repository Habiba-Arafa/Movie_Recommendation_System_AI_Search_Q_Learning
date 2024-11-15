import json
import heapq
from ucs_problem_modeling import Node, MovieRecommender
import random
import time
from pyvis.network import Network

with open('csvs_and_jsons\\movie_vectors.json','r') as file:
    movies= json.load(file)
with open('csvs_and_jsons\\weighted_graph.json', 'r') as file:
    graph= json.load(file)

def uniform_cost_search(problem, original_movie):
    net = Network(notebook=True, height="600px", width="100%")  
    priority_queue = []
    heapq.heappush(priority_queue, [0, Node.root(problem.initial_state,original_movie), original_movie])
    net.add_node(original_movie, label=original_movie, color="lightgreen")
    while priority_queue:
        cost, node, movie = heapq.heappop(priority_queue)
        cosine_similarity = MovieRecommender.compute_similarity(movies[movie], movies[original_movie])
        print("The next movie is:", movie,"with cosine similarity",round(cosine_similarity,2),"and the cost to get to this movie:", cost)
        print()
        print("----------------------------------------------------------------------------")
        state_tuple = tuple(node.state)
        if state_tuple in problem.visited and problem.visited[state_tuple] <= cost:
            continue
        problem.visited[state_tuple] = cost
        recommended_movie, cost = problem.goal_test(node,original_movie,movie)
        if recommended_movie and cost:
            net.show("ucs_tree.html")  
            return recommended_movie, cost
        for name, transition_cost in graph[movie].items():
            child_node = Node.child(node, movies[name], transition_cost, name)
            child_cost = child_node.path_cost
            net.add_node(name, label=name, color="lightblue")
            net.add_edge(child_node.parent.movie_name, name)
            heapq.heappush(priority_queue, [child_cost, child_node, name])
    net.show("ucs_tree.html")  
    return None, None


start_movie = random.choice(list(graph.keys()))
initial_state = movies[start_movie]
recommender= MovieRecommender(initial_state)
start_time= time.time()
recommended, cost = uniform_cost_search(recommender, start_movie)
end_time= time.time()
time_taken= end_time- start_time
if recommended and cost:
    print("Best match for", start_movie, "is", recommended," with a path cost of", cost)
else:
    print("No similar movies found")

print("Time taken for UCS algorithm", round(time_taken,2) ,"seconds")