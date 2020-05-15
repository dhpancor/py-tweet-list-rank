import tweepy
import re
import mongoengine
import html
import requests
from models.tweet import Tweet

MAX_TWEETS = 25000
TMDB_API_KEY = 'f023557327f3b5a2361162c5e9cccb3c'
mongoengine.connect(db='tweets_test4', username='root', password='example', authentication_source='admin', host='mongodb://localhost')


def main():
    # otro regex... va mejor con el nuevo regex = r"^[\*\-\d]\.?([\w ]+)$"  # link to regex https://regex101.com/r/jdXoqc/1
    regex = r"^[\*\-\d]+[ \.\-]+(.+)$"

    auth = tweepy.AppAuthHandler('2t3xURkcPZmJzL4xm9MulZz5i', 'T8RkbFyT5k9dcws8J6Ke72DC5JnNpDi1oDt7h2UFXHR9i4taHe')
    api = tweepy.API(auth, wait_on_rate_limit=True)
    for tweet in tweepy.Cursor(api.search, q="mis peliculas -filter:retweets", rpp=100, tweet_mode='extended', include_entities=False).items(MAX_TWEETS):
        matches = list(re.finditer(regex, tweet.full_text, re.MULTILINE))

        if not(tweet.is_quote_status or tweet.retweeted) and len(matches) > 2:
            #  new_tweet = Tweet(tweet_id=tweet.id_str, user_id=tweet.user.id_str, created_at=tweet.created_at)
            for num, match in enumerate(matches):
                sanitized_match = html.unescape(match.group(1).strip())
                r = requests.get('https://api.themoviedb.org/3/search/movie?api_key=' + TMDB_API_KEY + '&query=' + sanitized_match)
                if r.status_code == 200:
                    results = r.json()
                    if results['total_results'] > 0:
                        results = sorted(results['results'], key=lambda x: x['popularity'], reverse=True)
                        print(results[0]['title'] + " (previously " + sanitized_match + ")")
                    # if results['total_results]:
                #  new_tweet.preferences.append(sanitized_match)
                # print(sanitized_match)

            #  new_tweet.save()


if __name__ == '__main__':
    main()
    mongoengine.disconnect()
