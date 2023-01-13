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
import pymods.tweet

dotenv_path = './.env'
load_dotenv(dotenv_path=dotenv_path)

# Secret decoder ring
# print(emoji.demojize("📊"))

emojis = {
  "money": ":money_bag:",
  "hat": ":top_hat:",
  "sword": ":dagger:",
  "book": ":open_book:",
  "house": ":house_with_garden:",
  "badge": ":name_badge:",
  "pixa_wizard": ":man_mage:",
  "pixa_witch": ":woman_mage:",
  "pixa_wyvren": ":dragon_face:",
  "pixa_warg": ":wolf:",
  "pixa_brew": ":beer_mug:",
  "pixa_tome": ":framed_picture:",
  "heart": ":red_heart:",
  "wand": ":magic_wand:",
  "diamond": ":large_blue_diamond:",
  "stats": ":bar_chart:"
}
# msg = "Today's @pixa_nft stats " + emoji.emojize(emojis['stats']) + " ... "
msg = "i " + emoji.emojize(emojis['heart']) + "  @pixa_nft " + emoji.emojize(emojis['pixa_wizard']) + " " \
+ emoji.emojize(emojis['pixa_witch']) + " " \
+ emoji.emojize(emojis['pixa_wyvren']) + " " \
+ emoji.emojize(emojis['pixa_warg']) + " " \
+ emoji.emojize(emojis['pixa_brew']) + " " \
+ emoji.emojize(emojis['pixa_tome']) + " " \
+ emoji.emojize(emojis['wand']) + " " \
+ emoji.emojize(emojis['diamond']) + " " \
+ emoji.emojize(emojis['sword'])
pymods.tweet.sendTweet(msg)