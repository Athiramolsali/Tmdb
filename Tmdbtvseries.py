# -*- coding: utf-8 -*-
import json
import requests
api_key_counter = 0
error_status = False
tv_series_id = '1396'
language = 'en-US'
season_number = '1'
episode_number = 1
person_id = '66633'


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
        tmdb_tv_series_url =  tmdb_tv_series_base_url + tv_series_id+ '?api_key=' + api_key + '&language=' + language
        response = requests.request("GET", tmdb_tv_series_url)
        data = response.json()
        return(data)
    except Exception as e:
        global error_status
        error_status = True
        print("Function : get_details_tmdb_tv_series, Movie id: " + tv_series_id +  "\n Error : " + str(e)  )
        return None

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

def get_details_tv_episodes_details(tv_series_id,season_number,episode_number ):
    try:
        api_key = get_random_api_key()
        tmdb_episodes_url =  tmdb_tv_series_base_url + tv_series_id + '/season/'+ str(season_number) +'/episode/'+str(episode_number)+ '?api_key=' + api_key + '&language=' + language
        response = requests.request("GET", tmdb_episodes_url)
        data = response.json()
        return(data)
    except Exception as e:
        global error_status
        error_status = True
        print("Function : get_details_tv_episodes_details, TV Series id: " + str(tv_series_id) +  "\n Error : " + str(e)  )
        print("Tv_series: " + tv_series_id)
        return None


def get_person_details(persons_id, language):
    try:
        api_key = get_random_api_key()
        tmdb_person_details_url =  tmdb_person_base_url + persons_id+ '?api_key=' + api_key + '&language=' + language
        #print(tmdb_person_details_url)
        response = requests.request("GET", tmdb_person_details_url)
        data = response.json()
        return(data)
    except Exception as e:
        global error_status
        error_status = True
        print("Function : get_person_details, Person id: " + person_id +  "\n Error : " + str(e)  )
        return None

