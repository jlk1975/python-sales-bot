import argparse
import requests
import sys
import json
import tweepy
import os
import pyshorteners as sh
import time
from currency_symbols import CurrencySymbols
from dotenv import load_dotenv
from web3 import Web3 
from decimal import Decimal
from dateutil import tz
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

# test docker
# print("im a sales bot!")
# exit(0)

##################################### Functions ################################################
def getLastChecked(dbfile, collection):
        # Read JSON File
        jsonFile = open(dbfile, "r") # Open the JSON file for reading
        db = json.load(jsonFile) # Read the JSON into the buffer
        jsonFile.close() # Close the JSON file
        last_checked = db[collection]
        return(last_checked)
       
def saveLastChecked(dbfile, collection, last_checked):
    if print_db_file == True:
        printDBFile(dbfile, "Printing DB File " + dbfile + " BEFORE Update ..")
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

    if print_db_file == True:
        printDBFile(dbfile, "Printing DB File " + dbfile + " AFTER Update ..")
    
def get_log_prefix(collection):
    log_prefix = "[" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " : " + collection + "] ==>> "
    return log_prefix

def generateLastChecked(look_back_seconds): # This works, but you don't need it yet. Assume happy path for now.
    # print("generateLastChecked got called ..")
    # last_checked = datetime.strptime(datetime.now(), '%Y-%m-%dT%H:%M:%S.%f')
    now = datetime.now()
    datetime_offset = relativedelta(seconds=-look_back_seconds)
    last_checked = (now + datetime_offset).isoformat()
    return(last_checked)

def printDBFile(dbfile, msg):
    print("\n" + msg + "\n")
    jsonFile = open(dbfile, "r") # Open the JSON file for reading
    db = json.load(jsonFile) # Read the JSON into the buffer
    jsonFile.close() # Close the JSON file
    print(db)


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
    
    for event in events_list: # event is just a 'dict' !
        # Set Tweet Variables
        created_date = event['created_date']
        asset_name = event['asset']['name']
        total_price = event['total_price']
        token_decimals = event['payment_token']['decimals']
        token_eth_price = event['payment_token']['eth_price']
        token_usd_price = Decimal(event['payment_token']['usd_price'])
        formatted_units = Web3.fromWei(int(total_price), 'ether')
        formatted_usd_price = formatted_units * token_usd_price
        s = sh.Shortener()
        opensea_link = s.tinyurl.short(event['asset']['permalink'])
        formatted_eth_price = formatted_units * int(float(token_eth_price))

        #Format the Tweet
        tweetText = asset_name + " bought for " + str(formatted_eth_price) + ethSymbol + "($" + str(round(formatted_usd_price, 2)) + ")" + " #NFT " + opensea_link
        
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

def getMints(collection):
    new_mints = "getMints got called! ==>> Just testing new mints function!"
    return new_mints

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
my_parser.add_argument('-db',
                       '--database',
                       action='store_true',
                       help='PRINT DATABASE FILE (db.JSON)')
my_parser.add_argument('-t',
                       '--test',
                       action='store_true',
                       help='FOR TESTING, WILL USE .env_test for ENV variables if set.')
my_parser.add_argument('-p',
                       '--pause',
                       action='store_true',
                       help='FOR TESTING, WILL PAUSE SCRIPT FOR SLEEP TIME.')
my_parser.add_argument('-m',
                       '--mints',
                       action='store_true',
                       help='GET NEW "MINTS" (instead of Sales).')
                    
# Execute the parse_args() method
args = my_parser.parse_args()

# Set variables
collections = args.Collections.split()
sleep_time = args.sleep
dry_run = args.dryrun
print_db_file = args.database
testenv = args.test
pause_run = args.pause
get_mints = args.mints

# Old, but works..
# Load env variables from .env file
# load_dotenv()

if testenv == True:
    dotenv_path = './.env_test'
else:
    dotenv_path = './.env_prod'
load_dotenv(dotenv_path=dotenv_path)

# Print an env var here for testing...
TEST_VAR = os.getenv('ENV_FILE_NAME')
print("\n")
print("Using ENV Config: " + TEST_VAR)
print("\n")

# Set DB JS0N File
dbfile = "./data/db.json"
# OpenSea API Key
OPENSEA_API_KEY = os.getenv('OPENSEA_API_KEY')

# Experimental, if get_mints is set, we'll just exist the script for now until the
# looksrare api response parsing code is written and integrated into other existing functions
# this this same script. Some refactoring will be needed for sure!

if get_mints:
    for index, collection in enumerate(collections):
        print(get_log_prefix(collection) + "Checking for New Mints ..")
        new_mints = getMints(collection)
        print("\n")
        print(new_mints)
        print("\n")
    print("Some code will need be refactored to make getting new mints work, so for now I'll just exit!")    
    exit(0)
else:
    print("new_mints flag was false, I'll continue on with life, Nothing to see here! ... ")


if pause_run == True:
    print("Pausing Run for " + str(sleep_time) + " seconds for testing..")
    time.sleep(sleep_time)

for index, collection in enumerate(collections):
    print("\n")
    print(get_log_prefix(collection) + "Checking for New Sales ..")

    if index > 0 and sleep_time:
        print(get_log_prefix(collection) + "Waiting " + str(sleep_time) + " seconds until OpenSea API Call")
        time.sleep(sleep_time)  
   
    last_checked = getLastChecked(dbfile, collection)
    # Debug: print(last_checked)

    # Add a -t flag for this or something..
    """
    # TEST
    response = requests.get(
        'https://testnets-api.opensea.io/api/v1/events',
        params={
            'collection_slug': collection, 
            "event_type": "successful",
            "only_opensea": "false",
            "occurred_after": last_checked,  
            },
    )
    """

    # PROD
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
    
    # Do not remove next line, useful for troubleshooting...
    # print(json.dumps(json.loads(response.text), indent =2))
    
    number_of_sales = len(json_response['asset_events'])

    print("\n")
    print(get_log_prefix(collection) + str(number_of_sales) + " Sales Found since last check (" + last_checked + ")..")
    
    if number_of_sales > 0:
        print(get_log_prefix(collection) + "Prepping Tweets for " + str(number_of_sales) + " sales..")
        events_list = json_response['asset_events'] # Remember, this is just a list!
        sendTweets(events_list, collection, dbfile, dry_run, sleep_time)
    else:
        print(get_log_prefix(collection) + "No new sales, nothing to Tweet about.")

print("\n")
print("Done Checking for Sales @ " +datetime.now().strftime("%Y-%m-%d %H:%M:%S"))