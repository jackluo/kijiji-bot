##################### HEAD #######################

import requests
from lxml import html

################### FUNCTIONS ####################


# This function fetches the website and returns an html object
def get_url(url):

    try:
        if "http://" not in url: url = "http://"+ url
        response = requests.get(url)
    except:
        print "[ERROR] Connection error."
        quit()

    response = html.fromstring(response.text)
    return response
