##################### HEAD #######################

import requests
from lxml import html

import re
import csv

from crawly import *

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
def get_kijiji_query(max_pages=1):

    REGION = "/b-grand-montreal" # Montreal
    CODE = "/k0l80002" # Montreal

    while True:
        keyword = raw_input("Enter search query >>> ")
        keyword = keyword.strip().replace(" ", "-") 
        try: 
            response = get_url("http://www.kijiji.ca"+ REGION + "/" + keyword + CODE)
            break
        except:
            print "[Error] Search error."
            continue

    return response, keyword


# This function obtains the properties of each listing and returns a list of MainListing instances
def get_main_listings(response):

    titles = response.xpath('//div[@class="title"]/a/text()')
    titles = [_.strip() for _ in titles]

    dates = response.xpath('//span[@class="date-posted"]/text()')
    dates = [_.strip() for _ in dates]

    prices = response.xpath('//div[@class="price"]/text()')
    prices = [_.strip().replace(u"\xa0", u"").replace(u"$",u"").replace(u",",".") for _ in prices]

    links = response.xpath('//div[@class="title"]/a/@href')
    links = [_.strip() for _ in links]

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

    try:
        file = open(filename, "a")
        writer = csv.writer(file)

    except IOError:
        file = open(filename, "w")
        writer = csv.writer(file)
        writer.writerow(["#","Title", "Price", "Date", "Link"])

    except:
        print "[Error] File error."
        quit()

    for i, listing in enumerate(listings):
        i += 1
        row = [str(i), listing.title, listing.price, listing.date, listing.link]
        row = [_.encode('utf-8') for _ in row]
        writer.writerow(row)

    print "[Info] Wrote to {}".format(filename)


##################### MAIN #######################

response, keyword = get_kijiji_query()
main_listings = get_main_listings(response)

print_listings(main_listings)
export_listings(main_listings, keyword)


