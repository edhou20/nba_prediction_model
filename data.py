import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_soup(url):
    headers = {'User-Agent': 'Mozilla/5.0'} #prevent being flagged as bot
    res = requests.get(url, headers=headers) #sends get request to url
    res.raise_for_status() #returns None if no error, otherwise will raise exception
    return BeautifulSoup(res.content, 'html.parser') #.content gets you raw content
    #running BeautifulSoup() returns document as nested data structure, need to specify a type of parser, eg. html


def parse_table_to_df(soup, table_id):
    table = soup.find('table', id=table_id) #.find returns tag of 'table', refers to where param is located in doc
    if table is None:
        raise ValueError(f"Table with id '{table_id}' not found.")

    try:
        df = pd.read_html(str(table))[0] #reads HTML tables from a string, file-like obj, or URL and converts into list of dataframes
        # Drop rows where player/team is "Player" or "Team" (duplicate headers)
        df = df[df[df.columns[0]] != df.columns[0]] #filter out Basketball-Reference's repeating headers like Player
    except:
        df = pd.read_html(str(table), header=[0, 1])[0] #uses first 2 rows to create MultiIndex for columns. Each is a tuple (off/def/"", stat_name)
        df.columns = [flatten_col(col) if isinstance(col, tuple) else col for col in df.columns] #isinstance() a python function to check if obj is an instance of specific class/type
    return df.reset_index(drop=True)

def flatten_col(col_tuple):
    section, stat = col_tuple
    if section.strip().lower() == 'defense four factors':
        return f'def_{stat.strip()}'
    elif section.strip().lower() == 'offense four factors':
        return stat.strip()
    else:
        return stat

def scrape_player_stats(season_end_year):
    print("scraping player")
    url = f"https://www.basketball-reference.com/leagues/NBA_{season_end_year}_per_game.html"
    print(f"Scraping player stats from {url}")
    soup = get_soup(url)
    df = parse_table_to_df(soup, "per_game_stats")
    df["Season"] = f"{season_end_year-1}-{season_end_year}"
    return df

def scrape_team_stats(season_end_year):
    print("scraping team")
    url = f"https://www.basketball-reference.com/leagues/NBA_{season_end_year}.html"
    print(f"Scraping team stats from {url}")
    soup = get_soup(url)
    df = parse_table_to_df(soup, "advanced-team")
    df["Season"] = f"{season_end_year-1}-{season_end_year}"
    return df
