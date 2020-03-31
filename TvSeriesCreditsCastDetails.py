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


    
'''
Place holder for def tmdb_movie function equivalent in jomys code

'''

    
def get_details_tmdb_tv_series(tv_series_id, language):
    try:
        tv_series = {}
        api_key = get_random_api_key()
        tmdb_tv_series_url =  tmdb_tv_series_base_url + tv_series_id+ '?api_key=' + api_key + '&language=' + language
        response = requests.request("GET", tmdb_tv_series_url)
        data = response.json()
        return(data)
    except Exception as e:
        global error_status
        error_status = True
        print("Function : get_details_tmdb_movie, Movie id: " + tv_series_id +  "\n Error : " + str(e)  )
        print("Tv_series: " + tv_series)
        return None, None
    
def get_credits_tv_series(tv_series_id,language):
    try:
        tv_series = {}
        api_key = get_random_api_key()
        tmdb_credits_url =  tmdb_tv_series_base_url + tv_series_id+ '/credits' + '?api_key=' + api_key + '&language=' + language
        response = requests.request("GET", tmdb_credits_url)
        data = response.json()
        #print(data)
        return(data)
    except Exception as e:
        global error_status
        error_status = True
        print("Function : get_details_tmdb_movie, Movie id: " + tv_series_id +  "\n Error : " + str(e)  )
        print("Tv_series: " + tv_series)
        return None, None

def get_person_details(persons_id, language):
    try:
        api_key = get_random_api_key()
        tmdb_person_details_url =  tmdb_person_base_url + persons_id+ '?api_key=' + api_key + '&language=' + language
        response = requests.request("GET", tmdb_person_details_url)
        data = response.json()
        return(data)
    except Exception as e:
        global error_status
        error_status = True
        print("Function : get_person_details, Person id: " + person_id +  "\n Error : " + str(e)  )
        return None
    




def callNeo4j(payload, headers):
    r= requests.post(neo4j_base_url, json = payload, headers = headers)
    response_json = json.loads(r.text)
    #print(r)
    return response_json



def replace_none_with_empty_str(some_dict):
    return { k: ('' if v is None else v) for k, v in some_dict.items() }

    
    
def tv_series_cast_details(tv_series_id):
    
    series_cast = get_credits_tv_series(tv_series_id,language)
    series_cast["cast"] =[dict(character = k1["character"],credit_id=k1["credit_id"],id= k1["id"],name=k1["name"],gender=k1["gender"],order=k1["order"]) for k1 in series_cast["cast"]]
    casts_data = series_cast["cast"]
    for cast in casts_data:
        cast_details = cast
        cast_ids = cast_details['id']
        persons_id = str(cast_ids)
        person_detail = get_person_details(persons_id, language)
        person_details = replace_none_with_empty_str(person_detail)
        #print(person_details)        
        
        
        params = {}
        if 'character' in cast_details:
            params['character'] = cast_details['character']
        if 'credit_id' in cast_details:
            params['credit_id'] = cast_details['credit_id']
        if 'name' in cast_details:
            params['name'] = cast_details['name']
        if 'gender' in cast_details:
            params['gender'] = cast_details['gender']
        if 'order' in cast_details:
            params['order'] = cast_details['order']


        if 'id' in series_cast:
            params['id'] = str(series_cast['id'])
        if 'birthday' in person_details:
            params['birthday'] = person_details['birthday']
        if 'known_for_department' in person_details:
            params['known_for_department'] = person_details['known_for_department']
        if 'deathday' in person_details:
            params['deathday'] = person_details['deathday']
        if 'id' in person_details:
            params['person_id'] = str(person_details['id'])
        if 'name' in person_details:
            params['name'] = person_details['name']
        
        if 'also_known_as' in person_details:
            params['also_known_as'] = person_details['also_known_as']
        if 'gender' in person_details:
            params['gender'] = person_details['gender']
        if 'biography' in person_details:
            params['biography'] = person_details['biography']
        if 'popularity' in person_details:
            params['popularity'] = person_details['popularity']
        if 'place_of_birth' in person_details:
            params['place_of_birth'] = person_details['place_of_birth']
        if 'profile_path' in person_details:
            params['profile_path'] = person_details['profile_path']
        if 'adult' in person_details:
            params['adult'] = person_details['adult']
        if 'imdb_id' in person_details:
            params['imdb_id'] = person_details['imdb_id']
        if 'homepage' in person_details:
            params['homepage'] = person_details['homepage']

       

        payload = { "query" :"MERGE(n:Person{birthday:{birthday}, known_for_department:{known_for_department},deathday:{deathday},name:{name},person_id:{person_id},also_known_as:{also_known_as}, gender:{gender}, biography:{biography}, popularity:{popularity}, place_of_birth: {place_of_birth}, profile_path:{profile_path}, adult:{adult}, imdb_id:{imdb_id}, homepage:{homepage}}) RETURN n" }
        payload['params'] = params

        
        response_json = callNeo4j(payload, headers)
        if response_json is not None:
            payload={"query" :"MATCH (t:TvSeries),(p:Person) WHERE t.id ={tv_series_id} AND p.person_id = {person_id} MERGE (t)-[r:HAS_CAST{person_id:{person_id}, credit_id:{credit_id},character:{character},gender:{gender},order:{order}}]->(p) RETURN r"}
            params = {}
            params['tv_series_id'] = str(series_cast['id'])
            params['person_id'] = str(person_details['id'])
            params['character'] = cast_details['character']
            params['credit_id'] = cast_details['credit_id']
            params['gender'] = cast_details['gender']
            params['order'] = cast_details['order']
        
            
            payload['params'] = params
            #print(payload['params'])
            match_response_json = callNeo4j(payload, headers)
            print(match_response_json)
            
    