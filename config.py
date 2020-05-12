import os


# some configuration options
MY_TEAM = "Everton"
DATA_INPUT = "data/everton_wof_new.csv"
ENVIRONMENT = "TEST"
EMOJI_PREFIX = "\u26BD "  # emojis to show at the start of the tweet
TAGS = "#COYB #EFC #OTD"  # tags to be shown at the end of the tweet
# data required to authenticate to the twitter API
CONSUMER_KEY = os.environ['TWITTER_CONSUMER_KEY']
CONSUMER_SECRET = os.environ['TWITTER_CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['TWITTER_ACCESS_TOKEN_SECRET']
