import json
import requests
from TvSeriesToNeo4j import tvseries_to_neo4j,next_episode,last_episode
from TvSeriesGenreRelation import create_match_genre_tvseries
from MatchTvSeriesProductionCmpny import productioncompany_payload
from TvSeriesCreatedByRelationship import tvseries_createdby_payload
from TvSeriesCreditsCastDetails import tv_series_cast_details
from MatchTvSeriesWithSeason import tv_series_season_payload 
from MatchTvSeriesSeasonEpisode import tv_series_season_episodes_payload
from MatchJobTypesOfCrewTvseries import tv_series_job_types_crew

api_key_counter = 0
error_status = False
tv_series_id = '19885'
language = 'en-US'
headers = {"Authorization":"Basic bmVvNGo6dm9ubnVl"}
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
    #print(r)
    return response_json

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



def get_similar_tv_shows_tv_series(tv_series_id, language):
    try:
        tv_series = {}
        api_key = get_random_api_key()
        tmdb_similar_tv_shows_url =  tmdb_tv_series_base_url + tv_series_id+ '/similar' + '?api_key=' + api_key + '&language=' + language
        response = requests.request("GET", tmdb_similar_tv_shows_url)
        data = response.json()
        #print(data)
        return(data)
    except Exception as e:
        global error_status
        error_status = True
        print("Function : get_similar_tv_shows_tv_series, Movie id: " + tv_series_id +  "\n Error : " + str(e)  )
        print("Tv_series: " + tv_series)
        return None, None

def get_details_tmdb_tv_series(tv_series_id, language):
    try:
        tv_series = {}
        api_key = get_random_api_key()
        tmdb_tv_series_url =  tmdb_tv_series_base_url + str(tv_series_id)+ '?api_key=' + api_key + '&language=' + language
        response = requests.request("GET", tmdb_tv_series_url)
        data = response.json()
        return(data)
    except Exception as e:
        global error_status
        error_status = True
        print("Function : get_details_tmdb_movie, Movie id: " + str(tv_series_id) +  "\n Error : " + str(e)  )
        print("Tv_series: " + tv_series)
        return None, None



    
    
def similar_payload(tv_series_id):
   
    #tv_series_id = '19885'  
    tvseriesdetails = get_details_tmdb_tv_series(tv_series_id, language)
    similar_fn = get_similar_tv_shows_tv_series(tv_series_id, language)
    similar_fn["results"] =[dict(id=k1["id"],name = k1['name'],original_name=k1['original_name'],vote_count=k1['vote_count'],vote_average=k1['vote_average'],first_air_date=k1['first_air_date'],poster_path=k1['poster_path'],original_language=k1['original_language'],backdrop_path=k1['backdrop_path'],overview=k1['overview'],popularity=k1['popularity']) for k1 in similar_fn["results"]]
    #tvseriesdetails = get_details_tmdb_tv_series(tv_series_id, language)
    #tv_json = replace_none_with_empty_str(tvseries)

    similar = similar_fn["results"]
    #tvseriesid= str(tvseriesdetails["id"])
    #print(tvseriesid)
    for s in similar:
        similar_tv_shows = s
        
        similar_tv_series_id = s.get('id')
        tvseries = get_details_tmdb_tv_series(similar_tv_series_id, language)
        tv_json = replace_none_with_empty_str(tvseries)

        tv_series_node = tvseries_to_neo4j(similar_tv_series_id)
        tv_next = next_episode(similar_tv_series_id)
        tv_last = last_episode(similar_tv_series_id)
       
        payload={"query" :"MATCH (t:TvSeries),(n:TvSeries) WHERE t.id ={tv_series_id} AND n.id = {id} MERGE (t)-[r:IS_SIMILAR_TO]->(n) RETURN r"}
        params = {}
        params['tv_series_id'] = str(tvseriesdetails['id'])
        params['id'] = str(tv_json['id'])
        
        #print(params)
        payload['params'] = params
        #print(params)
        response_json = callNeo4j(payload, headers)
        
        join = create_match_genre_tvseries(str(similar_tv_series_id))
        match_tvseries_production_cmpny = productioncompany_payload(str(similar_tv_series_id), language)
        match_created_by = tvseries_createdby_payload(str(similar_tv_series_id), language)
        match_tvseries_crew = tv_series_cast(str(similar_tv_series_id))
        match_tvseries_crew = tv_series_job_types_crew(str(similar_tv_series_id))

        matchkeywords = keyword_payload(str(similar_tv_series_id))
        cast_credits = tv_series_cast_details(str(similar_tv_series_id))
        match_seasons = tv_series_season_payload(str(similar_tv_series_id), language)
        match_season_episode = tv_series_season_episodes_payload(str(similar_tv_series_id), language)

                
        




















