import numpy as np
import json
from sklearn.metrics.pairwise import cosine_similarity

with open('csvs_and_jsons/movie_vectors.json', 'r') as file:
    movie_vectors = json.load(file)

with open('csvs_and_jsons/random_user_genetics.json', 'r') as file:
    random_users = json.load(file)

movie_list = list(movie_vectors.keys())

def clean_movie_names(movie_list):
    cleaned_movies = []  
    for movie in movie_list:  
        cleaned_movie = movie.strip() 
        cleaned_movie = cleaned_movie.lower() 
        cleaned_movies.append(cleaned_movie)  
    return cleaned_movies  

cleaned_user_preferences = {}

for user_id, user_preferences in random_users.items():
    cleaned_movies = {}
    for movie, vector in user_preferences.items():
        cleaned_movie = clean_movie_names([movie])[0]
        cleaned_movies[cleaned_movie] = vector
    cleaned_user_preferences[user_id] = cleaned_movies


# initialize population randomly from the movies vector
def init_pop_randomly(pop_size, num_movies):
    population = [] 
    for individual in range(pop_size):
        recommended_movies = np.random.choice(movie_list, size=num_movies, replace=False)
        population.append(recommended_movies)

    return np.array(population)


# using cosine similarity to get fitness values for each individual in population 
def calc_fitness_similarity(population, user_id, similarity_threshold=0.8):
    fitness_vals = []
    
    user_preferences = cleaned_user_preferences[user_id]
    user_preference_vectors = list(user_preferences.values()) 
    
    for recommendation in population:
        fitness_score = 0
        matched_movies = set()  # To avoid double counting when add 1 for movie matches
        
        for movie in recommendation:
           
            recommended_vector = movie_vectors[movie]
            
            # Compare recommended movie with all user movies
            for movie_index, pref_vector in enumerate(user_preference_vectors):
                if movie_index in matched_movies:
                    continue  # skip if it already in matched
                
                similarity = cosine_similarity([recommended_vector], [pref_vector])[0][0]
                
                if similarity >= similarity_threshold:
                    fitness_score += 1
                    matched_movies.add(movie_index)  
                    break  
        
       
        fitness_vals.append(fitness_score / len(recommendation))  # normalize by number of recommended movies
    
    return fitness_vals

def selection(population, fitness_vals):
    probs = np.array(fitness_vals) / np.sum(fitness_vals)
    selected_indices = np.random.choice(np.arange(len(population)), size=len(population), p=probs)
    return population[selected_indices]

# combine two parent individuals and produce two individuals
def crossover(parent1, parent2, pc=0.7):
    if np.random.random() < pc:
        m = np.random.randint(1, len(parent1))  # Random crossover point
        child1 = np.concatenate([parent1[:m], parent2[m:]])
        child2 = np.concatenate([parent2[:m], parent1[m:]])
    else:
        child1, child2 = parent1.copy(), parent2.copy()
    return child1, child2

# make random changes in individual
def mutation(individual, mutation_rate=0.1):
    for i in range(len(individual)):
        if np.random.random() < mutation_rate:
            random_movie = np.random.choice(movie_list)
            individual[i] = random_movie
    return individual

# evolve population and merge selection crossover and mutation
def evolve_population(population, fitness_vals, crossover_prob=0.7, mutation_rate=0.1):
    selected_population = selection(population, fitness_vals)
    new_population = []
    
    for i in range(0, len(selected_population), 2):
        parent1 = selected_population[i]
        parent2 = selected_population[i + 1] if i + 1 < len(selected_population) else selected_population[i]
        child1, child2 = crossover(parent1, parent2, crossover_prob)
        child1 = mutation(child1, mutation_rate)
        child2 = mutation(child2, mutation_rate)
        new_population.append(child1)
        new_population.append(child2)
    return np.array(new_population)

def genetic_algorithm_for_recommendations(
    pop_size, num_movies, user_id, generations=3, crossover_prob=0.7, mutation_rate=0.1, track_interval=1000
):
    population = init_pop_randomly(pop_size, num_movies)
    
    for generation in range(generations):
        fitness_vals = calc_fitness_similarity(population, user_id)
  
        best_individual_index = np.argmax(fitness_vals)
        best_individual = population[best_individual_index]
        best_fitness_value = fitness_vals[best_individual_index]
        
        population = evolve_population(population, fitness_vals, crossover_prob, mutation_rate)
        
        worst_individual_index = np.argmin(fitness_vals)
        population[worst_individual_index] = best_individual
        fitness_vals[worst_individual_index] = best_fitness_value
        
        if (generation + 1) % track_interval == 0:
            avg_fitness = np.mean(fitness_vals)
            print(f"Generation {generation + 1}/{generations}:")
            print(f"  Average Fitness: {avg_fitness:.4f}")
            print(f"  Best Individual: {best_individual}")
            print("-" * 50)
    
    # Calculate final fitness values
    final_fitness_vals = calc_fitness_similarity(population, user_id)
    return population, final_fitness_vals


pop_size = 50
num_movies = 5
user_id = 'user1'
generations = 1000

evolved_population_final, fitness_vals_final = genetic_algorithm_for_recommendations(
    pop_size, num_movies, user_id, generations, crossover_prob=0.7, mutation_rate=0.1, track_interval=100 
)

print("Evolved Population Final:", evolved_population_final)
print("Fitness Values Final:", fitness_vals_final)

max_fitness = max(fitness_vals_final)

# filter population to only include individuals with the highest fitness
best_individuals = []
max_fitness = max(fitness_vals_final) 
for i in range(len(fitness_vals_final)):
    if fitness_vals_final[i] == max_fitness:
        best_individuals.append(evolved_population_final[i]) 

print("\nBest Individuals with Highest Fitness:")
print(f"  Highest Fitness Value: {max_fitness:.4f}")
for individual in best_individuals:
    print(f"  Individual: {individual}")