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
import requests
import twitter

# import the module
import tweepy

import sys
#!{sys.executable} -m pip install python-twitter 
import dotenv as dte
dte.load_dotenv()


# Originally stored access in a private environment but would not be able to access this on github
#Gets the parameters needed to access the API's from my private enviroment
twitterConsumerKey = os.environ.get("twitter_consumer_key")
twitterConsumerSecret = os.environ.get("twitter_consumer_secret")
twitterAccessToken = os.environ.get("twitter_access_token")
twitterAccessSecret = os.environ.get("twitter_access_secret")

#This is the Deepsocial account's twitter tokens
twitterConsumerKeyDs = os.environ.get("twitter_consumer_keyDs")
twitterConsumerSecretDs = os.environ.get("twitter_consumer_secretDs")
twitterAccessTokenDs = os.environ.get("twitter_access_tokenDs")
twitterAccessSecretDs = os.environ.get("twitter_access_secretDs")


auth = tweepy.OAuthHandler(twitterConsumerKey, twitterConsumerSecret)
auth.set_access_token(twitterAccessToken, twitterAccessSecret)

authDs = tweepy.OAuthHandler(twitterConsumerKeyDs, twitterConsumerSecretDs)
authDs.set_access_token(twitterAccessTokenDs, twitterAccessSecretDs)

api = tweepy.API(auth)

apiDs = tweepy.API(authDs)

#Enters the info to get access the twitter API and stores it
twitterAPI = twitter.Api(consumer_key=twitterConsumerKey, 
                          consumer_secret=twitterConsumerSecret, 
                          access_token_key=twitterAccessToken, 
                          access_token_secret=twitterAccessSecret)

twitterAPIDS = twitter.Api(consumer_key=twitterConsumerKeyDs, 
                          consumer_secret=twitterConsumerSecretDs, 
                          access_token_key=twitterAccessTokenDs, 
                          access_token_secret=twitterAccessSecretDs)



#Allows a user to post an update
def postStatus(message):
    #post the tweet an get the data about the new tweet
    status = twitterAPI.PostUpdate(message)
    #Use the tweet data to get the id to allow for deepsocial account to post and like the tweet
    RetweetStatus(status.id)
    likeStatus(status.id)
    return status

# Allows deep social to like and retweet the generated tweet
def likeStatus(id):
    apiDs.create_favorite(id)

def RetweetStatus(id):
    apiDs.retweet(id)



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

#Get the most popular tweets
def getPopularTweets():
    
    search = twitterAPI.GetSearch(raw_query=None, geocode=None, since_id=None, max_id=None, until=None, 
              since=None, count=20000, lang=None, locale=None, result_type='popular', include_entities=True, 
              return_json=True)
    
    return search





