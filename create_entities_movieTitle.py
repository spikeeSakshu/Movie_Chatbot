import json
import pandas as pd
import uuid

# movie_entries= json.load(open('data/movieBot/entities/movie_entries_en.json'))
save_path= 'data/movieBot/entities/'
title_akas= pd.read_csv('data/imdb/title_akas.tsv', sep='\t')
title_basics= pd.read_csv('data/imdb/title_basics.tsv', sep='\t')

data= pd.merge(title_akas, title_basics, left_on='titleId', right_on='tconst', right_index= False)
movie_titles= data[(data['titleType']=='movie') & ((data['language']=='hi') | (data['language']=='en'))]
# print(len(movie_titles.title.unique()))

movie_entries, i= [], 1
for index, title in enumerate(movie_titles.title.unique()):

    title_entity= {
        "value": title,
        "synonyms": [
            title
            ]
        }

    movie_entries.append(title_entity)

    if (index+1)%30000==0:
               
        new_entity_name= 'movie_'+str(i)
        new_entity= {
            "id": str(uuid.uuid4()),
            "name": new_entity_name,
            "isOverridable": True,
            "isEnum": False,
            "isRegexp": False,
            "automatedExpansion": False,
            "allowFuzzyExtraction": False
        }

        json.dump(new_entity, open(save_path+new_entity_name+'.json', 'w'), indent=4)
        json.dump(movie_entries, open(save_path+new_entity_name+'_entries_en.json', 'w'), indent=4)
        
        movie_entries= []
        i=i+1

        # exit()