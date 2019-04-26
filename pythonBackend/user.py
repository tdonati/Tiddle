import tweepy
import json
import secret
import requests
import flask
import re
from flask import json,Flask,render_template,request,redirect,url_for
from flask.json import dumps
from db import insert, search, update

auth = tweepy.OAuthHandler(secret.CONSUMER_KEY, secret.CONSUMER_SECRET)
auth.set_access_token(secret.ACCESS_TOKEN, secret.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

class User:
    def __init__(self, username):
        self.username = username
        self.user = api.get_user(username)
        self.user_id = self.user.id
        self.tweets= ""

        
        

    def get_data(self):

    # check if user exists
    #try:
    #    user = api.get_user(self.username)
    #except tweepy.TweepError:
        # if tweepy.TweepError is "[{'code': 50, 'message': 'User not found.'}]":
    #    return "Sorry, user not found!"

    # check if user is private
        try:
            tweetsObject = api.user_timeline(self.user_id, tweet_mode='extended')
        except tweepy.TweepError:
            return "Sorry, user is private!"

        tweets = []

        for i in range(len(tweetsObject)):
            status = tweetsObject[i]
            json_data = json.dumps(status._json)

            json_data = json.loads(json_data)

            text = json_data['full_text']

            if text[0:2] != 'RT':
                tweets.append(cleanTweet(text))
        	    #print(text)
        	    #print("\n")
        self.tweets = tweets

        return tweets
        


    def process_tweet(self, tweet):
        return {
            "time": tweet.created_at.strftime('%m/%d/%y'),
            "text": tweet.text,
            "_id": tweet.id,
            "user_id": self.user_id
        }

    def get_tweets(self):
        tweets = self.get_data()
        self.tweets = tweets
        insert_tweet({
            '_id': "u_" + str(self.user_id),
            'tweets': self.tweets,
            'username': self.username[1:],
            'user': self.user._json
            })
        return

    def makeuser(self):
    	insert_user({
    		'_id': "u_" + str(self.user_id),
            'tweets': self.tweets,
            'username': self.username[1:],
            'user': self.user._json
    		})

    



    def to_json(self):
        return dumps({
            'username': self.username,
            'user_id': self.user_id,
            'tweets': self.tweets
        })

class Search:
    pass

#@staticmethod
def insert_user(value):
    insert(value,'tweets')
    return

def insert_tweet(value):
    update(value, 'tweets')
    return

def cleanTweet(tweet):
    # clean Tweet of websites, \n, whatever
    text = re.sub(r'http\S+', '', tweet)
    text = re.sub(r'\n','',text)
    text = re.sub(r'@\S+', '', text)
    text = text.replace(u"\u201c","'")
    text = text.replace(u"\u201d", "'")
    text = text.replace(u"\u2018", "'")
    text = text.replace(u"\u2019", "'")
    text = text.replace(u"\u2026", "'")
    text = text.replace(u"\u2014", "'")
    text = text.replace(u"\U0001f60f", "'")
    text = text.replace(u"\U0001f924", "'")

    return text

def get_user(username):
    """
    If there is the user in the database, we will return that user, else error
    :param username: Twitter handle
    :return: User object
    """
    result = search({'username': username}, 'tweets')
    if not result:
        user = User("@{}".format(username))
        user.get_tweets()
        return json.loads(user.to_json())
    else:
        return result

if __name__ == '__main__':
    u = User('@gaspardetienne9')
    print(u.user_id)
