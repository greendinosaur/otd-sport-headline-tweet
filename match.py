import csv
from datetime import date
from datetime import datetime
import random

class Match:
    """ Stores key data fields about a specific match for the team """

    def __init__(self, date, competition, competition_round, opponent, place):
        """ initialises the main fields of Match

            date - the date of the match
            opponent - the opponent
            place - the location of the match (A, H or N)
            compeition - the name of the competition the match was part of
            competition_round - the round of the competition

        """
        self.date = date
        self.opponent = opponent
        self.place = place # A, H, N
        self.competition = competition
        self.competition_round = competition_round
        self.normal_time = "NT"
        self.match_report = "" # URL to a web-page with a detailed match report

    def calc_is_cup_winner(self):
        # determines if the match was a final and if won
        # assumes the team is the winner of a cup!
        if self.result == 'W' and self.competition_round == "Final":
            return True
        else:
            return False

    def calc_excitement_index(self):
        """ determines how exciting the match was
            if the match was a cup final and the team is a winner then that is super exciting
            otherwise the excitement index is based on the score differential
        """
        if self.calc_is_cup_winner():
            return 4
        
        score_diff = abs(self.score[0] - self.score[1])
        if score_diff > 3:  # a big win for a team
            return (3 if self.result == 'W' else -3)
        elif score_diff > 0: # a narrow win for a team
            return (2 if self.result =='W' else -2)
        elif score_diff == 0: # a draw
            return (1 if self.score[0] > 0 else 0)

    def set_result_data(self, result, score, normal_time="NT", match_report_url=""):
        """ sets details about the actual result between the team and the opponent

            result - whether the match was a W, L or D for the team
            score  - the end of match score as a tuple (n as int, m as int) in relation to the team
            normal_time - a flag indicates whether the score was at the end of normal time ("NT"), extra time ("AET") or penalty shoot-out ("PST")
            match_report_url - a webpage that contains a detailed match report

        """
        self.result = result
        self.score = score 
        self.normal_time = normal_time
        self.match_report_url = match_report_url
        self.excitement_index = self.calc_excitement_index()


def calc_result_myteam_first(score):
    """ Determines whether the team won, drew or lost based on the score 
        Returns a 'W', 'L', 'D'
    """
    result = ('W' if score[0]>score[1] else ('L' if score[0]<score[1] else 'D'))
    return result

def save_matches_to_file(fname_out, matches):
    """ saves a list of match(es) to file """
    with open(fname_out, 'a', newline='', encoding='utf8') as f:
        writer = csv.writer(f)
        for output_match in matches:
            writer.writerow([output_match.date.strftime("%Y-%m-%d"), output_match.competition, output_match.competition_round, output_match.place, output_match.opponent,output_match.result,str(output_match.score[0])+"-"+str(output_match.score[1]), output_match.normal_time, output_match.match_report_url])

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
            loaded_match = Match(match_date,match_details[1],match_details[2],match_details[4],match_details[3])
            loaded_match.set_result_data(match_details[5],tuple([int (n) for n in match_details[6].split('-')]),match_details[7],match_details[8].rstrip())
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




