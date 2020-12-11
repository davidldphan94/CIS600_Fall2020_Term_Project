"""
Sentiment Analysis used from NLTK sample code.

Link found here: http://www.nltk.org/howto/sentiment.html
"""

from nltk.sentiment.vader import SentimentIntensityAnalyzer


if __name__ == "__main__":
    f = open("tweets.txt", "r", encoding='utf-8')
    tweets = f.readlines()
    f.close()
    sid = SentimentIntensityAnalyzer()
    for tweet in tweets:
        print('Tweet: ' + tweet)
        ss = sid.polarity_scores(tweet)
        for k in sorted(ss):
            print('{0}: {1}, '.format(k, ss[k]), end='')
        print('\n')
