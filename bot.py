import tweepy
import time
import webbrowser
import config
import csv
import requests
import urllib.request

auth = tweepy.OAuthHandler(config.api_key, config.api_secret_key)
auth.set_access_token(config.access_token, config.access_token_secret)

api = tweepy.API(auth)
#api.update_status("Hello, Twitter! #UltraHacks")

stop = 0
#urllib.request.urlretrieve("http://127.0.0.1:8000/receiver/?check_all")

while stop < 1:
    stop += 1
    print("Checking dms")
    dms = api.list_direct_messages()
    for message in dms:
        data = message.message_create
        if 'MUTE' in data['message_data']['text']:
            check_field = "["+str(data['sender_id'])+","+str(message.id)+"]"
            urllib.request.urlretrieve("http://127.0.0.1:8000/receiver/?bot{}".format(config.api_secret_key)+check_field)
                  
    time.sleep(60)
