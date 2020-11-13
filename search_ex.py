import twitter
import json
import pdb


def login(stream=False):
    CONSUMER_KEY = ''
    CONSUMER_SECRET = ''
    OAUTH_TOKEN = ''
    OAUTH_TOKEN_SECRET = ''
    auth = twitter.oauth.OAuth(
        OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    if stream:
        twitter_api = twitter.TwitterStream(auth=auth)
    else:
        twitter_api = twitter.Twitter(auth=auth)
    return twitter_api

def retweet_extractor(): #uses streaming API, still working on it
    api = login(stream=True)
    stream = api.statuses.filter(track='memes')
    import pdb; pdb.set_trace()
    for tweet in stream: # identifying the same meme == looking and seeing the "retweeted status"
        if 'quoted_status' in tweet:
            text = tweet['quoted_status']
        elif 'extended_tweet' in tweet:
            text = tweet['extended_tweet']['full_text']
            print(text)
        else:
            print('retweeted_status')
            continue


if __name__ == '__main__':
    api = login()
    retweet = 0
    quoted = 0
    extended = 0 
    original_content = 0
    search_results = api.search.tweets(q="meme", count=5000)
    tweets = []
    for _ in range(5): #change as necessary to get more batches
        try:
            next_results = search_results['search_metadata']['next_results']
        except KeyError as e:
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
            # print(tweet)
    pdb.set_trace()
