##################### HEAD #######################

import requests
from lxml import html

import re

from crawly import *

#################### CONFIG ######################

search_terms = ["macbook retina 13 256 8", "macbook retina 15", "hasselblad", "leica"]
region = "montreal"
max_pages = 1


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
    keywords = "/" + keywords
    code = REGIONS[region][1]
    urls = []

    while True:
        try: 
            for i in xrange(max_pages):
                page = "/page-" + str(i + 1)
                url = "http://www.kijiji.ca" + location + keywords + page + code
                urls.append(url)
                print url
            break
        except:
            print "[Error] Search error."
            continue

    return urls


# This function obtains the properties of each listing and returns a list of MainListing instances
def select_main_listings(response):

    titles = response.xpath('//div[not(@class="search-item top-feature " or @class="search-item cas-channel regular-ad third-party" or @class="search-item cas-channel top-feature  third-party")]/div/div/div[@class="title"]/a/text()')
    titles = [title.strip() for title in titles]
    print len(titles)

    dates = response.xpath('//div[not(@class="search-item top-feature " or @class="search-item cas-channel regular-ad third-party" or @class="search-item cas-channel top-feature  third-party")]/div/div/div/span[@class="date-posted"]/text()')
    dates = [date.strip() for date in dates]
    print len(dates)

    prices = response.xpath('//div[not(@class="search-item top-feature " or @class="search-item cas-channel regular-ad third-party" or @class="search-item cas-channel top-feature  third-party")]/div/div/div[@class="price"]/text()')
    prices = [price.strip().replace(u"\xa0", u"").replace(u"$",u"").replace(u",",".") for price in prices]
    print len(prices)

    links = response.xpath('//div[not(@class="search-item top-feature " or @class="search-item cas-channel regular-ad third-party" or @class="search-item cas-channel top-feature  third-party")]/div/div/div[@class="title"]/a/@href')
    links = [link.strip() for link in links]
    print len(links)

    main_listings = [MainListing(titles[i], prices[i], dates[i], links[i]) for i, title in enumerate(titles)]

    return main_listings


##################### MAIN #######################

main_listings = []
sub_listings = []

print "-" * 80

keywords = prompt("-")
urls = get_url(keywords, region, max_pages)

print "-" * 80

for url in urls:
    response = load_page(url)
    main_listings += select_main_listings(response)

print "-" * 80

fields = ["title", "price", "date", "link"]
pretty_print(main_listings, fields)
export_csv(keywords, main_listings, fields)



