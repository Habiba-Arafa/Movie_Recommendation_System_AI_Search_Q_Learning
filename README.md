# 🎬 Movie Recommendation System using AI Search & Q-Learning

This repository contains an intelligent Movie Recommendation System powered by various Artificial Intelligence techniques. It uses **Graph Search Algorithms**, **Q-Learning**, and **Genetic Algorithms** to generate and evaluate personalized movie suggestions.

---

## 📁 Project Structure

```
movie_recommendation-main/
├── cleaning_and_generation_files/        # Data cleaning & synthetic user/graph generators
├── csvs_and_jsons/                        # Datasets, movie vectors, Q-tables, graphs
├── html_files/                            # Visual HTML graph/tree outputs
├── lib/                                   # JS libraries for HTML visualizations
├── searching/                             # AI Search & Reinforcement Learning algorithms
├── Project Description.pdf                # Project Overview
├── Qlearning.pdf                          # Q-learning implementation & results
└── README.md                              # Project documentation
```

---

## 🤖 Algorithms Used

### 🔍 Search Algorithms:
- **Breadth-First Search (BFS)**
- **Depth-First Search (DFS)**
- **Uniform Cost Search (UCS)**
- **Greedy Best-First Search (GBFS)**
- **A\* Search**
- **Iterative Deepening Search (IDS)**

Each search technique finds optimal movie recommendations based on graph traversal across movie similarities and genres.

### 🔁 Q-Learning (Reinforcement Learning):
- **States**: Binary movie vectors (representing features)
- **Actions**: Bit flips to change features
- **Rewards**: Cosine similarity improvement
- **Training**: Over 1000 episodes with a trained Q-table
- **Output**: A sequence of recommended movies using learned policy

### 🧬 Genetic Algorithms:
- Generate synthetic user preferences
- Evolve movie recommendations using crossover and mutation
- Score individuals based on similarity to user profile

---

## 📚 Datasets & Files

- `movie_dataset.csv`, `cleaned_movie_dataset.csv`: Raw and processed movie data
- `movie_vectors.json`: Binary vector representation of each movie
- `q_table_trained.json`: Q-values after learning optimal policy
- `random_users.json`: Synthetic user profiles
- `random_connections_graph.json`: Graph used in search algorithms

---

## 📊 Results (Q-Learning Highlights)

- Cosine similarity improved across iterations
- Actions with the highest impact were reinforced in the Q-table
- Final policy successfully recommends movies with similar genres
- Detailed explanation in `Qlearning.pdf`

---

## 🌐 Visualization

All graph-based algorithm visualizations can be opened in your browser:

- `html_files/astar_movie_recommendation.html`
- `html_files/bfs_tree.html`
- `html_files/dfs_tree.html`
- `html_files/weighted_graph_visualization.html`

These show how each algorithm searches through the movie network to generate recommendations.

---

## 🚀 How to Run

### 1. Install Dependencies

```bash
pip install numpy pandas scikit-learn matplotlib
```

### 2. Preprocess Data

```bash
python cleaning_and_generation_files/dataCleaning.py
```

### 3. Train Q-Learning

```bash
python searching/qlearning.py
```

### 4. Generate Recommendations

```bash
python searching/qlearning_test.py
```

### 5. Visualize Graph Searches

Open any file inside `html_files/` in your browser to see traversal paths.


## 📄 License

This project is licensed under the MIT License.
