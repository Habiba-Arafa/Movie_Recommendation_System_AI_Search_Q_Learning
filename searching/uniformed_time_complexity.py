from bfs import bfs_time_calculation
from dfs import dfs_time_calculation
from ucs import ucs_time_calculation

bfs_average=bfs_time_calculation()
dfs_average=dfs_time_calculation()
ucs_average= ucs_time_calculation()

time_taken={"bfs":bfs_average, "dfs":dfs_average, "ucs":ucs_average}

