from problem_modeling import MovieRecommender
import json
from problem_modeling import Node
from collections import deque
import heapq

with open('csvs_and_jsons\\weighted_graph.json', 'r') as file:
    graph = json.load(file)

with open('csvs_and_jsons\\random_users.json', 'r') as file:
    users = json.load(file)

priority_queue=[]
def uniform_cost_search(problem):
    visited={}
    heapq.heappush(priority_queue, [0,Node.root(problem.initial_state)])
    while heapq:
        cost,node = heapq.heappop(priority_queue)
        state_tuple= tuple(node.state)
        if state_tuple in visited and visited[state_tuple]<node[0]:
            continue
        recommended_movie= problem.goal_test(node.state)
        if recommended_movie:
            return recommended_movie
        for movie_index in range(len(problem.initial_state)):
            new_state= problem.actions(node.state, movie_index)
            child_node= Node.child(problem, node, new_state)
            heapq.heappush(priority_queue,[data[],child_node])
        
user_id  = 'user1'
movie ='Swept Away'
initial_state = users[user_id][movie] 
recommender = MovieRecommender(initial_state, user_id,movie)
recommended_movie = uniform_cost_search(recommender)
if recommended_movie:
    print("Recommended movie:", recommended_movie)
else:
    print("No similar preference found.")
