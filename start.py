from getMatchIDs import get_match_ids
from scraper import *
from helper import *


# Define number of threads to use
threads = 32
# Set to True to activate tabulation and False to disable it.
tab = True

# Make an array of existing Match IDs
existingMatchIDs = get_existing_data("matchIDs", 1)

# Get the last ID so we know when to stop looking
newMatchIDs = get_match_ids(existingMatchIDs[len(existingMatchIDs)-1])
if len(newMatchIDs) < 1:
    print("No new matches found!")
else:
    # Tell the user how many matches we will tabulate
    print("%s new matches to tabulate" % (len(newMatchIDs)))

    # Step 1: add to matches.csv
    if tab:
        tabulate("matchIDs", newMatchIDs)

    # Step 2: add new matches to the event join table
    events = get_existing_data("joinMatchEvent", 0)
    matchesToCheck = remove_existing_data(events, un_dimension(newMatchIDs, 1))
    newEvents = scrape(matchesToCheck, get_match_events, threads)
    if tab:
        tabulate("joinMatchEvent", newEvents)

    # Step 3: Add new events to eventIDs.csv
    eventIDs = get_existing_data("eventIDs", 3)
    eventsToCheck = remove_existing_data(eventIDs, un_dimension(newEvents, 1))
    newEventIDs = scrape(eventsToCheck, get_event_names, threads)
    if len(newEventIDs) < 1:
        print("No new event IDs to add!")
    elif tab:
        tabulate("eventIDs", newEventIDs)

    # Step 4: Update matchResults.csv
    newMatchInfo = scrape(matchesToCheck, get_match_info, threads)
    # Sometimes this returns a multi-dimensional array, so we remove it
    newMatchInfo = fix_array(fix_array(fix_array(newMatchInfo, 14), 14), 14)
    if tab:
        tabulate("matchResults", newMatchInfo)

    # Step 5: Update matchLineups.csv
    newMatchLineups = scrape(matchesToCheck, get_match_lineups, threads)
    if tab:
        tabulate("matchLineups", newMatchLineups)

    # Step 6: Update playerStats.csv
    newPlayerStats = scrape(matchesToCheck, get_player_stats, threads)
    # This returns a single array for each match with all of the player stats, so we un-array it
    newPlayerStats = fix_player_stats(newPlayerStats)
    if tab:
        tabulate("playerStats", newPlayerStats)

    # Step 7: Update teams.csv
    newTeams = get_new_iterable_items("team", find_max("teams", 2))
    newTeams = scrape(newTeams, get_teams, threads)
    if tab:
        tabulate("teams", newTeams)

    # Step 8: Update players.csv
    newPlayers = get_new_iterable_items("player", find_max("players", 2))
    newPlayers = scrape(newPlayers, get_players, threads)
    if tab:
        tabulate("players", newPlayers)
    print("Completed tabulation for %s new matches, %s new player stats, %s new events, %s new teams, and %s new players." % (len(matchesToCheck), len(newPlayerStats), len(newEventIDs), len(newTeams), len(newPlayers)))
