import json
import pandas as pd

# movie_entries= json.load(open('data/movieBot/entities/movie_entries_en.json'))

movie_entries= []
data= pd.read_csv('data/imdb/title_akas.tsv', sep='\t', low_memory=False)

movie_titles= data[(data['language']=='hi') | (data['language']=='en')]

for title in movie_titles.title.unique():
    if 'एपिसोड' in title:
        continue
    title_entity= {
        "value": title,
        # "synonyms": [
        #     title
        #     ]
        }

    movie_entries.append(title_entity)


json.dump(movie_entries, open('data/movieBot/entities/movie_entries_en.json', 'w'), indent=4 )