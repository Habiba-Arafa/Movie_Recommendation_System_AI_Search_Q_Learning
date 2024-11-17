import matplotlib.pyplot as plt
import numpy as np
from bfs import bfs_space_ans
from dfs import dfs_space_ans
from ucs import ucs_space_ans
from IDS import ids_space_ans
from Astar import astar_space_ans
from GBFS import gbfs_space_ans
dfs_space = dfs_space_ans()
print("DFS space:", dfs_space)
bfs_space = bfs_space_ans()
print("BFS space:", bfs_space)
ucs_space = ucs_space_ans()
print("UCS space:", ucs_space)
ids_space = ids_space_ans()
print("IDS space:", ids_space)
astar_space = astar_space_ans()
print("A* space:", astar_space)
greedy_bfs_space = gbfs_space_ans()
print("Greedy BFS space:", greedy_bfs_space)

start_rss = [dfs_space[0],bfs_space[0], ucs_space[0], ids_space[0], astar_space[0], greedy_bfs_space[0]]
end_rss = [bfs_space[1],bfs_space[1], ucs_space[1], ids_space[1], astar_space[1], greedy_bfs_space[1]]

print('Start RSS and VMS:', start_rss)
print('End RSS and VMS:', end_rss)

algorithms = ['DFS','BFS', 'UCS', 'IDS', 'A*', 'GBFS']

x = np.arange(len(algorithms))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots(figsize=(10, 6))

bars1_start = ax.bar(x - width/2, start_rss, width, label='Start RSS', color='lightgreen')
bars1_end = ax.bar(x + width/2, end_rss, width, label='End RSS', color='purple')

ax.set_xlabel('Algorithms')
ax.set_ylabel('Memory Usage (MB)')
ax.set_title('Memory Usage Comparison (Start vs. End) for Different Search Algorithms')
ax.set_xticks(x)
ax.set_xticklabels(algorithms)
ax.legend()

# Display the plot
fig.tight_layout()
plt.show()
