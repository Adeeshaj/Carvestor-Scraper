from bs4 import BeautifulSoup
import requests

# URL of the website to scrape
url = "https://ikman.lk/en/ads/sri-lanka/cars"

# Send an HTTP GET request and get the website's HTML content
response = requests.get(url)

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# Now, you can navigate and extract data from the parsed HTML using BeautifulSoup methods.
title = soup.find("h1").text
print(title)