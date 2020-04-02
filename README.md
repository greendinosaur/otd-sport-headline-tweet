# Goal
Goal of this project is to create a sports headline generator that will look up sports results for a specific team on this day in history, choose one at random and tweet it.

# Usage
*config.py* contains the various parameters required to generate a headline including the path to the data file

call *onthisday()* inside *onthisday.py* to generate a headline which can then be tweeted. Currently, it just prints the headline to the console.

Data file needs to be a csv file with the following data fields per row:

* Match date in the format YYYY-m-d e.g. 1980-11-08
* Name of the competition
* Competition round
* Location of the game one of H,A,N
* Opponent
* Result in terms of the team of interest. One of W, L, D
* Final score as n-m in terms of the team of interest e.g. 1-2 would be interepreted as the team of interest lost by 2 goals to 1
* Penalty shootout score as n-m in terms of the team of interest, no value if no data
* List of tuples with the time and name of team of interest scorers e.g. [(15,"Sharpe")], no value if no data

For example, 1980-11-08,Premier League 1980/1981,16. Round,A,Norwich City,L,1-2,,

# TODO
* It has not been tested against the twitter API yet.
* penalty shootout scores and scorers are not used
* does not distinguish between final score, aet, or pen shootout