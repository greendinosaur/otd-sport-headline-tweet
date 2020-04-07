import csv

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
        
    def set_match_report(self, match_report_url):
        self.match_report_url = match_report_url

def calc_result_traditional(location, score):
    """ calculates the result from the team's perspective

        location is where the match was played (home or away or neutral)
        score is a tuple (H, A) of traditional score with the home team first
        returns a 'W', 'L' or 'D'
    """ 
    if location == 'H' or location == 'N':
        if score[0] > score[1]:
        # home win
            return 'W'
        elif score[0] < score[1]:
            return 'L'
        else:
            return 'D'
    elif location == 'A':
        if score[0] > score[1]:
            return 'L'
        elif score[0] < score[1]:
            return 'W'
        else:
            return 'D'

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


