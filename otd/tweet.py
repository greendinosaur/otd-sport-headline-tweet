import tweepy
import config


def tweet_headline(message):
    """ tweets the provided message to twitter
        message is the status message to tweet
    """
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(config.CONSUMER_KEY,
                               config.CONSUMER_SECRET)
    auth.set_access_token(config.ACCESS_TOKEN,
                          config.ACCESS_TOKEN_SECRET)

    # Create API object
    api = tweepy.API(auth)

    # Create a tweet
    api.update_status(message)
