import requests
from bs4 import BeautifulSoup
import re
import json
import sys

def get_page_updated_time(domain, page_no):
    page_url = f"{domain}/en/ads/sri-lanka/cars?sort=date&order=desc&buy_now=0&urgent=0&page={page_no}"
    page = requests.get(page_url)
    soup = BeautifulSoup(page.text, "html.parser")
    updated_time = []
    try:
        updated_time = soup.find("div", class_="updated-time--1DbCk").text.split(" ")
    except AttributeError:
        updated_time = ['']
    updated_time_suffix = updated_time[-1]
    updated_time_prefix = updated_time[0]
    return updated_time_prefix, updated_time_suffix

def scrape_txt_fields(tag, class_, soup):
    results = soup.find_all(tag, class_=class_)
    values = list(map(_soup_text, results))
    return values

def _soup_text(value):
    return value.text

def preprocess_title(title):
    try:
        return title[0]
    except Exception as e:
        print(e)
        return None

def preprocess_location(location):
    try:
        return ''.join(location)
    except Exception as e:
        print(e)
        return None
    

def preprocess_date(date):
    try:
        return date[0].split(',')[0]
    except Exception as e:
        print(e)
        return None
    

def preprocess_price(price):
    try:
        currency, amount = _extract_currency_and_amount(price[0])
        return {
            "currency": currency,
            "amount": amount
        }
    except Exception as e:
        print(e)
        return None

def preprocess_properties(labels, values):
    try:
        return json.dumps({labels[i]: values[i] for i in range(len(labels))})
    except Exception as e:
        print(e)
        return None
    

def preprocess_description(description):
    try:
        return description[0]
    except Exception as e:
        print(e)
        return None
    


def _extract_currency_and_amount(currency_string):
    # Define a regular expression pattern to match currency values like "Rs 7,975,000"
    pattern = r'^([A-Za-z]+) (\d[\d,]*)$'

    # Use re.match to find the pattern in the input string
    match = re.match(pattern, currency_string)

    if match:
        # Extract the currency symbol and amount
        currency_symbol = match.group(1)
        amount_str = match.group(2)

        # Remove commas from the amount and convert it to an integer
        amount = int(amount_str.replace(',', ''))

        return currency_symbol, amount
    else:
        return None


def update_progress_bar(current, total, length=40, message="Progress"):
    """
    Update and display a dynamic progress bar on the same line.
    
    Args:
        current (int): The current progress value.
        total (int): The total number of steps.
        length (int, optional): The length of the progress bar. Default is 40.
        message (str, optional): The message to display next to the progress bar.
    """
    progress = current / total
    progress_length = int(length * progress)
    bar = "#" * progress_length + "-" * (length - progress_length)
    sys.stdout.write("\r[{:<{}}] {} {}/{}".format(bar, length, message, current, total))
    sys.stdout.flush()

