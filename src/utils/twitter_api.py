import os
import tweepy
from dotenv import load_dotenv

# 加載環境變量
load_dotenv()

API_KEY = os.getenv('API_KEY')
API_SECRET_KEY = os.getenv('API_SECRET_KEY')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')
BEARER_TOKEN = os.getenv('BEARER_TOKEN')

def authenticate_oauth():
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api

def authenticate_bearer_token():
    client = tweepy.Client(bearer_token=BEARER_TOKEN)
    return client

def fetch_followers_oauth(api, screen_name, max_followers=1000):
    followers = []
    for page in tweepy.Cursor(api.get_followers, screen_name=screen_name, count=200).pages():
        followers.extend(page)
        if len(followers) >= max_followers:
            break
    return followers

def fetch_user_timeline_oauth(api, screen_name, max_tweets=1000):
    tweets = []
    for status in tweepy.Cursor(api.user_timeline, screen_name=screen_name, tweet_mode='extended').items(max_tweets):
        tweets.append(status._json)
    return tweets

def get_user_id_bearer(client, username):
    user = client.get_user(username=username)
    return user.data.id

def fetch_followers_bearer_token(client, user_id, max_results=1000):
    followers = []
    for response in tweepy.Paginator(client.get_users_followers, id=user_id, max_results=200).pages():
        followers.extend(response.data)
        if len(followers) >= max_results:
            break
    return followers

def fetch_user_tweets_bearer_token(client, user_id, max_results=100):
    tweets = []
    for response in tweepy.Paginator(client.get_users_tweets, id=user_id, max_results=100).pages():
        tweets.extend(response.data)
        if len(tweets) >= max_results:
            break
    return tweets
