import configparser
import click
import mongoengine
from pymongo import MongoClient

import ui

config = configparser.ConfigParser()
config.read('config.ini')


def main():
    click.clear()
    click.echo(f'{click.style("Twitter Hashtag Ranking", fg="blue")} - v1')
    print("Select the database that you want to work on, or write the name of a new one.")

    forbidden_names = ['local', 'admin', 'config']

    mongoclient = MongoClient(host=config['MONGODB']['Host'], port=int(config['MONGODB']['Port']),
                              username=config['MONGODB']['Username'], password=config['MONGODB']['Password'])
    db_list = [db for db in mongoclient.list_database_names() if db not in forbidden_names]
    mongoclient.close()

    for db in db_list:
        print("\t- " + db)

    db_name = click.prompt("\nEnter the name of an existing database or a new one", confirmation_prompt=True, type=str)
    mongoengine.connect(db=db_name, username=config['MONGODB']['Username'], password=config['MONGODB']['Password'],
                        authentication_source=config['MONGODB']['Authentication_Source'],
                        host=config['MONGODB']['Host'])

    ui.menu()


if __name__ == '__main__':
    main()
    mongoengine.disconnect()
