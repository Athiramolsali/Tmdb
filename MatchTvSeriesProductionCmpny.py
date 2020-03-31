import json
import requests
api_key_counter = 0
error_status = False
#tv_series_id = '13916'
language = 'en-US'
#season_number = '1'
#episode_number = 1
#person_id = '66633'
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


def callNeo4j(payload, headers):
    r= requests.post(neo4j_base_url, json = payload, headers = headers)
    response_json = json.loads(r.text)
    return response_json






        #print(response_json)
def productioncompany_payload(tv_series_id, language):
    
        tv_json  = get_details_tmdb_tv_series(tv_series_id, language)
        production_company = tv_json['production_companies']
        
        for production_cmpny_ids in production_company:
            production_cmpny = replace_none_with_empty_str(production_cmpny_ids)
            params = {}
            if 'id' in tv_json:
                params['id'] = str(tv_json['id'])                   
            
            if 'name' in production_cmpny:
                params['name'] = production_cmpny['name']
            if 'id' in production_cmpny:
                params['production_company_id'] = str(production_cmpny['id'])
            if 'logo_path' in production_cmpny:
                params['logo_path'] = production_cmpny['logo_path']
           
            if 'origin_country' in production_cmpny:
                params['origin_country'] = production_cmpny['origin_country']
                   
                
            payload={"query" : "MERGE (p:ProductionCompany{ name :{name},production_company_id : {production_company_id},logo_path:{logo_path},origin_country:{origin_country}}) RETURN p"}    
            payload['params'] = params
            response_json = callNeo4j(payload, headers)
            if response_json is not None:
                payload={"query" :"MATCH (t:TvSeries),(p:ProductionCompany) WHERE t.id ={tv_series_id} AND p.production_company_id = {production_company_id} MERGE (t)-[r:PRODUCTION_COMPANIES]->(p) RETURN r"}
                params = {}
                params['tv_series_id'] = str(tv_json['id'])
                params['production_company_id'] = str(production_cmpny['id'])
                tv_series_id = str(tv_json['id'])
                production_company_id =  str(production_cmpny['id'])
                payload['params'] = params
                match_production_response_json = callNeo4j(payload, headers)
                print(match_production_response_json)