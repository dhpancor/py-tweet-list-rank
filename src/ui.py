import click
import tweets_extractor


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
        with_retweets = click.prompt("Include retweets?", type=click.Choice(['Yes', 'No'], False))
        if with_retweets.lower() == 'no':
            query += " -filter:retweets"

        print("There are 4 different modes for the extraction: (3 of them for movies and shows)")
        print(" - Strict mode: Only include each preference if there is only one result from The Movie Database.")
        print(" - Order by popularity: Only include the first result ordered by popularity.")
        print(" - TMBD: Include the first result based on TMBD criteria.")
        print(" - Keep user text: Do not use The Movie Database service. Useful for lists that aren't movies or shows.")

        mode = click.prompt("Select the mode",
                            type=click.Choice(['strict', 'order_by_popularity', 'tmdb', 'keep_user_text'], False))
        max_tweets = click.prompt("How many tweets do you want to process? (Not final amount of extracted tweets)",
                                  type=int)
        tweets_extractor.extract(query, mode, max_tweets)
