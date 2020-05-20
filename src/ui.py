import click
import tweets_extractor
from models.tweet import Tweet


def menu():
    click.clear()
    print("What do you want to do now?")
    print("\t1 - Extract tweets")
    print("\t2 - Generate rank of existing tweets (if existing)")
    print("\t9 - Exit")

    click.echo(
        f"\n{click.style('Warning:', fg='black', bg='red', bold=True)} some options are destructive and will lead to unexpected results. (e.g. overwrite existing tweets)")
    option = click.prompt("Enter the number of the option: ", confirmation_prompt=True,
                          type=click.Choice(['1', '2', '9'], False))

    if option == '1':
        query = click.prompt("Query for the tweets, or hashtag", type=str)
        with_retweets = click.prompt("Include retweets?", type=click.Choice(['Yes', 'No'], False), default='No')
        if with_retweets.lower() == 'no':
            query += " -filter:retweets"

        print("There are 4 different modes for the extraction: (3 of them for movies and shows)")
        print(" - Strict mode: Only include each preference if there is only one result from The Movie Database.")
        print(" - Order by popularity: Only include the first result ordered by popularity.")
        print(" - TMDB: Include the first result based on TMBD criteria.")
        print(" - Keep user text: Do not use The Movie Database service. Useful for lists that aren't movies or shows.")

        mode = click.prompt("Select the mode",
                            type=click.Choice(['strict', 'order_by_popularity', 'tmdb', 'keep_user_text'], False))
        max_tweets = click.prompt("How many tweets do you want to process? (Not final amount of extracted tweets)",
                                  type=int)
        tweets_extractor.extract(query, mode, max_tweets)
    elif option == '2':
        n_ranking = click.prompt("How many results should be in the ranking?", type=int)
        n_samples = click.prompt("How many  of the top preferences should each tweet have to be considered?", type=int)

        votes = {}

        for tweet in Tweet.objects():
            for i in range(len(tweet.preferences)):
                points = n_samples - i
                if points < 1:
                    break
                votes[tweet.preferences[i]] = votes.get(tweet.preferences[i], 0) + points

        print({k: v for k, v in sorted(votes.items(), key=lambda item: item[1], reverse=True)})

        """pipeline = [
            {"$match": {}}
            , {'$project': {'preferences': 1}}
            , {'$unwind': '$preferences'}
            , {'$group': {
                '_id': {'preferences': '$preferences'}
                , 'count': {'$sum': 1}
            }
            }
        ]

        data = list(Tweet.objects().aggregate(pipeline))
        print(sorted(data, key=lambda x: x['count'], reverse=True))"""
