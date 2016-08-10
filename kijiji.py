##################### HEAD #######################

import requests
from lxml import html

import re

from crawly import *

#################### CONFIG ######################

search_terms = ["macbook retina 13 256 8", "macbook retina 15", "hasselblad", "leica"]
region = "montreal"
max_pages = 3

REGIONS = {"montreal":("/b-grand-montreal","/k0l80002"), "toronto":("/b-gta-greater-toronto-area", "/k0l1700272")}

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
def get_url(keywords, region, max_pages):

    location = REGIONS[region][0]
    code = REGIONS[region][1]
    query = "/" + keywords
    urls = []

    while True:
        try: 
            for i in xrange(max_pages):

                BASE_URL = "http://www.kijiji.ca"
                page = "/page-" + str(i + 1)

                url = BASE_URL + location + query + page + code
                urls.append(url)
                print "[Info]", "URL found: ", url

            break
        except:
            print "[Error] Search error."
            continue

    return urls


# This function obtains the properties of each listing and returns a list of MainListing instances
def parse_main_listings(response):

    base_path = '//div[not(@class="search-item top-feature " or @class="search-item cas-channel regular-ad third-party" or @class="search-item cas-channel top-feature  third-party")]/div/div'

    titles = response.xpath(base_path + '/div[@class="title"]/a/text()')
    dates = response.xpath(base_path + '/div/span[@class="date-posted"]/text()')
    prices = response.xpath(base_path + '/div[@class="price"]/text()')
    links = response.xpath(base_path + '/div[@class="title"]/a/@href')

    main_listings = [MainListing(titles[i].strip(), prices[i].strip().replace(u"\xa0", u"").replace(u"$",u"").replace(u",","."), dates[i].strip(), links[i].strip()) for i, title in enumerate(titles) if (u"Recherch" or u"Looking for") not in title]

    return main_listings


##################### MAIN #######################


def main():

    #print "\x1b[8;80;160t"
    fields = ["title", "price", "date", "link"]
    main_listings = []
    sub_listings = []

    keywords = encode("-")
    urls = get_url(keywords, region, max_pages)

    for url in urls:
        response = load(url)
        main_listings += parse_main_listings(response)

    output_console(main_listings, fields)
    output_csv(keywords, main_listings, fields)


if __name__ == "__main__":
    main()

