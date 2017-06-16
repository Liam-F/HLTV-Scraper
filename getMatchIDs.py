from html import get_html
import re


print("Initialized script.")


def get_match_ids(stop):
    # Create an offset variable for lists that are paginated on HLTV
    offset = 0

    # Create an array of all of the Demo URLs on the page
    matchIDs = find_match_ids_at_url("https://www.hltv.org/results?offset=%s" % (offset))

    # Determine if we need to paginate and create a variable to keep track of pages
    morePages = end_check(matchIDs, stop)
    page = 1
    length = len(matchIDs)
    print(f"Parsed page {page}. {length} IDs found so far.")
    while morePages:
        # Offset by 100 to get the next 100 matches
        offset += 100
        moreMatchIDs = find_match_ids_at_url("https://www.hltv.org/results?offset=%s" % (offset))

        # Append the new IDs to the master list
        for m in moreMatchIDs:
            matchIDs.append(m)

        # Continue paginating and updating the user
        page += 1
        length = len(matchIDs)
        print(f"Parsed page {page}. {length} IDs found so far.")
        morePages = end_check(matchIDs, stop)

    # Ensure that there have been no changes to the page layout
    if len(matchIDs) % 100 != 0:
        print(f"HLTV altered results page layout for offset {offset}")

    # Determines where to stop the array
    slice = matchIDs.index(stop)
    # Remove unecessary entries
    matchIDs = matchIDs[:slice]

    # Adds the unique match identifier as an array to each item
    for i in range(0, len(matchIDs)):
        string = matchIDs[i]
        split = string.split("/", 1)[0:1]
        split.append(string)
        matchIDs[i] = split

    # Reverse the array so the most recent match is last
    matchIDs = matchIDs[::-1]
    print(f"Parsed {page} page(s).")
    return matchIDs


def end_check(matchIDs, stop):
    if stop in matchIDs:
        return False
    return True


def find_match_ids_at_url(url):
    # Get the HTML using get_html()
    html = get_html(url)

    # Create an array of all of the Match URLs on the page
    matchIDs = re.findall('"(.*?000"><a href="/matches/.*?)"', html)

    # Loop through the messy array and removes the pesky parts
    for i in range(0, len(matchIDs)):
        matchIDs[i] = matchIDs[i].split('/', 2)[-1]
    return matchIDs
