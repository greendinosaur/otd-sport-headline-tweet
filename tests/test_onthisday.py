from datetime import date
import onthisday
import match
import config

TEST_DATA_FILE = "tests/test_matches.csv"


@classmethod
def setup_class():
    config.DATA_INPUT = TEST_DATA_FILE


def test_generate_headline_won():
    matches = []
    new_match = match.Match(date.today(), "PREM", "1", "MAN U", 'H')
    new_match.set_result_data('W', (2, 1))
    matches.append(new_match)
    selected_match = match.choose_random_match(matches)
    assert onthisday.generate_headline(selected_match).find("beat") != -1


def test_generate_headline_lost():
    matches = []
    new_match = match.Match(date.today(), "PREM", "1", "MAN U", 'H')
    new_match.set_result_data('L', (2, 1))
    matches.append(new_match)
    selected_match = match.choose_random_match(matches)
    assert onthisday.generate_headline(selected_match).find("lost") != -1


def test_generate_headline_draw():
    matches = []
    new_match = match.Match(date.today(), "PREM", "1", "MAN U", 'H')
    new_match.set_result_data('D', (1, 1))
    matches.append(new_match)
    selected_match = match.choose_random_match(matches)
    assert onthisday.generate_headline(selected_match).find("drew") != -1


def test_generate_headline_nogame():
    matches = []
    selected_match = match.choose_random_match(matches)
    assert onthisday.generate_headline(selected_match).find("No game") != -1


def test_generate_headline_pst():
    new_match = match.Match(date(2019, 1, 1), "PREM", "", "MAN U", 'H')
    new_match.set_result_data('W', (4, 3), "PST", "")
    assert onthisday.generate_headline(new_match).find("penalties") > -1


def test_generate_headline_aet():
    new_match = match.Match(date(2019, 1, 1), "PREM", "", "MAN U", 'H')
    new_match.set_result_data('W', (4, 3), "AET", "")
    assert onthisday.generate_headline(new_match).find("after extra time") > -1


def test_format_intro_headline_date():
    new_match = match.Match(date(2019, 1, 1), "PREM", "1", "MAN U", 'H')
    new_match.set_result_data('L', (5, 1))
    assert onthisday.format_intro_headline(new_match).find("01 Jan, 2019") != -1


def test_format_intro_headline_roundnil():
    new_match = match.Match(date(2019, 1, 1), "PREM", "", "MAN U", 'H')
    new_match.set_result_data('L', (5, 1))
    assert onthisday.format_intro_headline(new_match).find("round") == -1


def test_format_intro_headline_roundnotnil():
    new_match = match.Match(date(2019, 1, 1), "PREM", "2", "MAN U", 'H')
    new_match.set_result_data('L', (5, 1))
    assert onthisday.format_intro_headline(new_match).find("round") != -1


def test_format_competition_round_headline_withround():
    new_match = match.Match(date(2019, 1, 1), "PREM", "2", "MAN U", 'H')
    new_match.set_result_data('L', (5, 1))
    assert onthisday.format_competition_round_headline(new_match).find("round") != -1


def test_format_competition_round_headline_noround():
    new_match = match.Match(date(2019, 1, 1), "PREM", "", "MAN U", 'H')
    new_match.set_result_data('L', (5, 1))
    assert onthisday.format_competition_round_headline(new_match).find("round") == -1


def test_get_otd_headline():
    # need to reset the config parameter to the test data file
    config.DATA_INPUT = TEST_DATA_FILE
    headline = onthisday.get_otd_headline(date(2012, 8, 17))
    assert headline.find("Liverpool") > -1
    assert headline.find("Premier League") > -1


def test_cupfinal_winners():
    new_match = match.Match(date(2019, 1, 1), "FA Cup", "Final", "MAN U", 'H')
    new_match.set_result_data('W', (5, 1))
    assert onthisday.generate_headline(new_match).find("are champions!") != -1


def test_cupfinal_losers():
    new_match = match.Match(date(2019, 1, 1), "FA Cup", "Final", "MAN U", 'H')
    new_match.set_result_data('L', (1, 5))
    assert onthisday.generate_headline(new_match).find("are champions!") == -1
