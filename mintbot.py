import json
import requests


response = requests.get(
    'https://api.looksrare.org/api/v1/events',
     params={
        "collection": "0xD8ab2B8b8A6036DcB91D44cbDf6e9a42a199EBE2", 
        "type": "MINT",
        "pagination[first]": 150,
     },
)
    
# json_response = response.json() # Deserialize, <class 'dict'>
    
# Do not remove next line, useful for troubleshooting...
print(json.dumps(json.loads(response.text), indent =2))