import requests
import json
import Fetch_Tmdb_Persons_Details 
from Fetch_Tmdb_Persons_Details import get_person_details
from Tmdbtvseries import get_details_tmdb_tv_series,get_details_tv_seasons,get_details_tv_episodes_details
api_key_counter = 0
error_status = False
#tv_series_id = '13916'
language = 'en-US'
headers = {"Authorization":"Basic bmVvNGo6dm9ubnVl"}
tv_series_id = '1396'
language = 'en-US'
neo4j_base_url = 'http://localhost:7474/db/data/cypher'
tv_json  = get_details_tmdb_tv_series(tv_series_id, language)



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

def get_details_tmdb_popular_tv_series_id():
    try:
        api_key = get_random_api_key()
        tmdb_tv_series_url =  tmdb_tv_series_base_url + 'popular'+ '?api_key=' + api_key + '&language=' + language
        response = requests.request("GET", tmdb_tv_series_url)
        data = response.json()
        #print(data)
        return(data)
    except Exception as e:
        global error_status
        error_status = True
        print("Function : get_details_tmdb_tv_series, Movie id: " + tv_series_id +  "\n Error : " + str(e)  )
        return None
    
    
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

def replace_none_with_empty_str(some_dict):
    return { k: (''if v is None else v) for k, v in some_dict.items() }


def create_node_tvseries_id():

    series_details =  get_details_tmdb_popular_tv_series_id()
    series_details["results"] =[dict(id=k1["id"]) for k1 in series_details["results"]]
    guest_id = series_details["results"]
    #print(guest_id)
    list = [ids for ids in guest_id]
    tvseriesid = []
    for value in list:
        tvseriesid.append(value['id'])
    list_of_tvseries = tvseriesid
    return list_of_tvseries




def callNeo4j(payload, headers):
    r= requests.post(neo4j_base_url, json = payload, headers = headers)
    response_json = json.loads(r.text)
    #print(r)
    return response_json



def get_details_tv_seasons(tv_series_id,season_number):
    try:
        api_key = get_random_api_key()
        tmdb_season_url =  tmdb_tv_series_base_url + tv_series_id+ '/season/'+ str(season_number) + '?api_key=' + api_key + '&language=' + language
        response = requests.request("GET", tmdb_season_url)
        data = response.json()
        #print(data)
        return(data)
    except Exception as e:
        global error_status
        error_status = True
        print("Function : get_details_tv_seasons, TV Series id: " + str(tv_series_id) +  "\n Error : " + str(e)  )
        return None

def join_tv_series_season_episode(tvseason_id,episode_id): 
    
    payload={"query" :"MATCH (n:TvSeasons),(e:TvEpisodes) WHERE n.tvseason_id = {tvseason_id} AND e.episode_id = {episode_id} MERGE (n)-[r:HAS_EPISODE]->(e) RETURN r"}
    params = {}
    params['tvseason_id'] = str(seasons_details['id'])
    params['episode_id'] = str(season['id'])

    tvseason_id = str(seasons_details['id'])
    episode_id =  str(season['id'])
    payload['params'] = params
    #print(episode_id)
    response_json = callNeo4j(payload, headers)
    #print(response_json)
    return response_json     




def tv_series_season_episodes_payload(tv_series_id, language):
    
    series_details = get_details_tmdb_tv_series(tv_series_id, language)
    series_details["seasons"]=[dict(id=k1["id"],season_number = k1["season_number"])for k1 in series_details["seasons"]]
    season_ids = series_details["seasons"]
    s_id = [d for d in season_ids if d.get('id')!= 0]
    #print(s_id)
    s = season_ids[:] 
    season_ids[:] = [d for d in season_ids if d.get('season_number') != 0]
    s = season_ids[:] 
    list = [ids for ids in s]
    #print(list)
    season_no = []
    for value in list:
        season_no.append(value['season_number'])
    s_number = season_no
    for season_number in s_number:
        seasons_details = get_details_tv_seasons(tv_series_id,season_number)
        #print(seasons_details)
        seasons_details["episodes"] =[dict(air_date=k1["air_date"],episode_number=k1["episode_number"],id=k1["id"],name = k1["name"],overview = k1["overview"],production_code = k1["production_code"],season_number = k1["season_number"],show_id = k1["show_id"],still_path = k1["still_path"],vote_average = k1["vote_average"],vote_count = k1["vote_count"]) for k1 in seasons_details["episodes"]]
    
        seasons = seasons_details["episodes"]
        for season_data in seasons:
            season = replace_none_with_empty_str(season_data)
            params = {}
            if 'id' in seasons_details:
                params['tvseason_id'] = str(seasons_details['id'])
                #print(params)
            if 'air_date' in season:
                params['air_date'] = season['air_date']
                
            if 'episode_number' in season:
                params['episode_number'] = season['episode_number']
            if 'id' in season:
                params['episode_id'] = str(season['id'])
            if 'name' in season:
                params['name'] = season['name']
            if 'overview' in season:
                params['overview'] = season['overview']
            if 'production_code' in season:
                params['production_code'] =season['production_code']
            if 'season_number' in season:
                params['season_number'] = season['season_number']
            if 'still_path' in season:
                params['still_path'] = season['still_path']
            if 'vote_average' in season:
                params['vote_average'] = season['vote_average']
            if 'show_id' in season:
                params['show_id'] = str(season['show_id'])
            if 'vote_count' in season:
                params['vote_count'] = season['vote_count']
             
            
            payload={"query" : "MERGE(n:TvEpisodes{air_date :{air_date},episode_number : {episode_number},episode_id:{episode_id},name:{name},overview:{overview},production_code:{production_code},season_number:{season_number},still_path:{still_path},vote_average:{vote_average},show_id:{show_id},vote_count:{vote_count}}) RETURN n"}    
            payload['params'] = params
            
            response_json = callNeo4j(payload, headers)
            if response_json is not None:
                payload={"query" :"MATCH (n:TvSeasons),(e:TvEpisodes) WHERE n.tvseason_id = {tvseason_id} AND e.episode_id = {episode_id} MERGE (n)-[r:HAS_EPISODE]->(e) RETURN r"}
                params = {}
                params['tvseason_id'] = str(seasons_details['id'])
                params['episode_id'] = str(season['id'])
            
                payload['params'] = params
                #print(episode_id)
                match_response_json = callNeo4j(payload, headers)
            #print(match_response_json)
        