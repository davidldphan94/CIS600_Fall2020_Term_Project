import twitter
import json
import pdb

import tweepy


def login():
    CONSUMER_KEY = ''
    CONSUMER_SECRET = ''
    OAUTH_TOKEN = ''
    OAUTH_TOKEN_SECRET = ''
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    twitter_api = tweepy.API(auth, wait_on_rate_limit=True)
    return twitter_api

def login_streaming():
    CONSUMER_KEY = ''
    CONSUMER_SECRET = ''
    OAUTH_TOKEN = ''
    OAUTH_TOKEN_SECRET = ''
    auth = twitter.oauth.OAuth(
        OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    twitter_api = twitter.TwitterStream(auth=auth)
    return twitter_api

def login_search():
    CONSUMER_KEY = ''
    CONSUMER_SECRET = ''
    OAUTH_TOKEN = ''
    OAUTH_TOKEN_SECRET = ''
    auth = twitter.oauth.OAuth(
        OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    twitter_api = twitter.Twitter(auth=auth)
    return twitter_api


def retweet_extractor_streaming():  # uses streaming API, still working on it
    api = login_streaming()
    stream = api.statuses.filter(track='memes')
    for tweet in stream:  # identifying the same meme == looking and seeing the "retweeted status"
        if 'quoted_status' in tweet:
            text = tweet['quoted_status']
        elif 'extended_tweet' in tweet:
            text = tweet['extended_tweet']['full_text']
            print(text)
        else:
            print('retweeted_status')
            continue

def retweet_extractor_search():
    api = login_search()
    retweet = 0
    quoted = 0
    original_content = 0
    search_results = api.search.tweets(q="meme,memes", count=5000)
    tweets = []
    for _ in range(5):  # change as necessary to get more batches
        try:
            next_results = search_results['search_metadata']['next_results']
        except KeyError:
            break
        kwarg = dict([kv.split('=') for kv in next_results[1:].split('&')])
        tweets += search_results['statuses']
        search_results = api.search.tweets(**kwarg)
    for tweet in tweets:
        if tweet['is_quote_status']:
            print('quoted_status')
            quoted += 1
        elif 'retweeted_status' in tweet:
            print('retweeted_status')
            retweet += 1
        else:
            print('original tweet')
            original_content += 1

if __name__ == '__main__':
    api = login()
    for tweet in tweepy.Cursor(api.search, q=["#meme", "#memes"]).items():
        print("Content: ", tweet.text)
        if tweet.retweet_count != 0:
            print("ID: ", tweet.id)
            print("Retweeters: ")  # This may show up empty sometimes
            for t in api.retweets(tweet.id):
                # Print all accounts that retweet
                print(t.user.screen_name, end=' ')
            print('\n\n')  # Separate Output a bit

