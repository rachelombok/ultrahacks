from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import config, user_handler, bot_handler
import tweepy

# Create your views here.
session = {}

def home(request):
    url = request.get_full_path()
    if 'update' in url and config.api_secret_key in url:
        user_handler.check_bot_dms()
        return HttpResponse("<h1>Bot Call</h1>")
    elif 'check_all' in url and config.api_secret_key in url:
        user_handler.check_all_dms()
        return HttpResponse("<h1>Bot Call</h1>")
    elif 'bot' in url:
        if config.api_secret_key in url:
            start = url.index('[')
            comma = url.index(',')
            end = url.index(']')
            values = {"user":url[start+1:comma], "link":url[comma+1: end]}
            user_handler.set_muted_words(values)
        return HttpResponse("<h1>Bot Call</h1>")
    elif not ('request_token' in session):
        auth = tweepy.OAuthHandler(config.api_key, config.api_secret_key)
        redirect_url = auth.get_authorization_url()
        session['request_token'] = auth.request_token
        return redirect(redirect_url)
    else:
        return home_old(request)

def home_old(request):
    if(request.GET.get('oauth_verifier', None) != None):
        user_handler.add_user(request.GET['oauth_verifier'], session)
    session.clear()
    return redirect("https://twitter.com/home")
