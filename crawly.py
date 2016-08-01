##################### HEAD #######################

import requests
from lxml import html

import sys
import csv

################### FUNCTIONS ####################


# This function prompts the keyord and returns it with chosen character as encoding
def prompt(character):

    keywords = raw_input("Enter search query >>> ")
    keywords = keywords.strip().replace(" ", character) 

    return keywords


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


# This function prints listings
def pretty_print(objects, fields):

    print "-" * 80

    for j in fields:
        for i, obj in enumerate(objects):
            i += 1
            print "[{:2}]".format(i), getattr(obj, j)
        print "-" * 80 


def table_print(objects, fields):

    row_headers = [field.capitalize() for field in fields]

    for j in fields:
        for i, obj in enumerate(objects):
            i += 1
            print "[{:2}]".format(i), getattr(obj, j)
        print "-" * 80


# This function exports listings as csv file:
def export_csv(filename, objects, fields):

    if ".csv" not in filename: filename = filename + ".csv"

    row_headers = [field.capitalize() for field in fields]

    try :
        file = open(filename, "a")
        writer = csv.writer(file)
    except :
        file = open(filename, "w")
        write = csv.writer(file)
        writer.writerow(row_headers)

    for obj in objects:
        row = [getattr(obj, field) for field in fields]
        row = [column.encode('utf-8') for column in row]
        writer.writerow(row)

    print "[Info] Wrote to {}".format(filename)
