import tweepy
import webbrowser
import time
import config
import urllib.request
import requests
import image_rec

from requests.auth import AuthBase


callback_uri = 'oob'
auth = tweepy.OAuthHandler(config.api_key, config.api_secret_key)

redirect_url = auth.get_authorization_url()
webbrowser.open(redirect_url)
user_pin_input = input("What is the pin? ")

auth.get_access_token(user_pin_input)

api = tweepy.API(auth)
me = api.me()

auth.consumer_key

messages = api.list_direct_messages()

data = api.rate_limit_status()

def check_picture(url):
    s = auth.oauth
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
            
    else:
        for word in muted_words:
            if word.lower() in str(message.message_create['message_data']['text']).lower():
                remove_message(message.id)

