from getMatchIDs import get_match_ids
from scraper import *
from helper import *


# Define number of threads to use
threads = 32
# Set to True to activate tabulation and False to disable it.
tab = check_args('notab', sys.argv)

# Make an array of existing Match IDs
existingMatchIDs = get_existing_data("matchIDs", 1)

# Get the last ID so we know when to stop looking
newMatchIDs = get_match_ids(existingMatchIDs[len(existingMatchIDs)-1])

# Run all tests for a specific Match ID
if not check_args('test', sys.argv):
    tests(threads)
    pass

elif len(newMatchIDs) < 1:
    print("No new matches found!")

# Just check for new matches and break out of the loop
elif not check_args('check', sys.argv):
    print(f"{len(newMatchIDs)} new matches to tabulate")
    if not check_args('debug', sys.argv):
        print_array("New matches", newMatchIDs)
    pass

else:
    # Tell the user how many matches we will tabulate
    print(f"{len(newMatchIDs)} new matches to tabulate")
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

    # Step 9: Summarize
    print(f"Completed tabulation for", end=' ')
    print(f"{len(matchesToCheck)} new matches,", end=' ')
    print(f"{len(newPlayerStats)} new player stats,", end=' ')
    print(f"{len(newEventIDs)} new events,", end=' ')
    print(f"{len(newTeams)} new teams,", end=' ')
    print(f"and {len(newPlayers)} new players.\n")

    # Step 10: Debug
    if not check_args('debug', sys.argv):
        print_array("New matches", matchesToCheck)
        print_array("Match lineups", newMatchLineups)
        print_array("Match results", newMatchInfo)
        print_array("Player stats", newPlayerStats)
        print_array("New teams", newTeams)
        print_array("New players", newPlayers)
