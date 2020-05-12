""" generates the headline and tweets it
"""
from otd import onthisday, tweet
import config


def main():
    """ generates a headline based on a historic match
        on this day and month
        It is then tweeted
    """
    headline = onthisday.get_otd_headline()
    print(headline)
    if config.ENVIRONMENT != "DEV" and headline != onthisday.NO_MATCH_HEADLINE:
        print("tweeting the headline")
        tweet.tweet_headline(headline)


if __name__ == "__main__":
    main()
