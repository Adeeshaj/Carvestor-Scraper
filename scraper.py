from bs4 import BeautifulSoup
import requests
from services.services import get_page_updated_time, scrape_txt_fields, preprocess_title, preprocess_location, preprocess_date, preprocess_price, preprocess_properties, preprocess_description

# URL of the website to scrape
domain = "https://ikman.lk"



# get listing urls for a day
TIME_SUFFIXES = ['', 'now', 'minutes', 'hour', 'hours', 'day', 'days']
listing_urls = []
page_no = 1
updated_time_prefix, updated_time_suffix = get_page_updated_time(domain, page_no)
is_current = True
while(updated_time_suffix in TIME_SUFFIXES and is_current):
    
    if(updated_time_suffix == 'days'):
        try:
            if (int(updated_time_prefix) > 1):
                is_current = False
        except Exception as e:
            print(str(e))

    page_url = f"{domain}/en/ads/sri-lanka/cars?sort=date&order=desc&buy_now=0&urgent=0&page={page_no}"
    print(page_url)
    page = requests.get(page_url)
    soup = BeautifulSoup(page.text, "html.parser")
    cards = soup.find_all("a", class_="card-link--3ssYv gtm-ad-item", attrs={'data-testid': 'ad-card-link'})
    for card in cards:
        url = f"{domain}{card['href']}"
        listing_urls.append(url)
    updated_time_prefix, updated_time_suffix = get_page_updated_time(domain, page_no)
    page_no += 1

listings = []
for url in listing_urls:
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    listing = {
        'title': preprocess_title(scrape_txt_fields('h1', 'title--3s1R8', soup)),
        'location': preprocess_location(scrape_txt_fields('a', 'subtitle-location-link--1q5zA', soup)),
        'date': preprocess_date(scrape_txt_fields('span', 'sub-title--37mkY', soup)),
        'price': preprocess_price(scrape_txt_fields('div', 'amount--3NTpl', soup)),
        'properties': preprocess_properties(scrape_txt_fields('div', 'word-break--2nyVq label--3oVZK', soup), scrape_txt_fields('div', 'word-break--2nyVq value--1lKHt', soup)),
        'description': preprocess_description(scrape_txt_fields('div', 'description--1nRbz', soup)),
    }
    listings.append(listing)
    



