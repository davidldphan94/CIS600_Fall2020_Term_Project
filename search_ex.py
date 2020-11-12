import twitter

def login():
  CONSUMER_KEY='aLQEDUQZrJg0y783OUjK0s0tD'
  CONSUMER_SECRET='29demwjvUdpQ5SQTA6cq7QIBbnkFoDd2dCYmpfg5nLNwaybs5v'
  OAUTH_TOKEN='1311720591922286597-FUJ4rBoPG3lTpiIxwUqliTdKRZ5EWt'
  OAUTH_TOKEN_SECRET='aqeX2Dm5sLoDeIFh6dxGHqO43ilRkw6wnKc3Xdd8QwuyM'
  auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,CONSUMER_KEY, CONSUMER_SECRET)
  twitter_api = twitter.Twitter(auth=auth)
  return twitter_api

if __name__ == '__main__':
  api = login()

  for tweet in api.search.tweets(q="#meme",count=5000).items():
    print(tweet)
  
