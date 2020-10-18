import tweepy
import csv
from . import config
import json
import urllib.request


def add_user(verifier, session):
    auth = tweepy.OAuthHandler(config.api_key, config.api_secret_key)
    try:
        auth.request_token = session['request_token']
    except:
        return
    
    try:
        auth.get_access_token(verifier)
        print(auth.access_token, auth.access_token_secret)
    except:
        return

    api = tweepy.API(auth)
    detected_user = False
    uid = api.me().id
    lines = []
    lines.append([api.me().id, auth.access_token, auth.access_token_secret, 0, 0])
    with open('users.csv', newline= '') as csvfile:
        userreader = csv.reader(csvfile)
        for row in userreader:
            lines.append(row)
            if row[0] == str(api.me().id):
                lines.remove(row)
                
    with open('users.csv','w', newline= '') as csvfile:
        userwriter = csv.writer(csvfile)
        userwriter.writerows(lines)

    auth = tweepy.OAuthHandler(config.api_key, config.api_secret_key)
    auth.set_access_token(config.access_token, config.access_token_secret)

    api = tweepy.API(auth)
    api.send_direct_message(uid, "Hey I'm going to keep your dm's clear from now on! Type 'MUTE' followed by a list of words and I'll add them to your block list! Messages should get checked every minute!")
    

def set_muted_words(values):
    user = values['user']
    words = values['link']
    lines = []
    with open('users.csv', newline= '') as csvfile:
        userreader = csv.reader(csvfile)
        for row in userreader:
            if row[0] == user:
                if int(row[3]) < int(words):
                    row[3] = words
            lines.append(row)
    with open('users.csv','w', newline= '') as csvfile:
        userwriter = csv.writer(csvfile)
        userwriter.writerows(lines)

def set_muted_images(values):
    user = values['user']
    image = values['link']
    lines = []
    with open('users.csv', newline= '') as csvfile:
        userreader = csv.reader(csvfile)
        for row in userreader:
            if row[0] == user:
                row[4] = image
            lines.append(row)
    with open('users.csv','w', newline= '') as csvfile:
        userwriter = csv.writer(csvfile)
        userwriter.writerows(lines)

def check_bot_dms():
    print("Checking_DMS")
    auth = tweepy.OAuthHandler(config.api_key, config.api_secret_key)
    auth.set_access_token(config.access_token, config.access_token_secret)

    api = tweepy.API(auth)
    dms = api.list_direct_messages()
    for message in dms:
        data = message.message_create
        if 'MUTE' in data['message_data']['text'] and not(str(data['sender_id']) in str(api.me().id)):
            check_field = "["+str(data['sender_id'])+","+str(message.id)+"]"
            urllib.request.urlretrieve("https://bouncerdjango.herokuapp.com/receiver/?bot{}".format(config.api_secret_key)+check_field)


def check_all_dms():
    lines = []
    print("Checking_All_DMS")
    
    with open('users.csv', newline= '') as csvfile:
        userreader = csv.reader(csvfile)
        for row in userreader:
            lines.append(row)
    
    for data in lines:
        auth = tweepy.OAuthHandler(config.api_key, config.api_secret_key)
        auth.set_access_token(data[1],data[2])
        try:
            api = tweepy.API(auth)
            message = api.get_direct_message(data[3])
            text = message.message_create['message_data']['text']
            words = text.replace("MUTE", '').split()
            
            dms = api.list_direct_messages()
            for dm in dms:
                delete = False
                text = dm.message_create['message_data']['text']
                for word in words:
                    if word.lower() in text.lower() and not(dm.id in data[3]):
                        delete = True
                if delete:
                    api.destroy_direct_message(dm.id)
                    print("Deleted something")

        except tweepy.TweepError:
            return