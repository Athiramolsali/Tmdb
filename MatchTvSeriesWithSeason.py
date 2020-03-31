import json
import requests
import Fetch_Tmdb_Persons_Details 
from Fetch_Tmdb_Persons_Details import get_person_details
from Tmdbtvseries import get_details_tmdb_tv_series,get_details_tv_seasons,get_details_tv_episodes_details

api_key_counter = 0
error_status = False
#tv_series_id = '13916'
language = 'en-US'
#season_number = '1'
#episode_number = 1
#person_id = '66633'
headers = {"Authorization":"Basic bmVvNGo6dm9ubnVl"}
#tv_series_id = '1396'
language = 'en-US'
neo4j_base_url = 'http://localhost:7474/db/data/cypher'
#tv_json  = get_details_tmdb_tv_series(tv_series_id, language)

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
    r = requests.post(neo4j_base_url, json = payload, headers = headers)
    response_json = json.loads(r.text)
    #print(r)
    return response_json



def tv_series_season_payload(tv_series_id, language):
     
        series_details = get_details_tmdb_tv_series(tv_series_id, language)
        #print(series_details)
        series_details["seasons"]=[dict(id=k1["id"],air_date=k1["air_date"],episode_count=k1["episode_count"],name = k1["name"],overview = k1["overview"],poster_path = k1["poster_path"],season_number = k1["season_number"])for k1 in series_details["seasons"]]
        season_ids = series_details["seasons"]
        #season_ids = list({v['id']:v for v in season_id}.values())   
        #print(season_ids)
        for s_id in season_ids: 
            #print(s_id)
            series_id = series_details['id']
            season_id = replace_none_with_empty_str(s_id)
            #print(series_id)
            #print(season_id)
            params ={}
            if 'id' in series_details:
                params['id'] = str(series_details['id'])
                #print(params)
            
            
            if 'air_date' in season_id:
                params['air_date'] = season_id['air_date']
            if 'episode_count' in season_id:
                params['episode_count'] = season_id['episode_count']
            if 'id' in season_id:
                params['tvseason_id'] = str(season_id['id'])
            if 'name' in season_id:
                params['name'] = season_id['name']
            if 'overview' in season_id:
                params['overview'] = season_id['overview']
            
            if 'poster_path' in season_id:
                params['poster_path'] = season_id['poster_path']
            if 'season_number' in season_id:
                params['season_number'] = season_id['season_number']
                   
                
                #print(params)
                
            payload={"query" : "MERGE (t:TvSeasons{ air_date :{air_date},episode_count : {episode_count},tvseason_id:{tvseason_id},name:{name},overview:{overview},poster_path:{poster_path},season_number:{season_number}}) RETURN t"}    
            payload['params'] = params
    # create or update production company
            response_json = callNeo4j(payload, headers)
            if response_json is not None:
                payload={"query" :"MATCH (t:TvSeries),(n:TvSeasons) WHERE t.id ={id} AND n.tvseason_id = {tvseason_id} MERGE (t)-[r:HAS_SEASON]->(n) RETURN r"}
                params = {}
                params['id'] = str(series_details['id'])
                params['tvseason_id'] = str(season_id['id'])
               
                payload['params'] = params
    #print(params)
                match_response_json = callNeo4j(payload, headers)
                print(match_response_json)


