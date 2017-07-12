from multiprocessing.dummy import Pool as ThreadPool
from html import get_html
from scraper import *
import csv
import sys


def scrape(array, function, threads):
    # Define the number of threads
    pool = ThreadPool(threads)
    # Tell the user what is happening
    print(f"Scraping {len(array)} items using {function} on {threads} threads.")
    # Calls get() and adds the filesize returned each call to an array called filesizes
    result = (pool.imap_unordered(function, array))
    pool.close()

    # Display progress as the scraper runs its processes
    while (len(array) > 1):
        completed = result._index
        # Break out of the loop if all tasks are done or if there is only one task
        if (completed == len(array)):
            sys.stdout.flush()
            sys.stdout.write('\r'+"")
            sys.stdout.flush()
            break
        # Avoid a ZeroDivisionError
        if completed > 0:
            sys.stdout.flush()
            sys.stdout.write('\r'+f"{completed/len(array)*100:.0f}% done. {len(array)-completed} left. ")
            sys.stdout.flush()
        sys.stdout.flush()

    pool.join()
    return list(result)


# Handle an error where data is not added to the end of the CSV file.
def add_new_line(file):
    # Add a newline to the end of the file if there is not one
    with open(file, "r+") as f:
        f.seek(0, 2)
        if (f.read() != '\n'):
            f.seek(0, 2)
            f.write('\n')
    return None


def tabulate(csvFile, array):
    if len(array) > 1:
        # Files must be in the csv directory inside the project folder
        # Opens the CSV file
        with open(f"csv/{csvFile}.csv", 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=',')
            # Add the array passed to the CSV file
            for i in array:
                if len(i) > 0:
                    writer.writerow(i)
        print(f"Succesfully tabulated {len(array)} rows to {csvFile}.csv.")
    return True


def get_existing_data(csvFile, colNum):
    # Add the values in colNum in csvFile to an array
    array = []
    print(f"Reading data from {csvFile}.csv.")
    with open(f"csv/{csvFile}.csv", encoding='utf-8') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            array.append(row[colNum])
    return array


def find_max(csvFile, colNum):
    # Find the maximum value in a column in an array
    array = []
    print(f"Reading data from {csvFile}.csv.")
    with open(f"csv/{csvFile}.csv", encoding='utf-8') as csvfile:
        next(csvfile)
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            array.append(int(row[colNum]))
    return max(array)


def remove_existing_data(existing, new, item):
    # Remove data we already have from the list of new data to parse
    for i in new[:]:
        if i in existing:
            new.remove(i)
    # Convert new values to a set to remove duplicates, then back to a list
    new = list(set(new))
    print(f"{len(new)} new {item} to check.")
    return new


def un_dimension(array, item):
    # Pulls specific items from an multi-dimensional array and returns them to one array
    result = []
    for i in range(0, len(array)):
        result.append(array[i][item])
    return result


def fix_match_results(array, length):
    temp = []
    for i in array:
        if len(i) == length:
            temp.append(i)
        elif type(i) != type(1):
            for b in i:
                if len(b) == length:
                    temp.append(b)
    return temp



def fix_player_stats(array):
    # Used to clean player stats for matches with more than one map
    newArray = []
    for i in range(0, len(array)):
        for b in range(0, len(array[i])):
            newArray.append(array[i][b])
    return newArray


def get_new_iterable_items(page, startID):
    # Increments unique IDs until we get the last one, then return them to a list
    print(f"Checking for new {page}s. This may take awhile.")
    check = True
    array = []
    while check:
        startID += 1
        html = get_html(f"https://www.hltv.org/{page}/{startID}/a")
        if html is None:
            check = False
        else:
            sys.stdout.write('\r'+f"New {page} found: {startID}")
            sys.stdout.flush()
            array.append(startID)
    print(f"\nFound {len(array)} new {page}s.")
    return array


def check_args(arg, array):
    # Determine if the argument was passed or not
    return arg in array


def print_array(string, array):
    # Prints each array in a multi-dimensional array
    for i in range(0, len(array)):
        print(f"{string}: {array[i][0:len(array[i])-1]}")
    print("")


def csv_lookup(csvFile, item, lookupColumn, resultColumn):
    array = []
    print(f"Reading data from {csvFile}.csv.")
    with open(f"csv/{csvFile}.csv", encoding='utf-8') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            if item in row[lookupColumn]:
                if item == row[lookupColumn]:
                    return row[resultColumn]
                pass
            pass
        pass


def tests(threads):
    # Use only one thread
    threads = int(threads/threads)

    # Add the single match ID to an array
    matchID = []
    try:
        matchID.append(sys.argv[sys.argv.index('test')+1])
    except IndexError as e:
        print(f"You must add an argument for the matchID after the 'test' argument!")
        return None

    # Tell the user what we are parsing
    print(f"\nBeginning test scrape for {matchID[0]}:\n")

    # Handle the Event ID
    eventID = scrape(matchID, get_match_events, threads)
    eventID[0][1] = csv_lookup('eventIDs', eventID[0][1], 3, 1)

    # Handle new match info
    matchInfo = fix_match_results(scrape(matchID, get_match_info, threads), 15)
    print(matchInfo)
    for i in range(0, len(matchInfo)):
        matchInfo[i][2] = csv_lookup('teams', matchInfo[i][2], 2, 0)
        matchInfo[i][8] = csv_lookup('teams', matchInfo[i][8], 2, 0)

    # Handle match lineup
    lineup = scrape(matchID, get_match_lineups, threads)
    for i in range(0, len(lineup[0])-1):
        lineup[0][i] = csv_lookup('players', lineup[0][i], 2, 0)[1:]

    # Handle player stats
    stats = fix_player_stats(scrape(matchID, get_player_stats, threads))
    for i in range(0, len(stats)):
        stats[i][1] = csv_lookup('players', stats[i][1], 2, 0)[1:]

    # Handle printing
    print(f"\nTest scrape results for {matchID[0]}:\n")
    print(f"Event: {eventID[0][1]}\n")
    print_array("Map results", matchInfo)
    print_array("Match lineup", lineup)
    print_array("Player stats", stats)
