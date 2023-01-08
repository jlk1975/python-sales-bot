import json
from decimal import Decimal
from web3 import Web3
from currency_symbols import CurrencySymbols
# import pyshorteners as sh

# list = ["wiz1", "wiz2", "wiz3"]
# list.append('hello')
# print(list)


with open('test_data.json') as f:
    data = json.load(f)

for asset_event in data['asset_events']:
    #  if type(asset_event['asset']) is dict:
    #     asset_name = asset_event['asset']['name']
    #     total_price = asset_event['total_price']
    #     formatted_units = Web3.fromWei(int(total_price), 'ether')
    #     token_eth_price = asset_event['payment_token']['eth_price']
    #     formatted_eth_price = formatted_units * int(float(token_eth_price))
    #     token_usd_price = Decimal(asset_event['payment_token']['usd_price'])
    #     formatted_usd_price = formatted_units * token_usd_price
    #     ethSymbol = CurrencySymbols.get_symbol('ETH')
    #     opensea_link = asset_event['asset']['permalink']
    #     # s = sh.Shortener()
    #     # opensea_link = s.tinyurl.short(event['asset']['permalink'])
      
    #     tweetText = asset_name + " bought for " \
    #     + str(formatted_eth_price) \
    #     + ethSymbol \
    #     + "($" + str(round(formatted_usd_price, 2)) + ")" \
    #     + " #NFT " + opensea_link

    #     print(tweetText)
    #     # print(len(tweetText)) #keep below 280

     if type(asset_event['asset_bundle']) is dict:
        # print(asset_event['created_date'])
        # print(asset_event['total_price'])
        # print(asset_event['payment_token']['decimals'])
        # print(asset_event['payment_token']['eth_price'])
        # print(Decimal(asset_event['payment_token']['usd_price']))

        sold_bundle_items = ""
        
        # print(len(asset_event['asset_bundle']['assets']))

        # for i, item in enumerate(items):
        for i, item in enumerate(asset_event['asset_bundle']['assets']):
            # print(i)
            # if i == len(asset_event['asset_bundle']['assets']) - 1:
            #     print("last")
        # for item in asset_event['asset_bundle']['assets']: #these are dictionaries.
            if len(sold_bundle_items) == 0:
                sold_bundle_items = sold_bundle_items + item['name']
            #  if i == len(items) - 1:
            elif i == len(asset_event['asset_bundle']['assets']) - 1:
                sold_bundle_items = sold_bundle_items + ", and " + item['name']
            else:
                sold_bundle_items = sold_bundle_items + ", " + item['name']

            # print(sold_bundle_items)
            # print(item['name'])
            # sold_bundle_items.append(item['name'])
            # print("  " + item['name'])
            # print("  " + item['permalink'])
            # s = sh.Shortener()
            # print(s.tinyurl.short(item['permalink']))

        tweetText = sold_bundle_items + " were bought for " #\
        # + str(formatted_eth_price) \
        # + ethSymbol \
        # + "($" + str(round(formatted_usd_price, 2)) + ")" \
        # + " #NFT " + opensea_link

        print(tweetText)
        # # print(len(tweetText)) #keep below 280
    