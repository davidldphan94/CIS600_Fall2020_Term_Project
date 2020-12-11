"""
Sentiment Analysis used from NLTK sample code.

Link found here: http://www.nltk.org/howto/sentiment.html
"""
from nltk.sentiment.vader import SentimentIntensityAnalyzer


if __name__ == "__main__":
    """
    Runs sentiment analysis on text file returned from meme_graph.py
    """
    f1 = open("tweets.txt", "r", encoding='utf-8')

    tweets = f1.readlines()
    f1.close()
    sid = SentimentIntensityAnalyzer()
    f2 = open("meme_analysis.txt", "w", encoding='utf-8')
    for tweet in tweets:
        print('Tweet: ' + tweet)
        ss = sid.polarity_scores(tweet)
        for k in sorted(ss):
            s = '{0}: {1}, '.format(k, ss[k]) + '\n'
            print(s)
            f2.writelines(s)
        print('\n')
    f2.close()
