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


