# Import necessary libraries
import os
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
from dotenv import load_dotenv

class TwitterClient(object):
    '''
    TwitterClient: A generic Twitter Class for fetching and processing tweets.
    Can filter retweets and perform sentiment analysis if specified.
    '''
    def __init__(self, query, retweets_only=False, with_sentiment=False):
        # Set your Twitter API credentials (Note: These should be kept secure, not hardcoded)

        load_dotenv()
        consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
       
        try:
            # Authenticate with the Twitter API using OAuth
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)

            # Store query parameters
            self.query = query
            self.retweets_only = retweets_only
            self.with_sentiment = with_sentiment

            # Create the Tweepy API object
            self.api = tweepy.API(self.auth)

            # Set the maximum number of tweets to fetch
            self.tweet_count_max = 100 
        except:
            print("Error: Authentication Failed")

    # Method to update the search query
    def set_query(self, query=''):
        self.query = query

    # Method to enable or disable retweet filtering
    def set_retweet_checking(self, retweets_only='false'):
        self.retweets_only = retweets_only

    # Method to enable or disable sentiment analysis
    def set_with_sentiment(self, with_sentiment='false'):
        self.with_sentiment = with_sentiment

    # Method to clean the tweet text (remove mentions, URLs, special chars)
    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    # Method to determine the sentiment of a tweet: positive, neutral, or negative
    def get_tweet_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    # Method to fetch tweets from Twitter based on the current settings
    def get_tweets(self):
        tweets = []

        try:
            # Search for tweets using the given query and count
            recd_tweets = self.api.search(q=self.query, count=self.tweet_count_max)

            # Skip if no tweets found
            if not recd_tweets:
                pass

            # Parse each tweet
            for tweet in recd_tweets:
                parsed_tweet = {}

                parsed_tweet['text'] = tweet.text
                parsed_tweet['user'] = tweet.user.screen_name
                
                # Add sentiment if enabled
                if self.with_sentiment == 1:
                    parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
                else:
                    parsed_tweet['sentiment'] = 'unavailable'

                # Check for retweets if filtering is enabled
                if tweet.retweet_count > 0 and self.retweets_only == 1:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                elif not self.retweets_only:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)

            return tweets

        except tweepy.TweepError as e:
            print("Error : " + str(e))
