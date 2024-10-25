import pandas as pd
import numpy as np
import json

df = pd.read_csv('movie_dataset.csv')
df.duplicated().sum()
df.drop(['budget', 'id', 'keywords', 'crew', 'vote_count', 'tagline', 'revenue',
         'production_countries', 'original_language', 'overview', 'status',
         'homepage', 'release_date', 'runtime', 'title', 'spoken_languages',
         'popularity'], axis=1, errors='ignore', inplace=True)
df = df.dropna()
df['vote_average'] = np.ceil(df['vote_average'])

unique_directors = df['director'].unique()[:30]
repeated_directors = np.tile(unique_directors, int(np.ceil(len(df) / 30)))[:len(df)]
df['director'] = repeated_directors

lst_genres = []
for genre in df["genres"].unique():
    for genre_word in str(genre).split(" "):
        lst_genres.append(genre_word)

genres = list(set(lst_genres))
if "Fiction" in genres:
    genres.remove("Fiction")
if len(genres) > 6: 
    genres[-6] = "Science Fiction"
for genre in genres:
    df[genre] = df['genres'].apply(lambda x: 1 if genre in x else 0)

df = df.drop(['genres'], axis=1)
df = pd.get_dummies(df, columns=['vote_average'], drop_first=True)
df = df.drop(['director', 'production_companies', 'index', 'cast'], axis=1, errors='ignore')
df.to_csv('cleaned_movie_dataset.csv')


movie_vector = {}
for index, row in df.iterrows():
    movie_title = row['original_title']

    genre_values = row[2:-10].tolist() 
    vote_one_hot = []

    for vote_col in [col for col in row.index if 'vote_average' in col]:
        count = row[vote_col]
        vote_one_hot.append(1 if count > 0 else 0)

    movie_vector[movie_title] = genre_values + vote_one_hot

with open('movie_vectors.json', 'w') as json_file:
    json.dump(movie_vector, json_file, indent=4)
print("tam benaga7")

    
