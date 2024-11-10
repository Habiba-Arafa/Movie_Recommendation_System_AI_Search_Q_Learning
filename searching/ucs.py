from problem_modeling import MovieRecommender
import json
import heapq
from problem_modeling import Node

with open('csvs_and_jsons\\random_users.json', 'r') as file:
    users = json.load(file)
with open('csvs_and_jsons\\movie_vectors2.json','r') as file:
    movies= json.load(file)
with open('csvs_and_jsons\\weighted_graph.json', 'r') as file:
    graph = json.load(file)

priority_queue = []
def uniform_cost_search(problem,movie_name):
    visited = {}
    heapq.heappush(priority_queue, [0, Node.root(problem.initial_state),movie_name])
    while priority_queue:
        cost, node ,movie_name= heapq.heappop(priority_queue)
        state_tuple = tuple(node.state)
        if state_tuple in visited and visited[state_tuple]<=cost:
            continue
        visited[state_tuple]=cost
        recommended_movie = problem.goal_test(node.state)
        if recommended_movie:
            return recommended_movie
        for name,cost in graph[movie_name].items():
            total_cost = node.path_cost + cost
            child_node = Node.child(problem, node, movies[name])
            heapq.heappush(priority_queue, [total_cost, child_node ,name])
    return None

user_id  = 'user1'
movie ='A Christmas Carol'
initial_state = users[user_id][movie] 
recommender = MovieRecommender(initial_state, user_id,movie)
recommended_movie = uniform_cost_search(recommender,movie)
if recommended_movie:
    print("Recommended movie:", recommended_movie)
else:
    print("No similar preference found.")