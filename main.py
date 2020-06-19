#!python3

import re

from bs4 import BeautifulSoup
import requests

# example target url: https://cloudblog.withgoogle.com/products/containers-kubernetes/rss

RSSBase = ""
BaseURL = "https://cloud.google.com"
URI = "/blog/products"

URL = BaseURL + URI

regex = r"^https://cloudblog.withgoogle.com/products/([a-z-]+)/rss$"

def get_page(url):

    return requests.get(url)

def return_rss_link(links):
    for link in links:
        ln = link.get("href")
        if re.match(regex, ln):
            return ln

if __name__ == "__main__":
    
    product_links = []
    
    response = get_page(URL)
    html = BeautifulSoup(response.text, "html.parser")

    divs = html.find_all("div", {"class": "products-navigation-list__content h-c-grid ng-star-inserted"})

    for div in divs:
        links = div.find_all("a")
        
        for link in links:
            product = link.get("href").split("/")[-1]
            product_links.append(URL + "/" + product)

    response = get_page(product_links[0])
    html = BeautifulSoup(response.text, "html.parser")
    links = html.find_all("a")
    
    for link in product_links:
        response = get_page(link)
        html = BeautifulSoup(response.text, "html.parser")
        print(return_rss_link(html.find_all("a")))