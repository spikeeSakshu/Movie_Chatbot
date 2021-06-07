import json
import pandas as pd

data= pd.read_csv('data/imdb/title_akas.tsv', sep='\t', low_memory=False)
movie_titles= data[(data['language']=='hi') | (data['language']=='en')]

print(len(movie_titles.title.unique()))
