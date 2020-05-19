# py-tweet-list-rank

This is a Python script that, using Tweepy, extracts tweets with a list format (using regular expressions) and stores them into a database for further analysis.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the dependencies.

```bash
pip install -r requirements.txt
```

## Usage
1. Rename `config.ini.example` to `config.ini`.
2. Set your credentials. You can avoid The Movie Database API key if you won't use an extraction mode.

## Extraction models
### Movies and shows only
* Strict mode: Only include each preference if there is only one result from The Movie Database. Otherwise omits it. (The most accurate)
* Order by popularity: Only include the first result ordered by popularity.
* TMBD: Include the first result based on TMBD criteria.
### Other use case
* Keep user text: Do not use The Movie Database service. Useful for lists that aren't movies or shows. Stores the preference as is, as the user wrote it originally.