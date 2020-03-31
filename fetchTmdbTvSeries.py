# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 14:13:32 2020

@author: viswa
"""

import json
import requests
api_key_counter = 0
error_status = False
tv_series_id = '1396'
language = 'en-US'

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
        return(data)
    except Exception as e:
        global error_status
        error_status = True
        print("Function : get_details_tmdb_movie, Movie id: " + tv_series_id +  "\n Error : " + str(e)  )
        print("Tv_series: " + tv_series)
        return None, None
    
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
        print("Function : get_details_tmdb_movie, Movie id: " + tv_series_id +  "\n Error : " + str(e)  )
        print("Tv_series: " + tv_series)
        return None, None
        
def get_recommendations(tv_series_id, language):
    try:
        tv_series = {}
        api_key = get_random_api_key()
        tmdb_recommendations_url =  tmdb_tv_series_base_url + tv_series_id+ '/recommendations' + '?api_key=' + api_key + '&language=' + language
        response = requests.request("GET", tmdb_recommendations_url)
        data = response.json()
        return(data)
    except Exception as e:
        global error_status
        error_status = True
        print("Function : get_details_tmdb_movie, Movie id: " + tv_series_id +  "\n Error : " + str(e)  )
        print("Tv_series: " + tv_series)
        return None, None
    
    
def get_details_tv_seasons(tv_series_id, language):
    try:
        tv_series = {}
        series_obj = get_details_tmdb_tv_series(tv_series_id, language)
        n_seasons = series_obj['number_of_seasons']
        for j in range(n_seasons):
            api_key = get_random_api_key()
            tmdb_season_url =  tmdb_tv_series_base_url + tv_series_id+ '/season/'+ str(j+1) + '?api_key=' + api_key + '&language=' + language
            response = requests.request("GET", tmdb_season_url)
            data = response.json()
        return(data)
    except Exception as e:
        global error_status
        error_status = True
        print("Function : get_details_tmdb_movie, Movie id: " + tv_series_id +  "\n Error : " + str(e)  )
        print("Tv_series: " + tv_series)
        return None, None
    
def get_credits_tv_seasons(tv_series_id, language):
    try:
        tv_series = {}
        series_obj = get_details_tmdb_tv_series(tv_series_id, language)
        n_seasons = series_obj['number_of_seasons']
        for j in range(n_seasons):
            api_key = get_random_api_key()
            tmdb_credits_tv_seasons_url =  tmdb_tv_series_base_url + tv_series_id + '/season/'+ str(j+1)+'/credits'+ '?api_key=' + api_key + '&language=' + language
            response = requests.request("GET", tmdb_credits_tv_seasons_url)
            data = response.json()
        return(data)
    except Exception as e:
        global error_status
        error_status = True
        print("Function : get_details_tmdb_movie, Movie id: " + tv_series_id +  "\n Error : " + str(e)  )
        print("Tv_series: " + tv_series)
        return None, None

def get_details_tv_episodes_details(tv_series_id, language):
    try:
        tv_series = {}
        series_obj = get_details_tmdb_tv_series(tv_series_id, language)
        n_seasons = series_obj['number_of_seasons']
        for i in range(0,n_seasons+1):
            season = i
            get_episodes_fn = get_episodes(tv_series_id,season)
        return(get_episodes_fn)
    except Exception as e:
        global error_status
        error_status = True
        print("Function : get_details_tmdb_movie, Movie id: " + tv_series_id +  "\n Error : " + str(e)  )
        print("Tv_series: " + tv_series)
        return None, None

def get_episodes(tv_series_id,season):
    try:
        
        tv_series = {}
        #series_obj = get_details_tmdb_tv_series(tv_series_id, language)
        api_key = get_random_api_key()
        tmdb_tv_series_url =  tmdb_tv_series_base_url + tv_series_id+ '?api_key=' + api_key + '&language=' + language
        response = requests.request("GET", tmdb_tv_series_url)
        data = response.json()
        data["seasons"] =[dict(episode_count=k1["episode_count"]) for k1 in data["seasons"]]
        jsonData = json.dumps(data)
        resp = json.loads(jsonData)
        #n_seasons = series_obj['number_of_seasons']
        no_of_episodes = resp['seasons'][season]['episode_count']
        for j in range(1,no_of_episodes+1):
            tmdb_episodes_url =  tmdb_tv_series_base_url + tv_series_id + '/season/'+ str(season) +'/episode/'+str(j)+ '?api_key=' + api_key + '&language=' + language
            response = requests.request("GET", tmdb_episodes_url)
            data = response.json()
        return(data)
    except Exception as e:
        global error_status
        error_status = True
        print("Function : get_details_tmdb_movie, Movie id: " + tv_series_id +  "\n Error : " + str(e)  )
        print("Tv_series: " + tv_series)
        return None, None

def get_credits_tv_episodes_details(tv_series_id, language):
    try:
        tv_series = {}
        series_obj = get_details_tmdb_tv_series(tv_series_id, language)
        n_seasons = series_obj['number_of_seasons']
        for i in range(0,n_seasons+1):
            season = i
            get_credicts_episode_fn = get_credits_episodes(tv_series_id,season)
        return(get_credicts_episode_fn)
    except Exception as e:
        global error_status
        error_status = True
        print("Function : get_details_tmdb_movie, Movie id: " + tv_series_id +  "\n Error : " + str(e)  )
        print("Tv_series: " + tv_series)
        return None, None
    
def get_credits_episodes(tv_series_id,season):
    try:
        
        tv_series = {}
        #series_obj = get_details_tmdb_tv_series(tv_series_id, language)
        api_key = get_random_api_key()
        tmdb_tv_series_url =  tmdb_tv_series_base_url + tv_series_id+ '?api_key=' + api_key + '&language=' + language
        response = requests.request("GET", tmdb_tv_series_url)
        data = response.json()
        data["seasons"] =[dict(episode_count=k1["episode_count"]) for k1 in data["seasons"]]
        jsonData = json.dumps(data)
        resp = json.loads(jsonData)
        #n_seasons = series_obj['number_of_seasons']
        no_of_episodes = resp['seasons'][season]['episode_count']
        for j in range(1,no_of_episodes+1):
            tmdb_credits_episodes_url =  tmdb_tv_series_base_url + tv_series_id + '/season/'+ str(season) +'/episode/'+str(j)+'/credits'+ '?api_key=' + api_key + '&language=' + language
            response = requests.request("GET", tmdb_credits_episodes_url)
            data = response.json()
            print(data)
        return(data)
    except Exception as e:
        global error_status
        error_status = True
        print("Function : get_details_tmdb_movie, Movie id: " + tv_series_id +  "\n Error : " + str(e)  )
        print("Tv_series: " + tv_series)
        return None, None
   
def get_images_tv_episodes_details(tv_series_id, language):
    try:
        tv_series = {}
        series_obj = get_details_tmdb_tv_series(tv_series_id, language)
        n_seasons = series_obj['number_of_seasons']
        for i in range(0,n_seasons+1):
            season = i
            api_key = get_random_api_key()
            get_images_episodes_fn = get_images_episodes(tv_series_id,season)
        return(get_images_episodes_fn)
    except Exception as e:
        global error_status
        error_status = True
        print("Function : get_details_tmdb_movie, Movie id: " + tv_series_id +  "\n Error : " + str(e)  )
        print("Tv_series: " + tv_series)
        return None, None
    
        
    
def get_images_episodes(tv_series_id,season):
    try:
        
        tv_series = {}
        series_obj = get_details_tmdb_tv_series(tv_series_id, language)
        api_key = get_random_api_key()
        tmdb_tv_series_url =  tmdb_tv_series_base_url + tv_series_id+ '?api_key=' + api_key + '&language=' + language
        response = requests.request("GET", tmdb_tv_series_url)
        data = response.json()
        data["seasons"] =[dict(episode_count=k1["episode_count"]) for k1 in data["seasons"]]
        jsonData = json.dumps(data)
        resp = json.loads(jsonData)
        n_seasons = series_obj['number_of_seasons']
        no_of_episodes = resp['seasons'][season]['episode_count']
        for j in range(1,no_of_episodes+1):
            tmdb_images_url =  tmdb_tv_series_base_url + tv_series_id + '/season/'+ str(season) +'/episode/'+str(j)+'/images'+ '?api_key=' + api_key + '&language=' + language
            response = requests.request("GET", tmdb_images_url)
            data = response.json()
        return(data)
    except Exception as e:
        global error_status
        error_status = True
        print("Function : get_details_tmdb_movie, Movie id: " + tv_series_id +  "\n Error : " + str(e)  )
        print("Tv_series: " + tv_series)
        return None, None

def get_videos_tv_episodes_details(tv_series_id, language):
    try:
        tv_series = {}
        series_obj = get_details_tmdb_tv_series(tv_series_id, language)
        n_seasons = series_obj['number_of_seasons']
        for i in range(0,n_seasons+1):
            season = i
            api_key = get_random_api_key()
            get_video_episodes_fn = get_video_episodes(tv_series_id,season)
        return(get_video_episodes_fn)
    except Exception as e:
        global error_status
        error_status = True
        print("Function : get_details_tmdb_movie, Movie id: " + tv_series_id +  "\n Error : " + str(e)  )
        print("Tv_series: " + tv_series)
        return None, None

def get_video_episodes(tv_series_id,season):
    try:
        
        tv_series = {}
        series_obj = get_details_tmdb_tv_series(tv_series_id, language)
        api_key = get_random_api_key()
        tmdb_tv_series_url =  tmdb_tv_series_base_url + tv_series_id+ '?api_key=' + api_key + '&language=' + language
        response = requests.request("GET", tmdb_tv_series_url)
        data = response.json()
        data["seasons"] =[dict(episode_count=k1["episode_count"]) for k1 in data["seasons"]]
        jsonData = json.dumps(data)
        resp = json.loads(jsonData)
        #n_seasons = series_obj['number_of_seasons']
        no_of_episodes = resp['seasons'][season]['episode_count']
        for j in range(1,no_of_episodes+1):
            tmdb_videos_episode_url =  tmdb_tv_series_base_url + tv_series_id + '/season/'+ str(season) +'/episode/'+str(j)+'/images'+ '?api_key=' + api_key + '&language=' + language
            response = requests.request("GET", tmdb_videos_episode_url)
            data = response.json()
        return(data)
    except Exception as e:
        global error_status
        error_status = True
        print("Function : get_details_tmdb_movie, Movie id: " + tv_series_id +  "\n Error : " + str(e)  )
        print("Tv_series: " + tv_series)
        return None, None