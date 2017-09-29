from html import get_html
import re
import math


print("Initialized script.")


def get_finished_events(stop=0):
    print("Looking for new completed events.")

    # Create an offset variable for lists that are paginated on HLTV
    offset = 0
    # Empty array to add new IDs to
    event_ids = []

    # Ensure we loop through the proper number of pages
    html = get_html('https://www.hltv.org/events/archive')
    num_pages = int(find_num_pages(html))
    page = 0

    # Loop through the pages of finished events
    for i in range(num_pages - 1):
        # Get the matches at the current offset
        more_event_ids = find_match_ids_at_url(f"https://www.hltv.org/events/archive?offset={offset}")

        # Offset by 50 to get the next 100 matches
        offset += 50

        # Append the new IDs to the master list
        for event in more_event_ids:
            event_ids.append([event, 0])

        # Break out when we see the most recent ID
        if not end_check(event_ids, stop):
            slice = event_ids.index([stop, 0])
            # Remove unecessary entries
            event_ids = event_ids[:slice]
            break

        # Continue paginating and updating the user
        page += 1
        length = len(event_ids)
        print(f"Parsed page {page}. {length} events found so far.")

    # Reverse the array so the most recent event is last
    event_ids = event_ids[::-1]
    print(f"Parsed {page} page(s).")
    return event_ids


def find_num_pages(html):
    pages = re.findall('1 - 50 of ....', html)[0]
    return math.ceil(int(pages[-4:]) / 50)


def end_check(matchIDs, stop):
    if [stop, 0] in matchIDs:
        return False
    return True


def find_match_ids_at_url(url):
    # Get the HTML using get_html()
    html = get_html(url)

    # Create an array of all of the Match URLs on the page
    event_ids = re.findall('events/.*/', html)

    # Loop through the messy array and removes the pesky parts
    for i in range(0, len(event_ids)):
        event_ids[i] = event_ids[i].split('/')[1]
    # print(event_ids[1:51])
    return event_ids[1:51]
