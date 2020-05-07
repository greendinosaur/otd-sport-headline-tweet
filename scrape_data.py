import requests
from datetime import datetime
import time
from bs4 import BeautifulSoup
import match


WF_URL = "https://www.worldfootball.net"


def parse_score(score):
    # 2:1 (0:1, 1:1) aet
    # score string could have aet or pso meaning after extra time or penalty shootout
    # the first score shown is the end score which may be the penalty shoot out if it was a pso
    scores = score.split(" ")
    normal_time = ("AET" if score.find("aet") > -1 else ("PSO" if score.find("pso") > -1 else "NT"))
    print(normal_time)
    return tuple([int(n) for n in scores[0].split(":")]), normal_time


def scrape_worldfootball(team, year):
    url = WF_URL + "/teams/{}/{}/3/"
    page = requests.get(url.format(team, year))
    soup = BeautifulSoup(page.text, 'html.parser')

    div_list_box = soup.find_all("div", {"class": "box"})

    competition = ""
    score = (1, 1)
    matches = []
    new_match = None
    match_report = ""
    normal_time = "NT"
    for div in div_list_box:
        div_class_data = div.find("div", {"class": "data"})
        if div_class_data:
            table_list = div_class_data.find_all(
                "table",
                {"class": "standard_tabelle", "cellpadding": "3", "cellspacing": "1"})
            if table_list:
                for table in table_list:
                    table_competition = table.find_all("td", {"colspan": "8", "class": "hell"})
                    if table_competition:
                        # if we have found a competition heading then know we have the result data
                        # need to loop over all of the rows inside this table
                        # if the row is a header then capture this as the competition
                        # then loop through all of the rows to see if they contain a result
                        table_rows = table.find_all("tr")
                        for row in table_rows:
                            if row.find_all("td", {"colspan": "8", "class": "hell"}):
                                print("competition found")  # of form name 1984/1985
                                competition = row.find("td").find("a").find("b").contents[0].strip()
                                print(row.find("td").find("a").find("b").contents[0].strip())
                            else:
                                if row.find("td"):
                                    cols = row.find_all("td")
                                    print(competition)
                                    competition_round = cols[0].find("a").contents[0].strip()
                                    print(competition_round)
                                    date = datetime.strptime(cols[1].find("a").contents[0].strip(), "%d/%m/%Y")
                                    print(date)
                                    location = cols[3].contents[0]
                                    print(location)
                                    opponent = cols[5].find("a").contents[0].strip()
                                    print(opponent)
                                    #  some of the matches have a results page linked from the score
                                    if cols[6].find("a"):
                                        score, normal_time = parse_score(cols[6].find("a").contents[0].strip())
                                        match_report = WF_URL + cols[6].find("a").get("href")
                                    else:
                                        score, normal_time = parse_score(cols[6].contents[0].strip())
                                        match_report = ""
                                    new_match = match.Match(
                                        date,
                                        competition,
                                        competition_round,
                                        opponent,
                                        location)
                                    new_match.set_result_data(
                                        match.calc_result_myteam_first(score),
                                        score,
                                        normal_time,
                                        match_report)
                                    matches.append(new_match)
                                    # TD[6] is score with everton first, shows 2:1 (0:1,1:1) aet
                                    # final score is before the brackets, in the brackets may
                                    # show half time and at end of normal tim
                                    # aet used to indicate after extra time
                                    # so up until the first space (or end of string as
                                    # HT score isn't always shown), is the end score
                                    # to get scorers, need to follow a link to go onto
                                    # match report page, not always present

    print(len(matches))
    return matches


# get the data and save to file
def get_and_saveworldfootball(club, start_year, end_year, fname):
    for i in range(start_year, end_year + 1):
        print("getting data for year", i)
        matches = scrape_worldfootball(club, str(i))
        match.save_matches_to_file(fname, matches)
        time.sleep(3)


get_and_saveworldfootball("everton-fc", 1980, 2019, "data/everton_wof_new.csv")
