##################### HEAD #######################

import requests
from lxml import html

import re
import csv

from crawly import *

#################### CONFIG ######################

REGIONS = {"montreal":("/b-grand-montreal","/k0l80002"), "toronto":("/b-gta-greater-toronto-area", "/k0l1700272")}
max_pages = 3
region = "montreal"

#################### CLASSES #####################


# Main page listings
class MainListing(object):
    def __init__(self, title, price, date, link):
        self.title = title
        self.price = price
        self.date = date
        self.link = link


# Currently unused because it doesn't provide much extra info
class SubListing(MainListing):
    def __init__(self, exact_date, for_sale, description):
        self.exact_date = exact_date
        self.for_sale = for_sale
        self.description = description


################### FUNCTIONS ####################


# This function parses the search query into a valid Kijiji link
def get_kijiji_url(max_pages, region):

    location = REGIONS[region][0]
    code = REGIONS[region][1]
    url = []

    while True:
        keyword = raw_input("Enter search query >>> ")
        keyword = keyword.strip().replace(" ", "-") 
        try: 
            url.append ("http://www.kijiji.ca"+ location + "/" + keyword + code)
        except:
            print "[Error] Search error."
            continue

    return urls, keyword


# This function obtains the properties of each listing and returns a list of MainListing instances
def fetch_main_listings(response):

    titles = response.xpath('//div[not(@class="search-item top-feature ")]/div/div/div[@class="title"]/a/text()')
    titles = [_.strip() for _ in titles]
    print len(titles)
    print "-" * 80

#    (@class="search-item cas-channel regular-ad third-party")

    dates = response.xpath('//div[not(@class="search-item top-feature ")]/div/div/div/span[@class="date-posted"]/text()')
    dates = [_.strip() for _ in dates]
    print len(dates)
    print "-" * 80

    prices = response.xpath('//div[not(@class="search-item top-feature ")]/div/div/div[@class="price"]/text()')
    prices = [_.strip().replace(u"\xa0", u"").replace(u"$",u"").replace(u",",".") for _ in prices]
    print len(prices)
    print "-" * 80

    links = response.xpath('//div[not(@class="search-item top-feature ")]/div/div/div[@class="title"]/a/@href')
    links = [_.strip() for _ in links]
    print len(links)
    print "-" * 80

    main_listings = [MainListing(titles[i], prices[i], dates[i], links[i]) for i, _ in enumerate(titles)]

    return main_listings


# This function prints listings
def print_listings(listings):

    print "-" * 80

    for j in ["title", "price", "date", "link"]:
        for i, listing in enumerate(listings):
            i += 1
            print "[{:2}]".format(i), getattr(listing, j)
        print "-" * 80


# This function exports listings as csv file:
def export_listings(listings, keyword):

    filename = keyword + ".csv"

    file = open(filename, "w")
    writer = csv.writer(file)
    writer.writerow(["#","Title", "Price", "Date", "Link"])

    for i, listing in enumerate(listings):
        i += 1
        row = [str(i), listing.title, listing.price, listing.date, listing.link]
        row = [_.encode('utf-8') for _ in row]
        writer.writerow(row)

    print "[Info] Wrote to {}".format(filename)


##################### MAIN #######################

keyword = prompt()
urls = get_kijiji_url(keyword, max_pages, region)
for url in urls:
    response = 

main_listings = fetch_main_listings(response)

print_listings(main_listings)
export_listings(main_listings, keyword)


