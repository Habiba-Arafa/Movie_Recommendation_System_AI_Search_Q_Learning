import json
import heapq
from ucs_problem_modeling import Node, MovieRecommender
import random

with open('csvs_and_jsons\\movie_vectors.json','r') as file:
    movies= json.load(file)
with open('csvs_and_jsons\\weighted_graph.json', 'r') as file:
    graph= json.load(file)

priority_queue = []
def uniform_cost_search(problem, movie_name):
    heapq.heappush(priority_queue, [0, Node.root(problem.initial_state), movie_name])
    while priority_queue:
        cost, node, movie_name = heapq.heappop(priority_queue)
        print("The next movie is:",movie_name, "and the cost to get to this movie:", cost)
        state_tuple = tuple(node.state)
        if state_tuple in problem.visited and problem.visited[state_tuple] <= cost:
            continue
        problem.visited[state_tuple] = cost
        recommended_movie, cost = problem.goal_test(node,movie_name)
        if recommended_movie and cost:
            return recommended_movie, cost
        for name, transition_cost in graph[movie_name].items():
            if name not in problem.visited:
                child_node = Node.child(problem, node, movies[name], transition_cost)
                child_cost = child_node.path_cost
                heapq.heappush(priority_queue, [child_cost, child_node, name])
    return None, None

start_movie = random.choice(list(graph.keys()))
initial_state = movies[start_movie]
recommender= MovieRecommender(initial_state)
recommended, cost = uniform_cost_search(recommender, start_movie)
if recommended and cost:
    print("Best match for ", start_movie, " is ", recommended," with a path cost of: ", cost)
else:
    print("No similar movies found")