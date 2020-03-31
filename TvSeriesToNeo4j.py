import json
import requests
from Tmdbtvseries import get_details_tmdb_tv_series,get_details_tv_seasons,get_details_tv_episodes_details

api_key_counter = 0
error_status = False
#tv_series_id = '13916'
language = 'en-US'

headers = {"Authorization":"Basic bmVvNGo6dm9ubnVl"}
#tv_series_id = '456'
tv_series_id = '40075'

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
#add last episode properties to existed node
def last_episode(tv_series_id):
    #tv_series_id = '40075'
    tvseries = get_details_tmdb_tv_series(str(tv_series_id), language)
    tv_json = replace_none_with_empty_str(tvseries)
    last_episode_to_air = tv_json['last_episode_to_air']
    params = {}
    if str(last_episode_to_air) != '':
        if 'id' in tv_json:
            params['id'] = str(tv_json['id'])

        if 'air_date' in last_episode_to_air:
            params['last_episode_to_air_air_date'] = last_episode_to_air['air_date']
    
        if 'episode_number' in last_episode_to_air:
            params['last_episode_to_air_episode_number'] = last_episode_to_air['episode_number'] 
        if 'id' in last_episode_to_air:
            params['last_episode_to_air_id'] = str(last_episode_to_air['id'])
        if 'name' in last_episode_to_air:
            params['last_episode_to_air_name'] = last_episode_to_air['name'] 
        if 'overview' in last_episode_to_air:
            params['last_episode_to_air_overview'] = last_episode_to_air['overview']
        if 'production_code' in last_episode_to_air:
            params['last_episode_to_air_production_code'] = last_episode_to_air['production_code']
        if 'season_number' in last_episode_to_air:
            params['last_episode_to_air_season_number'] = last_episode_to_air['season_number']
       
        if 'show_id' in last_episode_to_air:
            params['last_episode_to_air_show_id'] = str(last_episode_to_air['show_id'])
        if 'still_path' in last_episode_to_air:
            params['last_episode_to_air_still_path'] = last_episode_to_air['still_path']
        if 'vote_average' in last_episode_to_air:
            params['last_episode_to_air_vote_average'] = last_episode_to_air['vote_average']
        if 'vote_count' in last_episode_to_air:
            params['last_episode_to_air_vote_count'] = last_episode_to_air['vote_count']
        payload = {"query":"MATCH(t:TvSeries{id:{id}}) SET t += {last_episode_to_air_air_date:{last_episode_to_air_air_date},last_episode_to_air_episode_number:{last_episode_to_air_episode_number},last_episode_to_air_id:{last_episode_to_air_id},last_episode_to_air_name:{last_episode_to_air_name},last_episode_to_air_overview:{last_episode_to_air_overview},last_episode_to_air_production_code:{last_episode_to_air_production_code},last_episode_to_air_season_number:{last_episode_to_air_season_number},last_episode_to_air_show_id:{last_episode_to_air_show_id},last_episode_to_air_still_path:{last_episode_to_air_still_path},last_episode_to_air_vote_average:{last_episode_to_air_vote_average},last_episode_to_air_vote_count:{last_episode_to_air_vote_count}} RETURN t"}
        payload['params'] = params
        response_json = callNeo4j(payload, headers)
        #print(response_json)

    else:
        
        if last_episode_to_air == '':
            if 'id' in tv_json:
                params['id'] = str(tv_json['id'])
            
            if 'last_episode_to_air' in tv_json:
                params['last_episode_to_air'] = tv_json['last_episode_to_air']
            payload={"query" : "MATCH(t:TvSeries{id:{id}})SET t += {last_episode_to_air:{last_episode_to_air}}RETURN t"}
            payload['params'] = params

            response_json = callNeo4j(payload, headers)
##add next episode properties to existed node

def next_episode(tv_series_id):
    #tv_series_id = '40075'
    tvseries = get_details_tmdb_tv_series(str(tv_series_id), language)
    tv_json = replace_none_with_empty_str(tvseries)
    next_episode_to_air = tv_json['next_episode_to_air']
    last_episode_to_air = tv_json['last_episode_to_air']
    params = {}
    if str(next_episode_to_air) != '':
       
        if 'air_date' in next_episode_to_air:
            params['next_episode_to_air_air_date'] = next_episode_to_air['air_date'] 
    
        if 'episode_number' in next_episode_to_air:
            params['next_episode_to_air_episode_number'] = next_episode_to_air['episode_number'] 
        if 'id' in next_episode_to_air:
            params['next_episode_to_air_id'] = str(next_episode_to_air['id'])
        if 'name' in next_episode_to_air:
            params['next_episode_to_air_name'] = next_episode_to_air['name'] 
        if 'overview' in next_episode_to_air:
            params['next_episode_to_air_overview'] = next_episode_to_air['overview']
        if 'production_code' in next_episode_to_air:
            params['next_episode_to_air_production_code'] = next_episode_to_air['production_code']
        if 'season_number' in next_episode_to_air:
            params['next_episode_to_air_season_number'] = next_episode_to_air['season_number']
       
        if 'show_id' in next_episode_to_air:
            params['next_episode_to_air_show_id'] = str(next_episode_to_air['show_id'])
        if 'still_path' in next_episode_to_air:
            params['next_episode_to_air_still_path'] = next_episode_to_air['still_path']
        if 'vote_average' in next_episode_to_air:
            params['next_episode_to_air_vote_average'] = next_episode_to_air['vote_average']
        if 'vote_count' in next_episode_to_air:
            params['next_episode_to_air_vote_count'] = next_episode_to_air['vote_count']
        payload={"query" :"MATCH(t:TvSeries{id:{id}}) SET t += {next_episode_to_air_air_date:{next_episode_to_air_air_date},next_episode_to_air_episode_number:{next_episode_to_air_episode_number},next_episode_to_air_id:{next_episode_to_air_id},next_episode_to_air_name:{next_episode_to_air_name},next_episode_to_air_overview:{next_episode_to_air_overview},next_episode_to_air_production_code:{next_episode_to_air_production_code},next_episode_to_air_season_number:{next_episode_to_air_season_number},next_episode_to_air_show_id_id:{next_episode_to_air_show_id},next_episode_to_air_still_path: {next_episode_to_air_still_path},next_episode_to_air_vote_average: {next_episode_to_air_vote_average},next_episode_to_air_vote_count: {next_episode_to_air_vote_count}}RETURN t"}
        payload['params'] = params
        response_json = callNeo4j(payload, headers)
           
    else:
        
        if next_episode_to_air == '':
            
            if 'id' in tv_json:
                params['id'] = str(tv_json['id'])
        
            if 'next_episode_to_air' in tv_json :
                params['next_episode_to_air'] = tv_json['next_episode_to_air']
            payload={"query" : "MATCH (t:TvSeries{id:{id}})SET t +={next_episode_to_air:{next_episode_to_air}}RETURN t"}
            payload['params'] = params
            response_json = callNeo4j(payload, headers)




def tvseries_to_neo4j(tv_series_id):    
    tvseries = get_details_tmdb_tv_series(str(tv_series_id), language)
    tv_json = replace_none_with_empty_str(tvseries)
    params = {}
    
    if 'backdrop_path' in tv_json:
        params['backdrop_path'] = tv_json['backdrop_path']
    if 'first_air_date' in tv_json:
        params['first_air_date'] = tv_json['first_air_date']
    if 'homepage' in tv_json:
        params['homepage'] = tv_json['homepage']
    if 'id' in tv_json:
        params['id'] = str(tv_json['id'])
    if 'in_production' in tv_json:
        params['in_production'] = tv_json['in_production']   
    
    if 'name' in tv_json:
        params['name'] = tv_json['name']
  
    if 'number_of_episodes' in tv_json:
        params['number_of_episodes'] = tv_json['number_of_episodes']
    if 'number_of_seasons' in tv_json:
        params['number_of_seasons'] = tv_json['number_of_seasons']
    if 'original_language' in tv_json:
        params['original_language'] = tv_json['original_language']
    if 'original_name' in tv_json:
        params['original_name'] = tv_json['original_name']
    if 'overview' in tv_json:
        params['overview'] = tv_json['overview']
    if 'popularity' in tv_json:
        params['popularity'] = tv_json['popularity']
    if 'poster_path' in tv_json:
        params['poster_path'] = tv_json['poster_path']
    if 'status' in tv_json:
        params['status'] = tv_json['status']
    if 'type' in tv_json:
        params['type'] = tv_json['type']
    if 'vote_average' in tv_json:
        params['vote_average'] = tv_json['vote_average']
    if 'vote_count' in tv_json:
        params['vote_count'] = tv_json['vote_count']
        #print(params)
    
    payload={"query" : "MERGE(t:TvSeries {backdrop_path:{backdrop_path},first_air_date:{first_air_date},homepage:{homepage},id:{id},in_production:{in_production},name:{name},number_of_episodes:{number_of_episodes},number_of_seasons: {number_of_seasons},original_language: {original_language},original_name: {original_name},overview: {overview},popularity: {popularity},poster_path: {poster_path},status: {status},type: {type},vote_average:{vote_average} ,vote_count: {vote_count}}) RETURN t"}
    payload['params'] = params
    response_json = callNeo4j(payload, headers)
    next_episode_props = next_episode(tv_series_id)
    last_episode_props = last_episode(tv_series_id)
        

 