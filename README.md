# **CIS600 Fall2020 Term Project**

Contributors: David Phan, Matthew Moran, and Nicholas Weier

This is our final project for CIS600 Social Media and Data Mining.
Semester: Fall 2020
Professor: Edmund Yu
Syracuse University

Our project is centered around the tracking of memes in social networking, and the analysis of the information gained from such tracking.



### Description of Files:

  ### Figure_1.png
  A sample graph of our collected memes. 

  ### meme_graph.py
  Code that saves tweets to a text file (tweets.txt), as well as pulling memes to be added to the graph.
  
  ### nick_tweets.txt
  Memes that Nick collected through his phone while running meme_graph.py.  

  ### sentiment_analysis.py
  The implementation of sentiment analysis using NLTK and VADER to analyze any text in the memes that are posted on twitter. The code reads in the output text file of meme_graph.py (tweets.txt) and outputs the sentiment analysis results to a text file (meme_analysis.py).

  ### scrape_replies.py
  Code that scrapes replies to memes off the internet from a certain user, gathers the meme that is being replied after scraping the replies off twitter, and runs sentiment analysis on replies to the memes using VADER. 
  
  ### scrape_replies.txt
  Text file returned after runnign scrape_replies. Contains sentiment analysis of replies to a twitter handle scraped from twitter and the tweet replied to. 

### Instructions to Run:

Graph Generation and Sentiment Analysis on memes 
  1) Run meme_graph first using "python meme_graph.py" on the terminal. It should output a graph and a text file of tweets after iteration.
  2) Run sentiment analysis on the text file returned from meme_graph using "python sentiment_analysis.py" to return the sentiment analysis of the lines in the text file.

Sentiment Analysis on meme replies
  1) Run scrape_replies after running "python scrape_replies.py" on the terminal. Feel free to change the twitter handle in question if needed.
  2) Text file scrape_replies.txt should be returned, yielding all the sentiment analysis values run using VADER in NLTK. 
  


