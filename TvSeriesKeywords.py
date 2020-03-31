import json
import requests
api_key_counter = 0
error_status = False
tv_series_id = '1396'
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


def get_keywords(tv_series_id, language):
    try:
        tv_series={}
        api_key = get_random_api_key()
        tmdb_keywords_url = tmdb_tv_series_base_url + tv_series_id+ '/keywords' + '?api_key=' + api_key + '&language=' + language
        response = requests.request("GET", tmdb_keywords_url)
        data = response.json()
        return(data)
    except Exception as e:
        global error_status
        error_status = True
        print("Function : get_keywords, Movie id: " + tv_series_id +  "\n Error : " + str(e)  )
        print("Tv_series: " + tv_series)
        return None, None




def join_tv_series_keyword(tv_series_id, keyword_id):
    payload={"query" :"MATCH (s:TvSeries),(n:Keywords) WHERE s.id = {id} AND n.keyword_id = {keyword_id} MERGE (s)-[r:HAS_KEYWORDS]->(n) RETURN r"}
    params = {}
    params['id'] = str(keyword_fn["id"])
    params['keyword_id'] = str(keywords['id'])
    
    keyword_id =   str(keywords['id'])
    tv_series_id =  str(keyword_fn["id"])

    
    payload['params'] = params
    response_json = callNeo4j(payload, headers)
    #print(response_json)



    
    
def keyword_payload(tv_series_id):
   
    tv_series_id = str(tv_series_id)    
    keyword_fn = get_keywords(tv_series_id, language)
    keyword_fn["results"] =[dict(id=k1["id"],name = k1['name']) for k1 in keyword_fn["results"]]
    keys = keyword_fn["results"]
    tvseriesid= str(keyword_fn["id"])
    
    #print(tvseriesid)
    for k in keys:
        keywords = k
        
        params = {}
        if 'id' in tvseriesid:
            params['id'] = str(keyword_fn["id"])
        if 'id' in keywords:
            params['keyword_id'] = str(keywords['id'])
        if 'name' in keywords:
            params['keyword'] = keywords['name']
            #print(params)
            
        payload = { "query" :"MERGE(n:Keywords{keyword_id:{keyword_id},keyword:{keyword}}) RETURN n"}
        payload['params'] = params         
        response_json = callNeo4j(payload, headers)
        if response_json is not None:
            payload={"query" :"MATCH (s:TvSeries),(n:Keywords) WHERE s.id = {id} AND n.keyword_id = {keyword_id} MERGE (s)-[r:HAS_KEYWORDS]->(n) RETURN r"}
            params = {}
            params['id'] = str(keyword_fn["id"])
            params['keyword_id'] = str(keywords['id'])
            
            
        
            
            payload['params'] = params
            match_response_json = callNeo4j(payload, headers)
            #print(match_response_json)
    

    