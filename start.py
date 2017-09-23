from getMatchIDs import get_match_ids
from scraper import *
from helper import *


# Define number of threads to use
threads = 32
# Set to True to activate tabulation and False to disable it.
tab = not check_args('notab', sys.argv)

# Make an array of existing Match and Event IDs
existingMatchIDs = get_existing_data("matchIDs", 1)
existingEventIDs = get_existing_data("eventIDs", 3)

# Get the last ID so we know when to stop looking
newMatchIDs = get_match_ids(existingMatchIDs[-1])

# Run all tests for a specific Match ID
if check_args('test', sys.argv):
    tests()
    pass

elif len(newMatchIDs) < 1:
    print("No new matches found!")

# Just check for new matches and break out of the loop
elif check_args('check', sys.argv):
    print(f"{len(newMatchIDs)} new matches to tabulate")
    if check_args('debug', sys.argv):
        print_array("New matches", newMatchIDs, 0)
    pass

elif check_args('temp', sys.argv):
    pass

else:
    # Step 1: add new matches to the event join table
    events = get_existing_data("joinMatchEvent", 0)
    matchesToCheck = remove_existing_data(events, un_dimension(newMatchIDs, 1), 'matches')
    newEvents = scrape(matchesToCheck, get_match_events, threads)

    # Step 2: Update matchResults.csv
    newMatchInfo = scrape(matchesToCheck, get_match_info, threads)
    # Sometimes this returns a multi-dimensional array, so we remove it
    newMatchInfo = fix_match_results(newMatchInfo, 15)

    # Step 3: Update matchLineups.csv
    newMatchLineups = scrape(matchesToCheck, get_match_lineups, threads)

    # Step 4: Update playerStats.csv
    newPlayerStats = scrape(matchesToCheck, get_player_stats, threads)
    # This returns a single array for each match with all of the player stats, so we un-array it
    newPlayerStats = fix_player_stats(newPlayerStats)

    # Step 5: Add new events to eventIDs.csv
    eventsToCheck = remove_existing_data(existingEventIDs, un_dimension(newEvents, 1), 'events')
    newEventIDs = scrape(eventsToCheck, get_event_names, threads)
    if len(newEventIDs) < 1:
        print("No new event IDs to add!")

    # Step 6: Update teams.csv
    newTeams = get_new_iterable_items("team", find_max("teams", 2))
    newTeams = scrape(newTeams, get_teams, threads)

    # Step 7: Update players.csv
    newPlayers = get_new_iterable_items("player", find_max("players", 2))
    newPlayers = scrape(newPlayers, get_players, threads)

    # Step 8: Check event data
    if check_args('event', sys.argv):
        event_rewards = scrape(existingEventIDs, get_event_rewards, threads)
        event_winners = scrape(existingEventIDs, get_event_winners, threads)
    else:
        event_rewards = []
        event_winners = []

    # Step 9: Tabulate
    if tab:
        tabulate("matchIDs", newMatchIDs)
        tabulate("joinMatchEvent", newEvents)
        tabulate("matchLineups", newMatchLineups)
        tabulate("matchResults", newMatchInfo)
        tabulate("playerStats", newPlayerStats)
        tabulate("eventIDs", newEventIDs)
        tabulate("teams", newTeams)
        tabulate("players", newPlayers)
        tabulate("eventWinners", event_winners)
        tabulate("eventPrizes", event_rewards)

    # Step 10: Debug
    if check_args('debug', sys.argv):
        print_array("New matches", matchesToCheck, 1)
        print_array("Match lineups", newMatchLineups, 1)
        print_array("Match results", newMatchInfo, 1)
        print_array("Player stats", newPlayerStats, 1)
        print_array("New teams", newTeams, 1)
        print_array("New players", newPlayers, 1)
