from datetime import date
from datetime import datetime
import match
import csv

# helper functions to parse and normalise a dataset prior to saving it out
def parse_and_save_dataset(fname_in, fname_out):
    # load in the dataset and save it out again in a more normalised form
  #open the file, read a line in at a time
    file_in = open(fname_in, "r")
    matches = []
    loaded_match = None
    for line in file_in:
        match_details = line.split(',')
        match_date = datetime.strptime(match_details[0], "%Y-%m-%d")
        found_myteam = False
        opponent = ""
        place = 'N'
        everton_score = -1
        opponent_score = -1
        result = ''
        if match_details[5] == "Everton": # everton is the home team
            found_myteam = True   
            opponent = match_details[6]
            everton_score = int(match_details[7])
            opponent_score = int(match_details[8])
            place = ('H' if match_details[4] == "TRUE" else 'N')    
        elif match_details[6] == "Everton": # everton is the away team
            found_myteam = True
            opponent = match_details[5]
            everton_score = int(match_details[8])
            opponent_score = int(match_details[7])
            place = ('A' if match_details[4] == "TRUE" else 'N')
                
        if found_myteam:
            result = ('W' if everton_score > opponent_score else ('L' if everton_score < opponent_score else 'D'))
            loaded_match = match.Match(match_date,match_details[2],'',opponent,place)
            loaded_match.set_result_data(result,tuple(match_details[7],match_details[8]),"","")
            matches.append(loaded_match)


    file_in.close()
    match.save_matches_to_file(fname_out, matches)

   

parse_and_save_dataset("data/EFL_results.csv", "data/Everton_results.csv")