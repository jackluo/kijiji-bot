##################### HEAD #######################

import requests
from lxml import html

################### FUNCTIONS ####################


# This function prompts the keyord and returns it with - as space encoding
def prompt():

    keyword = raw_input("Enter search query >>> ")
    keyword = keywords.strip().replace(" ", "-") 

    return keyword


# This function parses the search query into a valid Kijiji link
def get_url(keyword, max_pages, region):

    location = REGIONS[region][0]
    code = REGIONS[region][1]
    url = []

    while True:
        keyword = raw_input("Enter search query >>> ")
        keyword = keyword.strip().replace(" ", "-") 
        try: 
            for i in xrange(max_pages):
                urls.append(url)
            break
        except:
            print "[Error] Search error."
            continue

    return urls

# This function fetches the website and returns an html object
def load_page(url):

    try:
        if "http://" not in url: url = "http://"+ url
        response = requests.get(url)
    except:
        print "[ERROR] Connection error."
        quit()

    try:
        response = html.fromstring(response.text)
    except:
        print "[ERROR] Parsing error."
        quit()

    return response


