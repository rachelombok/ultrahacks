import config
import tweepy

#setup authentication
auth = tweepy.OAuthHandler('ezQ7tprVDOz05zygVdCv5FuCI', '4eBqZlsnrpKwcsYA4bgM9o8uZVb6QBCJeBJiqdRM2zYBGVgq2g')
auth.set_access_token('1312494899363753991-v78aXjN9RizE4a4VgSIgrKw9CzbWX9', 'vtfQJd3gVoJgiZO7rqoCRAQReIR85NkNjIZgyvEIoBWyk')
api = tweepy.API(auth)

api.update_status(status="hello this is tweepy")