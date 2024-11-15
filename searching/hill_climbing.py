import random
import json

def hill_climbing_with_graph(graph, start_movie=None, max_iterations=1000):
  
    # take random movie if there is no started movie 
    if not start_movie:
        start_movie = random.choice(list(graph.keys()))
    
    # initialize current movie and score
    current_movie = start_movie
    current_score = 0 

    print(f"Starting Hill-Climbing from: {current_movie}")

    for iteration in range(max_iterations):

        neighbors = graph.get(current_movie, {})
        
       
       
        if not neighbors:
            print(f"No neighbors found for {current_movie}. Terminating.")
            break

       
        best_neighbor, best_score = max(neighbors.items(), key=lambda item: item[1])

        # if similarity not increase , stop and return the current state
        if best_score <= current_score:
            print(f"No better neighbor found. Ending at {current_movie} with score {current_score}.")
            return current_movie, current_score

        # go to best neighbor
        print(f"Moving to {best_neighbor} with score {best_score}")
        current_movie, current_score = best_neighbor, best_score

    return current_movie, current_score

if __name__ == "__main__":

    graph_path = "csvs_and_jsons//weighted_graph_smallerver.json"
    
    try:
        with open(graph_path, 'r') as file:
            weighted_graph = json.load(file)
    except FileNotFoundError:
        print(f"Error: File not found at {graph_path}")
        exit()

    start_movie = random.choice(list(weighted_graph.keys()))
    best_movie, best_score = hill_climbing_with_graph(weighted_graph, start_movie=start_movie)

    print(f"\nBest movie found: {best_movie} with a score of {best_score}")



    graph_path =  "csvs_and_jsons/custom_test_graph.json"
    
    try:
        with open(graph_path, 'r') as file:
            weighted_graph = json.load(file)
    except FileNotFoundError:
        print(f"Error: File not found at {graph_path}")
        exit()

    print("\n Test Case 1: Random Starting Movie ")
    start_movie = random.choice(list(weighted_graph.keys()))
    best_movie, best_score = hill_climbing_with_graph(weighted_graph, start_movie=start_movie)
    print(f"Result: {best_movie} with a score of {best_score}\n")

    print("\n Test Case 2: Iterating Through All Starting Movies")
    for start_movie in weighted_graph.keys():
        print(f"\nTesting from: {start_movie}")
        best_movie, best_score = hill_climbing_with_graph(weighted_graph, start_movie=start_movie)
        print(f"Result: {best_movie} with a score of {best_score}")

    # Test Case 3: Specific tests
    print("\n=== Test Case 3: Custom Scenarios ")

    #  Stop after moving to lesser similarity
    start_movie = "Avatar"
    print(f"\nTesting from {start_movie} (Lesser Similarity)")
    best_movie, best_score = hill_climbing_with_graph(weighted_graph, start_movie=start_movie)
    print(f"Result: {best_movie} with a score of {best_score}")

    #  Stop after finding equal similarity
    start_movie = "Inception"
    print(f"\nTesting from {start_movie} (Equal Similarity)")
    best_movie, best_score = hill_climbing_with_graph(weighted_graph, start_movie=start_movie)
    print(f"Result: {best_movie} with a score of {best_score}")
