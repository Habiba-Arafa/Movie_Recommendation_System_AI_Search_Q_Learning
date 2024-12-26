import json
with open('csvs_and_jsons\\movie_vectors.json', 'r') as file:
    movies = json.load(file)

def toggle_bit(index,list): 
    if(list[index]==0):
        list[index]=1
    else:
        list[index]=0
    return list


def createQTable():
    q_table={}
    for key,value in movies.items():
        q_table[key]=[]
        for bit in range(len(value)):
            toggled_value = toggle_bit(bit, value.copy())  # Toggle the bit and append
            q_table[key].append(toggled_value)
    return q_table

q_table=createQTable()
with open('csvs_and_jsons\\q_table.json', 'w') as json_file:
    json.dump(q_table, json_file, indent=4)

