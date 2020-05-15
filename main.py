import tweepy
import re

MAX_TWEETS = 5000


def main():
    # otro regex... va mejor con el nuevo regex = r"^[\*\-\d]\.?([\w ]+)$"  # link to regex https://regex101.com/r/jdXoqc/1
    regex = r"^[\*\-\d]+[ \.\-]+([\w ()]+)$"

    auth = tweepy.AppAuthHandler('2t3xURkcPZmJzL4xm9MulZz5i', 'T8RkbFyT5k9dcws8J6Ke72DC5JnNpDi1oDt7h2UFXHR9i4taHe')
    api = tweepy.API(auth, wait_on_rate_limit=True)
    for tweet in tweepy.Cursor(api.search, q="mis peliculas", rpp=100, tweet_mode='extended').items(MAX_TWEETS):

        matches = list(re.finditer(regex, tweet.full_text, re.MULTILINE))

        if len(matches) > 2:
            print(tweet.id)
            for num, match in enumerate(matches):
                print(match.group(1).strip())


if __name__ == '__main__':
    main()
