from bfs import bfs_time_calculation
from dfs import dfs_time_calculation
from ucs import ucs_time_calculation
from IDS import ids_time_calculation
from Astar import astar_time_calculation
from GBFS import gbfs_time_calculation
import matplotlib.pyplot as plt

# Calculate average times for each algorithm
bfs_average = bfs_time_calculation()
dfs_average = dfs_time_calculation()
ucs_average = ucs_time_calculation()
ids_average = ids_time_calculation()
astar_average = astar_time_calculation()
greedy_bfs_average = gbfs_time_calculation() 

time_taken = {
    "BFS": bfs_average,
    "DFS": dfs_average,
    "UCS": ucs_average,
    "IDS": ids_average,
    "A*": astar_average,
    "Greedy Best First": greedy_bfs_average
}

algorithms = list(time_taken.keys())
times = list(time_taken.values())

plt.bar(algorithms, times, color=['blue', 'green', 'red', 'purple', 'pink', 'violet'])
plt.xlabel('Search Algorithms')
plt.ylabel('Average Time (ms)')
plt.title('Average Time Taken by Search Algorithms')
plt.show()  