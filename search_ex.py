import twitter

def login():
  CONSUMER_KEY=''
  CONSUMER_SECRET=''
  OAUTH_TOKEN=''
  OAUTH_TOKEN_SECRET=''
  auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,CONSUMER_KEY, CONSUMER_SECRET)
  twitter_api = twitter.Twitter(auth=auth)
  return twitter_api

if __name__ == '__main__':
  api = login()

  for tweet in api.search.tweets(q="#meme",count=5000).items():
    print(tweet)
  
