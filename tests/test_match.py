import os
from datetime import date
import match


TEST_DATA_FILE = "tests/test_matches.csv"


def test_choose_random_match_none():
    assert match.choose_random_match(None) is None


def test_choose_random_match_emptylist():
    assert match.choose_random_match([]) is None


def test_choose_random_match_singleitem():
    matches = []
    new_match = match.Match(date.today(), "PREM", "1", "MAN U", 'H')
    new_match.set_result_data('W', (2, 1))
    matches.append(new_match)
    assert match.choose_random_match(matches) == new_match


def test_choose_random_match_multipleitems():
    matches = []
    new_match = match.Match(date.today(), "PREM", "1", "MAN U", 'H')
    new_match.set_result_data('W', (2, 1))
    matches.append(new_match)
    new_match1 = match.Match(date.today(), "PREM", "1", "MAN U", 'H')
    new_match1.set_result_data('W', (2, 1))
    matches.append(new_match1)
    assert not match.choose_random_match(matches) is None


def test_load_data_datematches():
    date_of_interest = date(2019, 8, 15)
    matches = match.load_matches_data(date_of_interest, TEST_DATA_FILE)
    print(matches)
    assert len(matches) == 1


def test_load_data_date_nomatches():
    date_of_interest = date(2019, 2, 15)
    matches = match.load_matches_data(date_of_interest, TEST_DATA_FILE)
    assert not matches


def test_load_data_date_twomatches():
    date_of_interest = date(2019, 8, 16)
    matches = match.load_matches_data(date_of_interest, TEST_DATA_FILE)
    assert len(matches) == 2


def test_load_data_match_data():
    date_of_interest = date(2019, 8, 15)
    matches = match.load_matches_data(date_of_interest, "tests/test_matches.csv")
    match_of_interest = matches[0]
    assert match_of_interest.date.month == date_of_interest.month
    assert match_of_interest.date.day == date_of_interest.day
    assert match_of_interest.opponent == "Arsenal"
    assert match_of_interest.place == "H"
    assert match_of_interest.competition == "Premier League"
    assert match_of_interest.result == 'L'
    assert match_of_interest.score == (1, 6)


def test_calc_excitement_index_nildraw():
    new_match = match.Match(date.today(), "PREM", "1", "MAN U", 'H')
    new_match.set_result_data('D', (0, 0))
    assert new_match.excitement_index == 0


def test_calc_excitement_index_nonnildraw():
    new_match = match.Match(date.today(), "PREM", "1", "MAN U", 'H')
    new_match.set_result_data('D', (1, 1))
    assert new_match.excitement_index == 1


def test_calc_excitement_index_lowwin():
    new_match = match.Match(date.today(), "PREM", "1", "MAN U", 'H')
    new_match.set_result_data('W', (2, 0))
    assert new_match.excitement_index == 2


def test_calc_excitement_index_highwin():
    new_match = match.Match(date.today(), "PREM", "1", "MAN U", 'H')
    new_match.set_result_data('W', (5, 1))
    assert new_match.excitement_index == 3


def test_calc_excitement_index_lowloss():
    new_match = match.Match(date.today(), "PREM", "1", "MAN U", 'H')
    new_match.set_result_data('L', (2, 0))
    assert new_match.excitement_index == -2


def test_calc_excitement_index_highloss():
    new_match = match.Match(date.today(), "PREM", "1", "MAN U", 'H')
    new_match.set_result_data('L', (5, 1))
    assert new_match.excitement_index == -3


def test_calc_result_myteam_first_win():
    score = (1, 0)
    assert match.calc_result_myteam_first(score) == 'W'


def test_calc_result_myteam_first_draw():
    score = (1, 1)
    assert match.calc_result_myteam_first(score) == 'D'


def test_calc_result_myteam_first_loss():
    score = (0, 1)
    assert match.calc_result_myteam_first(score) == 'L'


def test_save_matches_to_file():
    # create a match object
    # save to file
    # load it up again
    # check values are as expected
    new_match = match.Match(date.today(), "PREM", "1", "MAN U", 'H')
    new_match.set_result_data('W', (2, 0), "AET", "http://somewebsite")
    matches = []
    matches.append(new_match)
    match.save_matches_to_file("tests/test_save.csv", matches)
    loaded_matches = match.load_matches_data(date.today(), "tests/test_save.csv")
    assert(len(loaded_matches)) == 1
    loaded_match = loaded_matches[0]
    assert new_match.match_report_url == loaded_match.match_report_url
    assert new_match.normal_time == loaded_match.normal_time
    assert new_match.opponent == loaded_match.opponent
    assert new_match.place == loaded_match.place
    assert new_match.result == loaded_match.result
    assert new_match.score == loaded_match.score

    if os.path.exists("tests/test_save.csv"):
        os.remove("tests/test_save.csv")


def test_calc_is_cup_winner_winner():
    new_match = match.Match(date.today(), "FA Cup", "Final", "MAN U", 'N')
    new_match.set_result_data('W', (2, 0), "AET", "http://somewebsite")
    assert new_match.calc_is_cup_winner()


def test_calc_is_cup_winner_lost():
    new_match = match.Match(date.today(), "FA Cup", "Final", "MAN U", 'N')
    new_match.set_result_data('L', (0, 1), "AET", "http://somewebsite")
    assert not new_match.calc_is_cup_winner()


def test_calc_excitement_index_cupwinners_win():
    new_match = match.Match(date.today(), "FA Cup", "Final", "MAN U", 'N')
    new_match.set_result_data('W', (5, 1))
    assert new_match.excitement_index == 4


def test_calc_excitement_index_cupwinners_loss():
    new_match = match.Match(date.today(), "FA Cup", "Final", "MAN U", 'N')
    new_match.set_result_data('L', (1, 5))
    assert new_match.excitement_index == -3
