from scraper import get_teams
from helper import get_existing_data, tabulate, scrape

teamIds = get_existing_data("teams", 2)
#teamIds = [6301]
teams = scrape(teamIds, get_teams, 16)

tabulate("teams_w_ranking", teams)