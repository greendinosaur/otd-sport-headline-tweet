import tweepy
import config


def tweet_headline(message,
                   consumer_key = config.CONSUMER_KEY,
                   consumer_secret=config.CONSUMER_SECRET,
                   access_token=config.ACCESS_TOKEN,
                   access_token_secret=config.ACCESS_TOKEN_SECRET):
    """ tweets the provided message to twitter
        message is the status message to tweet
        can call with the twitter keys directly, otherwise, defaults
        to the values stored in the config
    """
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(consumer_key,
                               consumer_secret)
    auth.set_access_token(access_token,
                          access_token_secret)

    # Create API object
    api = tweepy.API(auth)

    # Create a tweet
    api.update_status(message)
