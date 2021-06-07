import json
import pandas as pd
import uuid

# movie_entries= json.load(open('data/movieBot/entities/movie_entries_en.json'))

movie_entries= []
title_akas= pd.read_csv('data/imdb/title_akas.tsv', sep='\t')
title_basics= pd.read_csv('data/imdb/title_basics.tsv', sep='\t')

data= pd.merge(title_akas, title_basics, left_on='titleId', right_on='tconst', right_index= False)
movie_titles= data[(data['titleType']=='movie') & ((data['language']=='hi') | (data['language']=='en'))]
print(len(movie_titles.title.unique()))

for index, title in enumerate(movie_titles.title.unique()):

    title_entity= {
        "value": title,
        "synonyms": [
            title
            ]
        }

    movie_entries.append(title_entity)

json.dump(movie_entries, open('data/movieBot/entities/movie_entries_en.json', 'w'), indent=4 )