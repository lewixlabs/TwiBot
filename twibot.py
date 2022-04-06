from datetime import datetime
import os
import tweepy
import time
import argparse
from dotenv import load_dotenv

load_dotenv()

consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")
bearer_token = os.environ.get("BEARER_TOKEN")

client = tweepy.Client(
    consumer_key=consumer_key, consumer_secret=consumer_secret,
    access_token=access_token, access_token_secret=access_token_secret,
    bearer_token=bearer_token
)

def main():

    parser = argparse.ArgumentParser(description='🐥🤖 TwitBot, Twitter Bot for Twitter')
    parser.add_argument('-t','--text', help='Twitter text', required=True)
    parser.add_argument('-u','--user', help='Twitter user', required=True)
    parser.add_argument('-s','--seconds', help='Seconds between each check', required=True, type=int)
    args = parser.parse_args()

    twitter_user = args.user

    last_tweet_id = 0

    print("Searching for last tweets")
    while(True):        
        search_query = "-is:retweet from:" + twitter_user
        json_response = client.search_recent_tweets(query=search_query)
        # print(json.dumps(json_response, indent=4, sort_keys=True))
        if json_response.meta['newest_id'] != last_tweet_id:
            print(datetime.now())
            print("FOUND!! ****************************************")
            
            print(json_response.data[0]['text'])
            print('newest_id: ' + json_response.meta['newest_id'])
            
            last_tweet_id = json_response.meta['newest_id']

            # retweet
            client.retweet(last_tweet_id)

            # like
            client.like(last_tweet_id)

            # reply with custom text
            client.create_tweet(text=args.text,in_reply_to_tweet_id=last_tweet_id)

            print("************************************************")
        else:
            print(datetime.now())
            print("Nothing new")
        
        time.sleep(args.seconds)
            

if __name__ == "__main__":
    main()
