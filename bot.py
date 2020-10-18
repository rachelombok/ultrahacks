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


while stop < 20:
    stop += 1
    print("Checking dms")
    urllib.request.urlretrieve("https://bouncerdjango.herokuapp.com/receiver/?update"+config.api_secret_key)
    urllib.request.urlretrieve("https://bouncerdjango.herokuapp.com/receiver/?check_all"+config.api_secret_key)
    time.sleep(60)
