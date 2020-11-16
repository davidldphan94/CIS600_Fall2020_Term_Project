import tweepy
import networkx as nx
import matplotlib.pyplot as plt

def login():
  CONSUMER_KEY=''
  CONSUMER_SECRET=''
  OAUTH_TOKEN=''
  OAUTH_TOKEN_SECRET=''
  auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
  auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET) 
  twitter_api = tweepy.API(auth,wait_on_rate_limit=True)
  return twitter_api

if __name__ == '__main__':
    api = login()
    G = nx.Graph()
    while nx.number_of_nodes(G) < 30:
        for tweet in tweepy.Cursor(api.search,q=["#meme","#memes"]).items():
            print("ID: ",tweet.id,"   Retweets: ",tweet.retweet_count)
            retweeters = [t.user.id for t in api.retweets(tweet.id)]
            if len(retweeters):
                G.add_node(tweet.id)
                for i in retweeters: G.add_edge(tweet.id,i)

    nx.draw(G, with_labels = True)
    plt.draw()
    plt.show()
