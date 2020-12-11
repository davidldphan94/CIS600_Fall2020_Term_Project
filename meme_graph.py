import tweepy
import networkx as nx
import matplotlib.pyplot as plt

def login():
    """
    Sets up Twitter API for use given OAUTH keys.
    """
    CONSUMER_KEY = ''
    CONSUMER_SECRET = ''
    OAUTH_TOKEN = ''
    OAUTH_TOKEN_SECRET = ''
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET) 
    twitter_api = tweepy.API(auth, wait_on_rate_limit=True)
    return twitter_api

if __name__ == '__main__':
    """
    Runs graph generation code.
    """
    api = login()
    G = nx.Graph()
    f = open('tweets.txt', 'w', encoding='utf-8')
    while nx.number_of_nodes(G) < 100:
        query = "meme,memes,#meme,#memes" #change if necessary
        for tweet in tweepy.Cursor(api.search, q=query, lang='en', result_type='popular').items(): 
            if 'retweeted_status' in tweet._json.keys(): #if the tweet found is a retweet
                tweet = tweet.retweeted_status #use the source of the tweet instead
            retweeters = [t.user.screen_name for t in api.retweets(tweet.id)]
            if len(retweeters) and tweet.user.screen_name not in G.nodes():
                print("ID: ",tweet.id,"   Retweets: ", tweet.retweet_count)
                for i in retweeters: G.add_edge(tweet.user.screen_name, i)
                f.writelines([tweet.text, "\n"])
                if nx.number_of_nodes(G) > 100:
                    break
        
    f.close()
    nx.draw(G, with_labels = True)
    plt.draw()
    plt.show()
