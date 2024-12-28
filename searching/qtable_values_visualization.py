import matplotlib.pyplot as plt
import json


with open('csvs_and_jsons/q_table_trained.json', 'r') as file:
    q_table = json.load(file)


plt.figure(figsize=(10, 6))
for movie, values in q_table.items():
    plt.plot(values, label=f"Movie: {movie}")
plt.title("Q-Values for Actions")
plt.xlabel("Action (Bit Index)")
plt.ylabel("Q-Value")
plt.legend()
plt.show()