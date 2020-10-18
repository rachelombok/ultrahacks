import tweepy
import webbrowser
import time
import config
import urllib.request
import requests
import image_rec

from requests.auth import AuthBase

auth = tweepy.OAuthHandler(config.api_key, config.api_secret_key)
auth.set_access_token(config.access_token, config.access_token_secret)

api = tweepy.API(auth)
me = api.me()

messages = api.list_direct_messages()

data = api.rate_limit_status()

def check_picture(url):
    s = auth.oauth
    s.max_redirects = 100
    data = s.get(url)
    with open('image.jpg', 'wb') as fobj:
        fobj.write(data.content)
    
    original = image_rec.ComparableImages("img1.jpg")
    compare = image_rec.ComparableImages("image.jpg")
    
    data = image_rec.compare_images(original.image_gray, compare.image_gray)

    if(data['mse'] < 10000 and data['ssim'] > 0.5):
        return True
    return False

muted_words = {"dog", "cat", "banana", "apple"}
def remove_message(id):
    api.destroy_direct_message(id)

for message in api.list_direct_messages():
    if 'attachment' in message.message_create['message_data']:
        if check_picture(message.message_create['message_data']['attachment']['media']['media_url']):
            remove_message(message.id)
            

