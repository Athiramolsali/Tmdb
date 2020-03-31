import json
import requests
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
        tmdb_credits_url =  tmdb_tv_series_base_url + str(tv_series_id)+ '/credits' + '?api_key=' + api_key + '&language=' + language
        response = requests.request("GET", tmdb_credits_url)
        data = response.json()
        #print(data)
        return(data)
    except Exception as e:
        global error_status
        error_status = True
        print("Function : get_credits_tv_series, Movie id: " + str(tv_series_id) +  "\n Error : " + str(e)  )
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

    
    
def tv_series_job_types_crew(tv_series_id):
    series_cast = get_credits_tv_series(tv_series_id,language)
    #print(series_cast)
    series_cast["crew"]=[dict(id = k1["id"],department=k1["department"],credit_id=k1["credit_id"],gender=k1["gender"],job=k1["job"])for k1 in series_cast["crew"]]
    crew_data = series_cast["crew"]
    tv_series_id = series_cast['id']
    for crew_job in crew_data:
        cast_details = crew_job
        job = crew_job.get("job")
        person_id = str(crew_job['id'])
        #print(person_id)

        person_detail = get_person_details(person_id, language)
        person_details = replace_none_with_empty_str(person_detail)

        params = {}
        
        if 'credit_id' in cast_details:
           params['credit_id'] = cast_details['credit_id']
        if 'department' in cast_details:
           params['department'] = cast_details['department']
        if 'gender' in cast_details:
            params['gender'] = cast_details['gender']
        if 'job' in cast_details:
            params['job'] = cast_details['job']


        if 'id' in series_cast:
            params['id'] = str(series_cast['id'])
            #print(params)
            
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
            
            
            

        payload = { "query" :"MERGE(n:Person{birthday:{birthday}, known_for_department:{known_for_department},deathday:{deathday},name:{name},person_id:{person_id},also_known_as:{also_known_as}, gender:{gender}, biography:{biography}, popularity:{popularity}, place_of_birth: {place_of_birth}, profile_path:{profile_path}, adult:{adult}, imdb_id:{imdb_id}, homepage:{homepage}}) RETURN n"}
        payload['params'] = params

        
        response_json = callNeo4j(payload, headers)
        if response_json is not None:
            params = {}
            
            if 'credit_id' in cast_details:
                params['credit_id'] = cast_details['credit_id']
            if 'department' in cast_details:
               params['department'] = cast_details['department']
            if 'gender' in cast_details:
                params['gender'] = cast_details['gender']
            if 'job' in cast_details:
                params['job'] = cast_details['job']
    
    
            if 'id' in series_cast:
                params['id'] = str(series_cast['id'])
            if 'id' in person_details:
                params['person_id'] = str(person_details['id'])
                #print(params)
            
            if job == 'Executive Producer':
                 payload={"query" :"MATCH (s:TvSeries),(n:Person) WHERE s.id={id} AND n.person_id = {person_id} MERGE (s)-[r:EXECUTIVE_PRODUCER{person_id:{person_id}, credit_id:{credit_id},department:{department},gender:{gender},job:{job}}]->(n) RETURN r"}
                 params = {}
                 params['id'] = str(series_cast['id'])
                 params['person_id'] = str(person_details['id'])
                 params['department'] = cast_details['department']
                 params['credit_id'] = cast_details['credit_id']
                 params['gender'] = cast_details['gender']
                 params['job'] = cast_details['job']
            
                 person_id =   str(person_details['id'])
                 tv_series_id = str(series_cast['id'])
                
                 payload['params'] = params
                 response_json = callNeo4j(payload, headers)

            if job == 'Costume Design':
                 payload={"query" :"MATCH (s:TvSeries),(n:Person) WHERE s.id={id} AND n.person_id = {person_id} MERGE (s)-[r:COSTUME_DESIGN_BY{person_id:{person_id}, credit_id:{credit_id},department:{department},gender:{gender},job:{job}}]->(n) RETURN r"}
                 params = {}
                 params['id'] = str(series_cast['id'])
                 params['person_id'] = str(person_details['id'])
                 params['department'] = cast_details['department']
                 params['credit_id'] = cast_details['credit_id']
                 params['gender'] = cast_details['gender']
                 params['job'] = cast_details['job']
            
                 person_id =   str(person_details['id'])
                 tv_series_id = str(series_cast['id'])
                
                 payload['params'] = params
                 response_json = callNeo4j(payload, headers)

            if job == 'Original Music Composer':
                 payload={"query" :"MATCH (s:TvSeries),(n:Person) WHERE s.id = {id} AND n.person_id = {person_id} MERGE (s)-[r:ORIGINAL_MUSIC_COMPOSER{person_id:{person_id}, credit_id:{credit_id},department:{department},gender:{gender},job:{job}} ]->(n) RETURN r"}
                 params = {}
                 params['id'] = str(series_cast['id'])
                 params['person_id'] = str(person_details['id'])
                 params['department'] = cast_details['department']
                 params['credit_id'] = cast_details['credit_id']
                 params['gender'] = cast_details['gender']
                 params['job'] = cast_details['job']
            
                 person_id =   str(person_details['id'])
                 tv_series_id = str(series_cast['id'])
                
                 payload['params'] = params
                 response_json = callNeo4j(payload, headers)

            if job == 'Production Design':
                 payload={"query" :"MATCH (s:TvSeries),(n:Person) WHERE s.id = {id} AND n.person_id = {person_id} MERGE (s)-[r:PRODUCTION_DESIGN_BY{person_id:{person_id}, credit_id:{credit_id},department:{department},gender:{gender},job:{job}}]->(n) RETURN r"}
                 params = {}
                 params['id'] = str(series_cast['id'])
                 params['person_id'] = str(person_details['id'])
                 params['department'] = cast_details['department']
                 params['credit_id'] = cast_details['credit_id']
                 params['gender'] = cast_details['gender']
                 params['job'] = cast_details['job']
            
                 person_id =   str(person_details['id'])
                 tv_series_id = str(series_cast['id'])
                
                 payload['params'] = params
                 response_json = callNeo4j(payload, headers)

            if job == 'Producer':
                 payload={"query" :"MATCH (s:TvSeries),(n:Person) WHERE s.id = {id} AND n.person_id = {person_id} MERGE (s)-[r:PRODUCED_BY{person_id:{person_id}, credit_id:{credit_id},department:{department},gender:{gender},job:{job}}]->(n) RETURN r"}
                 params = {}
                 params['id'] = str(series_cast['id'])
                 params['person_id'] = str(person_details['id'])
                 params['department'] = cast_details['department']
                 params['credit_id'] = cast_details['credit_id']
                 params['gender'] = cast_details['gender']
                 params['job'] = cast_details['job']
            
                 person_id =   str(person_details['id'])
                 tv_series_id = str(series_cast['id'])
                
                 payload['params'] = params
                 response_json = callNeo4j(payload, headers)

            if job == 'Music Producer':
                payload={"query" :"MATCH (s:TvSeries),(n:Person) WHERE s.id={id} AND n.person_id = {person_id} MERGE (s)-[r:MUSIC_PRODUCED_BY{person_id:{person_id}, credit_id:{credit_id},department:{department},gender:{gender},job:{job}}]->(n) RETURN r"}
                params = {}
                params['id'] = str(series_cast['id'])
                params['person_id'] = str(person_details['id'])
                params['department'] = cast_details['department']
                params['credit_id'] = cast_details['credit_id']
                params['gender'] = cast_details['gender']
                params['job'] = cast_details['job']
            
                person_id =   str(person_details['id'])
                tv_series_id = str(series_cast['id'])
                
                payload['params'] = params
                response_json = callNeo4j(payload, headers)

            if job == 'Special Effects Makeup Artist':
                payload={"query" :"MATCH (s:TvSeries),(n:Person) WHERE s.id={id} AND n.person_id = {person_id} MERGE (s)-[r:SPECIAL_EFFECTS_MAKEUP_ARTIST {person_id:{person_id}, credit_id:{credit_id},department:{department},gender:{gender},job:{job}}]->(n) RETURN r"}
                params = {}
                params['id'] = str(series_cast['id'])
                params['person_id'] = str(person_details['id'])
                params['department'] = cast_details['department']
                params['credit_id'] = cast_details['credit_id']
                params['gender'] = cast_details['gender']
                params['job'] = cast_details['job']
            
                person_id =   str(person_details['id'])
                tv_series_id = str(series_cast['id'])
                
                payload['params'] = params
                response_json = callNeo4j(payload, headers)

           
            if job == 'Editorial Production Assistant':
                payload={"query" :"MATCH (s:TvSeries),(n:Person) WHERE s.id={id} AND n.person_id = {person_id} MERGE (s)-[r:EDITORIAL_PRODUCTION_ASSISTANT{person_id:{person_id}, credit_id:{credit_id},department:{department},gender:{gender},job:{job}}]->(n) RETURN r"}
                params = {}
                params['id'] = str(series_cast['id'])
                params['person_id'] = str(person_details['id'])
                params['department'] = cast_details['department']
                params['credit_id'] = cast_details['credit_id']
                params['gender'] = cast_details['gender']
                params['job'] = cast_details['job']
            
                person_id =   str(person_details['id'])
                tv_series_id = str(series_cast['id'])
                
                payload['params'] = params
                response_json = callNeo4j(payload, headers)
            if job == 'Set Decoration':
                payload={"query" :"MATCH (s:TvSeries),(n:Person) WHERE s.id={id} AND n.person_id = {person_id} MERGE (s)-[r:SET_DECORATION_BY{person_id:{person_id}, credit_id:{credit_id},department:{department},gender:{gender},job:{job}}]->(n) RETURN r"}
                params = {}
                params['id'] = str(series_cast['id'])
                params['person_id'] = str(person_details['id'])
                params['department'] = cast_details['department']
                params['credit_id'] = cast_details['credit_id']
                params['gender'] = cast_details['gender']
                params['job'] = cast_details['job']
            
                person_id =   str(person_details['id'])
                tv_series_id = str(series_cast['id'])
                
                payload['params'] = params
                response_json = callNeo4j(payload, headers)

            if job == 'Sound Re-Recording Mixer':
                payload={"query" :"MATCH (s:TvSeries),(n:Person) WHERE s.id={id} AND n.person_id = {person_id} MERGE (s)-[r:SOUND_RE_RECORDING_MIXER{person_id:{person_id}, credit_id:{credit_id},department:{department},gender:{gender},job:{job}}]->(n) RETURN r"}
                params = {}
                params['id'] = str(series_cast['id'])
                params['person_id'] = str(person_details['id'])
                params['department'] = cast_details['department']
                params['credit_id'] = cast_details['credit_id']
                params['gender'] = cast_details['gender']
                params['job'] = cast_details['job']
            
                person_id =   str(person_details['id'])
                tv_series_id = str(series_cast['id'])
                
                payload['params'] = params
                response_json = callNeo4j(payload, headers)

            if job == 'Special Effects Supervisor':
                payload={"query" :"MATCH (s:TvSeries),(n:Person) WHERE s.id = {id} AND n.person_id = {person_id} MERGE (s)-[r:SPECIAL_EFFECTS_SUPERVISOR{person_id:{person_id}, credit_id:{credit_id},department:{department},gender:{gender},job:{job}} ]->(n) RETURN r"}
                params = {}
                params['id'] = str(series_cast['id'])
                params['person_id'] = str(person_details['id'])
                params['department'] = cast_details['department']
                params['credit_id'] = cast_details['credit_id']
                params['gender'] = cast_details['gender']
                params['job'] = cast_details['job']
            
                person_id =   str(person_details['id'])
                tv_series_id = str(series_cast['id'])
                
                payload['params'] = params
                response_json = callNeo4j(payload, headers)

            if job == 'First Assistant Camera':
                payload={"query" :"MATCH (s:TvSeries),(n:Person) WHERE s.id = {id} AND n.person_id = {person_id} MERGE (s)-[r:FIRST_ASSISTANT_CAMERA{person_id:{person_id}, credit_id:{credit_id},department:{department},gender:{gender},job:{job}} ]->(n) RETURN r"}
                params = {}
                params['id'] = str(series_cast['id'])
                params['person_id'] = str(person_details['id'])
                params['department'] = cast_details['department']
                params['credit_id'] = cast_details['credit_id']
                params['gender'] = cast_details['gender']
                params['job'] = cast_details['job']
            
                person_id =   str(person_details['id'])
                tv_series_id = str(series_cast['id'])
                
                payload['params'] = params
                response_json = callNeo4j(payload, headers)

                
                
        else:
                print("error")
            
            
            
            #match_response_json = join_tv_cast(tv_series_id, person_id)
        #rint(match_response_json)
            
    



