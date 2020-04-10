import tweepy
from datetime import date
from datetime import datetime
import match
import csv
import config
import emoji


# generate the headline with details of the round and competition
def format_competition_round_headline(match):
    if len(match.competition_round) > 0:
        round_prefix = (" " if match.competition_round.upper().find("ROUND") != -1 else " round ")
        return match.competition + round_prefix + match.competition_round
    else:
        return match.competition

# generate the intro of the headline with the date and competition details
def format_intro_headline(match):
    str_otd_intro = "OTD on {}, in the {}, "
    return str_otd_intro.format(match.date.strftime("%d %b, %Y"), format_competition_round_headline(match))

def generate_extra_time_headline(match):
    str_nt_details = ("" if match.normal_time == "NT" else (" after extra time" if match.normal_time=="AET" else " in penalties"))
    return str_nt_details   

# generate a headline for the selected match
def generate_headline(match):
   
    emoji.load_emoji_data("data/emoji.csv")
    str_headline_victory = " {} {} {} ({}-{}){} {}"
    str_headline_draw = " {} {} {} ({}-{}) {}"
    str_headline_body = ""
    str_nt_details = ""
    if match:
        # now generate the headline
        str_nt_details = generate_extra_time_headline(match)
        excitement_index = match.excitement_index
        selected_emoji = emoji.generate_emoji(excitement_index)
        if excitement_index >= 2:
            str_headline_body = str_headline_victory.format(config.MY_TEAM,"beat", match.opponent,match.score[0],match.score[1],str_nt_details,selected_emoji)
        elif excitement_index < 0:
            str_headline_body = str_headline_victory.format(config.MY_TEAM, "lost to", match.opponent,match.score[0],match.score[1],str_nt_details,selected_emoji)
        else:
            str_headline_body = str_headline_draw.format(config.MY_TEAM, "drew with", match.opponent, match.score[0], match.score[1],selected_emoji)
    else:
        return "No game played on this date"
    
    return config.EMOJI_PREFIX + format_intro_headline(match) + str_headline_body + get_otd_suffix()

def get_otd_suffix():
    return " " + config.TAGS

def get_otd_headline(date_of_interest = date.today()):
    # defaults to today's date
    all_matches = match.load_matches_data(date_of_interest, config.DATA_INPUT)
    selected_match = match.choose_random_match(all_matches)
    headline = generate_headline(selected_match)
    return headline
   

def tweet_headline(headline):
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
    auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)

    # Create API object
    api = tweepy.API(auth)

    # Create a tweet
    api.update_status(headline)
