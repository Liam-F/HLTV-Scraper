from html import get_html
from datetime import datetime
from string import digits
import re


def get_event_names(eventID):
    html = get_html("https://www.hltv.org/results?offset=0&event=%s" % (eventID))
    if html is None:
        print(f"Failed for {eventID}")
        return []

    # Find the type of event (online, LAN, etc), as well as the name and date of event
    eventType = re.findall('title=\".*\">.*</span></td>', html)
    eventNames = re.findall('<div class=\"eventname\">.*</div>', html)
    eventEndDate = re.findall('data-unix=\".*\">', html)
    eventPrize = re.findall('\$.*</td>', html)

    # Parse the eventType
    if len(eventType) > 0:
        eventType[0] = (eventType[0].split('>')[1]).replace("</span", "")
    else:
        eventType.append(0)

    # Parse the eventNames
    if len(eventNames) > 0:
        eventNames[0] = (eventNames[0].replace("<div class=\"eventname\">", "")).replace("</div>", "")
    else:
        eventNames.append(0)

    # Parse the eventEndDate
    if len(eventEndDate) > 0:
        eventEndDate[0] = (eventEndDate[0].split('\"')[1]).replace("\"", "")[:-3]
        eventEndDate[0] = datetime.utcfromtimestamp(int(eventEndDate[0])).strftime('%Y-%m-%d')
    else:
        eventEndDate.append(0)

    # Parse the eventPrize
    if len(eventPrize) > 0:
        eventPrize[0] = (eventPrize[0].replace("$", "")).replace("</td>", "")
    else:
        eventPrize.append(0)

    # Make an array for pool.map to process
    result = []
    result.append(eventType[0])
    result.append(eventNames[0])
    result.append(eventEndDate[0])
    result.append(eventID)
    result.append(eventPrize[0])
    return result


def get_event_rewards(eventID):
    html = get_html("https://www.hltv.org/events/%s/a" % (eventID))
    if html is None:
        print(f"Failed for {eventID}")
        return []

    # Find the total prizes
    eventPrizes = re.findall('class=\"prizeMoney\">\$.*<', html)

    # Parse the eventPrize
    if len(eventPrizes) > 0:
        for prize in range(0, len(eventPrizes)):
            eventPrizes[prize] = (eventPrizes[prize].split('$')[1]).replace("<", "")
    else:
        eventPrizes.append(0)

    # Make an array for pool.map to process
    return [eventID] + eventPrizes


def get_event_winners(eventID):
    html = get_html("https://www.hltv.org/events/%s/a" % (eventID))
    if html is None:
        print(f"Failed for {eventID}")
        return []

    # Find the total prize and prize winners
    prizeWinners = re.findall('/team.logo/.*\" class', html)

    # Parse the prizeWinners
    if len(prizeWinners) > 0:
        for prize in range(0, len(prizeWinners)):
            prizeWinners[prize] = (prizeWinners[prize].split('/')[3]).replace("\" class", "")
    else:
        prizeWinners.append(0)

    # Make an array for pool.map to process
    return [eventID] + prizeWinners


def get_match_events(matchID):
    html = get_html(f"https://www.hltv.org/matches/{matchID}")
    if html is None:
        print(f"Failed for {matchID}")
        return []

    # Find the type of event (online, LAN, etc)
    eventName = re.findall('\"/events/.*/', html)
    if len(eventName) < 1:
        print(f"Failed for {matchID}")
        return []

    # print eventType
    if len(eventName) > 1:
        eventName[0] = (eventName[0].replace("\"/events/", "")).split("/", 1)[0]
    else:
        eventName.append(0)

    # Make an array for pool.map to process
    array = []
    array.append(matchID)
    array.append(eventName[0])
    return array


def get_teams(teamID):
    html = get_html(f"https://www.hltv.org/team/{teamID}/a")
    if html is None:
        print(f"Failed for {teamID}")
        return []

    # Find the type of event (online, LAN, etc)
    teamName = re.findall('<div><span class=\"subjectname\">.*</span><br><i', html)
    if len(teamName) < 1:
        return []
    teamRanked = re.findall('<a href=\"\/ranking\/teams\">Ranked #(.*)<\/a>', html)
    if len(teamRanked) < 1:
        teamRanked = [None]
    teamCountry = re.findall('fa fa-map-marker\" aria-hidden=\"true\"></i>.*<', html)
    if len(teamCountry) < 1:
        teamCountry = re.findall('fa fa-map-marker\" aria-hidden=\"true\"></i>.*</div>', html)
    if len(teamCountry) < 1:
        return []

    if len(teamName) > 0:
        teamName[0] = (teamName[0].replace("<div><span class=\"subjectname\">", "")).replace("</span><br><i", "")
    else:
        teamName.append(0)

    if len(teamCountry) > 0:
        teamCountry[0] = (teamCountry[0].replace("fa fa-map-marker\" aria-hidden=\"true\"></i> ", "")).split("<", 1)[0]
    else:
        teamCountry.append(0)

    # Make an array for pool.map to process
    array = []
    array.append(teamName[0])
    array.append(teamCountry[0])
    array.append(teamID)
    array.append(teamRanked[0])

    return array


def get_match_info(matchID):
    html = get_html(f"https://www.hltv.org/matches/{matchID}")
    if html is None:
        print(f"Failed for {matchID}")
        return []

    # Find match date, team IDs, team names, map, and scores
    date = re.findall('data-unix=\".*\"', html)
    teamIDs = re.findall('src=\"https://static.hltv.org/images/team/logo/.*\" class', html)
    teamNames = re.findall('class=\"logo\" title=\".*\">', html)
    map = re.findall('<div class=\"mapname\">.*</div>', html)
    scores = re.findall('<div class=\"results\"><span class=\".*</span><span>', html)

    # Give up if no team names found
    if len(teamNames) < 1:
        return []

    # Find the match date
    if len(date) > 2:
        date = date[1]
        date = (date.replace("data-unix=\"", "")).replace("\"", "")[:-3]
        date = datetime.utcfromtimestamp(int(date)).strftime('%m/%d/%y')
    else:
        date.append(0)

    # Find the Teams respective IDs
    if len(teamIDs) > 0:
        teamIDs[0] = (teamIDs[0].replace("src=\"https://static.hltv.org/images/team/logo/", "")).replace("\" class", "")
        teamIDs[1] = (teamIDs[1].replace("src=\"https://static.hltv.org/images/team/logo/", "")).replace("\" class", "")
    else:
        teamIDs.append(0)

    # Find the map(s) that the match was played on
    if len(map) == 1:
        map[0] = (map[0].replace("<div class=\"mapname\">", "")).replace("</div>", "")
    elif len(map) > 1:
        for i in range(0, len(map)):
            map[i] = (map[i].replace("<div class=\"mapname\">", "")).replace("</div>", "")
    else:
        map.append(0)

    # Find the team starting and half sides
    sides = []
    try:
        if len(scores) == 1:
            if len(scores[0]) > 0:
                # If team 1 is T, team 2 is CT
                if re.findall('\"t\"|\"ct\"', scores[0])[0] == '\"t\"':
                    sides.append("T")
                    sides.append("CT")
                else:
                    sides.append("CT")
                    sides.append("T")
        elif len(scores) > 1:

            # Same as above, but looped for multiple matches
            for i in range(0, len(scores)):
                if len(scores[i]) > 0:
                    if re.findall('\"t\"|\"ct\"', scores[i])[0] == "\"t\"":
                        sides.append("T")
                        sides.append("CT")
                    else:
                        sides.append("CT")
                        sides.append("T")
        else:
            return []
    except IndexError:
        pass

    # Find the scores if there is only one map
    if len(map) == 1:
        scores[0] = re.findall('\d+', scores[0])

    # Find the scores if there are multiple maps
    elif len(map) > 1:
        for i in range(0, len(scores)):
            scores[i] = re.findall('\d+', scores[i])
    else:
        scores.append(0)

    for i in range(0, len(scores)):
        # If there was no overtime, make the OT value 0
        if len(scores[i]) == 6:
            scores[i].append(0)
            scores[i].append(0)
        elif len(scores[i]) > 6:
            # Do nothing, because OT scores are already calculated
            pass
        else:
            print(f"HLTV altered score layout for {matchID}")
            return []

    # Make an array for pool.map to process
    result = []

    # Create counter variable to access the proper item in the sides array
    sideCount = 0
    if len(map) > 1:
        for i in range(0, len(scores)):
            # Create a temp array so that each map's stats are each contained in their own array
            tempArray = []
            tempArray.append(date)
            tempArray.append(map[i])
            tempArray.append(teamIDs[0])
            tempArray.append(sides[sideCount])
            tempArray.append(scores[i][0])
            tempArray.append(scores[i][2])
            tempArray.append(scores[i][4])
            tempArray.append(scores[i][6])
            tempArray.append(teamIDs[1])
            tempArray.append(sides[sideCount + 1])
            tempArray.append(scores[i][1])
            tempArray.append(scores[i][3])
            tempArray.append(scores[i][5])
            tempArray.append(scores[i][7])
            tempArray.append(matchID)
            result.append(tempArray)
            sideCount += 2
    else:
        result.append(date)
        result.append(map[0])
        result.append(teamIDs[0])
        result.append(sides[0])
        result.append(scores[0][0])
        result.append(scores[0][2])
        result.append(scores[0][4])
        result.append(scores[0][6])
        result.append(teamIDs[1])
        result.append(sides[1])
        result.append(scores[0][1])
        result.append(scores[0][3])
        result.append(scores[0][5])
        result.append(scores[0][7])
        result.append(matchID)
    return result


def get_match_lineups(matchID):
    html = get_html(f"https://www.hltv.org/matches/{matchID}")
    if html is None:
        print(f"Failed for {matchID}")
        return []

    # Get all of the players in a match
    playerIDs = re.findall('<a href=\"/player/.*/', html)

    # Give up if no team names found
    if len(playerIDs) < 1:
        print(f"{matchID} failed, no players detected")
        return []
    for i in range(0, len(playerIDs)):
        playerIDs[i] = (playerIDs[i].split("/"))[2].split("/")[0]

    # Make an array for pool.map to process
    if len(playerIDs) > 15:
        players = []
        players.append(playerIDs[0])
        players.append(playerIDs[1])
        players.append(playerIDs[2])
        players.append(playerIDs[3])
        players.append(playerIDs[4])
        players.append(playerIDs[5])
        players.append(playerIDs[6])
        players.append(playerIDs[7])
        players.append(playerIDs[8])
        players.append(playerIDs[9])
        players.append(matchID)
        return players
    else:
        print(f"HLTV altered lineup layout for {matchID}")
        return []


def get_match_map_bans(matchID):
    html = get_html(f"https://www.hltv.org/matches/{matchID}")
    if html is None:
        print(f"Failed for {matchID}")
        return []

    # Get all of the picks and bans for a match
    raw_picks_and_bans = re.findall('<div>.\..*<', html)

    # Clean raw_picks_and_bans
    pick_type = [' picked ', ' removed ', ' was left over', "random"]
    picks_and_bans = []

    for item in raw_picks_and_bans:

        # Clean the resultant text
        item_clean = re.sub('<div>...', '', item)
        item_clean = item_clean.replace('<', '')
        # For each pick type, get the proper information for the array
        for pick in pick_type:
            if pick in item_clean:
                item = list(item_clean.partition(pick))

                # Remove trailing space
                item[1] = item[1].replace(' ', '')
        picks_and_bans.append(item)

    # Make an array for pool.map to process
    master_array = []
    if len(picks_and_bans) > 0:
        index = 1
        for choice in picks_and_bans:
            # For the items of length 3, we get [Team, type, Map]
            if len(choice) == 3 and 'wasleftover' not in choice and 'random' not in choice:
                array = []
                array.append(matchID)
                array.append(choice[0])
                array.append(index)
                array.append(choice[1])
                array.append(choice[2])
                master_array.append(array)
                index += 1

            else:
                # For the items of length 4 we get [Map, was, left, over] so this is randomized
                array = []
                array.append(matchID)
                array.append('')
                array.append(index)
                array.append('random')
                array.append(choice[0])
                master_array.append(array)
                index += 1
    else:
        # print(f"No picks for {matchID}")
        # Too many BO1s to call out an error here
        pass
        return []
    return master_array


def get_players(playerID):
    html = get_html(f"https://www.hltv.org/player/{playerID}/a")
    if html is None:
        print(f"Failed for {playerID}")
        return []

    # Find a player's name and country
    playerName = re.findall('Complete statistics for.*</a>', html)
    if len(playerName) < 1:
        return []
    playerCountry = re.findall('class=\"flag\" title=\".*\"> ', html)
    if len(playerCountry) < 1:
        return []

    # Parse the playerName
    if len(playerName) > 0:
        playerName[0] = (playerName[0].replace("Complete statistics for ", "")).replace("</a>", "")
    else:
        playerName.append(0)

    # Parse the playerCountry
    if len(playerCountry) > 0:
        playerCountry[0] = (playerCountry[0].replace("class=\"flag\" title=\"", "")).replace("\"> ", "")
    else:
        playerCountry.append(0)

    # Make an array for pool.map to process
    array = []
    array.append(playerName[0])
    array.append(playerCountry[0])
    array.append(playerID)

    return array


def get_player_stats(matchID):
    html = get_html(f"https://www.hltv.org/matches/{matchID}")
    if html is None:
        print(f"Failed for {matchID}")
        return []

    # Get maps
    maps = re.findall('<div class=\"stats-content\" id=\".*-content\">', html)
    if len(maps) > 0:
        for i in range(0, len(maps)):
            # Really messy way to clean the result
            maps[i] = (maps[i].replace("<div class=\"stats-content\" id=\"", "")).replace("-content\">", "").translate({ord(k): None for k in digits})
        maps.remove(maps[0])
    else:
        print(f"No player stats for {matchID}")
        return []

    # Get Player IDs
    players = re.findall('href=\"/player/.*/', html)
    if len(players) > 0:
        for i in range(0, len(players)):
            players[i] = (players[i].replace("href=\"/player/", "")).replace("/", "")
    else:
        print(f"No player IDs for {matchID}")
        return []

    # Find player KDs
    kd = re.findall('<td class=\"kd text-center\">.*</td>', html)
    kills = []
    deaths = []
    if len(kd) > 0:
        for i in range(0, len(kd)):
            kd[i] = (kd[i].replace("<td class=\"kd text-center\">", "")).replace("</td>", "")
            # Clean up the hyphenated numbers
            kills.append(kd[i][0:kd[i].find('-')])
            deaths.append(kd[i][kd[i].find('-') + 1:len(kd[i])])
    else:
        print(f"No player K/D for {matchID}")
        return []
    # Remove unnecessary instances of D
    deaths[:] = [x for x in deaths if x != 'D']
    # Remove unnecessary instances of K
    kills[:] = [x for x in kills if x != 'K']

    # Find player ADR
    adr = re.findall('<td class=\"adr text-center \">.*</td>', html)
    if len(adr) > 0:
        for i in range(0, len(adr)):
            adr[i] = (adr[i].replace("<td class=\"adr text-center \">", "")).replace("</td>", "")
    else:
        print(f"No player ADR for {matchID}")
        # Add blank items for when data is missing; number may need adjustment if we do BO7s later
        adr = [""] * 70

    # Find player KAST%
    kast = re.findall('<td class=\"kast text-center\">.*</td>', html)
    if len(kast) > 0:
        for i in range(0, len(kast)):
            kast[i] = (kast[i].replace("<td class=\"kast text-center\">", "")).replace("%</td>", "")
    else:
        print(f"No player KAST ratio for {matchID}")
        # Add blank items for when data is missing; number may need adjustment if we do BO7s later
        kast = [""] * 70

    # Find player rating
    rating = re.findall('<td class=\"rating text-center\">.*</td>', html)
    nonNumbers = []
    if len(rating) > 0:
        for i in range(0, len(rating)):
            rating[i] = (rating[i].replace("<td class=\"rating text-center\">", "")).replace("</td>", "")

            # Check if the value returned is a float, if not append it to a list for removal
            try:
                float(rating[i])
            except ValueError:
                nonNumbers.append(rating[i])

        # Remove duplicate non-float values
        nonNumbers = list(set(nonNumbers))

        # Remove non-float values from the array of player ratings
        for i in range(0, len(nonNumbers)):
            rating[:] = [value for value in rating if value != nonNumbers[i]]
    else:
        print(f"No player Rating for {matchID}")
        return []

    # Remove unnecessary instances of 'Rating'
    rating[:] = [x for x in rating if x != 'Rating']

    # Handle array building
    masterArray = []
    for i in range(0, len(maps)):
        # Arrays have data for multiple matches, so this offsets us by the amount to get each map separately
        offset = 10 * (i + 1)
        try:
            for b in range(0, 5):
                playerArray = []
                playerArray.append(maps[i])
                playerArray.append(players[b + offset])
                playerArray.append(kills[b + offset])
                playerArray.append(deaths[b + offset])
                playerArray.append(adr[b + offset])
                playerArray.append(kast[b + offset])
                playerArray.append(rating[b + offset])
                playerArray.append(matchID)
                masterArray.append(playerArray)
            for b in range(5, 10):
                playerArray = []
                playerArray.append(maps[i])
                playerArray.append(players[b + offset])
                playerArray.append(kills[b + offset])
                playerArray.append(deaths[b + offset])
                playerArray.append(adr[b + offset])
                playerArray.append(kast[b + offset])
                playerArray.append(rating[b + offset])
                playerArray.append(matchID)
                masterArray.append(playerArray)
        except IndexError:
                print(f"Player stats error with {matchID}")
    return masterArray
