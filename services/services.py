import requests
from bs4 import BeautifulSoup

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