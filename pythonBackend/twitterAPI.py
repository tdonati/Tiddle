import tweepy
import secret
import json
import requests

from flask import json,Flask,render_template,request
from flask.json import dumps
import re
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EmotionOptions
#Tweepy stuff
app = Flask(__name__)
@app.route('/')
def homepage():
    return render_template('testpage.html')

def getdata(nam):
    auth = tweepy.OAuthHandler(secret.CONSUMER_KEY, secret.CONSUMER_SECRET)
    auth.set_access_token(secret.ACCESS_TOKEN, secret.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    # check if user exists
    try:
        user = api.get_user(nam)
    except tweepy.TweepError:
        # if tweepy.TweepError is "[{'code': 50, 'message': 'User not found.'}]":
        return "Sorry, user not found!"

    # check if user is private
    try:
        tweetsObject = api.user_timeline(user.id, tweet_mode='extended')
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

    return tweets

def sentiment_analysis(tweets):
    # API_URL='https://gateway.watsonplatform.net/natural-language-understanding/api'
    # auth=secret.WATSON_KEY
    # natural_language_understanding = NaturalLanguageUnderstandingV1(
    # version='2018-11-16',
    # iam_apikey=auth,
    # url=API_URL
    # )
    # response = natural_language_understanding.analyze(
    #     text = data,
    #     features=Features(emotion=EmotionOptions())
    # ).get_result()
    # return json.dumps(response,indent=2)
    headers = {
    'Content-Type': 'application/json',
    }
    str_tweets = str(tweets)
    params = (
    ('version', '2018-11-16'),
    )

    data = ('{ "text":',str_tweets,',\n  "features": {\n    "sentiment": {},\n    "categories": {},\n    "concepts": {},\n    "entities": {},\n    "keywords": {}\n  }\n}')

    response = requests.post('https://gateway.watsonplatform.net/natural-language-understanding/api/v1/analyze', headers=headers, params=params, data=data, auth=('apikey', 'uAw0fr2xiGnaVGny0WCCQwYZqFJhJCLCB9cZ5qs9VurX'))
    return response.json()


def cleanTweet(tweet):
    # clean Tweet of websites, \n, whatever
    text = re.sub(r'http\S+', '', tweet)
    text = re.sub(r'\n','',text)
    return re.sub(r'@\S+', '',text)


@app.route('/return', methods=['GET', 'POST'])
def ourApp():
    nam = request.form.get('number')
    ret_tweets = getdata(nam);
    sentiment_data = sentiment_analysis(ret_tweets)
    return render_template('testpage.html', tweet=sentiment_data)


if __name__ == '__main__':
    app.run(debug=True)
"""

auth = tweepy.OAuthHandler(secret.CONSUMER_KEY, secret.CONSUMER_SECRET)
auth.set_access_token(secret.ACCESS_TOKEN, secret.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

user = api.get_user('JoeBiden')
userid = user.id

tweetsObject = api.user_timeline(user.id, tweet_mode='extended')

tweets = []

for i in range(20):
    status = tweetsObject[i]
    json_data = json.dumps(status._json)

    json_data = json.loads(json_data)
    #print(json_data)


    text = json_data['full_text']

    if text[0:2] != 'RT':
        tweets.append(text)
        print(text)
        print("\n")



"""

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