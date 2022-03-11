import requests
from bs4 import BeautifulSoup
import datetime as dt


def clean_review(review):
    """
    Keeps only the category of the review
    
    Args:
        review (str): Game review
    
    Returns:
        str: review category
    """
    return review.split(',')[0] if '%' in str(review) else float('NaN')


def get_review(url):
    """
    Scrapes the url website for the game review
    
    Args:
        url (str): Link to the web page for a given game
    
    Returns:
        str/float: review category or if missing 'NaN' value.
    """
    response = requests.get(url).text
    soup = BeautifulSoup(response, "html.parser")
    try:
        return soup.find('div', class_='summary').text.strip().split('\n')[0]
    except AttributeError:
        return float('NaN')