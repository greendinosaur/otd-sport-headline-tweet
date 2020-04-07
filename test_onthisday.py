import pytest
from datetime import date
import onthisday
import match


def test_choose_random_match_none():
    assert onthisday.choose_random_match(None) == None

def test_choose_random_match_emptylist():
    assert onthisday.choose_random_match([]) == None

def test_choose_random_match_singleitem():
    matches = []
    new_match = match.Match(date.today(), "PREM","1","MAN U",'H')
    new_match.set_result_data('W',(2,1))
    matches.append(new_match)
    assert onthisday.choose_random_match(matches) == new_match

def test_choose_random_match_multipleitems():
    matches = []
    new_match = match.Match(date.today(), "PREM","1","MAN U",'H')
    new_match.set_result_data('W',(2,1))
    matches.append(new_match)
    new_match1 = match.Match(date.today(), "PREM","1","MAN U",'H')
    new_match1.set_result_data('W',(2,1))
    matches.append(new_match1)
    assert onthisday.choose_random_match(matches) != None

def test_generate_headline_won():
    matches = []
    new_match = match.Match(date.today(), "PREM","1","MAN U",'H')
    new_match.set_result_data('W',(2,1))
    matches.append(new_match)
    selected_match = onthisday.choose_random_match(matches)
    assert onthisday.generate_headline(selected_match).find("beat") != -1

def test_generate_headline_lost():
    matches = []
    new_match = match.Match(date.today(), "PREM","1","MAN U",'H')
    new_match.set_result_data('L',(2,1))
    matches.append(new_match)
    selected_match = onthisday.choose_random_match(matches)
    assert onthisday.generate_headline(selected_match).find("lost") != -1

def test_generate_headline_draw():
    matches = []
    new_match = match.Match(date.today(), "PREM","1","MAN U",'H')
    new_match.set_result_data('D',(1,1))
    matches.append(new_match)
    selected_match = onthisday.choose_random_match(matches)
    assert onthisday.generate_headline(selected_match).find("drew") != -1

def test_generate_headline_nogame():
    matches = []
    selected_match = onthisday.choose_random_match(matches)
    assert onthisday.generate_headline(selected_match).find("No game") != -1

def test_generate_headline_pst():
    new_match = match.Match(date(2019, 1,1), "PREM","","MAN U",'H')
    new_match.set_result_data('W',(4,3),"PST","")
    assert onthisday.generate_headline(new_match).find("penalties") > -1

def test_generate_headline_aet():
    new_match = match.Match(date(2019, 1,1), "PREM","","MAN U",'H')
    new_match.set_result_data('W',(4,3),"AET","")
    assert onthisday.generate_headline(new_match).find("after extra time") > -1

def test_calc_excitement_index_nildraw():
    new_match = match.Match(date.today(), "PREM","1","MAN U",'H')
    new_match.set_result_data('D',(0,0))
    assert onthisday.calc_excitement_index(new_match) == 0

def test_calc_excitement_index_nonnildraw():
    new_match = match.Match(date.today(), "PREM","1","MAN U",'H')
    new_match.set_result_data('D',(1,1))
    assert onthisday.calc_excitement_index(new_match) == 1

def test_calc_excitement_index_lowwin():
    new_match = match.Match(date.today(), "PREM","1","MAN U",'H')
    new_match.set_result_data('W',(2,0))
    assert onthisday.calc_excitement_index(new_match) == 2

def test_calc_excitement_index_highwin():
    new_match = match.Match(date.today(), "PREM","1","MAN U",'H')
    new_match.set_result_data('W',(5,1))
    assert onthisday.calc_excitement_index(new_match) == 3

def test_calc_excitement_index_lowloss():
    new_match = match.Match(date.today(), "PREM","1","MAN U",'H')
    new_match.set_result_data('L',(2,0))
    assert onthisday.calc_excitement_index(new_match) == -2

def test_calc_excitement_index_highloss():
    new_match = match.Match(date.today(), "PREM","1","MAN U",'H')
    new_match.set_result_data('L',(5,1))
    assert onthisday.calc_excitement_index(new_match) == -3

def test_format_intro_headline_date():
    new_match = match.Match(date(2019, 1,1), "PREM","1","MAN U",'H')
    new_match.set_result_data('L',(5,1))
    assert onthisday.format_intro_headline(new_match).find("01 Jan, 2019") != -1

def test_format_intro_headline_roundnil():
    new_match = match.Match(date(2019, 1,1), "PREM","","MAN U",'H')
    new_match.set_result_data('L',(5,1))
    assert onthisday.format_intro_headline(new_match).find("round") == -1

def test_format_intro_headline_roundnotnil():
    new_match = match.Match(date(2019, 1,1), "PREM","2","MAN U",'H')
    new_match.set_result_data('L',(5,1))
    assert onthisday.format_intro_headline(new_match).find("round") != -1

def test_generate_headline_pst():
    new_match = match.Match(date(2019, 1,1), "PREM","","MAN U",'H')
    new_match.set_result_data('W',(4,3),"PST","")
    assert onthisday.generate_headline(new_match).find("penalties") > -1


def test_load_data_datematches():
    date_of_interest = date(2019,8,15)
    matches = onthisday.load_matches_data(date_of_interest,"tests/test_matches.csv")
    print(matches)
    assert len(matches) == 1

def test_load_data_date_nomatches():
    date_of_interest = date(2019,2,15)
    matches = onthisday.load_matches_data(date_of_interest,"tests/test_matches.csv")
    assert len(matches) == 0

def test_load_data_date_twomatches():
    date_of_interest = date(2019,8,16)
    matches = onthisday.load_matches_data(date_of_interest,"tests/test_matches.csv")
    assert len(matches) == 2

def test_load_data_match_data():
    date_of_interest = date(2019,8,15)
    matches = onthisday.load_matches_data(date_of_interest,"tests/test_matches.csv")
    match_of_interest = matches[0]
    assert match_of_interest.date.month == date_of_interest.month
    assert match_of_interest.date.day == date_of_interest.day
    assert match_of_interest.opponent == "Arsenal"
    assert match_of_interest.place == "H"
    assert match_of_interest.competition == "Premier League"
    assert match_of_interest.result == 'L'
    assert match_of_interest.score == (1,6)

def test_format_competition_round_headline_withround():
    new_match = match.Match(date(2019, 1,1), "PREM","2","MAN U",'H')
    new_match.set_result_data('L',(5,1))
    assert onthisday.format_competition_round_headline(new_match).find("round") != -1

def test_format_competition_round_headline_noround():
    new_match = match.Match(date(2019, 1,1), "PREM","","MAN U",'H')
    new_match.set_result_data('L',(5,1))
    assert onthisday.format_competition_round_headline(new_match).find("round") == -1

