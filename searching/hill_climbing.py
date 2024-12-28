import random
import json
import cProfile

def hill_climbing_with_graph(graph, start_movie=None, max_iterations=1000):
    if not start_movie:
        start_movie = random.choice(list(graph.keys()))
    
   
    current_movie = start_movie
    current_score = 0
    explored_path = []  
    returned_path = [current_movie] 

    print(f"Starting Hill-Climbing from: {start_movie}")

    for iteration in range(max_iterations):
        neighbors = graph.get(current_movie, {})
        explored_path.append(current_movie) 

        if not neighbors:
            print(f"No neighbors found for {current_movie}. Terminating.")
            break

        # get  best neighbor
        best_neighbor, best_score = max(neighbors.items(), key=lambda item: item[1])

        # if similarity not increase stop and return current state
        if best_score <= current_score:
            print(f"No better neighbor found. Ending at {current_movie} with score {current_score}.")
            return explored_path, returned_path, current_movie, current_score

        print(f"Moving to {best_neighbor} with score {best_score}")
        current_movie, current_score = best_neighbor, best_score
        returned_path.append(current_movie) 

    return explored_path, returned_path, current_movie, current_score

if __name__ == "__main__":

    graph_path = "csvs_and_jsons//weighted_graph.json"
    
    try:
        with open(graph_path, 'r') as file:
            weighted_graph = json.load(file)
    except FileNotFoundError:
        print(f"Error: File not found at {graph_path}")
        exit()




    
    def run():
       
        start_movie = random.choice(list(weighted_graph.keys()))
        explored_path, returned_path, best_movie, best_score = hill_climbing_with_graph(
            weighted_graph, start_movie=start_movie
        )

        print("\n=== Results ===")
        print(f"Explored Path: {' -> '.join(explored_path)}") 
        print(f"Returned Path: {' -> '.join(returned_path)}") 
        print(f"Returned Movie: {best_movie}")  
        print(f"Score of Returned Movie: {best_score}") 
    print("\n=== Profiling Hill Climbing ===")
    cProfile.run("run()")




    graph_path =  "csvs_and_jsons/custom_test_graph.json"
    
    try:
        with open(graph_path, 'r') as file:
            weighted_graph = json.load(file)
    except FileNotFoundError:
        print(f"Error: File not found at {graph_path}")
        exit()

    print("\n Test Case 1: Random Starting Movie ")

    def run2():
       
        start_movie = random.choice(list(weighted_graph.keys()))
        explored_path, returned_path, best_movie, best_score = hill_climbing_with_graph(
            weighted_graph, start_movie=start_movie)


        print("\n=== Results ===")
        print(f"Explored Path: {' -> '.join(explored_path)}") 
        print(f"Returned Path: {' -> '.join(returned_path)}") 
        print(f"Returned Movie: {best_movie}")  
        print(f"Score of Returned Movie: {best_score}")
        return best_movie 

    print("\n=== Profiling Hill Climbing ===")
    cProfile.run("run2()")


    





    print("\n Test Case 2: Iterating Through All Starting Movies")
    def run3():

        for start_movie in weighted_graph.keys():
            print(f"\nTesting from: {start_movie}")
            explored_path, returned_path, best_movie, best_score = hill_climbing_with_graph(
            weighted_graph, start_movie=start_movie)


        print("\n=== Results ===")
        print(f"Explored Path: {' -> '.join(explored_path)}") 
        print(f"Returned Path: {' -> '.join(returned_path)}") 
        print(f"Returned Movie: {best_movie}")  
        print(f"Score of Returned Movie: {best_score}")

        

    print("\n=== Profiling Hill Climbing ===")
    cProfile.run("run3()")  

    # Test Case 3: Specific tests
    print("\n=== Test Case 3: Custom Scenarios ")

    #  Stop after moving to lesser similarity

    def run4():
        start_movie = "Avatar"
        print(f"\nTesting from {start_movie} (Lesser Similarity)")
        explored_path, returned_path, best_movie, best_score = hill_climbing_with_graph(
            weighted_graph, start_movie=start_movie)


        print("\n=== Results ===")
        print(f"Explored Path: {' -> '.join(explored_path)}") 
        print(f"Returned Path: {' -> '.join(returned_path)}") 
        print(f"Returned Movie: {best_movie}")  
        print(f"Score of Returned Movie: {best_score}")

        

    print("\n=== Profiling Hill Climbing ===")
    cProfile.run("run4()")



        #  Stop after finding equal similarity
    start_movie = "Inception"
    print(f"\nTesting from {start_movie} (Equal Similarity)")
    best_movie, best_score = hill_climbing_with_graph(weighted_graph, start_movie=start_movie)
    print(f"Result: {best_movie} with a score of {best_score}")


    
    def run5():
        start_movie = "Inception"
        print(f"\nTesting from {start_movie} (Equal Similarity)")
        explored_path, returned_path, best_movie, best_score = hill_climbing_with_graph(
            weighted_graph, start_movie=start_movie)


        print("\n=== Results ===")
        print(f"Explored Path: {' -> '.join(explored_path)}") 
        print(f"Returned Path: {' -> '.join(returned_path)}") 
        print(f"Returned Movie: {best_movie}")  
        print(f"Score of Returned Movie: {best_score}")

    print("\n=== Profiling Hill Climbing ===")
    cProfile.run("run5()")
