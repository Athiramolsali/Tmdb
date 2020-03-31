import json
import requests
api_key_counter = 0
error_status = False
tv_series_id = '81355'
language = 'en-US'
season_number = '1'
episode_number = 1
#person_id = '66633'
import testing_tvseries_id 
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

def get_details_tmdb_tv_series(tv_series_id, language):
    try:
        api_key = get_random_api_key()
        tmdb_tv_series_url =  tmdb_tv_series_base_url + tv_series_id + '?api_key=' + api_key + '&language=' + language
        response = requests.request("GET", tmdb_tv_series_url)
        data = response.json()
        return(data)
    except Exception as e:
        global error_status
        error_status = True
        print("Function : get_details_tmdb_tv_series, Movie id: " + tv_series_id +  "\n Error : " + str(e)  )
        return None 




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
    
def replace_none_with_empty_str(some_dict):
    return { k: ('' if v is None else v) for k, v in some_dict.items() }


def callNeo4j(payload, headers):
    r= requests.post(neo4j_base_url, json = payload, headers = headers)
    response_json = json.loads(r.text)
    #print(r)
    return response_json

def series_created(tv_series_id):
    tmdb_tv_series = get_details_tmdb_tv_series(str(tv_series_id), language)
    tv_json = replace_none_with_empty_str(tmdb_tv_series)
    #tv_json["created_by"] =[dict(id=k1["id"],credit_id=k1["credit_id"]) for k1 in tv_json["created_by"]]
    series_created_id = tv_json["created_by"]
    for credit_ids in series_created_id:
        series_credit_id = replace_none_with_empty_str(credit_ids)
        params = {}
        if str(series_credit_id) != '':
            if 'id' in series_credit_id:
                params['person_id'] = str(series_credit_id['id'])
    
            if 'credit_id' in series_credit_id:
                params['credit_id'] = series_credit_id['credit_id']
            payload = {"query":"MATCH(n:Person{person_id:{person_id}}) SET n += {credit_id:{credit_id}} RETURN n"}
            payload['params'] = params
            response_json = callNeo4j(payload, headers)
            #print(response_json)
    else:
            if series_credit_id == '':
                if 'id' in tv_json:
                    params['id'] = str(series_credit_id['id'])
        
                if 'credit_id' in series_credit_id:
                    params['credit_id'] = series_credit_id['credit_id']
                payload = {"query":"MATCH(n:Person{person_id:{person_id}}) SET n += {credit_id:{credit_id}} RETURN n"}
                payload['params'] = params
                response_json = callNeo4j(payload, headers)




    
def tvseries_createdby_payload(tv_series_id, language):
   
        tmdb_tv_series = get_details_tmdb_tv_series(str(tv_series_id), language)
        tv_json = replace_none_with_empty_str(tmdb_tv_series)
        tv_json["created_by"] =[dict(id=k1["id"]) for k1 in tv_json["created_by"]]
        guest_id = tv_json["created_by"]
        id_list = [li['id'] for li in guest_id]

        for person_ids in id_list: 
            person_id = str(person_ids)
            person_detail = get_person_details(person_id, language)
            #print(person_detail)
            person_details = replace_none_with_empty_str(person_detail)

            #print(person_details)
            
            params = {}
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
    
            #print(params)
    
    
            payload = { "query" :"MERGE(n:Person{birthday:{birthday}, known_for_department:{known_for_department},deathday:{deathday},name:{name},person_id:{person_id},also_known_as:{also_known_as}, gender:{gender}, biography:{biography}, popularity:{popularity}, place_of_birth: {place_of_birth}, profile_path:{profile_path}, adult:{adult}, imdb_id:{imdb_id}, homepage:{homepage}}) RETURN n" }
            payload['params'] = params
    
            
            response_json = callNeo4j(payload, headers)
            person =  series_created(tv_series_id)
            
            if response_json is not None:
                person =  series_created(tv_series_id)

                payload={"query" :"MATCH (t:TvSeries),(n:Person) WHERE t.id ={id} AND n.person_id = {person_id} MERGE (t)-[r:CREATED_BY]->(n) RETURN r"}
                params = {}
                params['id'] = str(tv_json['id'])
                params['person_id'] = str(person_details['id'])
                tv_series_id = str(tv_json['id'])
                person_id =  str(person_details['id'])
                payload['params'] = params
                #print(params)
                match_response_json = callNeo4j(payload, headers)
                
                #print(match_response_json)

        
        
       
        #print(response_json)