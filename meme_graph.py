import tweepy
import networkx as nx
import matplotlib.pyplot as plt
import nltk

def login():
    CONSUMER_KEY = ''
    CONSUMER_SECRET = ''
    OAUTH_TOKEN = ''
    OAUTH_TOKEN_SECRET = ''
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET) 
    twitter_api = tweepy.API(auth, wait_on_rate_limit=True)
    return twitter_api

if __name__ == '__main__':
    seen = set()
    api = login()
    G = nx.Graph()
    f = open('tweets.txt', 'w', encoding='utf-8')
    while nx.number_of_nodes(G) < 100:
        for tweet in tweepy.Cursor(api.search, q="#meme", lang='en').items():
            if 'retweeted_status' in tweet._json.keys(): #if the tweet found is a retweet
                tweet = tweet.retweeted_status #use the source of the tweet instead
            print("ID: ",tweet.id,"   Retweets: ", tweet.retweet_count)
            retweeters = [t.user.screen_name for t in api.retweets(tweet.id)]
            if len(retweeters) and tweet.user.screen_name not in G.nodes():
                for i in retweeters: G.add_edge(tweet.user.screen_name, i)
                f.writelines([tweet.user.screen_name,"\n", tweet.text, "\n\n"])
                if nx.number_of_nodes(G) > 100:
                    break
        
    f.close()
    nx.draw(G, with_labels = True)
    plt.draw()
    plt.show()
