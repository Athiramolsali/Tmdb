import json
import requests
from Tmdbtvseries import get_details_tmdb_tv_series

api_key_counter = 0
error_status = False
language = 'en-US'

headers = {"Authorization":"Basic bmVvNGo6dm9ubnVl"}
tv_series_id = '81355'

language = 'en-US'
neo4j_base_url = 'http://localhost:7474/db/data/cypher'

with open('config.json') as json_file:
    config = json.load(json_file)
    
    api_keys = config["api_keys"]
    language = config["language"]
    tmdb_tv_series_base_url = config["tmdb_tv_series_base_url"]
    tmdb_person_base_url = config["tmdb_person_base_url"]

def get_random_api_key():
    # calls the global variable in the function
    global api_keys
    global api_key_counter
    api_key = api_keys[api_key_counter]
    api_key_counter += 1
    if api_key_counter == len(api_keys):
        api_key_counter = 0
    return api_key

def callNeo4j(payload, headers):
    r= requests.post(neo4j_base_url, json = payload, headers = headers)
    response_json = json.loads(r.text)
    return response_json

def replace_none_with_empty_str(some_dict):
    return { k: ('' if v is None else v) for k, v in some_dict.items() }


def get_details_tmdb_tv_series(tv_series_id, language):
    try:
        api_key = get_random_api_key()
        tmdb_tv_series_url =  tmdb_tv_series_base_url + tv_series_id+ '?api_key=' + api_key + '&language=' + language
        response = requests.request("GET", tmdb_tv_series_url)
        data = response.json()
        return(data)
    except Exception as e:
        global error_status
        error_status = True
        print("Function : get_details_tmdb_tv_series, Movie id: " + tv_series_id +  "\n Error : " + str(e)  )
        return None 
    return response_json

def replace_none_with_empty_str(some_dict):
    return { k: ('' if v is None else v) for k, v in some_dict.items() }




        

               
        
def create_match_genre_tvseries(tv_series_id):                  

    series_details  = get_details_tmdb_tv_series(tv_series_id, language)
    tv_json  = replace_none_with_empty_str(series_details)

    genres = tv_json['genres']
    
    for g in genres:
        genre = g     
        params = {}
        if 'id' in tv_json:
            params['id'] = str(tv_json['id'])
        if 'name' in genre:
            params['name'] = genre['name']
        if 'id' in genre:
            params['genre_id'] = str(genre['id'])
            #print(params)
        
        payload={"query" : "MERGE(n:Genre{name:{name},genre_id:{genre_id}}) RETURN n"}
        payload['params'] = params
        response_json = callNeo4j(payload, headers)
        if response_json is not None:
            payload={"query" :"MATCH (t:TvSeries),(n:Genre) WHERE t.id ={id} AND n.genre_id = {genre_id} MERGE (t)-[r:OF_GENRE]->(n) RETURN r"}
            params = {}
            params['id'] = str(tv_json['id'])
            params['genre_id'] = str(genre['id'])
            tv_series_id = str(tv_json['id'])
            genre_id =  str(genre['id'])
            payload['params'] = params
            #print(params)
            match_response_json = callNeo4j(payload, headers)
        
       
        
    