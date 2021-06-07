import pandas as pd

data= pd.read_csv('data/imdb/title_akas.tsv', sep='\t', low_memory=False)

print(data[data['language']=='en'])