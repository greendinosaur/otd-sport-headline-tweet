""" generates a sports headline based on a randomly selected match
"""
from datetime import date
import tweepy
import match
import config
import emoji

NO_MATCH_HEADLINE = "No game played on this date"

def format_competition_round_headline(selected_match):
    """ formats the competition round details

        match is the match used to create the headline
        returns the competition round details
    """
    if len(selected_match.competition_round) > 0:
        round_prefix = (" " if selected_match.competition_round.upper().find("ROUND") != -1 else " round ")
        return selected_match.competition + round_prefix + selected_match.competition_round
    return selected_match.competition

# generate the intro of the headline with the date and competition details
def format_intro_headline(selected_match):
    """ generates the introductory part of the headline to include date and competition

        match is the match used to create the headline
        returns the introductory part of the headline
    """
    str_otd_intro = "OTD on {}, in the {}, "
    return str_otd_intro.format(selected_match.date.strftime("%d %b, %Y"),
                                format_competition_round_headline(selected_match))

def generate_extra_time_headline(selected_match):
    """ generates additional data for the headline if the result
        occured in extra time or not

        match is the match used to create the headline
        returns the extra time headline details
    """
    str_nt_details = ("" if selected_match.normal_time == "NT"
                      else (" after extra time" if selected_match.normal_time == "AET" else " in penalties"))
    return str_nt_details

def generate_headline(selected_match):
    """  generates the actual headline

        match is the match used to generate the headline
        returns a string representing the headline
    """
    emoji.load_emoji_data()
    str_headline_champions = " {} are champions! {} beat {} ({}-{}){} {}"
    str_headline_victory = " {} {} {} ({}-{}){} {}"
    str_headline_draw = " {} {} {} ({}-{}) {}"
    str_headline_body = ""
    str_nt_details = ""
    if selected_match:
        # now generate the headline
        str_nt_details = generate_extra_time_headline(selected_match)
        excitement_index = selected_match.excitement_index
        selected_emoji = emoji.generate_emoji(excitement_index)
        if excitement_index == 4: # champions
            str_headline_body = str_headline_champions.format(
                                config.MY_TEAM,
                                config.MY_TEAM,
                                selected_match.opponent,
                                selected_match.score[0],
                                selected_match.score[1],
                                str_nt_details,
                                selected_emoji)
        elif excitement_index >= 2: # win
            str_headline_body = str_headline_victory.format(
                                config.MY_TEAM,
                                "beat",
                                selected_match.opponent,
                                selected_match.score[0],
                                selected_match.score[1],
                                str_nt_details,
                                selected_emoji)
        elif excitement_index < 0: # loss
            str_headline_body = str_headline_victory.format(
                                config.MY_TEAM,
                                "lost to",
                                selected_match.opponent,
                                selected_match.score[0],
                                selected_match.score[1],
                                str_nt_details,
                                selected_emoji)
        else: # draw
            str_headline_body = str_headline_draw.format(
                                config.MY_TEAM,
                                "drew with",
                                selected_match.opponent,
                                selected_match.score[0],
                                selected_match.score[1],
                                selected_emoji)
    else:
        return NO_MATCH_HEADLINE
    return config.EMOJI_PREFIX + format_intro_headline(selected_match) + str_headline_body + get_otd_suffix()

def get_otd_suffix():
    """ generates the suffix for the end of the headline
    """
    return " " + config.TAGS

def get_otd_headline(date_of_interest=date.today()):
    """ gets the headline for today's match

        date_of_interest is the date of the match, defaults to today's date
        returns the generated headline
    """
    all_matches = match.load_matches_data(date_of_interest,
                                          config.DATA_INPUT)
    selected_match = match.choose_random_match(all_matches)
    headline = generate_headline(selected_match)
    return headline

def tweet_headline(headline):
    """ tweets the provided headline to twitter
        headline is the status message to tweet
    """
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(config.CONSUMER_KEY,
                               config.CONSUMER_SECRET)
    auth.set_access_token(config.ACCESS_TOKEN,
                          config.ACCESS_TOKEN_SECRET)

    # Create API object
    api = tweepy.API(auth)

    # Create a tweet
    api.update_status(headline)
