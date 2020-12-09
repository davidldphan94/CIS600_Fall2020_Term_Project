from nltk.sentiment.vader import SentimentIntensityAnalyzer

if __name__ == "__main__":
    f = open("nick_tweets.txt", "r", encoding='utf-8')
    tweets = f.readlines()
    f.close()
    sid = SentimentIntensityAnalyzer()
    for tweet in tweets:
        print(tweet)
        ss = sid.polarity_scores(tweet)
        for k in sorted(ss):
            print('{0}: {1}, '.format(k, ss[k]), end='')
