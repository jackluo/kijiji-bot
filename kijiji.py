##################### HEAD #######################

import requests
from lxml import html

import re

from crawly import *

#################### CONFIG ######################

REGIONS = {"montreal":("/b-grand-montreal","/k0l80002"), "toronto":("/b-gta-greater-toronto-area", "/k0l1700272")}
max_pages = 1
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
def get_url(keyword, region, max_pages):

    location = REGIONS[region][0]
    code = REGIONS[region][1]
    url = []

        try: 
            for i in xrange(max_pages):
                url = "http://www.kijiji.ca" + location + "/" + keyword + code
                urls.append(url)
            break
        except:
            print "[Error] Search error."
            continue

    return urls


# This function obtains the properties of each listing and returns a list of MainListing instances
def select_main_listings(response):

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


##################### MAIN #######################

keyword = prompt("-")
urls = get_url(keyword, region, max_pages)
for url in urls:
    response = load_page(url)

main_listings = select_main_listings(response)

fields = {"Title":"title", "Price":"price", "Date":"date", "Link":"link"}
pretty_print(main_listings, fields.values())
export_csv(keywords, main_listings, fields)




