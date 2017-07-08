# HLTV Scraper

This is a multi-threaded Python scraper designed to pull data from HLTV.org and tabulate it into a series of CSV files. It is written in pure Python, so it should run on any system that can run Python 3. It is not compatible with Python 2, so you may need to install the latest Python release from [here](https://www.python.org/downloads/).

## Installation and Usage

Since this is written in pure Python, there are no dependencies to install. Simply clone the repository or download the zip file, then `cd` to the directory and run `python3 start.py`. There is (an outdated) video demonstration [here](https://twitter.com/rxcs/status/870564131715162112).

![](https://i.imgur.com/g5Wk3eS.png)

### Arguments

The script can take several arguments: `check`, `notab`, or `test`. 

-  `start.py check` will only check how many new matches need to be downloaded and do nothing else. 
-  `start.py notab` will let the script run but will disable the tabulation. 
-  `start.py test match_id` will print the results of a specific given match. For example, `start.py test 2312163/natus-vincere-vs-cloud9-esl-one-cologne-2017` will result in:

		Event: ESL One Cologne 2017
		
		Map results: ['2017-07-08', 'Mirage', 'Natus Vincere', 'CT', '13', '5', '8', 0, 'Cloud9', 'T', '16', '10', '6', 0]
		Map results: ['2017-07-08', 'Overpass', 'Natus Vincere', 'CT', '14', '6', '8', 0, 'Cloud9', 'T', '16', '9', '7', 0]
		
		Match lineup: ['GuardiaN', 'flamie', 'Edward', 'seized', 's1mple', 'Stewie2K', 'shroud', 'autimatic', 'Skadoodle', 'n0thing']
		
		Player stats: ['Mirage', 'GuardiaN', '25', '14', '87.1', '72.4', '1.38']
		Player stats: ['Mirage', 'seized', '18', '22', '81.3', '75.9', '1.05']
		Player stats: ['Mirage', 'Edward', '20', '19', '64.9', '62.1', '1.00']
		Player stats: ['Mirage', 'flamie', '15', '17', '65.7', '69.0', '0.92']
		Player stats: ['Mirage', 's1mple', '15', '22', '63.7', '48.3', '0.73']
		Player stats: ['Mirage', 'Stewie2K', '27', '21', '93.8', '72.4', '1.38']
		Player stats: ['Mirage', 'autimatic', '23', '19', '89.4', '75.9', '1.15']
		Player stats: ['Mirage', 'shroud', '14', '17', '59.8', '72.4', '0.93']
		Player stats: ['Mirage', 'n0thing', '18', '20', '68.5', '58.6', '0.88']
		Player stats: ['Mirage', 'Skadoodle', '12', '17', '48.7', '72.4', '0.80']
		Player stats: ['Overpass', 'flamie', '24', '22', '88.4', '73.3', '1.17']
		Player stats: ['Overpass', 's1mple', '23', '20', '88.0', '80.0', '1.13']
		Player stats: ['Overpass', 'Edward', '20', '22', '73.9', '70.0', '1.07']
		Player stats: ['Overpass', 'GuardiaN', '17', '20', '63.5', '60.0', '1.01']
		Player stats: ['Overpass', 'seized', '17', '22', '59.0', '73.3', '0.82']
		Player stats: ['Overpass', 'shroud', '26', '15', '76.1', '73.3', '1.40']
		Player stats: ['Overpass', 'Skadoodle', '26', '19', '81.5', '86.7', '1.24']
		Player stats: ['Overpass', 'Stewie2K', '18', '25', '90.7', '70.0', '1.10']
		Player stats: ['Overpass', 'autimatic', '22', '23', '75.2', '80.0', '1.09']
		Player stats: ['Overpass', 'n0thing', '14', '19', '62.4', '73.3', '0.91'] 

I recommend adding these aliases to your `.bash_profile`:

    alias scheck='cd Code/Python/HLTV\ Scraper && python3 start.py check'
    
    alias snotab='cd Code/Python/HLTV\ Scraper && python3 start.py notab'
    
    alias stest='cd Code/Python/HLTV\ Scraper && python3 start.py test'
    
    alias scraper='cd Code/Python/HLTV\ Scraper && python3 start.py'

Thus, `scheck` will check for the number of new matches to scrape, `snotab` will run without tabulation, `stest match_id` will run the test for `match_id`, and `scraper` will run the scraper normally.

## Getting New Matches

This works by scraping several pieces of data from the HLTV webpages. First, it will paginate through the match [results](https://www.hltv.org/results) page and determine which Match IDs are not yet in the database. If there are new IDs to tabulate, it will append them to the `matchIDs.csv` file. These new matches are stored in an array called `matchesToCheck`.

### Matching Matches to Events

Once these have been added, it compares `matchIDs.csv` to `joinMatchEvent.csv` file. `getMatchEvents.py` will parse `matchesToCheck` to find their respective Event IDs and append them to the `joinMatchEvent.csv` file. 

## Getting New Events

From there, `getEventNames.py` compares `eventIDs.csv` to `joinMatchEvent.csv` and scrapes the respective event results page to determine various data about the event. The data is then appended to `eventIDs.csv`. 

## Getting Match Results

Once the new events have been accounted for, the script takes `matchesToCheck` and sends them to `getMatchInfo.py` to scrape the necessary information.

### Handling Multiple Maps

Since this returns multidimensional arrays for matches with more than one map, the script calls `fix_array()` thrice to remove any extra dimensions. The method turns an array like this:

	[[1, 2, 3], [3, 4, 5], [['a', 'b', 'c'], ['c', 'd', 'e']], [5, 6, 7]]
 
 To an array like this:
 
	[[1, 2, 3], [3, 4, 5], [5, 6, 7], ['a', 'b', 'c'], ['c', 'd', 'e']]
 
 After that, it tabulates the new information to `matchResults.csv`.
 
## Getting Match Lineups 

Next, the script parses the same new matches stored in `matchesToCheck` and find the respective team lineups and tabulates the new information to `matchLineups.csv`.

## Getting player stats

Each match has player stats for each map. The script looks for these statistics using the matches stored in `matchesToCheck` and appends the new data to `playerStats.csv`.

## Updating Players and Teams

Each player and team on HLTV has a unique identification number that increases as new players are added to the database. To find new players and teams, we get the maximum identifier value form the respective `.csv` file and iterate over it using `get_iterable_items()`. From there the relevant pages are scraped and tabulated to `players.csv` and `teams.csv`.