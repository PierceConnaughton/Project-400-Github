#!/usr/bin/env python
# coding: utf-8

#region libraries

#Load in all the necessary libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import nltk
import re
import pickle

#stop words is used to remove words such as the, a, this etc.
from nltk.corpus import stopwords

#Stemming reduces words into there most basic form for example 'running ran run' the stem is run
from nltk.stem import PorterStemmer, WordNetLemmatizer

#Tokenize sentences/Words
from nltk.tokenize import sent_tokenize, word_tokenize

#Used for splitting the data into testing and training
from sklearn.model_selection import train_test_split

#using tfidfVectorizer for vectorizing our tweets
from sklearn.feature_extraction.text import TfidfVectorizer

#Using the logistic regression model
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

pd.set_option('display.width', 500)
pd.set_option('display.max_columns', 100)

#endregion libraries

#region Read and process data

#Read the data into a dataframe
df = pd.read_csv("Data/Twitter.csv")

#Examine the first couple of rows of the dataframe
df.head()

#Renaming the columns to something more fitting and clean
df = df.rename(columns={'clean_text': 'tweet', 'category': 'sentiment'})

df.head()

#Drop empty rows
df = df.dropna()

#Get how many rows and cols are there in the dataframe
df.shape
#As we can see there are over 150,000 tweets in the database

#Renaming the values of -1, 0, and 1 to Negative, Neutral and Positive to make more sense when im manipulating the list
df['sentiment'] = df['sentiment'].map({-1: 'Negative', 0: 'Neutral', 1: 'Positive'})  

#here we get a count of all the tweets that are in a certain group
sentimentPlot = sns.countplot(x = 'sentiment', data=df)

#store the english stop words
stopWords = stopwords.words('english')

#the tweet will be used for the input of our NLP model
tweets = df['tweet']

#function to take in a tweet clean it for processing and output it again
def cleanTweet(tweet):
    
    #convert tweet to lowercase
    tweet = tweet.lower()
    
    #removes any character not alphabetic or numeric
    tweet = re.sub(r"[^A-Za-z0-9]",' ', tweet)
    
    #tokenize the tweet
    token = word_tokenize(tweet)
    
    #remove the stop words and get the root of each word left over and return it to the list
    lm=WordNetLemmatizer()
    words = [lm.lemmatize(word) for word in token if word not in set(stopWords)]
    
    #return the tweet
    return ' '.join(words)

#for each tweet in the list clean it
tweets = tweets.apply(cleanTweet) 

df['tweet'] = tweets

df.head()

#function to split tweets
tweetWords = df.tweet.str.cat(sep=' ')

#token the tweets again
tokensTwo = word_tokenize(tweetWords)

#count number of words in database
print(len(tokensTwo))

#we then group up the same words together
tokenSets = set(tokensTwo)

#We can get the frequency distribution of these words
fd = nltk.FreqDist(tokensTwo)

#get the most commen 10
fd.tabulate(10)

#endregion Read and process data

#region Train Model

#variable to keep the best score
best = 0

#train the model 20 times
for _ in range(20):

    #Splitting my data into training and test data, with the test data being 10% of all tweets
    X_train, X_test, y_train, y_test = train_test_split(df.tweet, df.sentiment, test_size=0.1, random_state=1)

    #Creating a Logistic Regression model for our AI, and using TfidfVectorizer to speed up our code as it loops through the words and,
    #processing them into numbers that can be read faster
    model = Pipeline([('tfidf', TfidfVectorizer()), ('lgr', LogisticRegression())])

    #I then fit my training data onto the model
    model.fit(X_train, y_train)

    #I then test the model by using my left over test data, and find the accuracy
    acc = model.score(X_test, y_test)
    print("Accuracy: " + str(acc))

    # If the current model has a better score than one we've already trained then save it
    if acc > best:
        best = acc
        #save model to new file to be called on
        with open("sentiment.pickle", "wb") as f:
            pickle.dump(model, f)

#endregion Train Model


