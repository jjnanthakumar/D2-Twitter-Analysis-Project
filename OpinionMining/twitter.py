import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import json


class TwitterClient(object):
    ''' 
    Generic Twitter Class for sentiment analysis. 
    '''

    def __init__(self):
        ''' 
        Class constructor or initialization method. 
        '''
        # keys and tokens from the Twitter Dev Console
        # One App
        consumer_key = 'fILwZj2ySxHK4XiEwc5CMhw6P'
        consumer_secret = 'kAJJpFeb7LCOLSfbJH7htUhjeBlrjw8aU3H1uQtUEseGVoO9nZ'
        access_token = '1376156004316930051-pjCT0FL4sr5XQTtM6lbfPxk3nm78HM'
        access_token_secret = 'HaMiHWAV4gawyESV8MBPAe4f9GRzo5NCtuNi3BdSp323g'

        # Other app
        # consumer_key = 'Gi6j24WukcYQYsgaA832VM3Sw'
        # consumer_secret = 'c0b1HZYnRgrEkFFcuRLaZDYJe9xJwHb11rx5HzQtn8cLXiK56c'
        # access_token = '942033965182984193-bovax5qfv0R1gIKcvhWZA6BWHw2imVC'
        # access_token_secret = '3zorHcuf7pXR3PAqtBnLcAsCw6zon9YxiXEvmg4tJnaQb'

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        ''' 
        Utility function to clean tweet text by removing links, special characters 
        using simple regex statements. 
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        ''' 
        Utility function to classify sentiment of passed tweet 
        using textblob's sentiment method 
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        # print(analysis.detect_language())
        # print(analysis.sentiment_assessments)

        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query):
        ''' 
        Main function to fetch tweets and parse them. 
        '''
        data_dict = []
        # empty list to store parsed tweets
        tweets = []
        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search_30_day(
                environment_name='month', query=query, maxResults=100)
            # print(json.dumps(data['retweeted_status'],indent=4))
            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}
                data = tweet._json
                # print(json.dumps(data, indent=4))

                data_dict.append({
                    "id": data["id_str"],
                    "created_at": data["created_at"],
                    "tweet": data["text"],
                    "sentiment": self.get_tweet_sentiment(
                        data["text"]),
                    "user": {"id": data["user"]["id_str"],
                             "name": data["user"]["name"],
                             "profile_img": data["user"]["profile_image_url_https"]
                             },
                    "retweets": [
                        {
                            "id": data.get("retweeted_status", {}).get("id_str", ""),
                            "created_at": data.get("retweeted_status", {}).get("created_at", ""),
                            "tweet": data.get("retweeted_status", {}).get("text", ""),
                            "user": {
                                "id": data.get("retweeted_status", {}).get("user", {}).get("id_str", ""),
                                "name": data.get("retweeted_status", {}).get("user", {}).get("name", ""),
                                "profile_img": data.get("retweeted_status", {}).get("user", {}).get("profile_image_url_https", "")

                            },
                            "retweet_count": data.get("retweeted_status", {}).get("retweet_count", 0),
                            "favourite_count": data.get("retweeted_status", {}).get("favourite_count", 0)
                        }
                    ]
                })
                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(
                    tweet.text)

                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
            # return parsed tweets
            # print(json.dumps(data_dict, indent=4))
            tweets.append(data_dict)
            return tweets

        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))
