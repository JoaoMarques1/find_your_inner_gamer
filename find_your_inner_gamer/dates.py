import requests
from bs4 import BeautifulSoup
import datetime as dt


def convert_date(date):
    """
    Functions converts a string into a date, if the input value represents a date.
    If the input can not be converted, the functions returns the input value.

    Args:
        date (str): str representing a date

    Returns:
        datetime.datetime or input value
    """
    try:
        return dt.datetime.strptime(date, "%b %d, %Y")
    except:
        try:
            return dt.datetime.strptime(date, "%d %b, %Y")
        except:
            return date


def valid_date(date):
    """
    Checks if the input is the a datetime type.

    Args:
        date : The value we want to see if it's a date

    Returns:
        bool: True if type datetime else False
    """
    return isinstance(date, dt.datetime)


def get_date(url):
    """
    Scrapes the given url for the release date of the game.

    Args:
        url (str): Link to the web page for a give game

    Returns:
        str/float: a str representing the date or if missing return 'NaN'.
    """
    response = requests.get(url).text
    soup = BeautifulSoup(response, "html.parser")
    try:
        return soup.find('div', class_='date').text.strip()
    except AttributeError:
        return float('NaN')
