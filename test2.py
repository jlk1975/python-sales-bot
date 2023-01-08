import json
from decimal import Decimal
from web3 import Web3
from currency_symbols import CurrencySymbols

with open('test_data.json') as f:
    data = json.load(f)

for asset_event in data['asset_events']:
    total_price = asset_event['total_price']
    formatted_units = Web3.fromWei(int(total_price), 'ether')
    token_eth_price = asset_event['payment_token']['eth_price']
    formatted_eth_price = formatted_units * int(float(token_eth_price))
    token_usd_price = Decimal(asset_event['payment_token']['usd_price'])
    formatted_usd_price = formatted_units * token_usd_price
    ethSymbol = CurrencySymbols.get_symbol('ETH')

    if type(asset_event['asset']) is dict:
        asset_name = asset_event['asset']['name']
        opensea_link = asset_event['asset']['permalink']

        tweetText = asset_name + " bought for " \
        + str(formatted_eth_price) \
        + ethSymbol \
        + "($" + str(round(formatted_usd_price, 2)) + ")" \
        + " #NFT " + opensea_link

    if type(asset_event['asset_bundle']) is dict:
        bundle_slug = asset_event['asset_bundle']['slug']
        opensea_link = "https://opensea.io/bundles/ethereum/" + bundle_slug

        sold_bundle_items = ""
        for i, item in enumerate(asset_event['asset_bundle']['assets']):
            if len(sold_bundle_items) == 0:
                sold_bundle_items = sold_bundle_items + item['name']
            elif i == len(asset_event['asset_bundle']['assets']) - 1:
                sold_bundle_items = sold_bundle_items + ", and " + item['name']
            else:
                sold_bundle_items = sold_bundle_items + ", " + item['name']

        tweetText = sold_bundle_items + " were bought for " \
        + str(formatted_eth_price) \
        + ethSymbol \
        + "($" + str(round(formatted_usd_price, 2)) + ")" \
        + " #NFT " + opensea_link

    print(tweetText)