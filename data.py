import json
import pandas as pd
from pandas.io.parsers import read_csv


data = pd.read_csv("movie_metadata.csv")

print(data.columns)
print(data.head())
print(data.shape)

# Create a new data frame with relevant columns only
new_data = data[['genres', 'movie_title', 'imdb_score', 'movie_imdb_link']].copy()

print(f"new dataset columns: \n{new_data.columns}")
print("New data : \n",new_data)

#fetch all genres
#split based on verical pipes
#get its index
genres_all = [new_data.loc[i]['genres'].split('|') for i in new_data.index]

genres = sorted(list(set([item for sublist in genres_all for item in sublist])))

print("All genres: \n",genres)

#initalize all movie data and titles

all_data = list()
movie_title = list()

for i in new_data.index:

    #append moview title and index of movie
    movie_title.append((new_data.loc[i]["movie_title"].strip(),i,new_data.loc[i]["movie_imdb_link"].strip()))

    # add list of genres to movies to movie data
    #split data based on |
    #categories the genres into 1 and 0 if the genre exist 

    #so if it exist then 1 
    #if genre doesnt exist 0
    movie_data = [1 if genre in new_data.loc[i]["genres"].split("|") else 0 for genre in genres]

    #add imdb score to moview_data
    movie_data.append(new_data.loc[i]["imdb_score"])

    #append all data related to movie to all_data
    all_data.append(movie_data)




data_dump = r'data.json'
title_dump =r'titles_new.json'
with open(data_dump,'w+',encoding='utf-8') as f:
    json.dump(all_data,f)
with open(title_dump,'w+',encoding='utf-8') as f:
    json.dump(movie_title,f)
