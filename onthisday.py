import tweepy
import random
from datetime import date
from datetime import datetime
import match
import csv
import config


def load_matches_data(date_of_interest, fname):
    # load the matches data and returns those whose date (day and month) match
    file_in = open(fname, "r")
    matches = []
    loaded_match = None
    for line in file_in:
        match_details = line.split(',')
        match_date = datetime.strptime(match_details[0], "%Y-%m-%d")
        if match_date.day == date_of_interest.day and match_date.month == date_of_interest.month:
            # found a matching date
            loaded_match = match.Match(match_date,match_details[1],match_details[2],match_details[4],match_details[3])
            loaded_match.set_result_data(match_details[5],tuple([int (n) for n in match_details[6].split('-')]),"","")
            matches.append(loaded_match)

    file_in.close()
    return matches
  
# given a list of matches, choose one at random
def choose_random_match(matches):
    # choose a random match
    if matches:
        return random.choice(matches)
    else:
        return None

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

# generate a headline for the selected match
def generate_headline(match):
   
    str_headline_victory = " {} {} {} ({}-{})"
    str_headline_draw = " {} {} {} ({}-{})"
    # str_headline_cupwin = " {} won the {} cup. {} {} {} with a final score of ({},{})"
    str_headline_body = ""
    if match:
        # now generate the headline
        excitement_index = calc_excitement_index(match)
        if excitement_index >= 2:
            str_headline_body = str_headline_victory.format(config.MY_TEAM,"beat", match.opponent,match.score[0],match.score[1])
        elif excitement_index < 0:
            str_headline_body = str_headline_victory.format(config.MY_TEAM, "lost to", match.opponent,match.score[0],match.score[1])
        else:
            str_headline_body = str_headline_draw.format(config.MY_TEAM, "drew with", match.opponent, match.score[0], match.score[1])
    else:
        return "No game played on this date"
    
    return format_intro_headline(match) + str_headline_body

def calc_excitement_index(match):
    # use the differences in the scores to determine how exciting the game was
    score_diff = abs(match.score[0] - match.score[1])
    if score_diff > 3:  # a big win
        return (3 if match.result == 'W' else -3)
    elif score_diff > 0: # a narrow win
        return (2 if match.result =='W' else -2)
    elif score_diff == 0: # a draw
        return (1 if match.score[0] > 0 else 0)

def get_otd_headline(date_of_interest = date.today()):
    # defaults to today's date
    all_matches = load_matches_data(date_of_interest, config.DATA_INPUT)
    selected_match = choose_random_match(all_matches)
    headline = generate_headline(selected_match)
    if config.ENVIRONMENT == "DEV":
        print(headline)

def tweet_headline(headline):
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
    auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)

    # Create API object
    api = tweepy.API(auth)

    # Create a tweet
    api.update_status(headline)

get_otd_headline()