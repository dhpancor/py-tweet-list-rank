import configparser
import html
import re
import requests
import tweepy

from models.tweet import Tweet

config = configparser.ConfigParser()
config.read('config.ini')


def extract(query, mode='strict', max_tweets=5000):
    regex = r"^[\*\-\d]+[ \.\-]+(.+)$"

    auth = tweepy.AppAuthHandler(config['TWITTER']['Auth_Public_Key'], config['TWITTER']['Auth_Secret_Key'])
    api = tweepy.API(auth, wait_on_rate_limit=True)
    for tweet in tweepy.Cursor(api.search, q=query, rpp=100, tweet_mode='extended',
                               include_entities=False).items(max_tweets):
        new_tweet = Tweet(tweet_id=tweet.id_str, user_id=tweet.user.id_str, created_at=tweet.created_at)

        matches = list(re.finditer(regex, tweet.full_text, re.MULTILINE))

        if not (tweet.is_quote_status or tweet.retweeted) and len(matches) > 2:
            for num, match in enumerate(matches):
                sanitized_preference = html.unescape(re.sub(r'[\W_]+', '', match.group(1).strip()))
                if mode != 'keep_user_text':
                    r = requests.get('https://api.themoviedb.org/3/search/movie?api_key=' + config['TMDB'][
                        'Secret_Key'] + '&query=' + sanitized_preference)
                    if r.status_code == 200:
                        response = r.json()
                        if mode == 'strict':
                            if response['total_results'] == 1:
                                new_tweet.preferences.append(response['results'][0]['title'])
                        elif mode == 'order_by_popularity':
                            if response['total_results'] >= 1:
                                response['results'] = sorted(response['results'], key=lambda x: x['popularity'],
                                                             reverse=True)
                                new_tweet.preferences.append(response['results'][0]['title'])
                        elif mode == 'tmdb':
                            if response['total_results'] >= 1:
                                new_tweet.preferences.append(response['results'][0]['title'])
                else:
                    new_tweet.preferences.append(sanitized_preference)

            if len(new_tweet.preferences) >= 1:
                new_tweet.save()
