import json
import time

import requests
import random

DELAY = 5 # DELAY IN MINUTES

COLORS = {
    'red': 2,
    'orange': 3,
    'yellow': 4,
    'green': 6,
    'light_green': 8,
    'dark_blue': 12,
    'blue': 13,
    'light_blue': 14,
    'dark_purple': 18,
    'purple': 19,
    'pink': 23,
    'brown': 25,
    'black': 27,
    'gray': 29,
    'light_gray': 30,
    'white': 31
}

IMAGE = [
    (998, 999, "red"), # Example
    (117, 259, "dark_purple") # Example
] # List of tuples with following values (int:x, int:y, string:color (must be an element of colors))

client_auth = requests.auth.HTTPBasicAuth('client_id', 'client_secret') # 
post_data = {"grant_type": "password", "username": "REDDIT_USERNAME", "password": "REDDIT_PASSWORD"}
headers = {"User-Agent": "TestBot 123"}

response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)

TOKEN = response.json()['access_token']

headers = {
    "authorization": "Bearer " + TOKEN,
    "content-type": "application/json"
}

while True:
    current = random.choice(IMAGE)

    data = {"operationName": "setPixel",
            "variables": {
                "input": {
                    "actionName": "r/replace:set_pixel",
                    "PixelMessageData": {
                        "coordinate": {
                            "x": current[0],
                            "y": current[1]
                        },
                        "colorIndex": COLORS[current[2]],
                        "canvasIndex": 0
                    }
                }
            },
            "query": "mutation setPixel($input: ActInput!) {\n act(input: $input) {\n data {\n ... on BasicMessage {\n "
                     "id\n data {\n ... on GetUserCooldownResponseMessageData {\n nextAvailablePixelTimestamp\n "
                     "__typename\n }\n ... on SetPixelResponseMessageData {\n timestamp\n __typename\n }\n __typename\n "
                     "}\n __typename\n }\n __typename\n }\n __typename\n }\n}\n "
    }

    resp = requests.post("https://gql-realtime-2.reddit.com/query", data=json.dumps(data), headers=headers)
    if "errors" in resp.json():
        error = resp.json()["errors"]
        print("Error: " + str(error))
    else:
        print("Placed tile at " + str(current[0]) + ";" + str(current[1]) + " with color " + current[2])
        time.sleep(60 * DELAY)
