import argparse
import requests
import sys
import json
import tweepy
import os
import time
from currency_symbols import CurrencySymbols
from dotenv import load_dotenv
from web3 import Web3 
from decimal import Decimal
from dateutil import tz
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
import pyshorteners as sh #try without this


##################################### Functions ################################################
def getLastChecked(dbfile, collection):
        # Read JSON File
        jsonFile = open(dbfile, "r") # Open the JSON file for reading
        db = json.load(jsonFile) # Read the JSON into the buffer
        jsonFile.close() # Close the JSON file
        last_checked = db[collection]
        return(last_checked)
       
def saveLastChecked(dbfile, collection, last_checked):
    # Read JSON File
    jsonFile = open(dbfile, "r") 
    db = json.load(jsonFile)  
    jsonFile.close() 
    # Update JSON File in memory
    db[collection] = last_checked
    # Open , Update, Close JSON File
    jsonFile = open(dbfile, "w+")  
    jsonFile.write(json.dumps(db))
    jsonFile.close()
    
def get_log_prefix(collection):
    log_prefix = "[" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " : " + collection + "] ==>> "
    return log_prefix

def sendTweets(events_list, collection, dbfile, dry_run, sleep_time):
    #Setup Creds
    CONSUMER_KEY = os.getenv('CONSUMER_KEY')
    CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
    ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
    ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

    #Other variables
    ethSymbol = CurrencySymbols.get_symbol('ETH')
    
    #Setup Client
    client = tweepy.Client(consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET)
    
    #Sort Events List
    events_list.sort(key=lambda x: datetime.strptime(x['created_date'], '%Y-%m-%dT%H:%M:%S.%f'))
    
    # New for loop with bundles supported
    for event in events_list:
        created_date = event['created_date']
        total_price = event['total_price']
        formatted_units = Web3.fromWei(int(total_price), 'ether')
        token_eth_price = event['payment_token']['eth_price']
        formatted_eth_price = formatted_units * int(float(token_eth_price))
        token_usd_price = Decimal(event['payment_token']['usd_price'])
        formatted_usd_price = formatted_units * token_usd_price
        ethSymbol = CurrencySymbols.get_symbol('ETH')

        if type(event['asset']) is dict:
            asset_name = event['asset']['name']
            opensea_link = event['asset']['permalink']

            tweetText = asset_name + " bought for " \
            + str(formatted_eth_price) \
            + ethSymbol \
            + "($" + str(round(formatted_usd_price, 2)) + ")" \
            + " #NFT " + opensea_link

        if type(event['asset_bundle']) is dict:
            bundle_slug = event['asset_bundle']['slug']
            opensea_link = "https://opensea.io/bundles/ethereum/" + bundle_slug

            sold_bundle_items = ""
            for i, item in enumerate(event['asset_bundle']['assets']):
                if len(sold_bundle_items) == 0:
                    sold_bundle_items = sold_bundle_items + item['name']
                elif i == len(event['asset_bundle']['assets']) - 1:
                    sold_bundle_items = sold_bundle_items + ", and " + item['name']
                else:
                    sold_bundle_items = sold_bundle_items + ", " + item['name']

            tweetText = sold_bundle_items + " were bought for " \
            + str(formatted_eth_price) \
            + ethSymbol \
            + "($" + str(round(formatted_usd_price, 2)) + ")" \
            + " #NFT " + opensea_link

        #Send the Tweet
        print(get_log_prefix(collection) + "[Sale - " + created_date + "] Tweet: " + tweetText)
        
        if dry_run == False:
            response = client.create_tweet(text=tweetText)
            print(response)
            if sleep_time:
                print(get_log_prefix(collection) + "Waiting " + str(sleep_time) + " seconds until Twitter API Call")
                time.sleep(sleep_time)

        # Call saveLastChecked
        saveLastChecked(dbfile, collection, created_date)
############################### End Functions ################################################


############################### Main          ################################################

# Create the parser
my_parser = argparse.ArgumentParser(prog='salesbot', description='Check for NFT Sales')

# Add Positional (Required) Arguments:
my_parser.add_argument('Collections',
                       type=str,
                       help='the nft collection to check')

# Add Optional Arguments:
my_parser.add_argument('-s',
                       '--sleep',
                       type=int,
                       help='Time to Sleep in Seconds before next API call')
my_parser.add_argument('-d',
                       '--dryrun',
                       action='store_true',
                       help='DRY RUN, WILL NOT SEND TWEETS')
                    
# Execute the parse_args() method
args = my_parser.parse_args()

# Set variables
collections = args.Collections.split()
sleep_time = args.sleep
dry_run = args.dryrun

dotenv_path = './.env'
load_dotenv(dotenv_path=dotenv_path)


# Set DB JS0N File
dbfile = "./data/db.json"

# OpenSea API Key
OPENSEA_API_KEY = os.getenv('OPENSEA_API_KEY')

for index, collection in enumerate(collections):
    print("\n")
    print(get_log_prefix(collection) + "Checking for New Sales ..")

    if index > 0 and sleep_time:
        print(get_log_prefix(collection) + "Waiting " + str(sleep_time) + " seconds until OpenSea API Call")
        time.sleep(sleep_time)  
   
    last_checked = getLastChecked(dbfile, collection)
    print("Last checked: " + last_checked)

    # USE THIS FOR PROD DATA
    response = requests.get(
        'https://api.opensea.io/api/v1/events',
        params={
            'collection_slug': collection, 
            "event_type": "successful",
            "only_opensea": "false",
            "occurred_after": last_checked,  
            },
        headers={'X-API-KEY': OPENSEA_API_KEY},
    )
    json_response = response.json() # Deserialize, <class 'dict'>

    # READING FROM test_data.json has a flaw, really we need 1 test json data file for EACH collection.
    # NEW - USE THIS FOR TESTING, COMMENT OUT FOR PROD
    # with open('test_data.json') as f:
    #     json_response = json.load(f)
    # # # print(json_response)

    # Do not remove next line, useful for troubleshooting...
    # print(json.dumps(json.loads(response.text), indent =2))
    
    number_of_sales = len(json_response['asset_events'])

    print("\n")
    print(get_log_prefix(collection) + str(number_of_sales) + " Sales Found since last check (" + last_checked + ")..")
    
    if number_of_sales > 0:
        print(get_log_prefix(collection) + "Prepping Tweets for " + str(number_of_sales) + " sales..")
        events_list = json_response['asset_events']  
        sendTweets(events_list, collection, dbfile, dry_run, sleep_time)
    else:
        print(get_log_prefix(collection) + "No new sales, nothing to Tweet about.")

print("\n")
print("Done Checking for Sales @ " +datetime.now().strftime("%Y-%m-%d %H:%M:%S"))