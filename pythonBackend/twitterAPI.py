import tweepy
import secret
import requests
from flask import json
from flask.json import dumps

url = "https://api.twitter.com/1.1/statuses/user_timeline.json"

querystring = {"count":"2","user_id":"3248878103"}

payload = ""
headers = {
    'Authorization': "OAuth oauth_consumer_key='5p9bfzHYNr4PCXalLFhIYs7Gu',oauth_token='1098970060058750976-BtdgeuYMW4sTIG1TJqhkGFRavesa0T',oauth_signature_method='HMAC-SHA1',oauth_timestamp='1553566408',oauth_nonce='H9uimVpi3G7',oauth_version='1.0',oauth_signature=fWXpm4ClhSOxb7G3mBmMxsWvfdU%3D",
    'cache-control': "no-cache",
    'Postman-Token': "ec5cc3be-828f-44b7-ae5a-927585f2b26b"
    }

response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

print(response.text)

auth = tweepy.OAuthHandler(secret.CONSUMER_KEY, secret.CONSUMER_SECRET)
auth.set_access_token(secret.ACCESS_TOKEN, secret.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

user = api.get_user('perrydbucs')
userid = user.id


print(userid)
# print(user.screen_name)
# print(user.followers_count)
# for friend in user.friends():
#    print(friend.screen_name)




post_id = 0
for status in api.user_timeline():
   post_id = (status.id)

json_data = api.get_status(post_id)
print(json_data.text)
