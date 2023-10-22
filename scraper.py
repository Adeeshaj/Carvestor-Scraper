from bs4 import BeautifulSoup
import requests
import psycopg2
from services.services import get_page_updated_time, scrape_txt_fields, preprocess_title, preprocess_location, preprocess_date, preprocess_price, preprocess_properties, preprocess_description, update_progress_bar
import logging
import sys
import os
from dotenv import load_dotenv

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load the .env file
load_dotenv()

# URL of the website to scrape
domain = "https://ikman.lk"
db_name = "carvestor"
user = "adeeshaj"
password = ""
host = "localhost" 
port = "5432" 
table_name = "listings"

DB_URL =  os.environ.get("PSQL_DB_URL")

# get listing urls for a day
TIME_SUFFIXES = ['', 'now', 'minutes', 'hour', 'hours', 'day', 'days']
listing_urls = []
page_no = 1
updated_time_prefix, updated_time_suffix = get_page_updated_time(domain, page_no)
is_current = True
while(updated_time_suffix in TIME_SUFFIXES and is_current):
    if(updated_time_suffix == 'days'):
        try:
            if (int(updated_time_prefix) > 7):
                is_current = False
        except Exception as e:
            logging.exception(e)

    page_url = f"{domain}/en/ads/sri-lanka/cars?sort=date&order=desc&buy_now=0&urgent=0&page={page_no}"
    logging.info(f"Pages: {page_no} scraped")
    page = requests.get(page_url)
    soup = BeautifulSoup(page.text, "html.parser")
    cards = soup.find_all("a", class_="card-link--3ssYv gtm-ad-item", attrs={'data-testid': 'ad-card-link'})
    for card in cards:
        url = f"{domain}{card['href']}"
        listing_urls.append(url)
    updated_time_prefix, updated_time_suffix = get_page_updated_time(domain, page_no)
    page_no += 1

logging.info(f"found {len(listing_urls)} listings")

listings = []
for url in listing_urls:
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    price = preprocess_price(scrape_txt_fields('div', 'amount--3NTpl', soup))
    listing = {
        'listing_url': url,
        'title': preprocess_title(scrape_txt_fields('h1', 'title--3s1R8', soup)),
        'location': preprocess_location(scrape_txt_fields('a', 'subtitle-location-link--1q5zA', soup)),
        'date': preprocess_date(scrape_txt_fields('span', 'sub-title--37mkY', soup)),
        'price': price['amount'] if price else None,
        'price_currency': price['currency'] if price else None,
        'properties': preprocess_properties(scrape_txt_fields('div', 'word-break--2nyVq label--3oVZK', soup), scrape_txt_fields('div', 'word-break--2nyVq value--1lKHt', soup)),
        'description': preprocess_description(scrape_txt_fields('div', 'description--1nRbz', soup)),
    }
    listings.append(listing)
    #logging excecuted percentage
    percentage = int(len(listings)/len(listing_urls)*100)
    update_progress_bar(percentage, 100)

logging.info(f"processed {len(listings)} listings")

#adding data to database
# Create a connection to the database
conn = psycopg2.connect(DB_URL)

# Create a cursor
cur = conn.cursor()

try:
    for listing in listings:
        
        # Insert data from each dictionary into the database
        columns = ', '.join(listing.keys())
        values = ', '.join(['%s' for _ in listing])
        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
        cur.execute(insert_query, list(listing.values()))

    # Commit the transaction after inserting all the data
    conn.commit()

    logging.info("Data inserted successfully.")

except Exception as e:
    # Handle any errors
    conn.rollback()
    logging.exception(e)

finally:
    # Close the cursor and connection
    if cur:
        cur.close()
    if conn:
        conn.close()