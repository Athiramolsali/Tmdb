# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 15:20:14 2019

@author: Admin
"""

import fetchImdbMovie, fetchTmdbMovie
from neo4jConnector import  Movie
import pandas as pd
import json

tmdb_img_base_url = 'https://image.tmdb.org/t/p/w185/'



#to create logging dataframe            
def create_titles_file(input_file, outfile):
    titles = pd.read_csv(input_file, sep="\t")
    print(titles)
    #titles.titleType.unique()
    movie_titles = titles[titles.titleType == 'movie']
    # deleting the variable because of its large size
    del titles
    movie_titles = movie_titles[['tconst']]
    movie_titles.columns = ['title_ids']
    movie_titles = movie_titles.drop_duplicates()
    movie_titles['status'] = 0
    movie_titles['recommended_status'] = 0
    movie_titles.to_csv(outfile)
    
    
def fetchMovies(movie_id, language, fetch_recommended_movie = True):
    error_status = False
    recommended_movie_status = False
    movie_node = None
    try:
        movie_node, error_status = fetchTmdbMovie.tmdb_movie(movie_id = movie_id, language = language)
    except Exception as e: 
        error_status = True
        print("Fetching movies failed for:" + movie_id + "\n Error : " + str(e) )
        return None, error_status, recommended_movie_status
    if fetch_recommended_movie:
        try:
            recommended_movie_list = fetchImdbMovie.get_imdb_recommended_movies(movie_id)
            for recommended_movie_id in recommended_movie_list:
                movie = Movie.nodes.get_or_none(imdb_id = recommended_movie_id)
                if movie is None:
                    movie, err_status, rec_movie_status = fetchMovies(recommended_movie_id, language, fetch_recommended_movie = False)
                if movie is not None:
                    movie_node.similar_movies.connect(movie) 
        except Exception as e: 
            recommended_movie_status = True
            print("Fetching recommended movies failed for:" + movie_id + "\n Error : " + str(e) )
            return movie_node, error_status, recommended_movie_status
    return movie_node, error_status, recommended_movie_status
    

def get_current_index(titles):
    current_index = titles.loc[titles['status'] == 0].index
    if len(current_index):
        current_index = current_index[0]
    else:
        current_index = titles.loc[titles['recommended_status'] == 0].index
        if len(current_index):
            current_index = current_index[0]
        else:
            current_index = None
    return current_index
    


def main(config):
    language = config["language"]
    title_file = config["title_file"]
    title_df = pd.read_csv(title_file)     
    
    current_index = get_current_index(title_df)
    while current_index is not None:
        movie_id = title_df.title_ids[current_index]
        print("Fetching " + movie_id)
        movie_node, error_status, recommended_movie_status =fetchMovies(movie_id, language, fetch_recommended_movie = True)
        if error_status:
            title_df.status[current_index] = 1
        else:
            title_df.status[current_index] = 2
        if recommended_movie_status:
            title_df.recommended_status[current_index] = 1
        else:
            title_df.recommended_status[current_index] = 2
        print("Completed fetching " + movie_id)
        title_df.to_csv(title_file)
        current_index = get_current_index(title_df)
        
    


if __name__ == "__main__":
    with open('config.json') as json_file:
        config = json.load(json_file)
    main(config)

        
        


