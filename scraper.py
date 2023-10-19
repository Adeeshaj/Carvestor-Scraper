from bs4 import BeautifulSoup
import requests
from services.services import get_page_updated_time

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

print(len(listing_urls))


