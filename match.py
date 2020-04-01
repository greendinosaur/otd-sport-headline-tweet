import csv

# stores information about a match
class Match:
    def __init__(self, date, competition, competition_round, opponent, place):
        self.date = date
        self.opponent = opponent
        self.place = place # A, H, N
        self.competition = competition
        self.competition_round = competition_round

    def set_result_data(self, result, score, penalty_score, goal_scorers):
        self.result = result
        self.score = score # score is a tuple (n, m) in relation to home team
        self.penalty_score = penalty_score # a tuple in relation to home team
        self.goal_scorers = goal_scorers # a list of tuples containing the goal scorers and times of the goals


# calculates the result from my team's perspective
# score is a tuple (H, A) of traditional score with the home team first
def calc_result_traditional(location, score):
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
    result = ('W' if score[0]>score[1] else ('L' if score[0]<score[1] else 'D'))
    return result

def save_matches_to_file(fname_out, matches):
    with open(fname_out, 'a', newline='', encoding='utf8') as f:
        writer = csv.writer(f)
        for output_match in matches:
            writer.writerow([output_match.date.strftime("%Y-%m-%d"), output_match.competition, output_match.competition_round, output_match.place, output_match.opponent,output_match.result,str(output_match.score[0])+"-"+str(output_match.score[1]), output_match.penalty_score, output_match.goal_scorers])


