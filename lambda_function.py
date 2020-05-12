from otd import onthisday, tweet

print('Loading function')


def lambda_handler(event, context):
    # event is a dictionary, e.g. event['key1'])
    headline = onthisday.get_otd_headline()
    print(headline)
    # if you don't want it to tweet then setup a key called test inside the event
    if "test" not in event and headline != onthisday.NO_MATCH_HEADLINE:
        print("tweeting the headline")
        tweet.tweet_headline(headline)
    else:
        print("not tweeting")
    return headline
