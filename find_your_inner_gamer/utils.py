import requests
from bs4 import BeautifulSoup
import datetime as dt


def get_name(url):
    """
    Scrapes the url website for the game name
    
    Args:
        url (str): Link to the web page for a given game.
    
    Returns:
        str: Game name or if missing 'NaN' value.
    """
    response = requests.get(url).text
    soup = BeautifulSoup(response, "html.parser")
    try:
        return soup.find('h2', class_='pageheader').text.strip()
    except AttributeError:
        try:
            return soup.find('div', class_='apphub_AppName').text.strip()
        except AttributeError:
            return float('nan')