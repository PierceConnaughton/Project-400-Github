#!/usr/bin/env python
# coding: utf-8

#Importing all neccassary libraries
#to send get requests from API
import requests
#to save access tokens
import os
#Used for json responses
import json
import pandas as pd
#parse the dates and time into a readable formate
import datetime
import dateutil.parser
import unicodedata
#Used for checking the wait time between requests
import time

import twitter

import sys
#!{sys.executable} -m pip install python-twitter 
import dotenv as dte
dte.load_dotenv()


#Gets the parameters needed to access the API from my private enviroment
twitterConsumerKey = os.environ.get("twitter_consumer_key")
twitterConsumerSecret = os.environ.get("twitter_consumer_secret")
twitterAccessToken = os.environ.get("twitter_access_token")
twitterAccessSecret = os.environ.get("twitter_access_secret")




#Enters the info to get access the twitter API and stores it
twitterAPI = twitter.Api(consumer_key=twitterConsumerKey, 
                          consumer_secret=twitterConsumerSecret, 
                          access_token_key=twitterAccessToken, 
                          access_token_secret=twitterAccessSecret)



#Allows a user to post an update
def postStatus(message):
    status = twitterAPI.PostUpdate(message)
    return status

#Allows a user to get last 200 tweets from a specific user
def getTimeline(handle):
    timeline = twitterAPI.GetUserTimeline(screen_name=handle, count=200, include_rts=False)
    return timeline

def getPopularTweetsTerm(term):
    
    #term: what to search by. Optional if you include geocode.
    #since_id: get results more recent then specified ID
    #max_id: return results that are older then specified ID
    #until: returns tweets before given date
    #since: returns tweets after given date
    #geocode: location where to search tweets
    #count: number of results to return
    #result_type: type of result to return eg:recent, popular, mixed
    #include_entities: If true returns meta data of tweet such as hashtags
    #return_json: if true returns data as json instead of twitter.Userret
    
    search = twitterAPI.GetSearch(term = term, raw_query=None, geocode=None, since_id=None, max_id=None, until=None, 
              since=None, count=20000, lang=None, locale=None, result_type='popular', include_entities=True, 
              return_json=True)
    
    return search

def getPopularTweets():
    
    search = twitterAPI.GetSearch(raw_query=None, geocode=None, since_id=None, max_id=None, until=None, 
              since=None, count=20000, lang=None, locale=None, result_type='popular', include_entities=True, 
              return_json=True)
    
    return search





