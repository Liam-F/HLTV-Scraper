from multiprocessing.dummy import Pool as ThreadPool
from html import get_html
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
    while (True):
        completed = result._index
        # Break out of the loop if all tasks are done
        if (completed == len(array)):
            sys.stdout.write('\r'+f"100% complete. ")
            sys.stdout.flush()
            break
        # Avoid a ZeroDivisionError
        if completed > 0:
            sys.stdout.write('\r'+f"{completed/len(array)*100:.0f}% done. Waiting for {len(array)-completed} tasks to complete.")
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
    # Files must be in the csv directory inside the project folder
    # Opens the CSV file
    with open(f"csv/{csvFile}.csv", 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',')
        # Add the array passed in to the CSV file
        for i in range(0, len(array)):
            if len(array[i]) > 0:
                writer.writerow(array[i])
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


def remove_existing_data(existing, new):
    # Remove data we already have from the list of new data to parse
    for i in new[:]:
        if i in existing:
            new.remove(i)
    # Convert new values to a set to remove duplicates, then back to a list
    new = list(set(new))
    print(f"{len(new)} new items to add.")
    return new


def un_dimension(array, item):
    # Pulls specific items from an multi-dimensional array and returns them to one array
    result = []
    for i in range(0, len(array)):
        result.append(array[i][item])
    return result


def fix_array(array, value):
    # Used to clean match info results for matches with more than one map
    for i in range(0, len(array)):
        if len(array[i]) < value:
            for b in range(0, len(array[i])):
                array.append(array[i][b])
            array.remove(array[i])
    return array


def fix_player_stats(array):
    # Used to clean match info results for matches with more than one map
    newArray = []
    for i in range(0, len(array)):
        for b in range(0, len(array[i])):
            newArray.append(array[i][b])
    return newArray


def get_new_iterable_items(page, startID):
    # Iterate through unique IDs until we get the last one, then return them to a list
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
