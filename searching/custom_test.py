import json

custom_test_graph = {
    "Avatar": {
        "Pirates of the Caribbean: At World's End": 0.9,
        "Spectre": 0.85
    },
    "Pirates of the Caribbean: At World's End": {
        "The Dark Knight Rises": 0.7
    },
    "Spectre": {
        "Avatar": 0.85
    },
    "The Dark Knight Rises": {},  

    "Inception": {
        "Interstellar": 0.88,
        "Tenet": 0.88
    },
    "Interstellar": {
        "Inception": 0.88,
        "Dunkirk": 0.88
    },
    "Tenet": {
        "Inception": 0.88
    },
    "Dunkirk": {},  
}

custom_test_file_path = "custom_test_graph.json"
with open(custom_test_file_path, "w") as file:
    json.dump(custom_test_graph, file, indent=4)

print(f"Custom test graph saved as {custom_test_file_path}")
