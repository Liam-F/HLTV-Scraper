from getMatchIDs import get_match_ids
from getFinishedEvents import get_finished_events
from scraper import *
from helper import *


# Define number of threads to use
threads = 32
# Set to True to activate tabulation and False to disable it.
tab = not check_args('notab', sys.argv)

# Make an array of existing Match and Event IDs
existingMatchIDs = get_existing_data("matchIDs", 1)
existingEventIDs = get_existing_data("eventIDs", 3)
existing_completed_events = get_existing_data("completedEvents", 0)

# Get the last ID so we know when to stop looking
newMatchIDs = get_match_ids(existingMatchIDs[-1])
new_completed_events = get_finished_events(existing_completed_events[-1])

# Run all tests for a specific Match ID
if check_args('test', sys.argv):
    tests()
    pass

# Exit if there are no new matches
elif len(newMatchIDs) < 1 and len(new_completed_events) < 1:
    print("No new matches or events found!")

# Just check for new matches and break out of the loop
elif check_args('check', sys.argv):
    print(f"{len(newMatchIDs)} matches and {len(new_completed_events)} completed events to tabulate.")
    if check_args('debug', sys.argv):
        print_array('New matches', newMatchIDs, 0)
        print_array('New events', new_completed_events, 1)
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

    # Step 5: Update picksAndBans.csv
    raw_picks_and_bans = scrape(matchesToCheck, get_match_map_bans, threads)
    picks_and_bans = fix_player_stats(raw_picks_and_bans)

    # Step 6: Add new events to eventIDs.csv
    eventsToCheck = remove_existing_data(existingEventIDs, un_dimension(newEvents, 1), 'events')
    newEventIDs = scrape(eventsToCheck, get_event_names, threads)
    if len(newEventIDs) < 1:
        print("No new event IDs to add!")

    # Step 7: Update teams.csv
    newTeams = get_new_iterable_items("team", find_max("teams", 2))
    newTeams = scrape(newTeams, get_teams, threads)

    # Step 8: Update players.csv
    newPlayers = get_new_iterable_items("player", find_max("players", 2))
    newPlayers = scrape(newPlayers, get_players, threads)

    # Step 9: Check event prize data for eventPrizes.csv and eventWinners.csv
    event_rewards = scrape(un_dimension(new_completed_events, 0), get_event_rewards, threads)
    event_winners = scrape(un_dimension(new_completed_events, 0), get_event_winners, threads)

    # Step 10: Tabulate
    if tab:
        tabulate("matchIDs", newMatchIDs)
        tabulate("joinMatchEvent", newEvents)
        tabulate("matchLineups", newMatchLineups)
        tabulate("matchResults", newMatchInfo)
        tabulate("playerStats", newPlayerStats)
        tabulate("picksAndBans", picks_and_bans)
        tabulate("eventIDs", newEventIDs)
        tabulate("teams", newTeams)
        tabulate("players", newPlayers)
        tabulate("completedEvents", new_completed_events)
        tabulate("eventPrizes", event_rewards)
        tabulate("eventWinners", event_winners)

    # Step 11: Debug
    if check_args('debug', sys.argv):
        print_array("New matches", matchesToCheck, 1)
        print_array("Match lineups", newMatchLineups, 1)
        print_array("Match results", newMatchInfo, 1)
        print_array("Player stats", newPlayerStats, 1)
        print_array("New teams", newTeams, 1)
        print_array("New players", newPlayers, 1)
