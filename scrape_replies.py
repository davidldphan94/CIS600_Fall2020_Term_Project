import tweepy
from nltk.sentiment.vader import SentimentIntensityAnalyzer

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
    api = login()
    responses = {}
    handle = 'WholesomeMeme' #change if necessary
    for response in tweepy.Cursor(api.search, q='to:' + handle, result_type='recent').items(100):
        if hasattr(response, 'in_reply_to_screen_name') and hasattr(response, 'in_reply_to_status_id'):
            if response.in_reply_to_screen_name == handle:
                meme_id = response.in_reply_to_status_id
                if meme_id in responses:
                    responses[meme_id].append(response.text)
                else:
                    responses[meme_id] = [response.text]
    
    for meme_id in responses.keys():
        tweet = api.get_status(meme_id)
        responses[meme_id].insert(0, tweet.text)

    f = open("reply_analysis.txt", "w", encoding='utf-8')
    sid = SentimentIntensityAnalyzer()
    for meme_id in responses:
        #first element is the original tweet
        meme, replies = responses[meme_id][0], responses[meme_id][1:]
        f.writelines('Meme: ' + meme + '\n\n')
        for reply in replies:
            f.writelines('Reply: ' + reply + '\n')
            ss = sid.polarity_scores(reply)
            for k in sorted(ss):
                text = '{0}: {1}, '.format(k, ss[k])
                f.writelines(text)
            f.writelines('\n')
        f.writelines('\n')
    f.close()

        