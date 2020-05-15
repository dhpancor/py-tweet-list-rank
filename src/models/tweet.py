from mongoengine import *


class Tweet(Document):
    tweet_id = StringField(required=True, primary_key=True)
    user_id = StringField(required=True)
    created_at = DateTimeField(required=True)
    preferences = ListField(StringField(), required=True)
