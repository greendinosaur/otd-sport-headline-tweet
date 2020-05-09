import onthisday
import config
import tweet

print('Loading function')
# need to reference:
# match.py, otd.py, emoji.py
# config.py
# data/emoji.csv
# data/everton_wof_new.csv
# these will need adding to the zip file
# also any dependencies which is the tweepy library and its dependencies


def lambda_handler(event, context):
    # event is a dictionary, e.g. event['key1'])
    headline = onthisday.get_otd_headline()
    print(headline)
    if config.ENVIRONMENT != "DEV" and headline != onthisday.NO_MATCH_HEADLINE:
        print("tweeting the headline")
        tweet.tweet_headline(headline)
    return headline
