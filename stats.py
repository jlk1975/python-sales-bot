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
import emoji
from currency_symbols import CurrencySymbols
import time
import pymods.tweet

# Create the parser
my_parser = argparse.ArgumentParser(prog='statsbot', description='Tweet NFT Stats')

# Add Positional (Required) Arguments:
# my_parser.add_argument('Collections',
#                        type=str,
#                        help='the nft collection to check')

# Add Optional Arguments:
my_parser.add_argument('-s',
                       '--sleep',
                       type=int,
                       help='Time to Sleep in Seconds before next Tweet')
my_parser.add_argument('-d',
                       '--dryrun',
                       action='store_true',
                       help='DRY RUN, WILL NOT SEND TWEETS')
                    
# Execute the parse_args() method
args = my_parser.parse_args()

# Set variables
sleep_time = args.sleep
dry_run = args.dryrun

dotenv_path = './.env'
load_dotenv(dotenv_path=dotenv_path)

# Secret decoder ring
# print(emoji.demojize("📊"))

emojis = {
  "PixaBrews": ":beer_mug:",
  "PIXA Token": ":money_bag:",
  "PixaLE": ":large_blue_diamond:",
  "PixaWargs Official": ":wolf:",
  "PixaWitches": ":woman_mage:",
  "PixaWizards": ":man_mage:",
  "PixaWyverns": ":dragon_face:"
}

ethSymbol = CurrencySymbols.get_symbol('ETH')

files = ['pixabrews', 'pixale', 'pixawargsofficial', \
'pixawitches', 'pixawizards', 'pixawyverns']

chart = emoji.emojize(':bar_chart:')

msg = "\nToday's @pixa_nft stats! " + chart + " .. \n"
 
for file in files:
  fname = "pixa_stats/" + file + ".json"
  with open(fname, 'r') as f:
    collection_data = json.load(f)
    emj = emoji.emojize(emojis[collection_data['name']])
    cname = collection_data['name']
    floor = collection_data['floor']
    num_owners = collection_data['num_owners']
    avg_price = round(collection_data['average_price'], 3)
    volume = round(collection_data['total_volume'], 3)
    total_sales = collection_data['total_sales']
    total_supply = collection_data['total_supply']
    
    msg = " #" + cname + " " + emj + " stats " + chart + " for @pixa_nft .. \n" \
    + "    Floor: " + str(floor) + ethSymbol +"\n" \
    + "    Average Price: " + str(avg_price) + ethSymbol +"\n" \
    + "    Owners: " + str(num_owners) +"\n" \
    + "    Volume: " + str(volume) + ethSymbol +"\n" \
    + "    Sales: " + str(total_sales) +"\n" \
    + "    Supply " + str(total_supply) +"\n" \
    + "https://opensea.io/collection/" + file

    pymods.tweet.sendTweet(msg, dry_run)
    if sleep_time:
      time.sleep(sleep_time)