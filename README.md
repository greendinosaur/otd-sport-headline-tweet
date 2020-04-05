# Goal
This project is a sports headline generator that will look up sports results for a specific team on this day in history, choose one at random and tweet it.

It can be customised to suit any sports team and sports involve two competing teams. The main consideration is sourcing an appropriate dataset and massaging the data into the required format.

# Usage
## Pre-requisites
* Python 3.x
* [tweepy library](http://www.tweepy.org/) installed
* A bot account registered with [Twitter](https://developer.twitter.com/en) if you intend to tweet the match directly to twitter
* A suitable data file containing the historic match data

## Data-file format
The data file containing the matches needs to be a csv file with the following data fields per row. Take a look at [test_matches.csv](tests/test_matches.csv) in the tests folder for examples.

* Match date in the format YYYY-m-d e.g. 1980-11-08
* Name of the competition
* Competition round
* Location of the game one of H,A,N
* Opponent
* Result in terms of the team of interest. One of W, L, D
* Final score as n-m in terms of the team of interest e.g. 1-2 would be interepreted as the team of interest lost by 2 goals to 1
* Penalty shootout score as n-m in terms of the team of interest, no value if no data
* List of tuples with the time and name of team of interest scorers e.g. [(15,"Sharpe")], no value if no data

For example, 
```bash
 1980-11-08,Premier League 80/81,Matchday 16,A,Norwich City,L,1-2,,
```

## Installing the application
1. Create your own [fork of this
  repo](https://help.github.com/articles/fork-a-repo/)
2. Clone it to your machine:
 ```bash
  git clone git@github.com:${YOUR_GITHUB_USERNAME}/otd-sport-headline-tweet.git
  ```

## Configuring the application
[config.py](config.py) contains the various parameters required to generate a headline including the path to the data file and the twitter keys and secrets. Update the parameters to suit you.

## Running the application
```bash
python3 main.py
```
Will generate a headline which is tweeted automatically and also printed to the terminal.

# TODO
* Penalty shootout scores and scorers are not used
* Does not distinguish between final score, aet, or pen shootout
* Generate more exciting headlines

# License
This project is under the MIT license. See the [LICENSE](LICENSE) file for details
