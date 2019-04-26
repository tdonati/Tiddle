import tweepy
import secret
import json
import requests

from flask import json,Flask,render_template,request
from flask.json import dumps
import re
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EmotionOptions

from db import insert, search
from user import User
from movie import movie_rec

person_user = User("@JoeBiden")
movie = ['hotrod']

app = Flask(__name__)
@app.route('/')
def homepage():
    return render_template('login.html')


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
    str_tweets = tweets
    #for tweet in tweets:
    #    str_tweets += tweet

    seperator = ' '
    str_tweets = seperator.join(str_tweets)
    params = (
    ('version', '2018-11-16'),
    )
    # str_tweets = str_tweets.encode(encoding='UTF-8',errors='strict')
    # str_tweets = str_tweets.decode(encoding='UTF-8')
    data = ('{ "text":'+'"'+str_tweets+'"' +',\n  "features": {\n    "sentiment": {},\n    "categories": {},\n    "concepts": {},\n    "entities": {},\n    "keywords": {}\n  }\n}')
    #return data
    response = requests.post('https://gateway.watsonplatform.net/natural-language-understanding/api/v1/analyze', headers=headers, params=params, data=data, auth=('apikey', 'uAw0fr2xiGnaVGny0WCCQwYZqFJhJCLCB9cZ5qs9VurX'))
    response_json = response.json()
    response_json = str(response_json)
    response_json = response_json.replace("'",'"')
    response_json = json.loads(response_json)
    response_json = response_json["sentiment"]["document"]
    response_json = json.dumps(response_json)
    return response_json


def format_genre(inputs):
    ret = inputs.lower()
    ret = ret.capitalize()
    print(ret)
    return ret


def get_user(username):
    """
    If there is the user in the database, we will return that user, else error
    :param username: Twitter handle
    :return: User object
    """
    result = search({'username': username}, 'tweets')
    if not result:
        user = User(username)
        user.get_tweets()
        return user
    else:
        result.get_tweets()
        return result



@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    name = request.form.get('username')
    global person_user 
    person_user = get_user(name)
    return redirect(url_for('ourApp'))


@app.route('/return', methods=['GET','POST'])
def final():
    return render_template('testpage.html',tweet = movie)


@app.route('/genre', methods=['GET', 'POST'])
def ourApp():
    if request.method == 'POST':
        nam = request.form.get('genre')
        gen = str(nam)
        genre = format_genre(gen)
        #person_user.get_data();
        #sentiment_data = sentiment_analysis(person_user.tweets)
        sentiment_data = random.random()
        sent = 8
        global movie
        #movie = movie_rec(genre,sent)
        movie = movie_rec(genre,sent)
        return redirect(url_for('final'))
    return render_template('genre.html')

if __name__ == '__main__':
    app.run(debug=True)


#Tweepy stuff






""""
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

def sentiment_converter(data):
    document_data = json.loads(data)
    return (document_data["score"]+1)/2

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
    str_tweets=tweets
    seperator = ' '
    str_tweets = seperator.join(str_tweets)
    params = (
    ('version', '2018-11-16'),
    )
    # str_tweets = str_tweets.encode(encoding='UTF-8',errors='strict')
    # str_tweets = str_tweets.decode(encoding='UTF-8')
    data = ('{ "text":'+'"'+str_tweets+'"' +',\n  "features": {\n    "sentiment": {},\n    "categories": {},\n    "concepts": {},\n    "entities": {},\n    "keywords": {}\n  }\n}')
    #return data
    response = requests.post('https://gateway.watsonplatform.net/natural-language-understanding/api/v1/analyze', headers=headers, params=params, data=data, auth=('apikey', 'uAw0fr2xiGnaVGny0WCCQwYZqFJhJCLCB9cZ5qs9VurX'))
    response_json = response.json()
    response_json = str(response_json)
    response_json = response_json.replace("'",'"')
    response_json = json.loads(response_json)
    response_json = response_json["sentiment"]["document"]
    response_json = json.dumps(response_json)
    return response_json


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
    return text



@app.route('/return', methods=['GET', 'POST'])
def ourApp():
    nam = request.form.get('number')
    ret_tweets = getdata(nam);
    sentiment_data = sentiment_analysis(ret_tweets)
    score_data = sentiment_converter(sentiment_data)
    return render_template('testpage.html', tweet=score_data)


if __name__ == '__main__':
    app.run(debug=True)


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
