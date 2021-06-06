import pandas as pd

data= pd.read_csv('data/imdb/title_akas.tsv', sep='\t', low_memory=False)
print(len(data))
print(data.head())
print(data.language.unique())

print(data[data['language']=='en'])