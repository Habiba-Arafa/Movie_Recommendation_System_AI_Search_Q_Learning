from problem_modeling import compute_similarity
import json 
import random 
import time
import psutil
import os
with open('csvs_and_jsons\\movie_vectors.json', 'r') as file:
    data = json.load(file)

def temperature_schedule(iteration, initial_temp=1.0, decay_rate=0.99, min_temp=0):
    temp = initial_temp * (decay_rate ** iteration)
    return max(temp, min_temp)
    
def simulated_annealling(start_movie):
    current_similarity=0
    best_match_key=None
    i=0
    while temperature_schedule(i)>0.001:
        random_sel_movie= random.choice(list(data.keys()))
        next_similarity = compute_similarity(data[start_movie],data[random_sel_movie])
        delta = current_similarity-next_similarity
        if delta<0:
            current_similarity=next_similarity
            best_match_key=random_sel_movie
            print("Best of the neighbors is ", best_match_key, " with similarity ",current_similarity)
            print("--------------------------------------------------------------------------------------")
            print()
        else:
            random_number = random.random()
            if temperature_schedule(i) >= random_number:
                current_similarity=next_similarity
                best_match_key=random_sel_movie
                print("Accepting the suboptimal neighbor ", best_match_key, " with probability ", temperature_schedule(i),"and similarity of", current_similarity)
                print("--------------------------------------------------------------------------------------")
                print()
        i+=1
    return best_match_key, current_similarity

start_movie = random.choice(list(data.keys()))
print(f'Exploring recommendations for {start_movie}')
print()
initial_state = data[start_movie] 
start_time=time.time()
recommended_movie, similarity= simulated_annealling(start_movie)
end_time=time.time()
time_taken=end_time-start_time
print("Best match for",start_movie, "is", recommended_movie,"with a similarity of",similarity)
print("Simmulated annealing took", round(time_taken,2),"seconds")

