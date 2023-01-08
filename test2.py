import json
from decimal import Decimal
import pyshorteners as sh

with open('test_data.json') as f:
    data = json.load(f)

for asset_event in data['asset_events']:
     if type(asset_event['asset']) is dict:
        print("\n")
        print("Single Sale")
        print(asset_event['created_date'])
        print(asset_event['asset']['name'])
        print(asset_event['total_price'])
        print(asset_event['payment_token']['decimals'])
        print(asset_event['payment_token']['eth_price'])
        print(Decimal(asset_event['payment_token']['usd_price']))
        print(asset_event['asset']['permalink'])
    #     s = sh.Shortener()
    #     print(s.tinyurl.short(asset_event['asset']['permalink']))
     if type(asset_event['asset_bundle']) is dict:
        print("\n")
        print("Bundle Sale ...")
        print(asset_event['created_date'])
        print(asset_event['total_price'])
        print(asset_event['payment_token']['decimals'])
        print(asset_event['payment_token']['eth_price'])
        print(Decimal(asset_event['payment_token']['usd_price']))
        for item in asset_event['asset_bundle']['assets']: #these are dictionaries.
            print("  " + item['name'])
            print("  " + item['permalink'])
            # s = sh.Shortener()
            # print(s.tinyurl.short(item['permalink']))