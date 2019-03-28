import tweepy
import secret
import json
import requests
from flask import json
from flask.json import dumps
from flask import Flask, jsonify
from flask import render_template
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    auth = tweepy.OAuthHandler(secret.CONSUMER_KEY, secret.CONSUMER_SECRET)
    auth.set_access_token(secret.ACCESS_TOKEN, secret.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    user = api.get_user('JoeBiden')
    userid = user.id

    tweetsObject = api.user_timeline(user.id, tweet_mode='extended')

    tweets = ""

    for i in range(20):
        status = tweetsObject[i]
        json_data = json.dumps(status._json)

        json_data = json.loads(json_data)
        # print(json_data)

        text = json_data['full_text']
        if text[0:2] != 'RT':
            tweets += (text)
    return tweets

if __name__ == '__main__':
    app.run(debug=True)


#Tweepy stuff




"""
url = "https://api.twitter.com/1.1/statuses/user_timeline.json"

#Postman call only works with perrdbucs
querystring = {"count":"5","user_id":userid}

payload = ""
headers = {
    'Authorization': "OAuth oauth_consumer_key="'5p9bfzHYNr4PCXalLFhIYs7Gu'",oauth_token="'1098970060058750976-BtdgeuYMW4sTIG1TJqhkGFRavesa0T'",oauth_signature_method="'HMAC-SHA1'",oauth_timestamp="'1553720099'",oauth_nonce="'xZiet9XV8TK'",oauth_version="'1.0'",oauth_signature="'CLp%2FqNzgzcfsM19fgqBoXhtWKX4%3D'"",
    'cache-control': "no-cache",
    'Postman-Token': "42c6650f-10d2-4337-9e86-37ea5dd5dd55"
    }


response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

#print(response.text, "\n\n")

json_data = json.loads(response.text)

#print(json_data, "\n\n")


for tweet in json_data:
    #print(tweet)
    print(tweet['text'])

print("\n\n")




#print(userid)
# print(user.screen_name)
# print(user.followers_count)
# for friend in user.friends():
#    print(friend.screen_name)




post_id = 0
for status in api.user_timeline():
   post_id = (status.id)

json_data = api.get_status(post_id)
print(json_data.text)
"""
