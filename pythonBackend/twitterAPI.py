import tweepy
import secret
from flask import json
from flask.json import dumps



auth = tweepy.OAuthHandler(secret.CONSUMER_KEY, secret.CONSUMER_SECRET)
auth.set_access_token(secret.ACCESS_TOKEN, secret.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

user = api.get_user('perrydbucs')
# print(user.screen_name)
# print(user.followers_count)
# for friend in user.friends():
#    print(friend.screen_name)

#print(user.get_status())


post_id = 0
for status in api.user_timeline():
   post_id = (status.id)

json_data = api.get_status(post_id)
print(json_data.text)
