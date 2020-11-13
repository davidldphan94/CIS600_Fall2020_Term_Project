import tweepy

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

  for tweet in tweepy.Cursor(api.search,q=["#meme","#memes"]).items():
    print("Content: ",tweet.text)
    if tweet.retweet_count!=0:
      print("ID: ",tweet.id)
      print("Retweeters: ") # This may show up empty sometimes
      for t in api.retweets(tweet.id): print(t.user.screen_name,end=' ') # Print all accounts that retweet
    print('\n\n') # Separate Output a bit
  
