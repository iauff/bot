# -*- coding: iso-8859-1 -*-

import requests
import tweepy
import json
from tweepy import OAuthHandler
import pdb

twitter_id      = '753763924131123200' #substituir pelo twitter id do usuário: http://mytwitterid.com/
total_tweets    = 10

consumer_key    = 'ME3gfC1qGFyVyk81CNHJa5EWe'
consumer_secret = '5LuJl9HxWxR2a0R7zoVSWzTWg0KFZZkwHg2y08YbUDgTCB5epD'
access_token    = '753763924131123200-Ec4hPYqm9dBgEN9FRCIVu9VZKjIAaYp'
access_secret   = 'hBrcLank8Q6a42lfgx33K5ZyvUuJpk0PbCyW46DiHefhq'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

def getPostsUser():
    tweets = []
    api = tweepy.API(auth)
    for line in tweepy.Cursor(api.user_timeline).items(total_tweets):
        tweet = json.loads(json.dumps(line._json))
        tweets.insert(0, tweet)
    return tweets

def getPostsAmigos():
    tweets = []
    for line in tweepy.Cursor(api.home_timeline).items(total_tweets):
        tweet = json.loads(json.dumps(line._json))
        #pdb.set_trace()
        if tweet['id'] != twitter_id:
            tweets.insert(0, tweet)
    return tweets


if __name__ == "__main__":
    print (getPostsUser())
    print (getPostsAmigos())
