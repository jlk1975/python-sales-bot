import os
import tweepy
 
def sendTweet(msg, dry_run):
    #Setup Creds
    CONSUMER_KEY = os.getenv('CONSUMER_KEY')
    CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
    ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
    ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

    #Setup Client
    client = tweepy.Client(consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET)
    
    if dry_run == False:
        print("Stats Bot Sending Tweet..")
        response = client.create_tweet(text=msg)
        print(response)
    else:
        print("Stats Bot NOT Sending Tweet..Dry Run Only..")

    print(msg)   

  