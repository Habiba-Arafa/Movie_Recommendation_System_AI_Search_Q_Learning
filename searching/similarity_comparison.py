from bfs import bfs_comparison
from GBFS import gbfs_comparison
from Astar import astar_comparison
from genetics import main
from IDS import ids_comparison
from simualted_annealing import simulated_annealling
from qlearning_test import qlearning_comparison
import matplotlib.pyplot as plt

movies=['Avatar', 'Tangled','The Emperor\'s New Groove','The Expendables 2','Incendies']

avg_astar_score = astar_comparison()
avg_ids_score = ids_comparison(movies)
_,avg_simulated_annealing_score= simulated_annealling(movies[0])
avg_qlearning_score = qlearning_comparison(movies)
avg_bfs_score = bfs_comparison(movies)
avg_gbfs_score = gbfs_comparison()
avg_genetics_score = main()

time_taken = {
    "BFS": avg_bfs_score,
    "IDS": avg_ids_score,
    "A*": avg_astar_score,
    "Greedy Best First Search": avg_gbfs_score,
    "Genetics" : sum(avg_genetics_score)/len(avg_genetics_score),
    'Simulated annealing':avg_simulated_annealing_score,
    'Q learing': avg_qlearning_score
}

algorithms = list(time_taken.keys())
times = list(time_taken.values())
print(algorithms)
print(times)

plt.bar(algorithms, times, color=['blue', 'green', 'red', 'purple', 'pink', 'violet',"orange"])
plt.xlabel('Search Algorithms')
plt.ylabel('Average Cosine Similarity (ms)')
plt.title('Cosine similarity of the movie recommendation of each algorithm')
plt.show()  